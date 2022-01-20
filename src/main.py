import mariadb
import sys
from sshtunnel import SSHTunnelForwarder
import pandas as pd
from datetime import date
from DBConnection import dbConnection as dbc


def connect_to_db(user='jallgaierch', pw='P31bmiSIFeNrFyNI', host='127.0.0.1', port=3306, database='tinnitustyt17012022'):
    """
    Connects to MariaDB using the mariadb package, returns a cursor object for the database.
    :param user, default 'jallgaierch'
    :param pw, default 'P31bmiSIFeNrFyNI'
    :param host, default 'localhost'
    :param port, default 3306 (int)
    :param database: Name of the database copy, default 'tinnitustyt17012022'
    :return: cursor object
    """
    try:

        # TODO: Check SSH tunnel connection
        # works so far only using PUTTY (start external before running this script)
        # create SSH tunnel connection

        with SSHTunnelForwarder(
                ('81.169.177.204', 22),
                ssh_username=user,
                ssh_password=pw,
                remote_bind_address=(host, port)) as server:
            """
            con = MySQLdb.connect(user='mysql_username', passwd='mysql_password', db='mysql_db_name', host='mysql_host',
                                  port=server.local_bind_port)
            """
            # Connect to MariaDB Platform
            connection = mariadb.connect(
                user=user,
                password=pw,
                host=host,
                port=server.local_bind_port,
                database=database

            )
            
            cur = connection.cursor()
        """
        server = SSHTunnelForwarder(
            ('81.169.177.204', 22),
            ssh_username=user,
            ssh_password=pw,
            remote_bind_address=(host, port))

        server.start()

        # Connect to MariaDB Platform
        connection = mariadb.connect(
            user=user,
            password=pw,
            host=host,
            port=port,
            database=database

        )
        """
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    return connection

if __name__ == '__main__':

    print('main executed')

    dbc.open_ssh_tunnel()
    dbc.mysql_connect()

    # Test 1
    users = dbc.run_query("SELECT * FROM users")
    print('users.head():', '\t', users.head())

    # Test 2
    userCount = dbc.run_query("SELECT COUNT(*) FROM users")
    print('userCount: ', '\t', userCount)

    dbc.mysql_disconnect()
    dbc.close_ssh_tunnel()

    # drop unknown user_ids
    users.dropna(axis='rows', subset=['id'], inplace=True)
    # save dataframe to dir
    tday = date.today().strftime("%y-%m-%d")
    tday = "22-01-17" # database is just a view from that date
    # users.to_csv(f'results/dataframes/tyt/{tday}_users.csv')



