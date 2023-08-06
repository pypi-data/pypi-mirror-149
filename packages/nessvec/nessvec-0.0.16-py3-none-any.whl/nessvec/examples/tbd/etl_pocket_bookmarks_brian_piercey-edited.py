import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction import DictVectorizer
url = 'https://bjpcjp.github.io/pocket-links.html'

# no lists or tables for the bookmarks:
# dfs = pd.read_html(url)
# dfs[0]


resp = requests.get(url)
content = resp.text
soup = BeautifulSoup(content, "lxml")
divs = soup.find_all("div", {"class": "x-grid"})
div = soup.find("div", {"class": "x-grid"})


# no lists or tables for the bookmarks:
# >>> div = soup.find("div", {"class": "cell"})
# >>> datas = div.find_all("li")
# ...  # Iterate through all li tags
# ... for data in datas:
# ...     # Get text from each tag
# ... print(data.text)
# ... print(f"Total {len(datas)} li tag found")

divs = soup.find_all('div', {'class': 'cell'})
div = divs[1]
hrefs = div.find_all('a', href=True)
strongs = div.find_all('strong')

df = pd.DataFrame([[t.text.split(','), h['href']] for (t, h) in zip(strongs, hrefs)], columns='tags url'.split())
df['tags'] = [[t.strip().lower() for t in tags] for tags in df['tags']]
dicts = [dict(zip(tags, [1] * len(tags))) for tags in df['tags']]
dftags = pd.DataFrame(dicts)

dftags.T.sum().mean()
# 1.7 tags per bookmark

# dv = DictVectorizer()
# df['tags'] = [[t.strip().lower() for t in tags] for tags in df['tags']]
# dicts = [dict(zip(tags, [1] * len(tags))) for tags in df['tags']]
# dv.fit(dicts)
# # len(dv.get_feature_names())
# dftags = pd.DataFrame(dv.transform(dicts).todense(), columns=dv.get_feature_names())
# dftags
df = pd.concat([df, dftags])
df.to_csv('data/pocket_bookmark_tags_by_brian_piercy.csv')
