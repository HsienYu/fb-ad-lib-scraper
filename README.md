# fb-ad-lib-scraper

## scrape images from FB ad library

### install and setup

# MacOS

brew cask install geckodriver

example: `python scrapead.py -i 3 -k puma -l TW`

args:

```
usage: scrapead.py [-h] -k KEYWORD -l LOCATION -i MAX_ITERATIONS

optional arguments:
  -h, --help            show this help message and exit
  -k KEYWORD, --keyword KEYWORD
                        keyword for fb ads searches
  -l LOCATION, --location LOCATION
                        country or location ex. TW
  -i MAX_ITERATIONS, --max_iterations MAX_ITERATIONS
                        max_iterations counting times
```

# Linux
