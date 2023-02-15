#%%
import requests
from pprint import pprint
import pandas as pd
import json
from datetime import datetime
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
warnings.filterwarnings("ignore")

#contributors

contributors_url=f"https://api.github.com/repos/pandas-dev/pandas/stats/contributors"
response = requests.get(contributors_url)
contributors = json.loads(response.text)

df_contributors = pd.DataFrame(columns=['id','name','nb_contributions'])
# Afficher la liste des contributeurs
for contributor in contributors:
    
    new_row = {'id': contributor["author"]['id'], 'name': contributor['author']['login'], 'nb_contributions': contributor['total'] }
    df_contributors = df_contributors.append(new_row, ignore_index=True)  
print(df_contributors)
#df_contributors.to_csv('list_cont.csv',index=False)

#-------------------------------------------------------commits--------------------------------------------

commits_url=f"https://api.github.com/repos/pandas-dev/pandas/commits"
params = {
    'per_page': 200
}
commits_data = requests.get(commits_url,params=params)
commits = json.loads(commits_data.text)

#commits=json.dumps(commits_data)
df_commit = pd.DataFrame(columns=['id','name','commit_date','sha'])
for contributor in commits:
    new_row = {'id': contributor["author"]['id'], 'name': contributor["commit"]['author']['name'], 'commit_date':contributor['commit']['author']['date'], 'sha':contributor['commit']['tree']['sha'] }
    df_commit = df_commit.append(new_row, ignore_index=True) 


df_commit[['date', 'time']] = df_commit['commit_date'].str.split('T', expand=True) 
  
print(df_commit)
#df_commit.to_csv('list_commits.csv',index=False)

# ------------------------------------commit monitoring----------------------------------------------------
count = df_commit[['date']].value_counts()

monitoring=count.to_frame()
monitoring.reset_index(level=0, inplace=True)
monitoring.rename(columns = {0:'nb_commits'}, inplace = True)

with open('monitoring file.txt', 'w') as f:
    f.write('Date de monitoring : ')
    f.write('\n')
    f.write(str(datetime.now()))
    for index,row in monitoring.iterrows():
        if int(row['nb_commits']) < 11:
            f.write('\n MOINS DE 2 COMMITS : \n')
            
            f.write((str(row['date'])) )
            f.write(': nombre de commits = ')
            f.write( str(row['nb_commits']))
            
        else:
            f.write('\n Le nombre de commits par jour \n')
            f.write((str(row['date'])) )
            f.write(': nombre de commits = ')
            f.write( str(row['nb_commits']))
            

#-----------------------------------------Visualisation--------------------------------------------------

contributions_par_contributeur = df.groupby('nb_contributions').size()
plt.figure(figsize=(30, 28))
plt.title('Nombre de contributeurs par nombre contribution')
plt.xlabel('Nombre de contribution')
plt.ylabel('Nombre de contributeur')

plt.xlim(0, 30)
plt.ylim(0, 30)
plt.hist(contributions_par_contributeur, bins=10)

#-----------------------------------------Bonus-----------------------------------------------
cont = []
com = []

for item in contributors:
    cont.append(item['author']['login'])

    for week in item['weeks']:
        timestamp = datetime.fromtimestamp(week['w'])
        com.append([item['author']['login'], timestamp.date(), week['c']])

df = pd.DataFrame(com, columns=['contributor', 'date', 'commits'])
print( df, cont)
