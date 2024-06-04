import pandas as pd
import re
import matplotlib.pyplot as plt

# President mandates
president = {
    'Jacques Chirac': [1995, 2007],
    'Nicolas Sarkozy': [2007, 2012],
    'François Hollande': [2012, 2017],
    'Emmanuel Macron': [2017, 2022],}

# Add president mandates to graphs
def add_pres(president):
    # Add vertical lines for each presidential term
    for president, years in president.items():
        plt.axvline(x=years[0], color='k', linestyle='--', linewidth=1)
        plt.text(
            years[0] + 0.5, 
            plt.ylim()[1] - 5, 
            president, 
            rotation=90, 
            verticalalignment='top')

# Read the Excel file into a DataFrame
df = pd.read_excel("data/T_3301.xlsx", sheet_name="Data")
GDP = pd.read_excel("data/FRA_GDP.xlsx")

# Remove all starting whitespace
df.rename(columns=lambda x: x.strip(), inplace=True)

###FOCUS ON WHOLE EXPENSES

# Dataframe with all "global" budget
global_df = [col for col in df.columns if re.match(r'^\d{2} ', col)]
global_df = pd.concat([df.iloc[:,0],df[global_df]], axis=1)

# Add GDP
global_df = global_df.merge(GDP, on='Annuel')

# Do expenses as a proportion of the GDP
global_df.iloc[:,1:11,] = global_df.iloc[:,1:11,].div(global_df.PIB, axis=0)*100

df_column = global_df[global_df.columns.drop(['Annuel', 'PIB'])].columns

# Plot 
fig, ax = plt.subplots()
ax.stackplot(df['Annuel'], global_df[global_df.columns.drop(['Annuel', 'PIB'])].transpose(), labels=df_column)

# Add vertical lines for each presidential term
add_pres(president)

plt.xlabel('Years')
plt.ylabel("in % of GDP")
plt.title('Evolution of the National Expense in France')
plt.legend(loc='lower left')
plt.show()

###FOCUS ON SOCIAL SECURITY EXPENSES

# Dataframe with all "global" budget
Secu_df = [col for col in df.columns if re.match(r'^10.\d{1}', col)]
Secu_df = pd.concat([df.iloc[:,0],df[Secu_df]], axis=1)

# Add GDP
Secu_df = Secu_df.merge(GDP, on='Annuel')

# Do expenses as a proportion of the GDP
Secu_df.iloc[:,1:10,] = Secu_df.iloc[:,1:10,].div(Secu_df.PIB, axis=0)*100

df_column = Secu_df[Secu_df.columns.drop(['Annuel', 'PIB'])].columns

# Plot 
fig, ax = plt.subplots()
ax.stackplot(df['Annuel'], Secu_df[Secu_df.columns.drop(['Annuel', 'PIB'])].transpose(), labels=df_column)

add_pres(president)
plt.xlabel('Years')
plt.ylabel("in % of GDP")
plt.title('Evolution of the Social Security Expense in France')
plt.legend(loc='lower left')
plt.grid(True, axis='y')
plt.show()

# Since François Hollande
president_FH = {
    'François Hollande': [2012, 2017],
    'Emmanuel Macron': [2017, 2022],}
fig, ax = plt.subplots()
ax.plot(df['Annuel'][17:28], Secu_df[Secu_df.columns.drop(['Annuel', 'PIB'])][17:28], label=df_column)

add_pres(president_FH)
plt.xlabel('Years')
plt.ylabel("in % of GDP")
plt.title('Evolution of the Social Security Expense in France')
plt.legend(loc='lower left')
plt.grid(True, axis='y')
plt.show()

###FOCUS ON SECTORS https://juste-repartition.fr/wp-content/uploads/2022/11/Estimation-depenses-publiques-France-2022.xlsx

#create a new dataframe
df_sector = df.copy()
df_sector = df_sector.merge(GDP, on='Annuel')

df_sector.columns = [col[:4] for col in df_sector.columns]

df_sector["Retraites"] = df_sector["10.2"] + df_sector["10.3"]
df_sector["Assurance-maladie-santé"] = df_sector["10.1"] + df_sector["07.1"] + df_sector["07.2"] + df_sector["07.3"] + df_sector["07.4"] + df_sector["07.5"] + df_sector["07.6"]
df_sector["Famille"] = df_sector["10.4"]
df_sector["Chomage"] = df_sector["10.5"]
df_sector["Autres solidarités"] = df_sector["10.6"] + df_sector["10.7"] + df_sector["10.8"] + df_sector["10.9"]
df_sector["Education"] = df_sector["09.1"] + df_sector["09.2"] + df_sector["09.3"] + df_sector["09.4"] + df_sector["09.5"] + df_sector["09.6"] + df_sector["09.7"] + df_sector["09.8"] + df_sector["01.4"]
df_sector["Soutien à l'économie"] = df_sector["01.2"] + df_sector["04.1"] + df_sector["04.2"] + df_sector["04.4"] + df_sector["04.6"] + df_sector["04.7"] + df_sector["04.8"] + df_sector["04.9"]
df_sector["Transports et urbanisme"] = df_sector["04.5"] + df_sector["06.1"] + df_sector["06.2"] + df_sector["06.3"] + df_sector["06.4"] + df_sector["06.5"] + df_sector["06.6"]
df_sector["Services Généraux"] = df_sector["01.1"] + df_sector["01.3"] + df_sector["01.5"] + df_sector["01.6"] + df_sector["01.8"]
df_sector["Environnement et Energie"] = df_sector["04.3"] + df_sector["05.1"] + df_sector["05.2"] + df_sector["05.3"] + df_sector["05.4"] + df_sector["05.5"] + df_sector["05.6"]
df_sector["Culture et sport"] = df_sector["08.1"] + df_sector["08.2"] + df_sector["08.3"] + df_sector["08.4"] + df_sector["08.5"] + df_sector["08.6"]
df_sector["Défense, Sécurité et Justice"] = df_sector["02.1"] + df_sector["02.2"] + df_sector["02.3"] + df_sector["02.4"] + df_sector["02.5"] + df_sector["03.1"] + df_sector["03.6"] + df_sector["03.2"] + df_sector["03.3"] + df_sector["03.4"] + df_sector["03.5"]
df_sector["Charges de la dette"] = df_sector["01.7"]

df_column = [col for col in df_sector.columns if re.match(r'^[A-Z]', col)]
df_sector = df_sector[df_column]

df_sector.iloc[:,2:15,] = df_sector.iloc[:,2:15,].div(df_sector.PIB, axis=0)*100

# Plot 
fig, ax = plt.subplots()
ax.plot(df['Annuel'], df_sector[df_sector.columns.drop(['Annu', 'PIB'])], label=df_column[2:])

add_pres(president)
plt.xlabel('Years')
plt.ylabel("in % of GDP")
plt.title('Evolution of the Expense per Sector in France')
plt.legend(loc='lower left')
plt.grid(True, axis='y')
plt.show()

# Since François Hollande
fig, ax = plt.subplots()
ax.plot(df_sector['Annu'][17:28], df_sector[df_sector.columns.drop(['Annu', 'PIB'])][17:28], label=df_column[2:])

add_pres(president_FH)
plt.xlabel('Years')
plt.ylabel("in % of GDP")
plt.title('Evolution of the Expense per Sector in France')
plt.legend(loc='lower left')
plt.grid(True, axis='y')
plt.show()