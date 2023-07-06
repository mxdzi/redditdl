# redditdl

A simple Python script for downloading images from reddit.com.

## How to use

Images are saved in a folder named after the subreddit inside the `downloads` folder.
By default, a subreddit is sorted by new, and images from yesterday are downloaded.

To download all images from a subreddit, pass the subreddit name as the first argument.:

    redditdl.py xxx

To download all images from several subreddits pass them as positional arguments:

    redditdl.py xxx yyy zzz

To show progress use `-v` flag:

    redditdl.py xxx -v

## Tests

Run tests with:

    pytest --cov=redditdl --cov-report html
