# Author Johannes Allgaier

# imports
import pandas as pd
import numpy as np
import json
from geopy.geocoders import Nominatim
import time


def find_new_data(latest_df, latest_export):
    """
    Drops all lines in latest_export with answer_ids that are already in latest_df.
    This saves a lot of computation when an update for the data is requested.

    Returns
    -------
    latest_export df that contains only answer ids that are not in latest_df

    """

    # rename 'id' to 'answer_id'
    latest_export.rename(columns={'id': 'answer_id'}, inplace=True)
    # set answer_id column as index
    latest_export.set_index('answer_id', inplace=True)

    df_answer_ids = set(latest_df.index)
    latest_answer_ids = set(latest_export.index)

    new_ids = list(latest_answer_ids - df_answer_ids)

    # return reduced latest_export
    return latest_export.loc[new_ids, :]

def create_dataframe(df):
  """
  Reads in a answer csv file and creates a df that contains the answers for
  one user per line.

  Returns
  -------
  Merged df from answers, client and sensordata.

  """

  # Replace None with Nan
  df = df.fillna(value=np.nan)

  meta_cols = ['user_id', 'questionnaire_id', 'locale',
               'flags', 'deleted_at', 'created_at', 'updated_at']

  ans_df = pd.DataFrame()
  sens_df = pd.DataFrame()
  client_df = pd.DataFrame()
  meta_df = pd.DataFrame()

  for i, idx in enumerate(df.index):

    # meta data
    meta_df.loc[idx, meta_cols] = df.loc[idx, meta_cols]

    # answers
    ans_ls = json.loads(df.loc[idx, :]['answers'])
    ans_dic = {dic['label']: dic['value'] for dic in ans_ls}
    # required for correct appending of dic to DataFrame
    try:
      ans_dic['symptoms'] = [ans_dic['symptoms']]
    except:
      pass

    ans_df = ans_df.append(pd.DataFrame(ans_dic, index=[idx]))

    # sensordata
    if not pd.isna(df.loc[idx, 'sensordata']):
      sens_dic = json.loads(df.loc[idx, :]['sensordata'])[0]
      sens_df = sens_df.append(pd.DataFrame(sens_dic, index=[idx]))

    # clientdata
    client_dic = json.loads(df.loc[idx, :]['client'])
    client_df = client_df.append(pd.DataFrame(client_dic, index=[idx]))

  # %% Merge new data
  res = pd.concat([meta_df, ans_df, sens_df, client_df], axis=1)

  # Rename 'id' to 'answer_id'
  res = res.rename(columns={'id':'answer_id'})

  return res


def brush_up_dataframe(df):
    """
    Takes a corona health pre-dataframe and does the following:
        1. Expand all symptoms to extra columns
        2. Creates a column for operating systems
        3. Converts GPS locations to country codes (slow!)
        4. Merges different age types (some are integer, some are string-bins like '20-29')
        5. Merges different versions of the questionnaire
        6. Gets the corona-check result
    Parameters
    ----------
    df : dataframe generated from script 'create_pre_df.py'

    Returns
    -------
    None.

    """

    # get all symptoms
    print('1. Expand all symptoms to extra columns')
    ls = ['fever', 'sorethroat', 'runnynose', 'cough', 'losssmell', 'losstaste',
          'shortnessbreath', 'headace', 'musclepain', 'diarrhea', 'generalweakness']

    # append col to df
    # set all symptoms per default as false
    for col in ls:
        df[col.lower()] = False

    # loop over df
    for idx in df.index:
        # if there is a symtpom, set the corresponding column on True
        if type(df.loc[idx, 'symptoms']) != float:
            for s in df.loc[idx, 'symptoms']:
                df.loc[idx, s.lower()] = True

                # 2. Creates a column for operating systems
    print('2. Creates a column for operating systems')
    df['operating_system'] = None
    for i, idx in enumerate(df.index):
        if 'Android' in df.loc[idx, 'os']:
            df.loc[idx, 'operating_system'] = 'Android'
        elif 'iOS' in df.loc[idx, 'os']:
            df.loc[idx, 'operating_system'] = 'iOS'
        else:
            continue

    # 3. Converts GPS locations to country codes (slow!)
    print('Get country codes for all available sensordata. This takes a while.')

    # get all idxs that have a value in latitude and longitude
    idx_lat = df[df['latitude'].notna()].index
    idx_lon = df[df['longitude'].notna()].index
    idxs = list(set(idx_lat) & set(idx_lon))

    # create a locater object using the geopy library
    locator = Nominatim(user_agent="openmapquest", timeout=10)

    # get list of gps df
    ls_of_gps = [list(df.loc[i, ['latitude', 'longitude']]) for i in idxs]

    # define the country code column
    df['country_code'] = None

    # loop over gps df # TODO: Debug geocoder, throws runtime error
    for i, gps in enumerate(ls_of_gps):

        coordinates = f"{gps[0]}, {gps[1]}"
        location = locator.reverse(coordinates)
        # get the country code
        try:
            df.loc[idxs[i], 'country_code'] = dict(location.raw)['address']['country_code'].upper()
            time.sleep(1)
        except:
            print(f'No country_code for {dict(location.raw)}')
        print('countrycode ', i, 'of', len(ls_of_gps))

    # 4. Merges different age types
    print('4. Merges different age types')

    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 130]
    # select only questionnaire_id == 1
    age_series = pd.cut(df[df['questionnaire_id'] == 1]['age'].astype('float'), bins, right=False)

    df.loc[age_series.index, 'age'] = age_series

    mapping = {'[0.0, 10.0)': '00-09',
               '[10.0, 20.0)': '10-19',
               '[20.0, 30.0)': '20-29',
               '[30.0, 40.0)': '30-39',
               '[40.0, 50.0)': '40-49',
               '[50.0, 60.0)': '50-59',
               '[50, 60)':'50-59', # one outlayer in the dataset?
               '[60.0, 70.0)': '60-69',
               '[70.0, 80.0)': '70-79',
               '[80.0, 130.0)': '80+'
               }

    # convert intervall objects to str
    df['age'] = df['age'].astype('str')

    # replace values for age
    df.replace({'age': mapping}, inplace=True)

    # cols to drop
    cols_to_drop = ['flags', 'deleted_at', 'os', 'name']
    df.drop(columns=cols_to_drop, inplace=True)

    # Replace YES with NO and vice versa for questionnaire_id == 2
    print('5. Merge different versions of the questionnaire')

    # get all questions with version 2
    idxs = df[df['questionnaire_id'] == 2].index

    # invert answer meaning
    df.loc[idxs, 'research'].replace({'YES': 'NO',
                                      'NO': 'YES'},
                                     inplace=True)

    # get corona results
    print('6. Get the corona-check result')

    any_symptoms_idxs = df[df.symptoms.notnull()].index
    idxs1 = df.loc[any_symptoms_idxs, 'person'][df['person'] == 'YES'].index
    idxs2 = df.loc[any_symptoms_idxs, 'person'][df['person'] == 'NO'].index

    no_symptoms_idxs = df[df.symptoms.isnull()].index
    idxs3 = df.loc[no_symptoms_idxs, 'person'][df['person'] == 'YES'].index
    idxs4 = df.loc[no_symptoms_idxs, 'person'][df['person'] == 'NO'].index

    df['corona_result'] = None
    df.loc[idxs1, 'corona_result'] = 1
    df.loc[idxs2, 'corona_result'] = 2
    df.loc[idxs3, 'corona_result'] = 3
    df.loc[idxs4, 'corona_result'] = 4

    # save df to csv
    print('Done.\n\n\n\n')

    return df

def main():
    pass


if __name__ == '__main__':
    main()
