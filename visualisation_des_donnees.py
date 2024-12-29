import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ace_tools_open as tools

# Load the data
df = pd.read_csv("Calendrier_et_resultats_Premier_League_clean.csv", index_col=['Date'])
df.index = pd.to_datetime(df.index)

plt.figure(figsize=(15, 10))
sns.countplot(data=df, x='Domicile', order=df['Domicile'].value_counts().index)
df2 =df.copy()

clubs = list(set(df2["Domicile"]))

for club in clubs :
    df_to_plot = df2[df2["Domicile"] == club]
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_to_plot, x=df_to_plot.index, y="winner").set_title(f'Winner for {club} at Domicile')
    plt.show()

df2 =df.copy()

clubs = list(set(df2["Domicile"]))

for club in clubs :
    df_to_plot = df2[df2["Extérieur"] == club]
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_to_plot, x=df_to_plot.index, y="winner").set_title(f'Winner for {club} at Extérieur')
    plt.show()

#On compare ici le nombre de victoire à domicile et à l'extérieur pour chaque club (aussi match nul, et défaite)

df4 =df.copy()

clubs = list(set(df2["Domicile"]))

for club in clubs :
    df_dom = df2[df2["Domicile"] == club]
    df_ext = df2[df2["Extérieur"] == club]
    esp_dom = df_dom["winner"].value_counts(normalize=True)
    esp_ext = df_ext["winner"].value_counts(normalize=True)
    if 1 not in esp_dom.index:
        esp_dom[1] = 0
    if 1 not in esp_ext.index:
        esp_dom[1] = 0
    print(f'Pour le club {club}, il y a {esp_dom[1]*100:.2f}% de victoire à domicile, {esp_dom[-1]*100:.2f}% de défaite à domicile et {esp_dom[0]*100:.2f}% de match nul à domicile')
    print(f'Pour le club {club}, il y a {esp_ext[1]*100:.2f}% de victoire à l extérieur, {esp_ext[-1]*100:.2f}% de défaite à l extérieur et {esp_ext[0]*100:.2f}% de match nul à l exterieur ')

data = pd.read_csv('Calendrier_et_resultats_Premier_League_clean.csv')

# On convertit la colonne Date en datetime
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')

# On définit une saison qui commence en août et se termine en mai
data['Season'] = data['Date'].apply(lambda x: f"{x.year}-{x.year + 1}" if x.month >= 8 else f"{x.year - 1}-{x.year}")

home_wins = data[data['winner'] == 1]

# On groupe par Saison et club pour compter le nombre de victoires à domicile
home_wins_count = home_wins.groupby(['Season', 'Domicile']).size().reset_index(name='Home Wins')

tools.display_dataframe_to_user(name="Premier League Home Wins by Season and Club", dataframe=home_wins_count)

pivot_table = home_wins_count.pivot(index='Season', columns='Domicile', values='Home Wins')

# Plotting
pivot_table.plot(kind='bar', stacked=True, figsize=(15, 7))
plt.title("Home Wins by Club and Season in the Premier League")
plt.xlabel("Season")
plt.ylabel("Number of Home Wins")
plt.legend(title="Club", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()