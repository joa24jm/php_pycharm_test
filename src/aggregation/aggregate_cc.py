# Author Johannes Allgaier

# imports
import pandas as pd
import os
import json
from numpyencoder import NumpyEncoder

def main():
    # read in latest ch dataframe
    cc_dfs = sorted([df for df in os.listdir('../../results/dataframes/cc/') if 'corona-check-data' in df])
    # last df is the latest
    df_name = cc_dfs[-1]
    # read in
    df = pd.read_csv(f'../../results/dataframes/cc/{df_name}')

    # get some basic facts
    facts = {'n_users':None,
             'n_countries':None,
             'n_cor':None}
    # No. of users
    facts['n_users'] = df.user_id.nunique()
    # No. of countries
    facts['n_countries'] = df.country_code.nunique()
    # No. of corona evaluations
    facts['n_cor'] = df.corona_result.count()
    # Save to json
    with open(f'../../www/json/cc/basic_facts.json', 'w') as fp:
        json.dump(facts, fp, cls=NumpyEncoder)

    # Age Distribution
    df.age.replace({'[50, 60)':'50-59'}, inplace=True)
    age_distr = dict(df.age.value_counts().sort_index())
    # Save to json
    with open(f'../../www/json/cc/age_distribution.json', 'w') as fp:
        json.dump(age_distr, fp, cls=NumpyEncoder)

    # Corona result
    res_dic = {1:'Suspected coronavirus (COVID-19) case',
               2:'Symptoms, but no known contact with confirmed corona case',
               3:'Contact with confirmed corona case, but currently no symptoms',
               4:'Neither symptoms nor contact'}
    df.corona_result.replace(res_dic, inplace=True)
    corona_res = pd.crosstab(df.age, df.corona_result)
    corona_res.to_csv('../../www/json/cc/corona_result.csv', index_label='age')

if __name__ == '__main__':
    main()
