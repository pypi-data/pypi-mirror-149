# RSS Reader

## Description

Command-line RSS reader utility implemented in Python

## Installation

### 1. Install from PyPI repository

Run ```pip install rss-reader-sardor-irgashev```

### 2. Clone from GitLab

1. Clone the repository
2. Install necessary requirements by running ```pip install -r requirements.txt```

## Interface

Utility provides the following interface:

```shell
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --date DATE    News publishing date
  --to-html HTML Convert news to HTML
  --to-pdf PDF   Convert news to PDF
  --colorize     Enables colorized output
```

## Usage Examples

```
> python3 rss_reader.py http://rss.cnn.com/rss/edition_world.rss --limit 1
```

```shell
    Feed Title: CNN.com - RSS Channel - World

    News Title: China's Weibo shows user locations to combat 'bad behavior'
    Date Published: Thu, 28 Apr 2022 15:55:04 GMT
    Description: Weibo, China's equivalent of Twitter, told users on Thursday it would start to publish their IP locations on their account pages and when they post comments, in a bid to combat "bad behavior" online.
    Link: https://www.cnn.com/2022/04/28/tech/weibo-user-location-bad-behavior/index.html
    Image: https://cdn.cnn.com/cnnnext/dam/assets/220428104403-weibo-app-china-file-restricted-super-169.jpg

    ====================================================================================
```

```
> python3 rss_reader.py http://rss.cnn.com/rss/edition_world.rss --limit 1 --json
```

```shell
    [
        {
            "Feed Title": "CNN.com - RSS Channel - World",
            "Feed Source": "http://rss.cnn.com/rss/edition_world.rss",
            "News Item": {
                "News Title": "China's Weibo shows user locations to combat 'bad behavior'",
                "Publication Date": "Thu, 28 Apr 2022 15:55:04 GMT",
                "Description": "Weibo, China's equivalent of Twitter, told users on Thursday it would start to publish their IP locations on their account pages and when they post comments, in a bid to combat \"bad behavior\" online.",
                "Link": "https://www.cnn.com/2022/04/28/tech/weibo-user-location-bad-behavior/index.html",
                "Image Link": "https://cdn.cnn.com/cnnnext/dam/assets/220428104403-weibo-app-china-file-restricted-super-169.jpg"
            }
        }
    ]
```

```
> python3 rss_reader.py http://rss.cnn.com/rss/edition_world.rss --date 20220428 --limit 1
```

```shell
    Feed Title: CNN.com - RSS Channel - World

    News Title: China's Weibo shows user locations to combat 'bad behavior'
    Date Published: Thu, 28 Apr 2022 15:55:04 GMT
    Description: Weibo, China's equivalent of Twitter, told users on Thursday it would start to publish their IP locations on their account pages and when they post comments, in a bid to combat "bad behavior" online.
    Link: https://www.cnn.com/2022/04/28/tech/weibo-user-location-bad-behavior/index.html
    Image: https://cdn.cnn.com/cnnnext/dam/assets/220428104403-weibo-app-china-file-restricted-super-169.jpg

    ====================================================================================
```

```
>  python3 rss_reader.py http://rss.cnn.com/rss/edition_world.rss --date 20220428 --limit 1 --json
```

```shell
    [
        {
            "Feed Title": "CNN.com - RSS Channel - World",
            "Feed Source": "http://rss.cnn.com/rss/edition_world.rss",
            "News Item": {
                "News Title": "China's Weibo shows user locations to combat 'bad behavior'",
                "Publication Date": "Thu, 28 Apr 2022 15:55:04 GMT",
                "Description": "Weibo, China's equivalent of Twitter, told users on Thursday it would start to publish their IP locations on their account pages and when they post comments, in a bid to combat \"bad behavior\" online.",
                "Link": "https://www.cnn.com/2022/04/28/tech/weibo-user-location-bad-behavior/index.html",
                "Image Link": "https://cdn.cnn.com/cnnnext/dam/assets/220428104403-weibo-app-china-file-restricted-super-169.jpg"
            }
        }
    ]
```

```
> python3 rss_reader.py --date 20220428 --limit 1
```

```shell
    Feed Title: CNN.com - RSS Channel - World

    News Title: China's Weibo shows user locations to combat 'bad behavior'
    Date Published: Thu, 28 Apr 2022 15:55:04 GMT
    Description: Weibo, China's equivalent of Twitter, told users on Thursday it would start to publish their IP locations on their account pages and when they post comments, in a bid to combat "bad behavior" online.
    Link: https://www.cnn.com/2022/04/28/tech/weibo-user-location-bad-behavior/index.html
    Image: https://cdn.cnn.com/cnnnext/dam/assets/220428104403-weibo-app-china-file-restricted-super-169.jpg

    ====================================================================================
```

```
> python3 rss_reader.py --date 20220428 --json --limit 1
```

```shell
    [
        {
            "Feed Title": "CNN.com - RSS Channel - World",
            "Feed Source": "http://rss.cnn.com/rss/edition_world.rss",
            "News Item": {
                "News Title": "China's Weibo shows user locations to combat 'bad behavior'",
                "Publication Date": "Thu, 28 Apr 2022 15:55:04 GMT",
                "Description": "Weibo, China's equivalent of Twitter, told users on Thursday it would start to publish their IP locations on their account pages and when they post comments, in a bid to combat \"bad behavior\" online.",
                "Link": "https://www.cnn.com/2022/04/28/tech/weibo-user-location-bad-behavior/index.html",
                "Image Link": "https://cdn.cnn.com/cnnnext/dam/assets/220428104403-weibo-app-china-file-restricted-super-169.jpg"
            }
        }
    ]
```

```
> python3 rss_reader.py http://rss.cnn.com/rss/edition_world.rss --to-pdf ./ --to-html ./
```

```shell
Creates both HTML and PDF files at the specified location
```

#### Alternatives with installation from PyPI

```
> rss_reader http://rss.cnn.com/rss/edition_world.rss --limit 1
```

```shell
    Feed Title: CNN.com - RSS Channel - World

    News Title: China's Weibo shows user locations to combat 'bad behavior'
    Date Published: Thu, 28 Apr 2022 15:55:04 GMT
    Description: Weibo, China's equivalent of Twitter, told users on Thursday it would start to publish their IP locations on their account pages and when they post comments, in a bid to combat "bad behavior" online.
    Link: https://www.cnn.com/2022/04/28/tech/weibo-user-location-bad-behavior/index.html
    Image: https://cdn.cnn.com/cnnnext/dam/assets/220428104403-weibo-app-china-file-restricted-super-169.jpg

    ====================================================================================
```

```
> rss_reader http://rss.cnn.com/rss/edition_world.rss --limit 1 --json
```

```shell
    [
        {
            "Feed Title": "CNN.com - RSS Channel - World",
            "Feed Source": "http://rss.cnn.com/rss/edition_world.rss",
            "News Item": {
                "News Title": "China's Weibo shows user locations to combat 'bad behavior'",
                "Publication Date": "Thu, 28 Apr 2022 15:55:04 GMT",
                "Description": "Weibo, China's equivalent of Twitter, told users on Thursday it would start to publish their IP locations on their account pages and when they post comments, in a bid to combat \"bad behavior\" online.",
                "Link": "https://www.cnn.com/2022/04/28/tech/weibo-user-location-bad-behavior/index.html",
                "Image Link": "https://cdn.cnn.com/cnnnext/dam/assets/220428104403-weibo-app-china-file-restricted-super-169.jpg"
            }
        }
    ]
```

```
> rss_reader http://rss.cnn.com/rss/edition_world.rss --date 20220428 --limit 1
```

```shell
    Feed Title: CNN.com - RSS Channel - World

    News Title: China's Weibo shows user locations to combat 'bad behavior'
    Date Published: Thu, 28 Apr 2022 15:55:04 GMT
    Description: Weibo, China's equivalent of Twitter, told users on Thursday it would start to publish their IP locations on their account pages and when they post comments, in a bid to combat "bad behavior" online.
    Link: https://www.cnn.com/2022/04/28/tech/weibo-user-location-bad-behavior/index.html
    Image: https://cdn.cnn.com/cnnnext/dam/assets/220428104403-weibo-app-china-file-restricted-super-169.jpg

    ====================================================================================
```

```
> rss_reader http://rss.cnn.com/rss/edition_world.rss --date 20220428 --limit 1 --json
```

```shell
    [
        {
            "Feed Title": "CNN.com - RSS Channel - World",
            "Feed Source": "http://rss.cnn.com/rss/edition_world.rss",
            "News Item": {
                "News Title": "China's Weibo shows user locations to combat 'bad behavior'",
                "Publication Date": "Thu, 28 Apr 2022 15:55:04 GMT",
                "Description": "Weibo, China's equivalent of Twitter, told users on Thursday it would start to publish their IP locations on their account pages and when they post comments, in a bid to combat \"bad behavior\" online.",
                "Link": "https://www.cnn.com/2022/04/28/tech/weibo-user-location-bad-behavior/index.html",
                "Image Link": "https://cdn.cnn.com/cnnnext/dam/assets/220428104403-weibo-app-china-file-restricted-super-169.jpg"
            }
        }
    ]
```

```
> rss_reader --date 20220428 --limit 1
```

```shell
    Feed Title: CNN.com - RSS Channel - World

    News Title: China's Weibo shows user locations to combat 'bad behavior'
    Date Published: Thu, 28 Apr 2022 15:55:04 GMT
    Description: Weibo, China's equivalent of Twitter, told users on Thursday it would start to publish their IP locations on their account pages and when they post comments, in a bid to combat "bad behavior" online.
    Link: https://www.cnn.com/2022/04/28/tech/weibo-user-location-bad-behavior/index.html
    Image: https://cdn.cnn.com/cnnnext/dam/assets/220428104403-weibo-app-china-file-restricted-super-169.jpg

    ====================================================================================
```

```
> rss_reader --date 20220428 --json --limit 1
```

```shell
    [
        {
            "Feed Title": "CNN.com - RSS Channel - World",
            "Feed Source": "http://rss.cnn.com/rss/edition_world.rss",
            "News Item": {
                "News Title": "China's Weibo shows user locations to combat 'bad behavior'",
                "Publication Date": "Thu, 28 Apr 2022 15:55:04 GMT",
                "Description": "Weibo, China's equivalent of Twitter, told users on Thursday it would start to publish their IP locations on their account pages and when they post comments, in a bid to combat \"bad behavior\" online.",
                "Link": "https://www.cnn.com/2022/04/28/tech/weibo-user-location-bad-behavior/index.html",
                "Image Link": "https://cdn.cnn.com/cnnnext/dam/assets/220428104403-weibo-app-china-file-restricted-super-169.jpg"
            }
        }
    ]
```

```
> rss_reader http://rss.cnn.com/rss/edition_world.rss --to-pdf ./ --to-html ./
```

```shell
Creates both HTML and PDF files at the specified location
```

## Feed Sources

1. https://moxie.foxnews.com/feedburner/latest.xml
2. https://www.scmp.com/rss/5/feed
3. http://rss.cnn.com/rss/edition_world.rss
4. https://globalnews.ca/feed/
5. https://www.washingtontimes.com/rss/headlines/news/world/