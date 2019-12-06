import argparse
from datetime import datetime, date, timedelta
from pathlib import Path

import requests

version = 1.1


def download(subreddit):
    session = requests.Session()
    session.headers.update({'User-Agent': 'reddit-dl'})
    after = None
    posts_to_download = []

    while True:
        payload = {'after': after, 'limit': 100}
        result = session.get('http://www.reddit.com/r/' + subreddit + '/new.json', params=payload).json()
        after = result['data']['after']
        print(subreddit, len(result['data']['children']))
        for post in result['data']['children']:
            if date.today() + timedelta(days=-2) < date.fromtimestamp(post['data']['created']) < date.today():
                if 'post_hint' in post['data'] and post['data']['post_hint'] == 'image':
                    posts_to_download.append(post)
                else:
                    print(subreddit, post['data']['url'], datetime.fromtimestamp(post['data']['created']))
            elif date.fromtimestamp(post['data']['created']) < date.today() + timedelta(days=-2):
                break
        else:
            if after is None:
                break
        break

    download_path = Path.cwd().joinpath('download', subreddit)
    if posts_to_download:
        download_path.mkdir(parents=True, exist_ok=True)

    for post in posts_to_download:
        result = session.get(post['data']['url'])
        if result.status_code == 200:
            save_image(post, download_path, result)


def save_image(post, download_path, result):
    permalink = post['data']['permalink'].split('/')
    filename = permalink[-2] + "#" + permalink[-3]
    fileext = "." + post['data']['url'].split('.')[-1].replace('?', '')
    with open(download_path.joinpath(filename + fileext), 'wb') as file:
        file.write(result.content)


def main(args):
    for subreddit in args.subreddits:
        print(subreddit)
        download(subreddit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Reddit Downloader")
    parser.add_argument('subreddits', metavar='subreddit', nargs='+', help='Names of subreddits to download')
    parser.add_argument('--version', '-V', action='version', version=f"%(prog)s {version}")
    args = parser.parse_args()
    main(args)
