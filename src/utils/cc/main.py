from datetime import date
from pathlib import Path
import tables

if __name__ == '__main__':
  print('main executed')

  # get all tables, this takes a while
  tabs = tables.get_all_tables()

  # get different dataframes from the cc study
  dfs = dict(list(tabs['answers'].groupby('questionnaire_id')))

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
