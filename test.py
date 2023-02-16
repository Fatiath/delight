#%%
#importation des bibliothèques

import requests
from pprint import pprint
import pandas as pd
import json
from datetime import datetime
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
warnings.filterwarnings("ignore")

#------------------------- données contributeurs--------------------------------

contributors_url=f"https://api.github.com/repos/pandas-dev/pandas/stats/contributors" #url api
response = requests.get(contributors_url)
contributors = json.loads(response.text) #récupération des données

df_contributors = pd.DataFrame(columns=['id','name','nb_contributions']) #création d'un dataframe vide

# récupération des informations des contributeurs et ajout dans le dataframe
for contributor in contributors:
    new_row = {'id': contributor["author"]['id'], 'name': contributor["author"]['login'], 'nb_contributions': contributor['total'] }
    df_contributors = df_contributors.append(new_row, ignore_index=True)  
print('Informations contributeurs :')

#affichage des informations des contributeurs
print(df_contributors)

#-------------------------------------------------------commits--------------------------------------------
#%%

liste_contributeurs = [] #définition d'une liste vide
liste_commits = [] #définition d'une liste vide

for contributor in contributors:
    liste_contributeurs.append(contributor['author']['login']) #récupération et ajout du login du contributeur dans liste_contributeurs

    for week in contributor['weeks']:
        timestamp = datetime.fromtimestamp(week['w']) #récupération de la valeur week et conversion en date
        liste_commits.append([contributor['author']['login'], timestamp.date(), week['c']]) #ajout des données du commit dans liste_commits

df = pd.DataFrame(liste_commits, columns=['contributor', 'date', 'commits'])

# ------------------------------------commit monitoring----------------------------------------------------
count = df.groupby('date')['commits'].sum() #comptage du nombre de commit par date

monitoring=count.to_frame()
monitoring.reset_index(level=0, inplace=True)
#insertion des jours avec moins de 2 commits dans un fichier texte jours_peu_actifs
with open('monitoring.txt', 'w') as f:
    f.write('Date de monitoring : ')
    f.write('\t')
    f.write(str(datetime.now()))
    for index,row in monitoring.iterrows():
        if int(row['commits']) < 2:
            f.write('\n MOINS DE 2 COMMITS : \n')
            f.write((str(row['date'])) )
            f.write(': nombre de commits = ')
            f.write( str(row['commits']))
            f.write('\n')
        else:
            f.write('\n')
            f.write((str(row['date'])) )
            f.write(': nombre de commits = ')
            f.write( str(row['commits']))
            f.write('\n')

#-----------------------------------------Visualisation--------------------------------------------------
#%%
#comptage du nombre de contributeur par contribution
contributions_par_contributeur = df_contributors.groupby('nb_contributions').size()

plt.figure(figsize=(30, 28))
#définition du titre et des axes de l'histogramme
plt.title('Nombre de contributeurs par nombre contribution')
plt.xlabel('Nombre de contribution')
plt.ylabel('Nombre de contributeur')
contributions_par_contributeur.plot(kind='bar')

#%%
#-----------------------------------------Bonus-----------------------------------------------
print('Nombre total de commit sur la branche principale du répertoire: ',str(df['commits'].sum()))

activity = [] #creation d'une liste vide

#récupération et calcul de statistiques des contributeurs
for contributor in liste_contributeurs:
    df_contributor = df[df['contributor'] == contributor]
    total_contributor_commits = df_contributor['commits'].sum() #nombre total de commit
    anciennete_en_jours = (datetime.now().date() - df_contributor['date'].min()).days #ancienneté du contributeur
    contributor_commits_per_day = total_contributor_commits / anciennete_en_jours #nombre de contribution par jour
    activity.append([contributor, total_contributor_commits, anciennete_en_jours, contributor_commits_per_day]) #insertion des infos dans la liste

df_activity = pd.DataFrame(activity, columns=['contributeur', 'total_commits', 'anciennete_en_jours', 'commits_par_jour'])
print('Activité contributeurs')
print(df_activity)

#affichage du nombre de commit par contributeur par ordre décroissant de commits
df_contributors = df_contributors.sort_values(by='nb_contributions', ascending=False)

# Création de la figure et des axes
fig, ax = plt.subplots()

# Création du graphique à barres avec les valeurs triées
bar_plot = ax.bar(df_contributors['name'], df_contributors['nb_contributions'])
plt.title('Total Commits by Contributor')
plt.xlabel('Contributor')
plt.ylabel('Total Commits')
plt.xticks(rotation=90)
fig.set_size_inches(10, 8)
plt.show()

