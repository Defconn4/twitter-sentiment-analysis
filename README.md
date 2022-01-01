# A Rudimentary Implementation of Twitter Sentiment Analysis

## Check out & Run the Code
- Clone the repository.
- Optionally, run `install.py` (I will explain more details later).
- Head to `classify.py` in your favorite IDE and place your Twitter authentication credentials where noted near the top of the file.
- Feel free to change the constant `NUM_TWEETS` to fetch > 10 tweets at a time from the Twitter API (though number of requests API to 180 requests per 15 minutes)!
- Run the code in your terminal and enter any string of your choice and see how it everyone else feels about it!

## Backstory & Intentions
### Origin
This project was stuck in my own personal-project purgatory for the longest time due to a variety of circumstances, largely COVID, academics and general laziness. This was something I envisioned to be fleshed out much more in scale


Intentions on where I want to take this project/what I want it to be able to do:
1) Be able to search tweets containing a keyword/sentence (string is passed in regardless).
2) Parse the tweet by removing any additonal characters (repeated characters), URLS/links, symbols, etc.

Files needed: (2 & 3 are found here: https://github.com/karanluthra/twitter-sentiment-training)
1) Authentification.py
2) install.py 
3) corpus.csv

4) Get verified on Twitter so you can apply for Twitter API usage
==> Get verified on Twitter so you can use the Twitter API, details found here in this article
===> https://towardsdatascience.com/creating-the-twitter-sentiment-analysis-program-in-python-with-naive-bayes-classification-672e5589a7ed

5) Need the following libraries once Python is installed (w/ IDE):
==> twitter
====> pip install python-twitter
==> nltk
====> pip install --user -U nltk
^^^^^^^^^
Notes: "--user" means that packages are installed wiithin your home directory to void system python installation.
"-U" means upgrade (? - I think this is what is means), which forces updates in case of a backed-installation.
^^^^^^^^^
==> (optional) numpy
====> pip install --user -U numpy

==> textblob
====> pip install textblob

==> NLTK corpora
====> python -m textblob.download_corpora

==> oauth2
===> pip install python-oauth2

To test installation:
run python, then type import nltk
==> If the line runs, then it's all good to go, should look like ">>>" for the interpretaor waiting for a next command

==> re
====> Stands for "Regular Expresion" syntax, which is useful for checking if a particular string mataches a given regular expression.
A regular expression is a sequence of characters that forms a search pattern.
==> csv
====> Allows you to work with Excel files pretty much.
==> time
====> Allows you access time and time conversions
==> json
====> Javascript Object Notation, uses human-readable text to store and transmit data object consisting of attributes - value pairs and array data types.

NOTE: re, csv, time, & json are standard libraries in python 3.8 so they do not need to be installed separately.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

UPDATE: 7/19/20

What is done:
- Wrote the basic code to authenticate use of Twitter API.
- Built a very basic test set, and organized the tweets in the terminal for viewing prior to making a data set for testing.
- TODO: Want to figure out how to use status.place to get actual geolocation of a tweet

Next steps:
1) Get the Niek Sanders' Corpus model for 5k hand-classified tweets.
===> Twitter still uses the REST API v1.1 so you can do Niek Sander's corpus installation found here: 
           https://github.com/karanluthra/twitter-sentiment-training

Done:
1) Downloaded twitter-sentiment training:
===> Installation:
0) Make sure you have all packages installed that are to be imported: oauth2
====> THIS WAS WRITTEN IN PYTHON 2, had to change some of the defunct functions.
====> #1) raw_input() function renamed to input()
              #2) Line 94: Changed 'rb' to 'r' for opening in text mode ==> 'rb' opens the file in binary mode, used for files that don't contain text.
                     open(filename, mode)
              #3) Line 177: Changed 'wb' to 'r' for writing to a file.
              #4) Lines 190 - 192: Changed max tweets per hour to 720, since requests in 2020 have been raised to 180 per 15 minutes (so 720 per hour).
                    ==> Found here for 'GET: search/tweets': https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits
              #5) Changed print statements in entire program to include parentheses around strings to be printed (must be defunct from 2.7 to allow no () ).
              #6) Changed Line 245 & Line 221 to stop reading bytes to unicode (rb -> r or wb -> w)
1) Set access key and (access) secret, consumer key and (consumer) secret to global variables in install.py
2) Start script in cmd, navigate to correct directory and type: python install.py
3) Hit enter 3 times to accept defaults.
4) Wait until script indicates that it's done.
==> Script will automatically resume where it left off if downloading is interrupted. Completed corpus will in a file named full-corpus.csv

NOTE: Any original scripts from Niek J. Sanders found on his offical website (e.g. http://www.sananalytics.com/lab/twitter-sentiment/) are defunct and the domain has been sold.
I updated the scripts to work with Python 3, see changelog above for install.py


Jan. 4th - 18:
1) Been working on implementing the training_data into an array of dictionaries, so you don't have to wait 8 hours to re-read all tweets from the full_corpus.
2) Created the file `training_set_added_keys.csv` to add keys "topic", "tweet_id", etc.. to the training_data file so I can more easily convert it.

To convert the file: this finally worked:

1) Use csv.DictReader(filename).
      1a) Add the row for each column in the training_set_added_keys.csv that has the 'topic', 'label', 'tweet_id', 'text'
2) Clean the 'filename' csv file (in our case was training_set_added_keys.csv) by removing the blank rows.
      2a) Then remove the leading and trailing single quotes from the tweet_ids so that we can see them as integers.
3) Then we need to conver the csv file (now called keys_cleaned.csv) to a list of dictionaries for tweet pre-processing.
# References to line 218 in code.

1/24/21: Biggest Issue, when i was working on the training_set_added_keys.csv for some reason all the tweet IDs were made the same number. Need to fix this immediately before moving on.


7/9/21 (almost started this a year ago wow):

Resources:

1) For information on the Tweet object: https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet

2) For information on the User object: https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user

3) Tweepy API docs: https://docs.tweepy.org/en/v3.5.0/api.html#tweepy-api-twitter-api-wrapper

4) Python-Twitter API docs: https://python-twitter.readthedocs.io/en/latest/index.html

Links left in Chrome:

1) https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html
2) https://docs.python.org/3/library/csv.html
3) https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character
4) https://stackoverflow.com/questions/30750843/python-3-unicodedecodeerror-charmap-codec-cant-decode-byte-0x9d

7/27/21:

UPDATE:
- Turns out you don't care about the Tweet ID after you build the Training Set, all you need is the tweet text and the tweet sentiment (text and label).
