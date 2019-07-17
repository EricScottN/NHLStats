#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from altair import Chart, X, Y, Color, Scale
import altair as alt


# <h1>Read in scraped CSV's</h1>

# In[2]:


roster_df = pd.read_csv('Roster_Data.csv')
stats_df = pd.read_csv('Stats_Data.csv')


# <h1>Merge Full Names back into Stats dataframe</h1>

# In my first pass on the NHL API, I didn't think to add full names but thought afterwards that it would be beneficial to have player names. In order to do so, the player names on the roster dataframe must be merged into the stats dataframe

# In[3]:


stats_df = stats_df.merge(roster_df[['id', 'fullName']], on='id')
stats_df['season'] = stats_df['season'].astype(str)
stats_df.dtypes


# <h1>How Many Points Are Scored By Each Age Group?</h1>

# First, group by age, the average amount of points scored

# In[4]:


avg_points_by_age = stats_df.groupby('age', as_index = False)['points'].mean()
avg_points_by_age


# In[5]:


Chart(avg_points_by_age).mark_bar().encode(
    x ='age',
    y ='points')


# <h3>Most points are scored at the age of 22 and points begin to fall at age 29</h3>

# <h1>How many points are scored by each age group each season</h1>

# In[6]:


avg_points_by_season = stats_df.groupby(['season', 'age'], as_index = False)['points'].mean()
avg_points_by_season.head()


# In[7]:


avg_points_by_season.sort_values(by=['points'], ascending = False)
avg_points_by_season.head()


# In[8]:


alt.Chart(avg_points_by_season).mark_area().encode(
    x="season",
    y="points",
    color = "age:N"
)


# <h3>It looks like scoring has been increasing each season at all age groups!</h3>

# <h1>How Old Were the Top Twenty Leading Scorers</h1>

# In[16]:


top_twenty_points = stats_df.nlargest(20, ['points'])


# In[26]:


Chart(top_twenty_points).mark_bar().encode(
    x ='age',
    y ='points',
    color = 'fullName')


# <h3>Blake Wheeler is an exception to the rule</h3>

# In[28]:


Chart(stats_df[stats_df['fullName']=='Blake Wheeler']).mark_bar().encode(
    x ='age',
    y ='points')


# In[ ]:




