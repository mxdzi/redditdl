#!/usr/bin/env python3.11
import argparse
from datetime import datetime, date, timedelta
from pathlib import Path

import requests

version = 1.4

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0'


class Redditdl:
    def __init__(self, subreddit, verbose=False):
        self.subreddit = subreddit
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        self.posts_to_download = []

    def download(self):
        print(f"Downloading from subreddit: {self.subreddit}")
        self._get_posts()
        if self.posts_to_download:
            print(f"Images to download: {len(self.posts_to_download)}")
            self._download_images()

    def _get_posts(self):
        after = None
        url = f"https://www.reddit.com/r/{self.subreddit}/new.json"
        while True:
            payload = {'after': after, 'limit': 100}
            result = self.session.get(url, params=payload).json()
            after = result['data']['after']
            if self.verbose:
                print(f"Found: {len(result['data']['children'])} posts")
            for post in result['data']['children']:
                post_date = date.fromtimestamp(post['data']['created'])
                date_past = date.today() + timedelta(days=-2)
                if date_past < post_date < date.today():
                    if post['data'].get('post_hint') == 'image':
                        self.posts_to_download.append(post)
                    else:
                        if self.verbose:
                            print(f"Non image: {datetime.fromtimestamp(post['data']['created'])} {post['data']['url']}")
                elif post_date < date_past:
                    return
            if after is None:
                return

    def _download_images(self):
        download_path = Path.cwd().joinpath('download', self.subreddit)
        download_path.mkdir(parents=True, exist_ok=True)
        for post in self.posts_to_download:
            if self.verbose:
                print(f"Downloading image: {datetime.fromtimestamp(post['data']['created'])} {post['data']['url']}")
            result = self.session.get(post['data']['url'])
            if result.status_code == 200:
                self._save_image(post, download_path, result)

    @staticmethod
    def _save_image(post, download_path, result):
        permalink = post['data']['permalink'].split('/')
        filename = permalink[-2] + "#" + permalink[-3]
        fileext = "." + post['data']['url'].split('.')[-1].replace('?', '')
        author = post['data']['author']
        with open(download_path.joinpath(f"{filename}@{author}{fileext}"), 'wb') as file:
            file.write(result.content)


def main(args):  # pragma: no cover
    for subreddit in args.subreddits:
        redditdl = Redditdl(subreddit, args.verbose)
        redditdl.download()


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(prog="Reddit Downloader")
    parser.add_argument('subreddits', metavar='subreddit', nargs='+', help='Names of subreddits to download')
    parser.add_argument('--verbose', '-v', action="store_true", help="Show more info when downloading")
    parser.add_argument('--version', '-V', action='version', version=f"%(prog)s {version}")
    args = parser.parse_args()
    main(args)
