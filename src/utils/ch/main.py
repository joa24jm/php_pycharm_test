from datetime import date
from pathlib import Path
import tables
import ast
import pandas as pd

def get_dataframes(ans, qs):
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

  # declare a string '[a , b , c]' as a list [a, b, c]
  ans['answers'] = ans['answers'].apply(ast.literal_eval)
  ans['client'] = ans['client'].apply(ast.literal_eval)

  # get questionnaire ids for studies (! several ids for the same study)
  gqs = qs.groupby('name')

  # initialize result_dic
  res_dic = dict.fromkeys(gqs.groups.keys())

  # TODO: Check that loop works as expected
  # iterate over every questionnaire (no matter the version)
  for key in gqs.groups.keys():

    # TODO: check that if key is Baseline Parent, Baseline Children, Baseline Heart drop the right and append the right dfs

    # gets the questionnaire ids belonging to this questionnaire
    q_ids = gqs.get_group(key).id.values.tolist()

    # count NULL answers per questionnaire id
    i = 0
    sub_df = ans[ans.questionnaire_id.isin(q_ids)]
    output = pd.DataFrame()

    for idx in sub_df.index:

      # get additional info answer_id, user_id, date
      info = pd.DataFrame(
        sub_df.loc[idx, ['questionnaire_id', 'id', 'user_id', 'created_at', 'sensordata']]).transpose().reset_index(
        drop=True)

      # get client data
      client = pd.DataFrame(sub_df.loc[idx, 'client'], index=[0])

      # get answers
      cache_df = pd.DataFrame.from_dict(sub_df['answers'][idx])

      # if answers is empty, continue in loop
      if cache_df.empty:
        i += 1
        continue

      cache_dict = dict(zip(cache_df.label, cache_df.value))
      answers_df = pd.DataFrame.from_dict(cache_dict, orient='index').transpose()

      # concat info, client, and answers
      df_concat = pd.concat([info, answers_df, client], axis=1)

      # write ans_concat at the end of output
      output = output.append(df_concat, ignore_index=True)

    # get meaningful filename
    fname = key.replace(' ', '_').lower()

    # handle surrogates
    output = output.applymap(lambda x: str(x).encode("utf-8", errors="ignore").decode("utf-8", errors="ignore"))

    # Check shape of output! should be 1540 for parents, but its 440 written
    print(fname)
    print(output.shape)
    print()

    # save file to dic
    res_dic[key] = output

  # return result
  return res_dic



if __name__ == '__main__':
  print('main executed')

  # get all tables, this takes a while
  tabs = tables.get_all_tables()

  # get all answers from all quetionnnaires
  ans = tabs['answers']

  # get questionnaires table
  qs = tabs['questionnaires']


  dfs_dic = get_dataframes(ans, qs)


  # get different dataframes from the cc study
  dfs = dict(list(tabs['answers'].groupby('questionnaire_id')))

  # Inactive FollowUp Questaionnaires have to be appended to active FollowUp
  # Inactive Baselin questionnaires can be dropped



  # TODO: Merge different versions of RKI questionnaires and save separately

  qs = tabs['questionnaires']

  # TODO: Unstack dataframe answersheets, for ideas, check \Dropbox (University of Wuerzburg)\20-05-12_Corona_Check


  # save dataframe to dir
  tday = date.today().strftime("%y-%m-%d")

  # write date to CSV file
  path = '../../../results/dataframes/cc'
  Path(path).mkdir(parents=True, exist_ok=True)

  # safe all tables to disk
  for key in tabs.keys():
    tabs[key].to_csv(f'{path}/{tday}_{key}.csv')
