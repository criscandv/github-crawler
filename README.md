# Github crawler

> This is a basic spider with the propose of search and extract info from the github search.

>The function of the spider is search between Repositories, Wikis and Issues with the keywords passed to the spider.

>Before start, we need to use Python 3.x <br>
>Is recommend the use of virtualenv, but is not a requirement <br>
>The project dependences is inside requirements.txt, to install we use pip and run
>```pip install -r requirements.txt```
>After that, the requirements will be installed and we'll can use the spider.

>To run the spider we have to pass some arguments which are:
> - keywords: It's a string, each word has to be separated with comma: jwt,python
> - proxies: It's a string, each ip direction has to be separated with comma: https://36.89.229.97:35098,https://103.57.70.248:55441
> - type: It's a string, choose between Repositories, Wikis or Issues

>Then, you can run the spider execute the next command:    
```
scrapy runspider github-crawler.py -a keywords='jwt' -a proxies='https://36.89.229.97:35098,https://103.57.70.248:55441' -a type='Repositories'
```

>The spider will return a json document named ```urls_github.json``` with the data.

**Important**: Proxies from the example may not be available and results could be different by the time you read this document.