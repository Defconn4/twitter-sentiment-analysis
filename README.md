# A Rudimentary Implementation of Twitter Sentiment Analysis

## Check out & Run the Code
- Clone the repository.
- You will need to obtain authentication credentials to use the Twitter API by registering on the [Twitter Developer Platform](https://developer.twitter.com/en).
   - Sign up, click on the Apps button, create an App, and request access for your own personal use. Your application may take up to a day to be approved, but more likely a couple of a hours.
- Optionally, run `install.py` (see details below).
- Head to `classify.py` in your favorite IDE and place your Twitter authentication credentials where noted near the top of the file.
- Feel free to change the constant `NUM_TWEETS` to fetch > 10 tweets at a time from the Twitter API (though number of requests API to 180 requests per 15 minutes)!
- Run the code in your terminal and enter any string of your choice and see how it everyone else feels about it!

## Packages needed:
### NOTE: It might be quciker running `classify.py` in cmd and seeing what needs to be installed ;).
- python twitter
   - `pip install python-twitter`
- Natural Langugae Toolkit (nltk)

   - `pip install --user -U nltk`
   
      - NOTE: `--user` means that packages are installed wiithin your home directory to void system python installation.
      - Pretty sure `-U` means "upgrade". which forces updates in case of a backed-installation.
 
- NLTK corpora
    - `python -m textblob.download_corpora`

- textblob
   - `pip install textblob`

- oauth2
   - `pip install python-oauth2`

## install.py
When I originally started this project, I was closely following a tutorial which utilized the repository [`karanluthra/twitter-sentiment-training`](https://github.com/karanluthra/twitter-sentiment-training), which was an update of a script developed by Niek J. Sanders (his domain has since been sold, but credit where credit is due) for his own Twitter Sentiment Classifier. `karanluthra`'s repository simply updated the script to work with Twitter's REST API v1.1 from nearly a decade ago, thus it was udpated to incorporate the authentication capability.

Long story short, the script would download a massive repository of tweets (~5200) for use, which we would then authenticate each tweet using the Twitter API in `classifiy.py`. However, this script can take up to 18 hours from my own personal experience, so I included the files `corpus.csv` and `tweet_data.csv` in my repository to skip this step. The former is the original full corpus obtained by running `install.py`. The latter is simply the authenticated tweets from the full corpus. The process of authentication done in `classify.py` is very slow as well, hence why I've included `tweet_data.csv`.

## **Basically, the code is ready to use right out of the box so you don't need to wait days like I did!**

### If you plan to use `install.py`
   1) Set access key and (access) secret, consumer key and (consumer) secret to global variables in install.py
   2) Start script in cmd, navigate to correct directory and type: `python install.py`
   3) Hit enter 3 times to accept default script parameters.
   4) Wait until script indicates that it's done.
      - Script will automatically resume where it left off if downloading is interrupted. Completed corpus will in a file named full-corpus.csv

### Important notes about install.py
I updated `install.py` to work with Python 3 as it was originally written for Python 2, see below for details:
   1) raw_input() function renamed to input().
   2) **Line 94:** Changed `rb` to `r` for opening in text mode. `rb` opens the file in binary mode, which is used for files that don't contain text.
   3) **Line 177:** Changed `wb` to `r` for writing to a file.
   4) **Lines 190 - 192:** Changed max tweets per hour to 720, since requests in 2020 have been raised to 180 per 15 minutes (so 720 per hour).
      - Found here for 'GET: search/tweets': https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits
   6) Changed print statements in entire program to include parentheses around strings to be printed. This must be some weird thing from Py2.7 that didn't allow `()` within print statements.
   7) Changed **Line 221 & Line 245** to stop reading bytes to unicode.



## Backstory & Intentions
### Origin
This project was stuck in my own personal-project purgatory for the longest time due to a variety of circumstances, largely COVID, academics and general laziness. This was something I envisioned I would flesh out, but by the time I sat down again at random intervals over the past year, I found that the age old programming problem of "project-burnout" had hit me. So, I wanted to finally put this old dog to rest. It was still a very fun project and I'm excited to move onto move complex and intricate projects in the future!

This project was great for quick exposure to REST API mechanics and usage, as well as text manipulation, and data aggregation, cleaning, and organization.

## Roadmap for improvement
1) Determine why some strings produce purely neutral sentiments when they are *clearly* polarizing topics on Twitter. Get creative and you can think of plenty of examples :)
2) Implement a more rigorous procedure for determining overall sentiments.
3) To be determined...

# Sources:
1) https://towardsdatascience.com/creating-the-twitter-sentiment-analysis-program-in-python-with-naive-bayes-classification-672e5589a7ed
2) https://github.com/karanluthra/twitter-sentiment-training/blob/master/corpus.csv
3) https://developer.twitter.com/en/docs/twitter-api/api-reference-index
4) https://python-twitter.readthedocs.io/en/latest/twitter.html#module-twitter.api
5) https://docs.tweepy.org/en/v3.5.0/api.html#tweepy-api-twitter-api-wrapper
