import streamlit as st
import pandas as pd
import numpy as np

@st.cache
def readDataframes():
    country = pd.read_csv('./country.csv',decimal=',')

    exchange = pd.read_csv(
        './euro-daily-hist_1999_2022.csv',
        decimal=',',
        parse_dates=['Period\\Unit:'],
        )
    
    return country,exchange

country,exchange = readDataframes()

"""
# Impacto da importação/exportação dos Estados Unidos no câmbio
"""



"""
Os dados utilizados forma estraídos dos seguintes links:

* https://www.kaggle.com/datasets/lsind18/euro-exchange-daily-rates-19992020
* https://www.census.gov/foreign-trade/balance/c5700.html

Os arquivos foram baixados no dia 18/05/2022

"""


"""

## Exploração dos dados
Os dados de exportação dos Estados Unidos, as colunas representão os 12 meses
do ano anotados como exportação e importação, assim como também o geral anual.
As linhas contém um país de comparação e o ano do dado.

"""

"""
### Dados de exportação/importação
Todos os valores apresentados se encontram em milhões de dolares, abaixo é
possível selecionar um país específico para visualizar as exportações e
importações anuais.
"""
@st.cache
def getUniqueCountries(dataframe, column):
    return dataframe[column].unique()

countries = getUniqueCountries(country,'CTYNAME')

selectedCountry = st.selectbox(
    'Selecione um pais para visualizar os dados anuais de um país: ',
    countries
    )


@st.cache
def subselectByCountry(country,selection):
    subset = country[country['CTYNAME']==selection]
    subset = subset[['year','IYR','EYR']]
    subset['year'] = subset['year'].astype('string')
    subset = subset.set_index('year')
    print(subset.index)
    return subset

st.line_chart(subselectByCountry(country,selectedCountry))

"""
###  Dados de câmbio
Os dados estão atualmente relativos ao euro (EUR)
"""

st.write(exchange)

coins = exchange.columns[1:]
selectedCoin = st.selectbox(
    'Selecione uma moeda para visualizar os dados em relação ao EUR dos últimos 365 dias: ',
    coins
    )
@st.cache
def subselectByCoint(exchange,selection):
    subset = exchange[['Period\\Unit:',selection]].head(365)
    subset = subset[subset[selection].str.contains('-')==False]
    subset[selection] = subset[selection].astype('float')
    subset = subset.set_index('Period\\Unit:')
    return subset


st.line_chart(subselectByCoint(exchange,selectedCoin))

"""
## Impacto do câmbio na exportação/importação
"""

countryPair = {
    '[Australian dollar ]': 'Australia',
    '[Bulgarian lev ]': 'Bulgaria',
    '[Brazilian real ]': 'Brazil',
    '[Canadian dollar ]': 'Canada',
    '[Swiss franc ]': 'Switzerland',
    '[Chinese yuan renminbi ]': 'China',
    '[Czech koruna ]': 'Czech Republic',
    '[Estonian kroon ]': 'Estonia',
    '[UK pound sterling ]': 'United Kingdom',
    '[Greek drachma ]': 'Greece',
    '[Hong Kong dollar ]': 'Hong Kong',
    '[Croatian kuna ]': 'Croatia',
    '[Hungarian forint ]': 'Hungary',
    '[Indonesian rupiah ]': 'Indonesia',
    '[Israeli shekel ]': 'Indonesia',
    '[Indian rupee ]': 'India',
    '[Iceland krona ]': 'Iceland',
    '[Japanese yen ]': 'Japan',
    '[Korean won ]': 'Korea, South',
    '[Lithuanian litas ]': 'Lithuania',
    '[Mexican peso ]': 'Mexico',
    '[Malaysian ringgit ]': 'Malaysia',
    '[New Zealand dollar ]': 'New Zealand',
    '[Philippine peso ]': 'Philippines',
    '[Polish zloty ]': 'Poland',
    '[Romanian leu ]': 'Romania',
    '[Russian rouble ]': 'Russia',
    '[Swedish krona ]': 'Sweden',
    '[Singapore dollar ]': 'Singapore',
    '[Slovenian tolar ]': 'Slovenia',
    '[Slovak koruna ]': 'Slovakia',
    '[Thai baht ]': 'Thailand',
    '[Turkish lira ]': 'Turkey',
    '[South African rand ]': 'South Africa'
    }

selectedPair = st.selectbox(
    'Selecione um par:',
    countryPair.keys()
    )

#maxDate = 

#fromDate = st.date_input('Desde:')
#toDate = st.date_input('Até:')
st.write(selectedPair)

def filterResult(exchange,country,pairs,selection):
    selectedCountry = pairs[selection]
    selectedCoin = selection
    months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

    countrySubset = country[country['CTYNAME']==selectedCountry]

    data = []
    for r in countrySubset.iterrows():
        y = r[1]
        for m in months:
            data.append({
                'date':'%s %s'%(m,y['year']),
                'importValue': y['I%s'%m],
                'exportValue': y['E%s'%m],
                })
    
    dt = pd.DataFrame(data)

    dt = dt.set_index('date')
    return dt

st.write(filterResult(exchange,country,countryPair,selectedPair))
st.line_chart(filterResult(exchange,country,countryPair,selectedPair))
st.line_chart(subselectByCoint(exchange,selectedPair))
