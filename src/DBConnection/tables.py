import dbConnection

# answers, standard answers, users, questionnaires, ...

def test():
  dbConnection.run(queries=[])

def get_all_users():
  sql_query = "SELECT * FROM users"

  result = dbConnection.run(sql_query)

  return result

def get_all_answers():
  sql_query = "SELECT * FROM answers"

  result = dbConnection.run(sql_query)

  return result

# users = get_all_users()
# print('users - BEGIN')
# print('users.head():', '\t', users.head())
# print('users - END')

# answers = get_all_answers()
# print('answers - BEGIN')
# print('answers.head():', '\t', answers.head())
# print('answers - END')
