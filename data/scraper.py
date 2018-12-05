from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
from unidecode import unidecode

quote_page = 'http://metrolyrics.com/{}-lyrics-eminem.html'
filename = 'eminem-songs.csv'
songs = pd.read_csv(filename)

for index, row in songs.iterrows():
    page = urlopen(quote_page.format(row['song']))
    soup = BeautifulSoup(page, 'html.parser')
    verses = soup.find_all('p', attrs={'class': 'verse'})

    lyrics = ''

    for verse in verses:
        text = verse.text.strip()
        text = re.sub(r"\[.*\]\n", "", unidecode(text))
        if lyrics == '':
            lyrics = lyrics + text.replace('\n', '|-|')
        else:
            lyrics = lyrics + '|-|' + text.replace('\n', '|-|')

    songs.at[index, 'lyrics'] = lyrics

    print('saving {}'.format(row['song']))
    songs.head()

print('writing to .csv')
songs.to_csv(filename, sep=',', encoding='utf-8')