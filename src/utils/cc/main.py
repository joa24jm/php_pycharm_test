from datetime import date
from pathlib import Path
import tables
from cc_helpers import create_dataframe, brush_up_dataframe, find_new_data
from src.aggregation import aggregate_cc
import pandas as pd
import os


if __name__ == '__main__':
  print('main executed')

  # get all tables, this takes a while
  tabs = tables.get_all_tables()

  # get different dataframes from the cc study
  df = tabs['answers']
  qs = tabs['questionnaires']

  # this goes into the else section when ran for the first time:
  Path('../../../results/dataframes/cc').mkdir(parents=True, exist_ok=True)
  if any(os.scandir('../../../results/dataframes/cc')):
    # read in last exported df to find out new answer_ids
    dates = [f.split('_')[0] for f in os.listdir('../../../results/dataframes/cc/') if 'corona-check-data' in f]
    old = pd.read_csv(f'../../../results/dataframes/cc/{sorted(dates)[-1]}_corona-check-data.csv',
                      index_col='answer_id')

    # find diff from old df
    print('Find new data since last export')
    new = find_new_data(old, df)
    if new.shape[0] == 0:
      print('Nothing to export, 0 new answers since last export.')
      exit()
    print(f'Found {new.shape[0]} new answers')

    # unstack the data
    print('Unstack new data')
    new = create_dataframe(new)
  else:
    print('Patience. This takes a while.')
    new = create_dataframe(df)

  # brush up new data
  print('Brush up new data')
  new = brush_up_dataframe(new)

  if any(os.scandir('../../../results/dataframes/cc/')):
    # append to old data
    print('Merge old and new data')
    new = old.append(new)

  # save dataframe to dir
  tday = date.today().strftime("%y-%m-%d")
  #
  # write date to CSV file
  path = '../../../results/dataframes/cc'
  Path(path).mkdir(parents=True, exist_ok=True)

  # safe all tables to disk
  new.to_csv(f'{path}/{tday}_corona-check-data.csv', index_label='answer_id')

  print(f'All done. New dataframe has shape {new.shape}.')

  # run aggregation pipeline
  aggregate_cc.main()