import pandas as pd

face = pd.read_csv('data/opinions/facebook_cachaca.csv')
face = face[face.is_opinative == True]

if 'my_opinion' not in face.columns:
    face['my_opinion'] = None

face = face[face.my_opinion.isnull()]

for i, r in face.iterrows():
    print(f'"{r.text}" -> {r.labels}')
    my_opinion = input('Você concorda? ')
    if my_opinion == 'stop':
        break
    face.at[i, 'my_opinion'] = my_opinion

face.to_csv('data/opinions/facebook_cachaca2.csv', index=False)
