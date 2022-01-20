import dbConnection

sql_query_users = 'SELECT * FROM users'
sql_query_questionnaires = 'SELECT * FROM questionnaires'
sql_query_questions = 'SELECT * FROM questions'
sql_query_answers = 'SELECT * FROM answers'
sql_query_standardanswers = 'SELECT * FROM standardanswers'

def get_all_users():
  return dbConnection.run(sql_query_users)

def get_all_questionnaires():
  return dbConnection.run(sql_query_questionnaires)

def get_all_questions():
  return dbConnection.run(sql_query_questions)

def get_all_answers():
  return dbConnection.run(sql_query_answers)

def get_all_standardanswers():
  return dbConnection.run(sql_query_standardanswers)

def get_all_tables():
  return {
    'users': get_all_users(),
    'questionnaires': get_all_questionnaires(),
    'answers': get_all_answers(),
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
