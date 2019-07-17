#!/usr/bin/env python
# coding: utf-8

# In[49]:


import requests
import pandas as pd
from pandas.io.json import json_normalize
import json


# <h1>Get Statistics for Each Player</h1>

# <h3>Load in Roster Data</h3>

# Load in Roster Data CSV scraped from the NHL API.

# In[445]:


roster_db = pd.read_csv('Roster_Data.csv')
roster_db.head(5)


# In[421]:


roster_db.columns


# <h3>Filter data</h3>

# I need a few things. Player ID for API calls and amount of years pro to only include those players who have been in the pros for over 10 years. Also need position to not include goalies, as I am not looking for goalie stats.

# In[446]:


pro_roster_db = roster_db[(roster_db['accruedSeasons']>=10) & (roster_db['position']!= 'G') &
                         (roster_db['onRoster'] == 'Y')]
pro_roster_db.shape


# Sample set is down to 100 players

# Since age is not included in the player information, only date of birth, a column needs to be calculated

# In[447]:


pro_roster_db['age'] = pd.Timestamp('now') - pd.to_datetime(pro_roster_db['birthDate'])
pro_roster_db['age'] = pro_roster_db['age'].astype('timedelta64[Y]')


# <h1>Get Each Individual Players' Stats from Past Ten Seasons</h1>

# A list of seasons will be needed to append to the NHL API call to get individual stats for each player for each of the last ten seasons they've played in the NHL

# In[428]:


seasons = ['20182019','20172018','20162017','20152016','20142015','20132014','20122013','20112012','20102011','20092010']


# A new dataframe must be created to hold all stats from every season for every player

# In[439]:


all_stats_db = pd.DataFrame()


# For each row in the pro_roster dataframe, each season in seasons must be iterated through. For each iteration, the player ID from that row will be appeneded onto the NHP API call, including an additional modifier which will append the season to that players stats from that respective season. Each row of data will then be formatted to JSON and normalized. Additionally, the id, season, and age will be added as columns to that row. From there, each row is appeneded to the all_stats dataframe. For each pass through seasons, the age modifier will increase, and subtracted from that players age each season that passes as they will have been a year younger for each pass.

# In[439]:


for index, row in pro_roster_db.iterrows():
    age_modifier = 0
    for season in seasons:
        url = 'https://statsapi.web.nhl.com/api/v1/people/' + str(row['id']) + '/stats?stats=statsSingleSeason&season=' + season
        print(url)
        stats_data = requests.get(url)
        stats_json = stats_data.json()
        stats = json_normalize(stats_json,record_path = ['stats','splits'])
        stats['id'] = int(row['id'])
        stats['season'] = season
        stats['age'] = row['age'] - age_modifier
        all_stats_db = all_stats_db.append(stats, ignore_index = True)
        age_modifier += 1


# In[451]:


all_stats_db


# <b>There were almost 1000 calls to the NHL API! Wow! I hope I don't get arrested!</b>

# Because that JSON was deeply nested, there is still a column of data (stat) that has not been normalized. Using list comprehension, that column can be normalized and put into a new, better dataframe using pertinent information from the old dataframe including age, player id, and season

# In[452]:


best_stats = pd.DataFrame([stat for stat in all_stats_db.stat])


# In[453]:


best_stats.set_index(all_stats_db.index)
best_stats['age'] = all_stats_db.age
best_stats['season'] = all_stats_db.season
best_stats['id'] = all_stats_db.id


# In[454]:


best_stats


# <h1>Save to CSV</h1>

# <h3>Again, after almost 1000 NHL API calls, I would rather not unnecessarily call it again</h3>

# In[444]:


best_stats.to_csv('Stats_Data.csv', index = None)

