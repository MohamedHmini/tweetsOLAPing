# tweetsOLAPing : an end-to-end social-media data-warehousing project :

i'll walk you through an execution example using light-weight (very) data to show you the results.

## Table of Contents :
- [0- ENV set-up:](#0--env-set-up-)
- [1- ETL pipeline :](#1--etl-pipeline--)
  * [a) Extraction :](#a--extraction--)
  * [b) Transformation :](#b--transformation--)
  * [c) Loading :](#c--loading--)
    + [SSIS modeling :](#ssis-modeling--)
    + [SSAS cube modeling :](#ssas-cube-modeling--)
- [2. Analysis :](#2-analysis--)
  * [MDX queries :](#mdx-queries--)
  * [powerBI report :](#powerbi-report--)

## 0- ENV set-up:

the extraction/transformation steps of the pipeline will need the following environment set-up :
```shell
pip install virtualenv
```
```shell
virtualenv tweetsOLAPingENV
```
```shell
source tweetsOLAPingENV/bin/activate
```
```shell
pip install -r requirements.txt
```

as far as the Loading ETL step and the final analysis, make sure you have the following :
1. MSSMS (microsoft Sql server managment studio).
2. SSDT (Sql server data tools).
3. SSIS (Sql server integration service).
4. SSAS (Sql server analysis service).
5. powerBI.

## 1- ETL pipeline : 
### a) Extraction :

the very first step is to prepare the <b>tweetsPOOLs.csv</b> file as in https://github.com/MohamedHmini/tweetsOLAPing/blob/master/extraction/archivedTweetsCrawler/tweetsPOOLs.csv.

then we shall execute the <b>Scrapy Spider</b> to crawl the archive needed website pages as follows : 

```shell
  cd extraction/archivedTweetsCrawler
  scrapy crawl -o tweetsSTREAMs.csv tweets
```
after that you will get a file like the one in here : https://github.com/MohamedHmini/tweetsOLAPing/blob/master/sample-data/tweetsSTREAMs.csv

the next step is to structure that CSV file into a tree like structure composed of directories and files :
```shell
  cd extraction/
  python tweetsPOOLsParser.py tweetsSTREAMs.csv ../root_urls/
```
the output will be somewhat like this (light-weight) example : https://github.com/MohamedHmini/tweetsOLAPing/tree/master/sample-data/urls_root

next we have to perform a random selection to select only some URLs and not all, note that each URL will bring you up to 5000 tweets :

```shell
  cd extraction/
  python urlsRandomSelector.py ../root_urls/ ../chosen_urls.txt 700
```

again check this link for an output example : https://github.com/MohamedHmini/tweetsOLAPing/blob/master/sample-data/chosen_urls.txt

now after that we have all the needed URLs in a single file we can start downloading :

```shell
  cd extraction/
  python tweetsDownloader.py ../chosen_urls.txt ../downloaded_pools/ ../download_error.txt
```

again check this link for an output example : https://github.com/MohamedHmini/tweetsOLAPing/tree/master/sample-data/downloaded-pools

after we downloaded the files you will notice that they are compressed with a .bz2 file extension thus you have to decompress them somehow, i won't provide a solution in this stage.

again check this link for an output example : https://github.com/MohamedHmini/tweetsOLAPing/tree/master/sample-data/decompressed-pools

note that i provide a script to lookup tweets from the twitterAPI directly using the downloaded tweets IDs, cause the tweets have been pulled in the stream by the collected you will find that most of them has zero metrics, i solve this solution using a context-aware random generator.

### b) Transformation :

as for the transformation it's composed of two parts, first we transform our data from JSON to CSV and create all the needed derived attributes, also we shall remove twitto duplicates using, beware that the cleanUsersCSV.py script will using multi-threading to speed-up the I/O operations and the result will be stored in a directory, you can then merge them on your own.

```shell
  cd transformation/
  python prepareTweets.py ../decompressed_pools/ ../tweets.csv ../twittos.csv ../trans-err.txt
  python cleanUsersCSV.py ../twittos.csv ../twittos
```

the second part consists of performing NLP analysis on the tweets to generate the sentiment-score and the content-classification, you have to provide the projectkey.json file from google NLP APIin the same directory.

```shell
  cd transformation/
  python performNLPanalysis.py ../decompressed_pools/ ../tweets_sentiments.csv ../sent-err.txt
```

again check this link for an output example : https://github.com/MohamedHmini/tweetsOLAPing/tree/master/sample-data/processed

### c) Loading :

before starting the SSIS process you have to provide a normalized data in the right path (shall be fixed) :

```shell
  cd loading/
  python dataNormalization.py ../twittos.csv ../tweets.csv ../data/normalized
```

again check this link for an output example : https://github.com/MohamedHmini/tweetsOLAPing/tree/master/sample-data/normalized-data

for SSIS logic i provide the full model : https://github.com/MohamedHmini/tweetsOLAPing/tree/master/loading/tweetsOLAPing_loading

as well as the SSAS logic is fully provided : https://github.com/MohamedHmini/tweetsOLAPing/tree/master/analysis/tweetsOLAPing_analysis

#### SSIS modeling : 

after setting up all the connections ( the normalized data as well as the OLEDB destinations), we now arrive at the integration step or the data loading : 

<p align="center">
  <img src="./imgs/SSIS-global-process.jpg" />
</p>
<p align="center">
  <img src="./imgs/dates-data-flow.jpg" />
</p>
<p align="center">
  <img src="./imgs/ts-data-flow.jpg" />
</p>
<p align="center">
  <img src="./imgs/loc-data-flow.jpg" />
</p>
<p align="center">
  <img src="./imgs/twmd-data-flow.jpg" />
</p>
<p align="center">
  <img src="./imgs/usrmd-data-flow.jpg" />
</p>
<p align="center">
  <img src="./imgs/tw-data-flow.jpg" />
</p>
<p align="center">
  <img src="./imgs/usr-data-flow.jpg" />
</p>

#### SSAS cube modeling : 

<p align="center">
  <img src="./imgs/model.jpg" />
</p>

## 2. Analysis :

### MDX queries : 

```sql
SELECT 
  NON EMPTY
  (
    [Twitto Meta Data].[User Category].children, 
    [Measures].[Retweet Count]
  ) ON COLUMNS,
  NON EMPTY 
  (
    [Twitto Meta Data].[User Activity].children
  ) ON ROWS
FROM
  [TweetsOLAPing_cube]
```

```sql
SELECT 
  NON EMPTY
  (
    [Twitto Meta Data].[User Category].children, 
    [Measures].[Retweet Count]
  ) ON COLUMNS,
  NON EMPTY 
  (
    [Twitto Meta Data].[User Activity].children, 
    [Tweet Meta Data].[Sentiment Tag].children
  ) ON ROWS
FROM
  [TweetsOLAPing_cube]
```

```sql
SELECT 
  NON EMPTY
  (
    [Tweet Meta Data].[Media Type].children, 
    [Measures].[Retweet Count]
  ) ON COLUMNS,
  NON EMPTY 
  (
    [Tweet Meta Data].[Has Hashtags].children, 
    [Date].[Weekday].children
  ) ON ROWS
FROM
  [TweetsOLAPing_cube]
```

### powerBI report :

the final report is provided in : https://github.com/MohamedHmini/tweetsOLAPing/tree/master/analysis/powerBI

here are some examples :

![alt text](analysis-example/analysis1.gif)
![alt text](analysis-example/analysis2.gif)
![alt text](analysis-example/analysis3.gif)
![alt text](analysis-example/analysis4.gif)
![alt text](analysis-example/analysis5.gif)


<b> MOHAMED-HMINI 2020</b>
