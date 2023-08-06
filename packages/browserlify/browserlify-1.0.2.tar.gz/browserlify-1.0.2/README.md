# Browserlify Python SDK

![GitHub](https://img.shields.io/github/license/browserlify/python-sdk)

The [Browserlify API](https://browserlify.com/docs/apis/token.html) Python Library

## Usage

### Requirements
You should be signed up as a developer on the [browserlify.com](https://browserlify.com) so that you can create and manage your API token, It's free Sign up.

### Installation
To easily install or upgrade to the latest release, use [pip](http://www.pip-installer.org/).

```shell
pip install --upgrade browserlify
```

### Table of Contents
- [Getting Started](#getting-started)
- [PDF generation](#pdf-generation)
- [Screenshot](#Screenshot)
- [Web Scraping](#web-scraping)
- [cli](#cli)

### Getting Started
1. First create a new api key in the [Dashboard](https://browserlify.com/app/), and retrieve your API Token.
1. We then need to supply these keys to the browserlify `Option` class so that it knows how to authenticate.
```python
from browserlify import pdf, Option

opt = Option(YOUR_TOKEN)
```
### PDF generation
```python
from browserlify import pdf, Option

opt = Option(YOUR_TOKEN)
opt.paper = 'A4'
opt.full_page = True
opt.wait_load = 5000 # Wait document loaded <= 5,000 ms

try:
    content = pdf('https://example.org', opt)
    open('example.org.pdf','wb+').write(content)
except Exception as bre:
    print('pdf fail', bre)
```
### Screenshot
```python
from browserlify import screenshot, Option

opt = Option(YOUR_TOKEN)
opt.full_page = True
opt.wait_load = 5000 # Wait document loaded <= 5,000 ms

try:
    content = screenshot('https://example.org', opt)
    open('example.org.png','wb+').write(content)
except Exception as bre:
    print('screenshot fail', bre)
```

### Web Scraping
```python
from browserlify import scrape, Option,Flow

opt = Option(YOUR_TOKEN)
opt.flows = [
    Flow(action="waitload", timeout=5000), # Wait document loaded <= 5,000 ms
    Flow(name="title", action="text", selector="h1")
]

try:
    content = scrape('https://example.org', opt)
    print(content)
    # output:
    # {"page":1,"data":{"title":"Example Domain"}}
except Exception as bre:
    print('scrape fail', bre)
```
### cli
`scripts/browserlify`: 
 - `pdf` pdf generation
 - `screenshot` take screenshot
 - `content` get website content
 - `scrape` get website content

```shell
browserlify cli tool

positional arguments:
  {pdf,screenshot,content,scrape}
                        commands help
    pdf                 pdf generation help
    screenshot          take screenshot help
    content             get content help
    scrape              web scrape help

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
```
#### convert url to pdf
```shell
browserlify pdf -t YOUR_TOKEN -o browserlify.com.pdf -w 5000 --fullpage https://browserlify.com
```

#### take screenshot
```shell
browserlify screenshot -t YOUR_TOKEN -o browserlify.com.png -w 5000  --fullpage  https://browserlify.com
```
#### get page content
```shell
browserlify content -t YOUR_TOKEN -o browserlify.com.json -w 5000 https://browserlify.com
```
#### scrape page
```shell
browserlify scrape -t YOUR_TOKEN -o example.com.json -w 5000 -f flows.json https://example.com
```