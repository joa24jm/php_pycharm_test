from datetime import date
from pathlib import Path
import tables
import ast
import pandas as pd
import json

def get_dataframes(ans: pd.DataFrame, qs: pd.DataFrame) -> dict:
    """
  Reads in, merges, sorts and unstacks the dataframes from the CH database.

  :param ans: Table 'answers' from the CH database
         qs:  Table 'questionnaires' from the CH database

  :return: dic of dfs in the form: {'Parent Baseline' : df,
                                    'Parent FollowUp':  df,
                                    'Heart Baseline':   df,
                                    'Heart FollowUp':   df,
                                    'Children Baseline':df,
                                    'Children FollowUp':df,
                                    'Stress Baseline':  df,
                                    'Stress FollowUp':  df,
                                    'Compass Baseline': df,
                                    'CC Interim':       df
                                    }
  """

    # set answers id as index
    ans = ans.set_index('id')

    # declare a string '[a , b , c]' as a list [a, b, c]
    ans['answers'] = ans['answers'].apply(ast.literal_eval)
    ans['client'] = ans['client'].apply(ast.literal_eval)

    # get questionnaire ids for studies (! several ids for the same study)
    gqs = qs.groupby('name')

    # initialize result_dic
    keys = [key.replace(' ', '_').lower() for key in gqs.groups.keys()]
    res_dic = dict.fromkeys(keys)

    # write date to CSV file
    path = '../../../results/dataframes/ch'
    Path(path).mkdir(parents=True, exist_ok=True)

    # iterate over every questionnaire (no matter the version)
    for key, key2 in zip(keys, gqs.groups.keys()):

        # gets the questionnaire ids belonging to this questionnaire
        q_ids = gqs.get_group(key2).id.values.tolist()

        # select only answers that belong to this questionnaire
        sub_df = ans[ans.questionnaire_id.isin(q_ids)]

        # create an output df
        output = pd.DataFrame()

        i = 0

        for a_id in sub_df.index:

            # print(key, '\t', a_id, i)
            # get additional info answer_id, user_id, date
            info = pd.DataFrame(sub_df.loc[a_id,
                                           ['questionnaire_id', 'user_id', 'created_at', 'sensordata']].to_dict(),
                                index=[a_id])

            # get sensordata from info if available
            if not info.sensordata.isnull().values.any():
                info.sensordata = info.sensordata.apply(ast.literal_eval)
                json_struct = json.loads(info.sensordata.to_json(orient="records"))
                sens_data = pd.json_normalize(json_struct[0][0]).rename(index={0: a_id}).add_prefix('sensordata_')
                info = pd.concat([info, sens_data], axis='columns')
                info.drop(columns='sensordata', inplace=True)

            # get client data
            client = pd.DataFrame(sub_df.loc[a_id, 'client'], index=[a_id])

            # get answers
            cache_df = pd.DataFrame.from_dict(sub_df.loc[a_id, 'answers'])
            if cache_df.empty:
                continue
            try: # if the values in cache_dict are a list, then pd.DataFrame.from_dict() expects two columns
                 # however we only have one answer ids
                 # solution: cast the list as a str so it becomes one object
                cache_dict = dict(zip(cache_df.label, cache_df.value))
                vals = [str(val) for val in cache_dict.values()]
                cache_dict = dict(zip(cache_df.label, vals))
                answers_df = pd.DataFrame.from_dict(cache_dict, orient='index', columns=[a_id]).transpose()

                # concat info, client, and answers
                df_concat = pd.concat([info, answers_df, client], axis='columns', ignore_index=False)

                # write ans_concat at the end of output
                output = output.append(df_concat, ignore_index=False)
            except:
                print('exception occurred ', a_id)
                continue
            i+=1

        # handle surrogates ('utf-8' codec can't encode characters, ..., surrogates not allowed)
        output = output.applymap(lambda x: str(x).encode("utf-8", errors="ignore").decode("utf-8", errors="ignore"))

        # get meaningful filename
        # fname = key.replace(' ', '_').lower()
        fname = key

        print(fname)
        print(output.shape)
        if 'created_at' in output.columns:
            print(output.created_at.min())
            print(output.created_at.max())

        # save file to dic
        res_dic[key] = output

    # return result
    return res_dic

def remove_na(df):
    """
    Drop column if less than 1 % are non NaN values
    Return df
    :param df:
    :return: df with dropped columns
    """

    # drop NaN values
    df.dropna(axis='columns', thresh=int(0.01 * len(df)), inplace=True)

    return df

if __name__ == '__main__':
    print('main executed')

    # # get all tables, this takes a while
    # tabs = tables.get_all_tables()
    # print('All tables loaded.')
    #
    # # get all answers from all quetionnnaires
    # ans = tabs['answers']
    #
    # # get questionnaires table
    # qs = tabs['questionnaires']




    # get ALL dataframes from the ch database (This takes a while)
    # Parent, Children, Heart, Compass,
    print('Unstacking dataframes, this takes a while')
    dfs_dic = get_dataframes(ans, qs)

    # check results
    print(dfs_dic.keys())

    # remove nan values
    for key in dfs_dic.keys():
        dfs_dic[key] = remove_na(dfs_dic[key])

    # save dataframes to directory
    tday = date.today().strftime("%y-%m-%d")

    # write date to CSV file
    path = '../../../results/dataframes/ch'
    Path(path).mkdir(parents=True, exist_ok=True)

    # safe all tables to disk
    for key in dfs_dic.keys():

        # save to disc
        dfs_dic[key].to_csv(f'{path}/{tday}_{key}.csv', index_label='answer_id', index=True)

        print(f'Removing nan values for {key}')
        print('shape before drop:', dfs_dic[key].shape)
        # read in all dataframes again to cast 'nan' to NaN (float)
        dfs_dic[key] = pd.read_csv(f'{path}/{tday}_{key}.csv', na_values='nan', index_col='answer_id')
        # remove columns that have more than 99 % nan values
        dfs_dic[key] = remove_na(dfs_dic[key])
        print('shape after drop:', dfs_dic[key].shape)

        # Again, save to disc
        dfs_dic[key].to_csv(f'{path}/{tday}_{key}.csv', index_label='answer_id', index=True)

    # save information about all questionnaires
    qs.to_csv(f'{path}/{tday}_questionnaires.csv')
    ans.to_csv(f'{path}/{tday}_answers.csv')

    print('All done.')