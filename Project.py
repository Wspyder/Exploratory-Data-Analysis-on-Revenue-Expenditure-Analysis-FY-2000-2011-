import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


excel_path = "C:/Users/pc/Downloads/Revenue_Expenditure_FY_2000-11for yashhh.csv"
df = pd.read_csv(excel_path)

numeric_cols = df.select_dtypes(include='number').columns
categorical_cols = df.select_dtypes(exclude='number').columns


df_filled = df.copy()
for col in numeric_cols:
    df_filled[col].fillna(df_filled[col].mean(), inplace=True)


for col in categorical_cols:
    if df_filled[col].isna().any():
        df_filled[col].fillna(df_filled[col].mode()[0], inplace=True)
df_filled.info()
df_filled.describe()
df_filled.head(10)
df_filled.columns = df_filled.columns.str.strip() 


fiscal_columns = [col for col in df_filled.columns if col.startswith("FY")]
df_filled_melted = df_filled.melt(
    id_vars=['Sector', 'Major Head', 'Cat', 'Cat2', 'Identity'],
    value_vars=fiscal_columns,
    var_name='Fiscal Year',
    value_name='Expenditure'
)

df_filled_melted['Fiscal Year'] = df_filled_melted['Fiscal Year'].apply(lambda x: 2000 + int(x[-2:]))

# Chart 1: Union Government Expenditure Over Time
plt.figure(figsize=(10, 6))
union_data = df_filled_melted[df_filled_melted['Identity'] == 'A Union Govt']
sns.lineplot(data=union_data, x='Fiscal Year', y='Expenditure', marker='o')
plt.title('Union Government Revenue Expenditure (2000–2011)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#Observation:
    #The Union's spending steadily increased, especially post-2004.
#Conclusion: 
    #Indicates expanding national programs and growing fiscal responsibilities.
    

# Chart 2: Top 5 States by Total Expenditure
state_data = df_filled_melted[df_filled_melted['Cat2'] == 'S']
top_states = state_data.groupby('Identity')['Expenditure'].sum().nlargest(5).index
top_states_data = state_data[state_data['Identity'].isin(top_states)]

plt.figure(figsize=(10, 6))
sns.barplot(data=top_states_data, x='Identity', y='Expenditure', estimator=sum, ci=None)
plt.title('Top 5 States by Total Revenue Expenditure (2000–2011)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#Observation:
    #Maharashtra, Uttar Pradesh, and Andhra Pradesh dominate.

#Conclusion:
    #High expenditure aligns with larger population and economic activity in these states.

# Chart 3: Area Chart - Top 3 States Expenditure Trend
top3_states = top_states[:3]
area_data = state_data[state_data['Identity'].isin(top3_states)]
area_pivot = area_data.pivot_table(index='Fiscal Year', columns='Identity', values='Expenditure', aggfunc='sum')

area_pivot.plot(kind='area', figsize=(12, 6), stacked=True)
plt.title('Revenue Expenditure Trend - Top 3 States')
plt.ylabel('Expenditure')
plt.xlabel('Fiscal Year')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#Observation: 
    #Maharashtra leads significantly; all top 3 states show growth trends.

#Conclusion: 
    #These states possibly have robust public service structures and developmental initiatives.

# Chart 4: Pie Chart - Union vs States vs UTs Share
category_data = df_filled_melted[df_filled_melted['Cat2'].isin(['U', 'S', 'UT'])]
category_share = category_data.groupby('Cat2')['Expenditure'].sum()
category_share.index = ['Union', 'States', 'UTs']

plt.figure(figsize=(8, 8))
plt.pie(category_share, labels=category_share.index, autopct='%1.1f%%', startangle=140)
plt.title('Expenditure Share: Union vs States vs UTs (2000–2011)')
plt.tight_layout()
plt.show()
#Observation:
    #States contribute the majority (over 60%) of total expenditure.

#Conclusion: 
    #Reflects India's federal structure — states are key in delivering services.


# Chart 5: Heatmap - State-wise Expenditure Across Years
heatmap_data = state_data.pivot_table(index='Identity', columns='Fiscal Year', values='Expenditure', aggfunc='sum')

plt.figure(figsize=(14, 10))
sns.heatmap(heatmap_data, cmap='YlGnBu', linewidths=0.5)
plt.title('State-wise Revenue Expenditure Heatmap (2000–2011)')
plt.tight_layout()
plt.show()
#Observation: 
    #Strong yearly consistency in spending among top states.

#Conclusion: 
    #Enables identification of high-spending states and fiscal priorities over time.

# Chart 6: Boxplot - Expenditure Distribution by Category
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_filled_melted[df_filled_melted['Cat2'].isin(['U', 'S', 'UT'])], x='Cat2', y='Expenditure')
plt.title('Distribution of Revenue Expenditure by Category')
plt.xlabel('Category (U: Union, S: State, UT: Union Territory)')
plt.ylabel('Expenditure')
plt.tight_layout()
plt.show()
#Observation: 
    #Union’s expenditure shows higher central tendency; UTs show less variation.

#Conclusion: 
    #UTs operate on smaller budgets; Union manages major schemes across the nation.
#In Conclusion we can say that:
    #This project explored India's public revenue expenditure trends from the 
    #fiscal year 2000 to 2011, covering Union Government, States, and Union Territories. 
    #Using six diverse visualizations, we uncovered insights into the distribution, trends,
    #and variability of spending across different governing bodies