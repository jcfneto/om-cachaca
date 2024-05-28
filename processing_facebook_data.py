import re

import pandas as pd
from pandas import DataFrame


URL_PATTERN = r'^(https?:\/\/)?([\w\-]+(\.[\w\-]+)+)(\/[\w\-._~:/?#[\]@!$&\'()*+,;%=]*)?$'
DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
COLS_TO_REMOVE = ['index', 'Unnamed: 10', 'is_url', 'is_date']


def is_url(url: str) -> bool:
    if isinstance(url, str):
        if re.match(URL_PATTERN, url):
            return True
    return False


def is_date(date: str) -> bool:
    if re.match(DATE_PATTERN, date):
        return True
    return False


def processing(df: DataFrame, pattern_to_empty: list = None) -> DataFrame:
    if pattern_to_empty:
        for p in pattern_to_empty:
            df.permalink_url = df.permalink_url.replace(p, '')
    df.text = df.text.fillna('') + df.permalink_url
    return df


def main():

    data = pd.read_csv(
        'data/raw/facebook-dataset-CachacaOM-completo.csv', low_memory=False
    ).iloc[:, 1:11]

    print(f'Iniciando com {data.shape[0]} registros.')

    columns = data.iloc[:, 2:-1].columns
    COLS_MAPPER = {columns[i]: columns[i + 1] for i in range(len(columns) - 1)}

    for i in range(5):
        data['is_url'] = data.permalink_url.map(is_url)
        data_misaligned = data[data['is_url'] == False].copy()
        data_misaligned = processing(data_misaligned, ['-)', ':'])

        for t, f in COLS_MAPPER.items():
            data_misaligned[t] = data_misaligned[f]

        data = pd.concat(
            [data[data.is_url == True], data_misaligned], ignore_index=True
        )

    data['is_date'] = data.created_time.map(is_date)

    # não é typo o isin a seguir
    data = data[
        (data.is_date == True) & (data.repetido.isin(['True', 'False']))
    ].dropna(subset=['text'])

    data.drop(columns=COLS_TO_REMOVE).to_csv(
        'data/processed/facebook_cachaca.csv', index=False
    )

    print(f'Finalizando com {data.shape[0]} registros.')


if __name__ == '__main__':
    main()
