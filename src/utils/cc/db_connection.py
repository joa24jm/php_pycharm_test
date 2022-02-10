__author__ = 'CV'
__copyright__ = 'Copyright 2022, TYH Dashboard Project'
__credits__ = ['CV', 'JA']
__license__ = 'GPL'
__version__ = '0.0.2'
__maintainer__ = 'CV'
__email__ = '???'
__status__ = 'Development'

import os
import logging
from unittest import result
from dotenv import load_dotenv
import pymysql
import pandas as pd
import sshtunnel
from sshtunnel import SSHTunnelForwarder

################################################################
## Load .env variables
################################################################
load_dotenv()
ssh_host = os.environ.get('ssh_host')
ssh_username = os.environ.get('ssh_username')
ssh_password = os.environ.get('ssh_password')
database_username = os.environ.get('database_username')
database_password = os.environ.get('database_password')
database_name = os.environ.get('database_name')
localhost = os.environ.get('localhost')
################################################################

################################################################
# Uncomment (out)
################################################################
# print('================================')
# print('ssh_host', '\t\t', ssh_host)
# print('ssh_username', '\t\t', ssh_username)
# print('ssh_password', '\t\t', ssh_password)
# print('database_username', '\t', database_username)
# print('database_password', '\t', database_password)
# print('database_name', '\t\t', database_name)
# print('localhost', '\t\t', localhost)
# print('================================')
################################################################

################################################################
# Guide: https://mariadb.com/de/resources/blog/how-to-connect-python-programs-to-mariadb/
################################################################
def open_ssh_tunnel(verbose=False):
  """Open an SSH tunnel and connect using a username and password.
  
  :param verbose: Set to True to show logging
  :return tunnel: Global SSH tunnel connection
  """

  logging.info('open_ssh_tunnel')
  
  if verbose:
    sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
  
  global tunnel
  tunnel = SSHTunnelForwarder(
    (ssh_host, 22),
    ssh_username = ssh_username,
    ssh_password = ssh_password,
    remote_bind_address = ('127.0.0.1', 3306)
  )
  
  tunnel.start()

def mysql_connect():
  """Connect to a MySQL server using the SSH tunnel connection
  
  :return connection: Global MySQL database connection
  """
  
  global connection
  
  connection = pymysql.connect(
    host='127.0.0.1',
    user=database_username,
    passwd=database_password,
    db=database_name,
    port=tunnel.local_bind_port
  )

def run_query(sql):
  """Runs a given SQL query via the global database connection.
  
  :param sql: MySQL query
  :return: Pandas dataframe containing results
  """
  
  return pd.read_sql_query(sql, connection)

def mysql_disconnect():
  """Closes the MySQL database connection.
  """
  
  connection.close()

def close_ssh_tunnel():
  """Closes the SSH tunnel connection.
  """
  
  tunnel.close

def run_multiple(queries):
  open_ssh_tunnel()
  mysql_connect()

  result = {}

  for query_name, query in queries.items():
    result[query_name] = run_query(query)

  mysql_disconnect()
  close_ssh_tunnel()

  return result

def run(query):
  open_ssh_tunnel()
  mysql_connect()

  result = run_query(query)

  mysql_disconnect()
  close_ssh_tunnel()

  return result

################################################################
# main
################################################################

def main():
  # Get head of users
  users_query = 'SELECT * FROM users'
  users = run(users_query)
  print('users.head():', '\t', users.head())

  # Get the user count
  users_count_query = 'SELECT COUNT(*) FROM users'
  userCount = run(users_count_query)
  print('User count: ', '\t', userCount.values[0][0])

  # Run multiple queries in the same connection and return the head
  questionnaires_query = 'SELECT * FROM questionnaires'
  queries = {
    'users': users_query,
    'questionnaires': questionnaires_query
  }
  results = run_multiple(queries)
  print(dict(map(lambda item: (item[0], item[1].head()), results.items())))

if __name__ == '__main__':
  main()
