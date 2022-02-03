import pandas as pd
import glob
import json
from pathlib import Path

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
        df = pd.read_csv(csv_file, index_col='Unnamed: 0')
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
    ans = create_readable_answers_df(dfs_dic['answers'], cb)

    # write date to CSV file
    path = '../../results/output/tyt'
    Path(path).mkdir(parents=True, exist_ok=True)
    ans.to_csv(path+'/22-01-17_answers_unstacked.csv', index=False)

    # create codebook
    cb = create_codebook(dfs_dic['questions'])

    ######################################################
    # test aggregtation
    ans = pd.read_csv('../../results/output/tyt/22-01-17_answers_unstacked.csv')

    # ans.head()

    # count gender (gives series)
    sex_distribution = ans['5'].value_counts()

    # count gender by handedness (gives dataframe)
    sex_by_handedness = pd.crosstab(ans['5'], ans['6'])

    # number of users
    num_users = ans.user_id.nunique()

    # range date of data
    ans_raw = pd.read_csv('../../results/dataframes/tyt/22-01-17_answers.csv')
    start_date = ans_raw.created_at.min()
    end_date = ans_raw.created_at.max()

if __name__=='__main__':
    main()
