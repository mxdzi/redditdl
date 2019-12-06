import argparse
from datetime import datetime, date, timedelta
from pathlib import Path

import requests

version = 1.1


class Redditdl:
    def __init__(self, subreddit):
        self.subreddit = subreddit
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'reddit-dl'})
        self.posts_to_download = []

    def download(self):
        self._get_posts()
        self._download_images()

    def _get_posts(self):
        after = None
        while True:
            payload = {'after': after, 'limit': 100}
            result = self.session.get('http://www.reddit.com/r/' + self.subreddit + '/new.json', params=payload).json()
            after = result['data']['after']
            print(self.subreddit, len(result['data']['children']))
            for post in result['data']['children']:
                if date.today() + timedelta(days=-2) < date.fromtimestamp(post['data']['created']) < date.today():
                    if 'post_hint' in post['data'] and post['data']['post_hint'] == 'image':
                        self.posts_to_download.append(post)
                    else:
                        print(self.subreddit, post['data']['url'], datetime.fromtimestamp(post['data']['created']))
                elif date.fromtimestamp(post['data']['created']) < date.today() + timedelta(days=-2):
                    break
            else:
                if after is None:
                    break
            break

    def _download_images(self):
        download_path = Path.cwd().joinpath('download', self.subreddit)
        if self.posts_to_download:
            download_path.mkdir(parents=True, exist_ok=True)

        for post in self.posts_to_download:
            result = self.session.get(post['data']['url'])
            if result.status_code == 200:
                self._save_image(post, download_path, result)

    def _save_image(self, post, download_path, result):
        permalink = post['data']['permalink'].split('/')
        filename = permalink[-2] + "#" + permalink[-3]
        fileext = "." + post['data']['url'].split('.')[-1].replace('?', '')
        with open(download_path.joinpath(filename + fileext), 'wb') as file:
            file.write(result.content)


def main(args):  # pragma: no cover
    for subreddit in args.subreddits:
        print(subreddit)
        redditdl = Redditdl(subreddit)
        redditdl.download()


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(prog="Reddit Downloader")
    parser.add_argument('subreddits', metavar='subreddit', nargs='+', help='Names of subreddits to download')
    parser.add_argument('--version', '-V', action='version', version=f"%(prog)s {version}")
    args = parser.parse_args()
    main(args)
