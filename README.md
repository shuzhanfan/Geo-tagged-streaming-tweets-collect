# Geo-tagged-streaming-tweets-collect

The scripts can download and store Geo-tagged Twitter streaming messages into a database using a python package called [Tweepy](http://www.tweepy.org). It connects to the [Twitter official streaming API][] and downloads data. You need to specify the twitter apps account credentials, the mongodb host, and the location coordinates in the config file before run the scripts. The downloaded tweets will then be saved into a database, either MySQL or MongoDB.

I also wrote a blog article about how to collect Twitter streaming data. Read the article [Here](https://shuzhanfan.github.io/2018/03/twitter-streaming-collection/).

<!--refs-->
[Twitter official streaming API]: https://developer.twitter.com/en/docs
