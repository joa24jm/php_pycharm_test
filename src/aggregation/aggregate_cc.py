# Author Johannes Allgaier

# imports
import pandas as pd
import os
import json
from numpyencoder import NumpyEncoder

# working directory should be \src\utils\cc\
def main():
    # read in latest ch dataframe
    cc_dfs = sorted([df for df in os.listdir('../../../results/dataframes/cc/') if 'corona-check-data' in df])
    # last df is the latest
    df_name = cc_dfs[-1]
    # read in
    df = pd.read_csv(f'../../../results/dataframes/cc/{df_name}')

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
    with open(f'../../../www/json/cc/basic_facts.json', 'w') as fp:
        json.dump(facts, fp, cls=NumpyEncoder)

    # Age Distribution
    df.age.replace({'[50, 60)':'50-59'}, inplace=True)
    age_distr = dict(df.age.value_counts().sort_index())
    # Save to json
    with open(f'../../../www/json/cc/age_distribution.json', 'w') as fp:
        json.dump(age_distr, fp, cls=NumpyEncoder)

    # Corona result
    res_dic = {1:'Suspected coronavirus (COVID-19) case',
               2:'Symptoms, but no known contact with confirmed corona case',
               3:'Contact with confirmed corona case, but currently no symptoms',
               4:'Neither symptoms nor contact'}
    df.corona_result.replace(res_dic, inplace=True)
    corona_res = pd.crosstab(df.age, df.corona_result)
    corona_res.to_csv('../../../www/json/cc/corona_result.csv', index_label='age')

    # Country by number of evaluations
    # read in iso2 -> countryname mapping and convert to dict
    iso2 = pd.read_csv('../../../src/sources/iso2-country-mapping.csv', encoding='cp1250')
    cc_dict = dict(zip(iso2.ISO2, iso2.en))
    corona_evals_by_country = pd.crosstab(df.country_code, df.corona_result).sum(axis=1)
    corona_evals_by_country = pd.DataFrame(corona_evals_by_country, columns=['count'])
    corona_evals_by_country['country'] = corona_evals_by_country.index.map(cc_dict)
    corona_evals_by_country = corona_evals_by_country[corona_evals_by_country['country'].notna()]
    corona_evals_by_country = dict(zip(corona_evals_by_country['country'],
                        corona_evals_by_country['count']))

    # re-assign dict keys

    # Save to json
    with open(f'../../../www/json/cc/corona_evals_by_country.json', 'w') as fp:
        json.dump(corona_evals_by_country, fp, cls=NumpyEncoder)

    # get a count of the symptoms
    symptoms_ls = ['fever', 'sorethroat', 'runnynose', 'cough', 'losssmell', 'losstaste', 'shortnessbreath',
                   'headace', 'musclepain', 'diarrhea']
    symptoms_count = dict(df.loc[:, symptoms_ls].sum())
    # Save to json
    with open(f'../../../www/json/cc/symptoms_count.json', 'w') as fp:
        json.dump(symptoms_count, fp, cls=NumpyEncoder)

    # Education by country for the top 5 countries
    top_five_countries = df.country_code.value_counts().iloc[:5].index.to_list()
    # get iso2 mapping
    edu_by_country = pd.crosstab(df.education, df.country_code).loc[:, top_five_countries]
    edu_by_country = edu_by_country.reindex(['9ORLESS', '10TO11', '12ORMORE', 'NOANSWER'])
    # get speaking country names
    edu_by_country.columns = [cc_dict[col] for col in edu_by_country.columns]
    # normalize values to 100 %
    for col in edu_by_country.columns:
        edu_by_country[col] = edu_by_country[col] / edu_by_country[col].sum()

    # transpose for javascript
    edu_by_country = edu_by_country.transpose()
    # save to csv
    edu_by_country.to_csv('../../../www/json/cc/edu_by_country.csv', index_label='country')


if __name__ == '__main__':
    main()
