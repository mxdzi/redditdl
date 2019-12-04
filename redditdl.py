import sys
from datetime import datetime, date, timedelta
from pathlib import Path

import requests


def download(subreddit):
    session = requests.Session()
    session.headers.update({'User-Agent': 'reddit-dl'})
    after = None
    download_path = Path.cwd().joinpath('download', subreddit)
    download_path.mkdir(parents=True, exist_ok=True)
    while True:
        payload = {'after': after, 'limit': 100}
        result = session.get('http://www.reddit.com/r/' + subreddit + '/new.json', params=payload).json()
        after = result['data']['after']
        print(subreddit, len(result['data']['children']))
        for post in result['data']['children']:
            if date.today() + timedelta(days=-2) < date.fromtimestamp(post['data']['created']) < date.today():
                if 'post_hint' in post['data']:
                    if post['data']['post_hint'] == 'image':
                        result = session.get(post['data']['url'])
                        if result.status_code == 200:
                            download_image(post, download_path, result)
                    else:
                        print(subreddit, post['data']['url'], datetime.fromtimestamp(post['data']['created']))
            elif date.fromtimestamp(post['data']['created_utc']) < date.today() + timedelta(days=-2):
                break
        else:
            if after is None:
                break
        break


def download_image(post, download_path, result):
    permalink = post['data']['permalink'].split('/')
    filename = permalink[-2] + "#" + permalink[-3]
    fileext = "." + post['data']['url'].split('.')[-1].replace('?', '')
    with open(download_path.joinpath(filename + fileext), 'wb') as file:
        file.write(result.content)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        reddits = sys.argv[1].split(',')
        for reddit in reddits:
            print(reddit)
            download(reddit)
