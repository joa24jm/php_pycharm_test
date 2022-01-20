import dbConnection

# answers, standard answers, users, questionnaires, ...

def test():
  dbConnection.run(queries=[])

def get_all_users():
  sql_query = "SELECT * FROM users"

  users = dbConnection.run(sql_query)

  return users

# users = get_all_users()
# print('users.head():', '\t', users.head())
# print('TEST END')
