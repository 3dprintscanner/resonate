
# coding: utf-8

# In[261]:


get_ipython().run_line_magic('config', 'IPCompleter.greedy=True')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[262]:


def set_date(row):
    if row['plannedtime'] == 0:
        timeval = row['event_time'] + pd.Timedelta(minutes=row['lateness'])
    else:
        timeval = pd.to_datetime(row.plannedtime, format='%Y%m%d%H%M%S%f')
    return timeval
    


# In[263]:


def set_hour(row):
    return row['event_time'].hour


# In[264]:


names = ['trustid','tiploc','event_time','event_type','lateness','direction','platform','plannedtime','messagetime']

first_file = pd.read_csv("C:\\Users\\WAKANDA\\Downloads\\Interview\\Interview\\trust_move_20180604.csv", header=3, skipfooter=5,names=names, engine='python')

first_file['event_time'] =  pd.to_datetime(first_file['event_time'], format='%Y%m%d%H%M%S%f')
first_file.plannedtime = first_file.apply(set_date, axis=1)
first_file['hour'] = first_file.apply(set_hour, axis=1)
print(first_file.shape)
print(first_file.tail())
first_file['plannedtime'] =  pd.to_datetime(first_file['plannedtime'], format='%Y%m%d%H%M%S%f')
print(first_file.head())


# In[265]:


most_delayed_services = first_file.groupby(['trustid'], as_index=False)['lateness'].agg(np.sum).sort_values('lateness')[0:500]
print(most_delayed_services)

#print(most_delayed_services.columns)
trust_ids = most_delayed_services['trustid']
#print(trust_ids)
only_latest_entries = first_file[first_file['trustid'].isin(trust_ids)]
latest_tiplocs = only_latest_entries.groupby(['tiploc'], as_index=False)
#print(latest_tiplocs.groups)

latest_tiplocs_by_direction = only_latest_entries.groupby(['tiploc','direction'], as_index=False).size().sort_values(ascending=False)
latest_tiplocs_by_direction.unstack().plot()
size = latest_tiplocs.size().sort_values(ascending=False)
print(size)
size.plot(x='tiploc')
lateness_std_dev=first_file.lateness.agg(np.std)
lateness_max=first_file.lateness.agg(np.max)
lateness_min=first_file.lateness.agg(np.min)
print(lateness_std_dev)
print(lateness_max)
print(lateness_min)


# In[266]:


# Get the relative frequency of these tiplocs and join them on the CSV data, export to some files we can create a heatmap with
sum_top_delays  = sum(size)
print(sum_top_delays)


print(size)

relative_freqs = size / sum_top_delays

print(relative_freqs)


# In[267]:


stations = pd.read_csv("C:\\Users\\WAKANDA\\Downloads\\Interview\\Interview\\locations.csv")

stations_cleaned = stations.dropna()
frame = pd.DataFrame(relative_freqs)
joined = frame.join(stations_cleaned.set_index('tiploc'))
print(joined.columns.values)
to_export = joined[[0,'longitude','latitude']].dropna()

print(joined)
print(to_export)

to_export.to_csv('first_day_map.csv',header=False)


# In[268]:


# Group lateness by tiploc then plot by frequency

tiploc_groups = first_file.groupby(['hour','tiploc'])
print(tiploc_groups['lateness'].agg(np.sum))
most_delayed_tiplocs = first_file.groupby(['tiploc'], as_index=False)['lateness'].agg(np.sum).sort_values('lateness')



# take each of the 25 most delayed tiplocs and plot their delays as the day goes

bp = most_delayed_tiplocs.plot(x='tiploc', y='lateness')




