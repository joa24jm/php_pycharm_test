import sys
from sshtunnel import SSHTunnelForwarder
import pandas as pd
from datetime import date
from remote import db_connection as dbc
from remote import tables
from pathlib import Path

if __name__ == '__main__':
  print('main executed')

  users = tables.get_all_users()
  print('users.head():', '\t', users.head())

  # drop unknown user_ids
  users.dropna(axis='rows', subset=['id'], inplace=True)
  
  # save dataframe to dir
  tday = date.today().strftime("%y-%m-%d")
  tday = "22-01-17" # database is just a view from that date

  # write date to CSV file
  path = 'results/dataframes/tyt'
  Path(path).mkdir(parents=True, exist_ok=True)
  users.to_csv(f'{path}/{tday}_users.csv')
