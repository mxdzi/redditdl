# redditdl

A simple Python script for downloading the images from reddit.com.

## How to use

Images are saved in folder named after subreddit inside `downloads` folder.
By default a subreddit is sorted by new and images from yesterday are downloaded.

To download all images from subreddit pass subreddit name as first argument:

    redditdl.py xxx

To download all images from several subreddits pass comma separated list of subreddits as first argument:

    redditdl.py xxx,yyy,zzz
