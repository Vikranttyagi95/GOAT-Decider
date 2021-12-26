import requests
import pandas as pd
from bs4 import BeautifulSoup

players = ['federer','nadal','djokovic']

for player in players:

    url = f"https://tennisexplorer.com/player/{player}/"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    player_info = []

    #  Finding the info of the player

    for tag in soup.find_all(class_='date'):
        val = tag.string
        if ":" in val:
            key = val.split(':')[0]
            value = val.split(':')[1].lstrip()
            player_info.append({key:value})

    #  Finding the table for player stats

    table = soup.find('table', class_ = "result balance")

    stats = []
    for tag in table.tbody.find_all('td'):
        if tag.string is not None:
            stats.append(tag.string)

    final_stats = []
    for i in range(7):
        lst = []
        for value in stats[i::7]:
            lst.append(value)

        final_stats.append(lst)



    #  Creating a dataframe
    pdf = pd.DataFrame(player_info)

    df = pd.DataFrame(final_stats)
    df = df.T
    df.columns = ["Year","Summary","Clay","Hard","Indoor","Grass","Not Set"]
    df = df.astype(str)
    pdf.to_csv(f"{player}_info.csv", index=False)
    df.to_csv(f"{player}_stats.csv", index=False)
