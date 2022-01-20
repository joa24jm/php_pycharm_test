import pandas as pd
import glob


def read_in_dataframes():
    """
    Reads in all .csv files from the tyt project
    :return:
    """
    csv_files = glob.glob('..\\..\\results\\dataframes\\tyt\\*.csv')

    dfs_dic = dict()

    for csv_file in csv_files:
        name = csv_file.split('\\')[-1].split('.')[0]
        df = pd.read_csv(csv_file, index_col='Unnamed: 0')
        dfs_dic[name] = df

    return dfs_dic

def main():

    # read in all csv files that are in the tyt project
    dfs_dic = read_in_dataframes()

    #
if __name__=='__main__':
    main()