#!/usr/bin/env python
# coding: utf-8

# In[20]:


import requests
import pandas as pd
from pandas.io.json import json_normalize
import json


# <h1>Get Team Data</h1>

# <h3>More specifically, get each current NHL team's ID to use in NHL API calls</h3>

# The NHL API call used to get each current NHL team information

# In[21]:


url = 'https://statsapi.web.nhl.com/api/v1/teams'


# Using requests to get the teams data

# In[22]:


teams_data = requests.get(url)
print(teams_data)


# <b>SUCCESS!</b>

# Now a look at the teams data in JSON format

# In[23]:


teams_json = teams_data.json()
teams_json


# The team information is robust and deeply nested. It will need to be normalized (or flattened) to efficiantly work with

# In[24]:


teams_db = json_normalize(teams_json['teams'])
teams_db.head()


# Team ID's are located in the columns

# In[25]:


teams_db.columns


# Store all Team ID's in a list to use for NHL API call on individual teams current teams rosters

# In[26]:


team_ids = teams_db['id'].values
team_ids


# <h1>Get Roster Data</h1>

# <h3>More specifically, to get all player ID's from each teams current roster</h3>

# The NHL API call used to get current roster by team. Team ID must be appended to the url for each team

# In[27]:


url = 'https://records.nhl.com/site/api/player/byTeam/'


# Create an empty dataframe to append each teams roster

# In[28]:


roster_db = pd.DataFrame()


# For each team ID in team ID's, the team ID must first be appended to the url string for the NHL API call. Next, the roster data for that team must be loaded in, formatted to JSON, normalized, and appended to the roster dataframe to create one large dataframe of all the players, including their player ID's which will again be used to call the NHL API.

# In[29]:


for team_id in team_ids:
    team_roster_url = url + str(team_id)
    print('The roster url is ' + team_roster_url)
    print('Getting response from API page')
    team_roster_data = requests.get(team_roster_url)
    print(team_roster_data)
    team_roster_json = team_roster_data.json()
    team_roster_db = json_normalize(team_roster_json['data'])
    print('Appending data to Roster Database...')
    roster_db = roster_db.append(team_roster_db)
    print('Data appended successfully')
roster_db


# <h1>Export to CSV for use in data analysis</h1>

# <h3>While the NHL API is free to use, I would prefer working with the stored information in a CSV, to not make unnecessary calls later on when getting each players stats.</h3>

# In[99]:


roster_db.to_csv('New_Roster_Data.csv', index = None)


# In[ ]:




