import pandas as pd
import glob
import json
from pathlib import Path
from datetime import datetime#
import numpy as np

def create_codebook(questions_df):
    """

    :param questions_df: dfs_dic['questions']
    :return:
    """

    return dict(zip(questions_df['id'].values, questions_df['question'].values))

def read_in_dataframes():
    """
    Reads in all .csv files from the tyt project
    :return:
    """
    csv_files = glob.glob('..\\..\\results\\dataframes\\tyt\\*.csv')

    dfs_dic = dict()

    for csv_file in csv_files:
        name = csv_file.split('\\')[-1].split('.')[0].split('_')[-1]
        try:
            df = pd.read_csv(csv_file, index_col='Unnamed: 0')
        except:
            df = pd.read_csv(csv_file)
        dfs_dic[name] = df

    return dfs_dic

def get_values_from_answers_table(ans, question_id, cb):
    """
    :param ans: answers dataframe
    :param question_id: id of the question
    :param cb: codebook holding the question to the question_id
    :return: res: dataframe with all the answers to the question
    """

    res = ans[ans.question_id==question_id][['id','user_id','answer','created_at']].set_index('created_at')
    res.rename(columns={'id':'answer_id', 'answer': cb[question_id]}, inplace = True)

    return res

def create_readable_answers_df(ans, cb):

    res = pd.DataFrame(index=ans.user_id.unique(), columns=cb.keys())

    for user_id in res.index:
        print(user_id)
        for question_id in res.columns:
            try:
                # TODO: Faster solution than that? pd.pivot, pd.unstack?
                res.loc[user_id, question_id] = ans[(ans.user_id==user_id) & (ans.question_id==question_id)].answer.values[0]
            except:
                # TODO: Better exception?
                pass
    return res

def create_stats(df):

    # TODO Which information is interesting? What to show on the website?
    # baseline stats
    pass

def main():

    # read in all csv files that are in the tyt project
    dfs_dic = read_in_dataframes()

    # drop unknown user_ids
    dfs_dic['users'].dropna(axis='rows', subset=['id'], inplace=True)

    # drop unknown user_ids in answers
    dfs_dic['answers'].dropna(axis='rows', subset=['user_id'], inplace=True)

    # create codebook
    cb = create_codebook(dfs_dic['questions'])

    # get gender information
    gender_df = get_values_from_answers_table(dfs_dic['answers'], 5, cb)
    gender_s = gender_df.iloc[:, -1].value_counts()

    # this takes a couple of minutes
    if 'unstacked' not in dfs_dic.keys():
        ans = create_readable_answers_df(dfs_dic['answers'], cb)
        # write date to CSV file
        date_str = '22-01-17'
        path = '../../dataframes/tyt'
        Path(path).mkdir(parents=True, exist_ok=True)
        ans.to_csv(path + f'/{date_str}_answers_unstacked.csv', index=False)
    else:
        ans = dfs_dic['unstacked']

    # create codebook
    cb = create_codebook(dfs_dic['questions'])

    ######################################################
    # test aggregation

    # count gender (gives series)
    sex_distribution = ans['5'].value_counts()

    # count gender by handedness (gives dataframe)
    sex_by_handedness = pd.crosstab(ans['5'], ans['6'])
    sex_by_handedness.to_json('../../www/json/tyt/sex_by_handedness.json')

    # number of users
    num_users = ans.user_id.nunique()

    # range date of data
    ans_raw = pd.read_csv('../../results/dataframes/tyt/22-01-17_answers.csv')
    start_date = ans_raw.created_at.min()
    end_date = ans_raw.created_at.max()

    # Age distribution
    ans.replace('??.??.????', np.NaN, inplace=True)
    ans['4'] = pd.to_datetime(ans['4'], format='%d.%m.%Y', errors='coerce')
    ans['4'].dt.year.value_counts().sort_index().to_json('../../www/json/tyt/age_distribution.json')



if __name__=='__main__':
    main()
