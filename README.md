## Requirement
* Python 3.7
* nodejs10
* MySQL5.7
* npm
* Docker Compose

## Getting started
### clone
```
$ git clone https://github.com/nxquang1994/django-brief.git
$ git checkout develop
```
### Setup Environment
```
※Specify mysql port, web port and host argument
$ ./tools/setup.sh 3306 8080 passonate.dev.com
```

### Setup and run docker container
```
$ make start
```

### Setup custom domain
```
※Add custom domain into /ect/hosts
ex) 127.0.0.1 passonate.dev.com
```

### Run unit test
```
$ make test
```

### Api analysis rss feed
```
$ http://localhost:8080/api/feeds/analysisRssFeedItem
ex) Body parameter
{
    "urls": "http://rss.cnn.com/rss/edition_entertainment.rss,http://www.reddit.com/r/python/.rss"
}
```
### Web Page
```
$ http://localhost:8080/web/
```
