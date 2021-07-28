# fb-ad-lib-scraper

## scrape images from FB ad library with color pallte detected

### install and setup

# MacOS

install webdriver:

```
brew cask install geckodriver
```

example usage(make sure you create an images folder in the same directoty):

```
python scrapead.py -i 3 -k puma -l TW
```

args:

```

usage: scrapead.py [-h] -k KEYWORD -l LOCATION -i MAX_ITERATIONS



optional arguments:

-h, --help show this help message and exit

-k KEYWORD, --keyword KEYWORD

keyword for fb ads searches

-l LOCATION, --location LOCATION

country or location ex. TW

-i MAX_ITERATIONS, --max_iterations MAX_ITERATIONS

max_iterations counting times

```

output format example:

```

{'keyword': 'puma', 'url': 'https://scontent.ftpe8-2.fna.fbcdn.net/v/t39.35426-6/s600x600/208830383_198298485538155_1011019614495988451_n.jpg?_nc_cat=100&ccb=1-3&_nc_sid=cf96c8&_nc_ohc=3b7PdFVMgqkAX8mGQsb&_nc_ht=scontent.ftpe8-2.fna&oh=6b344dbe19ae536fcd44baebdf6358d9&oe=60F1ED3A', 'filePath': '/Users/chenghsienyu/Documents/GitRepos/fb-ad-lib-scraper/images/208830383_198298485538155_1011019614495988451_n.jpg', 'date': '2021/07/13', 'color': ['e3b06e', '301b10', '944021', 'f3e8d9', 'bc7d1f']}

```

# Linux
