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

※for production. specify production argument
e.g.
$ ./tools/setup.sh 3306 8080 passonate.dev.com production
```

### Setup and run docker container
```
$ make start
```

### Setup custom domain
```
※If you want to use custom domain, Add custom domain into /ect/hosts
ex) 127.0.0.1 passonate.dev.com
```

### Api analysis rss feed
```
$ http://localhost:8080/api/feeds/analysisRssFeedItem
ex) Body parameter
{
    "urls": "http://www.smartbrief.com/servlet/rss?b=ASCD,http://www.newyorker.com/feed/humor"
}

※Use custom domain
ex)
$ http://passonate.dev.com:8080/api/feeds/analysisRssFeedItem
```

### Web Page
```
$ http://localhost:8080/web/

※Use custom domain
ex)
$ http://passonate.dev.com:8080/web/
```

### Run unit test
```
$ make test
```
