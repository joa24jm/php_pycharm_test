from datetime import date
from pathlib import Path
from src.utils.tyt import tables

if __name__ == '__main__':
  print('main executed')

  # get all tables, this takes a while
  tabs = tables.get_all_tables()



  # save dataframe to dir
  tday = date.today().strftime("%y-%m-%d")
  tday = "22-01-17" # database is just a view from that date

  # write date to CSV file
  path = '../../../results/dataframes/tyt'
  Path(path).mkdir(parents=True, exist_ok=True)

  # safe all tables to disk
  for key in tabs.keys():
    tabs[key].to_csv(f'{path}/{tday}_{key}.csv')
