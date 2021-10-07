import requests
import pandas as pd

from env import CLIENT_ID, SECRET_KEY, USER, PASSWORD

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
data = {
    'grant_type': 'password',
    'username': USER,
    'password': PASSWORD
}

headers = {'User-Agent': 'reddit_instagram_app/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'

res = requests.get('https://oauth.reddit.com/r/Sneakers/hot',
                headers=headers)

df = pd.DataFrame()

for post in res.json()['data']['children']:
    df = df.append({
        'Title': post['data']['title'].encode('utf8'),
        'Ups': post['data']['ups'],
        'Selftext': post['data']['selftext'],
        'Url' : post['data']['url']
    }, ignore_index=True)
    
df = df.sort_values(by=['Ups'], ascending=False)
df.to_excel('output.xlsx',index=False)