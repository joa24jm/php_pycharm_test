if __name__ == '__main__':
  import db_connection as dbc
else:
  from . import db_connection as dbc

sql_query_users = 'SELECT * FROM users'
sql_query_questionnaires = 'SELECT * FROM questionnaires'
sql_query_questions = 'SELECT * FROM questions'
sql_query_answers = 'SELECT * FROM answers'
sql_query_standardanswers = 'SELECT * FROM standardanswers'

def get_all_users():
  return dbc.run(sql_query_users)

def get_all_questionnaires():
  return dbc.run(sql_query_questionnaires)

def get_all_questions():
  return dbc.run(sql_query_questions)

def get_all_answers():
  return dbc.run(sql_query_answers)

def get_all_standardanswers():
  return dbc.run(sql_query_standardanswers)

def get_all_tables():
  return {
    'users': get_all_users(),
    # 'questionnaires': get_all_questionnaires(),
    # 'questions': get_all_questions(),
    # 'answers': get_all_answers(),
    # 'standardanswers': get_all_standardanswers(),
  }

# def test():
#   dbConnection.run(queries=[])

def main():
  print('GO')
  for key, value in get_all_tables().items():
    print(key + '.head() - BEGIN')
    print(value.head())
    print(key + '.head() - END')
  print('FINISH')

if __name__ == '__main__':
  main()
