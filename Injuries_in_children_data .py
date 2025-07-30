#!/usr/bin/env python
# coding: utf-8

# ### Importing necessary libraries

# In[39]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ### Loading and Analyzing the raw data

# In[40]:


# Load the CSVs
df_0_14 = pd.read_csv('Compare_areas.csv')
df_15_24 = pd.read_csv('Compare_areas (15-24).csv')


# In[41]:


df_0_14


# In[42]:


df_15_24


# ### Darlington combined injury admission rate (0–24)

# In[44]:


# Combine counts and denominators to compute combined rate
combined_count = darlington_0_14['Count'].str.replace(',', '').astype(int).values[0] + \
                 darlington_15_24['Count'].str.replace(',', '').astype(int).values[0]

combined_denominator = darlington_0_14['Denominator'].astype(int).values[0] + \
                       darlington_15_24['Denominator'].astype(int).values[0]

combined_rate = (combined_count / combined_denominator) * 10000

print(f"Darlington combined injury admission rate (0–24): {combined_rate:.2f} per 10,000")


# ### Filterinig and Extracting the relevent data

# In[45]:


# Read CSVs
df_0_14 = pd.read_csv('Compare_areas.csv')
df_15_24 = pd.read_csv('Compare_areas (15-24).csv')

# Filter for 2023/24
df_0_14 = df_0_14[df_0_14['Time period'] == '2023/24']
df_15_24 = df_15_24[df_15_24['Time period'] == '2023/24']

# Extract relevant rows
dar_0_14 = df_0_14[df_0_14['AreaName'] == 'Darlington']
eng_0_14 = df_0_14[df_0_14['AreaName'] == 'England']

dar_15_24 = df_15_24[df_15_24['AreaName'] == 'Darlington']
eng_15_24 = df_15_24[df_15_24['AreaName'] == 'England']


# ### Injury Admissions in Darlington by Age Group

# In[46]:


# Get counts and convert
count_0_14 = int(dar_0_14['Count'].str.replace(',', '').values[0])
count_15_24 = int(dar_15_24['Count'].str.replace(',', '').values[0])

# Pie chart
labels = ['0–14 years', '15–24 years']
sizes = [count_0_14, count_15_24]
colors = ['#66b3ff', '#ff9999']

plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Injury Admissions in Darlington by Age Group (2023/24)', fontsize=13)
plt.axis('equal')
plt.tight_layout()
plt.show()


# ### Darlington Admissions: Count Vs Rate by Age Group

# In[51]:


fig, ax1 = plt.subplots(figsize=(8,6))

ax1.bar(['0–14', '15–24'], [count_0_14, count_15_24], color='#69b3a2', label='Count')
ax1.set_ylabel('Number of Admissions', color='#69b3a2')

ax2 = ax1.twinx()
ax2.plot(['0–14', '15–24'], [darlington_0_14['Value'].values[0], darlington_15_24['Value'].values[0]],
         color='blue', marker='o', label='Rate')
ax2.set_ylabel('Admissions per 10,000', color='blue')

plt.title('Darlington Admissions: Count vs Rate by Age Group')
plt.tight_layout()
plt.show()


# ### Ranking of NE Areas by Injury Admission Rates (0–14 yrs)

# In[29]:


# Rankings for 0–14
peer_0_14 = df_0_14[df_0_14['AreaName'].isin(peer_areas)]
peer_0_14_sorted = peer_0_14.sort_values('Value', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=peer_0_14_sorted, x='Value', y='AreaName', palette='coolwarm')
plt.title('Ranking of NE Areas by Injury Admission Rates (0–14 yrs)')
plt.xlabel('Admissions per 10,000')
plt.tight_layout()
plt.show()



# ### Ranking of NE Areas by Injury Admission Rates (15–24 yrs)

# In[30]:


# Rankings for 15–24
peer_15_24 = df_15_24[df_15_24['AreaName'].isin(peer_areas)]
peer_15_24_sorted = peer_15_24.sort_values('Value', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=peer_15_24_sorted, x='Value', y='AreaName', palette='coolwarm')
plt.title('Ranking of NE Areas by Injury Admission Rates (15–24 yrs)')
plt.xlabel('Admissions per 10,000')
plt.tight_layout()
plt.show()


# ### Darlington vs Peers: Rate vs Count (0–24 yrs)

# In[33]:


# --- Step 2: Prepare 0–14 ---
peer_0_14 = df_0_14[df_0_14['AreaName'].isin(peer_areas)].copy()
peer_0_14['Count'] = peer_0_14['Count'].astype(str).str.replace(',', '').astype(float)

# --- Step 3: Prepare 15–24 ---
peer_15_24 = df_15_24[df_15_24['AreaName'].isin(peer_areas)].copy()
peer_15_24['Count'] = peer_15_24['Count'].astype(str).str.replace(',', '').astype(float)

# --- Step 4: Aggregate to 0–24 ---
peer_combined = peer_0_14[['AreaName', 'Count', 'Value']].copy()
peer_combined = peer_combined.rename(columns={'Count': 'Count_0_14', 'Value': 'Rate_0_14'})
peer_combined['Count_15_24'] = peer_15_24.set_index('AreaName').loc[peer_combined['AreaName'], 'Count'].values
peer_combined['Rate_15_24'] = peer_15_24.set_index('AreaName').loc[peer_combined['AreaName'], 'Value'].values

# --- Step 5: Total for 0–24 ---
peer_combined['Total_Count_0_24'] = peer_combined['Count_0_14'] + peer_combined['Count_15_24']
peer_combined['Total_Rate_0_24'] = peer_combined[['Rate_0_14', 'Rate_15_24']].mean(axis=1)  # or use weighted avg if denominator is available

# --- Step 6: Plot ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Sort by Rate for consistency
peer_combined_sorted = peer_combined.sort_values('Total_Rate_0_24', ascending=False)

# Plot Rate
sns.barplot(data=peer_combined_sorted, x='Total_Rate_0_24', y='AreaName', ax=axes[0], palette='PuBu')
axes[0].set_title('Admission Rate (0–24 yrs)')
axes[0].set_xlabel('Rate per 10,000')

# Plot Count
sns.barplot(data=peer_combined_sorted, x='Total_Count_0_24', y='AreaName', ax=axes[1], palette='YlOrBr')
axes[1].set_title('Total Admissions Count (0–24 yrs)')
axes[1].set_xlabel('Admission Count')

# Overall Title
plt.suptitle('Darlington vs Peers: Rate vs Count (0–24 yrs)', fontsize=15)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()


# ### Darlington Injury Admissions Counts and Rates by Age Group (2023/24)

# In[34]:


import matplotlib.pyplot as plt

age_groups = ['0–14', '15–24', '0–24 Combined']
counts = [count_0_14, count_15_24, combined_count]
rates = [dar_0_14['Value'].values[0], dar_15_24['Value'].values[0], combined_rate]

fig, ax1 = plt.subplots(figsize=(8, 5))

# Bar plot for counts
ax1.bar(age_groups, counts, color='skyblue', alpha=0.7, label='Admission Counts')
ax1.set_ylabel('Admission Counts', color='skyblue')
ax1.tick_params(axis='y', labelcolor='skyblue')

# Line plot for rates on second y-axis
ax2 = ax1.twinx()
ax2.plot(age_groups, rates, color='darkorange', marker='o', linewidth=2, label='Admission Rate per 10,000')
ax2.set_ylabel('Admission Rate per 10,000', color='darkorange')
ax2.tick_params(axis='y', labelcolor='darkorange')

plt.title('Darlington Injury Admissions Counts and Rates by Age Group (2023/24)')
fig.tight_layout()
plt.show()



# In[ ]:




