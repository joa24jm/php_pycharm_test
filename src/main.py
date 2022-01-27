# import mariadb
import sys
from sshtunnel import SSHTunnelForwarder
import pandas as pd
from datetime import date
# from db_connection import db_connection as dbc
# sys.path.append("./remote")
from remote import db_connection as dbc
from remote import tables
from pathlib import Path

if __name__ == '__main__':
  print('main executed')

  # dbc.open_ssh_tunnel()
  # dbc.mysql_connect()

  # Test 1
  # users = dbc.run_query("SELECT * FROM users")
  users = tables.get_all_users()
  print('users.head():', '\t', users.head())

  # # Test 2
  # userCount = dbc.run_query("SELECT COUNT(*) FROM users")
  # print('userCount: ', '\t', userCount)

  # dbc.mysql_disconnect()
  # dbc.close_ssh_tunnel()

  # drop unknown user_ids
  users.dropna(axis='rows', subset=['id'], inplace=True)
  # save dataframe to dir
  tday = date.today().strftime("%y-%m-%d")
  tday = "22-01-17" # database is just a view from that date

  path = 'results/dataframes/tyt'
  Path(path).mkdir(parents=True, exist_ok=True)
  users.to_csv(f'{path}/{tday}_users.csv')
