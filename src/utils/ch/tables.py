import sys, os
sys.path.append(os.path.join(sys.path[0], '..', '..', '..'))

__author__ = 'CV'
__copyright__ = 'Copyright 2022, Dashboard Project'
__credits__ = ['CV', 'JA']
__license__ = 'GPL'
__version__ = '0.0.1'
__maintainer__ = 'CV'
__email__ = '???'
__status__ = 'Development'

if __name__ == '__main__':
  import db_connection as dbc
else:
  from src.utils.ch import db_connection as dbc

# sql_query_users = 'SELECT * FROM users'
sql_query_questionnaires = 'SELECT * FROM questionnaires'
# sql_query_questions = 'SELECT * FROM questions'
sql_query_answers = 'SELECT * FROM answersheets'


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
    # 'users': get_all_users(),
    'questionnaires': get_all_questionnaires(),
    # 'questions': get_all_questions(),
    'answers': get_all_answers(),
    # 'standardanswers': get_all_standardanswers(),
  }

def main():
  print('GO')
  for key, value in get_all_tables().items():
    print(key + '.head() - BEGIN')
    print(value.head())
    print(key + '.head() - END')

  tables = dbc.run_multiple({
    # 'users': sql_query_users,
    'questionnaires': sql_query_questionnaires,
    # 'questions': sql_query_questions,
    'answers': sql_query_answers,
    # 'answers': sql_query_answers
  })
  print(dict(map(lambda item: (item[0], item[1].head()), tables.items())))

  print('FINISH')

if __name__ == '__main__':
  main()
