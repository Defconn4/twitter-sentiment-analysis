# Note: Using the python-twitter API.
from nltk.corpus.reader import sentiwordnet, wordlist
import twitter
import pandas as pd
import re
import nltk
import numpy as np
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
import csv

# Constant for number of tweets fetched from Twitter API.
NUM_TWEETS = 10

""" Utility Functions """
def parse_csv(file_name):
    df = pd.read_csv(file_name)
    return df

def convert_to_df(record_lst):
	return pd.DataFrame(record_lst)


""" initialize API instance - source: https://towardsdatascience.com/creating-the-twitter-sentiment-analysis-program-in-python-with-naive-bayes-classification-672e5589a7ed

Example Use:
consumer_key='YOUR_CONSUMER_KEY',
consumer_secret='YOUR_CONSUMER_SECRET',
access_token_key='YOUR_ACCESS_TOKEN_KEY',
access_token_secret='YOUR_ACCESS_TOKEN_SECRET')

NOTE: consumer_key & consumer_secret listed as "API key" & "API key secret" on Twitter Developer page. 
"""
api = twitter.Api(consumer_key='',
					consumer_secret='',
					access_token_key='',
					access_token_secret='',
					tweet_mode = 'extended')													# Allow for non-truncated tweet text. Field text in JSON response must be 'status.full_text'

"""
	Searches for tweets containing a specified term, returns an iterable containing twitter.Status objects.
	NOTE: Twitter limits the number of request you can through the API to 180 requests per 15 minutes.
"""
def buildTestSet():
	try:
		
		search_term = input("Enter a word or phrase to be searched: ")

		# Limit to the number of tweets to search is 100 (regardless if you type a larger number).
		tweets_fetched = api.GetSearch(term = search_term, count = NUM_TWEETS, since = '2021-01-01')

		print("\n")
		print("Fetched Tweet(s): " + str(len(tweets_fetched)) + "\nTweet(s) contain the following term: " + search_term)
		print("\n")

		return [{"user": status.user.screen_name, "user_id": status.user.id_str, "created_at": status.user.created_at, "text": status.full_text, "label": None, "Tweet ID": status.id} for status in tweets_fetched]
		
	except:
		print("Something went wrong!")
		return None

"""
	Using Niek Sanders' Corpus of 5k+ classified tweets:
 	To build the training set, repeat until EOF: 180 requests per 15 minutes.
 	15 min * 60 sec = 900 sec
 	(900 seconds / 180 tweets)
 	Credit: https://gist.github.com/AnasAlmasri/33caec97bca7f33f8c1f8ab457a0b056#file-sentimentanalysis-py

	Possibly a result of API requests (tweet IDs need to be ints not strings), tweet IDs will be rounded/truncated, making them pretty much useless.
	You don't need them past this point anyways, but just something worth mentioning.
"""
def buildTrainingSet(trainingFile, tweetDataFile):

	import csv
	import time
	corpus = []

	with open(trainingFile, "r") as csvfile:
		lineReader = csv.reader(csvfile, delimiter = ',', quotechar ="\"")
		for row in lineReader:
			if not row:									# Check if the row is empty.
				continue
			corpus.append({"topic": row[0], "label": row[1], "tweet_id": row[2]})

	sleep_time = 900/180
	trainingDataSet = []

	for tweet in corpus:		
		try:
			status = api.GetStatus(tweet["tweet_id"])
			print("Tweet fetched: " + status.full_text)
			tweet["text"] = status.full_text
			trainingDataSet.append(tweet)
			time.sleep(sleep_time)
		except Exception as e:
			print(e)
			continue
	
	print("\n\nTraining_Set Finished!\n\n")
	
	# Write quotes to empty CSV file in current directory.
	with open(tweetDataFile, 'w', encoding='utf-8') as csvfile:
		linewriter = csv.writer(csvfile, delimiter = ',', quotechar = "\"")
		for tweet in trainingDataSet:
			try:
				linewriter.writerow([tweet["tweet_id"], tweet["text"], tweet["label"], tweet["topic"]])
			except Exception as e:
				print(e)

	return trainingDataSet

# Clean up tweets for classification (removes "stop" words)
class PreProcessTweets:
	def __init__(self):
		self.stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER', 'URL'])

	def processTweets(self, list_of_tweets):
		processed_tweets = []
		for tweet in list_of_tweets:
			processed_tweets.append((self.clean_tweets(tweet["text"]), tweet["label"]))
		return processed_tweets
	
	def clean_tweets(self, tweet):
		tweet = tweet.lower()														# convert text to lower-case
		tweet = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet) 			# remove URLs (use raw string)
		tweet = re.sub('@[^/s]+', 'AT_USER', tweet) 								# remove usernames
		tweet = re.sub(r'#([^\s]+)', r'\1', tweet) 									# remove the # in #hashtag
		tweet = word_tokenize(tweet) 												# remove repeated characters (helloooooooo into hello)
		return [word for word in tweet if word not in self.stopwords]

"""
	Naive Bayes Classification: 
	1) Build vocabulary of all words present in the training data set.
	word_features represents a list of distinct words - with # of occurences in the set as a key. 
"""
def buildVocab(preprocessedTrainingData):
	vocab = []
	for (words, sentiment) in preprocessedTrainingData:
		vocab.extend(words)
	
	wordlist = nltk.FreqDist(vocab)
	features = wordlist.keys()
	return features

"""
	2) Parse training set data and compare every word against current tweet assigning a number as such:
	label 1 (true): if word in vocabulary is found in tweet (present)
	label 0 (false): if word in vocabulary is not found in tweet (absent)
"""
def extract_features(tweet):
		tweet_words = set(tweet)
		features = {}
		for word in word_features:
			features['contains(%s)' % word] = (word in tweet_words)		# JSON key 'contains word X' where X is the word.
		
		return features

# ================================================================= Auxillary Functions ================================================================= 

"""
	Removes blank rows from csv containing tweet data.
	Add rows headers at the top of csv indicating tweet_id, text, label (sentiment), and topic.
"""
def clean_tweet_data():

	df = parse_csv('./tweet_data.csv')
	convert_to_df(df)

	try:		
		df = df.dropna('index', 'all')
		df.columns = ['tweet_id', 'text', 'label', 'topic']		# Removes first tweet for no reason, fuck it.
	except Exception as e:
		print("In clean_tweet_data(): ", e)

	# Overwrite tweet_data.csv in current directory to avoid file confusion.
	df.to_csv('tweet_data.csv', index = False)
	print("Blank rows removed & columns headers added to tweet_data.csv. Check csv file for changes.\n")

"""
	In conjuction with clean_tweet_data(), this function avoid having to build the training set (which takes hours) each time you run the program
	by taking tweetData formed in tweet_data.csv and placing into a dataframe-like array of dictionaries. Keys are tweet_id, text, label, topic respectively.
"""
def composeTweetData(tweetData):
	cleanedSet = []
	x = 0
	with open(tweetData, 'r', encoding = 'utf8') as csvfile:
		reader = csv.DictReader(csvfile)
		for tweetDict in reader:
			cleanedSet.append(tweetDict)
	return cleanedSet

# ================================================================= Debugging Functions =================================================================

""" 
	Test fetching of tweets - debugging function.
	Use this function conservatively to avoid racking up API requests.
"""
def fetchTweetsTest():
	tweet_count = 1
	tweets_dict = buildTestSet() 	# List of tweets

	# Iterate through dictionaries
	for tweet in tweets_dict:
		print("------------------------------------------------------------------------------------------------------------")
		print("Tweet #%d\n" % tweet_count)
		print("Tweet created at: %s" % tweet['created_at'])
		print("Tweet text: %s" % tweet['text'])

		print("\n\tTweet made by user: %s\n\tUser ID: %s" % (tweet['user'], tweet['user_id']) )
		print("------------------------------------------------------------------------------------------------------------")
		print("\n")
		tweet_count += 1

	return None

# ================================================================= Control Flow ========================================================================

"""
	This may look unusual to organize the function calls like this, but coming back to this code after a nearly semester-long hiatus was a headache
	and a half. This helped immensely in trying to figure out the control flow.
"""
# test authentication
#print(twitter_api.VerifyCredentials())

# build test set for training
testDataSet = buildTestSet()

# print tweets fetched from buildTestData() - for debugging.
#fetchTweetsTest()

# 8 hour function setup - argument filling
trainingFile = "./corpus.csv" 					# Need escape sequence so backslashes for directory interpreted correctly within string.
tweetDataFile = "./tweet_data.csv"				# This file will be created once the function has run once.

# TODO: build the training set - only need to run once to create tweet_data.csv
#trainingData = buildTrainingSet(trainingFile, tweetDataFile)

# cleanup tweet_data.csv - removes blank rows & add column headers
clean_tweet_data()

# convert tweet_data.csv to an array of dictionaries as below,
# so you don't have to rebuild the training set every time you run the program.
tweetDataDict = composeTweetData(tweetDataFile)

# tweet pre-processing before classification.
tweetProcessor = PreProcessTweets()
preprocessedTrainingData = tweetProcessor.processTweets(tweetDataDict)
preprocessedTestSet = tweetProcessor.processTweets(testDataSet)

# Naive Bayes Classification broken down into 4 steps:
# 1) Building the vocabulary.
# 2) Matching tweets against our vocabulary.
# 3) Building our feature vector.
word_features = buildVocab(preprocessedTrainingData)
trainingFeatures = nltk.classify.apply_features(extract_features, preprocessedTrainingData) # apply_features performs feature extraction.

# 4) Training the classifer.
NBayesClassifer = nltk.NaiveBayesClassifier.train(trainingFeatures)

# Model testing & rudimentary valdiation
NBResultLabels = [NBayesClassifer.classify(extract_features(tweet[0])) for tweet in preprocessedTestSet]

# Get the majority vote
pos = NBResultLabels.count('positive')
neg = NBResultLabels.count('negative')
neutral = NBResultLabels.count('neutral')
sentiments = [neg, neutral, pos]

if sentiments.index(max(sentiments)) == 0:
	print("\nOverall negative sentiment of: " + str(100 * (neg/NUM_TWEETS)) + "%\n")

elif sentiments.index(max(sentiments)) == 1:
	print("\nOverall neutral sentiment of: " + str(100 * (neutral/NUM_TWEETS)) + "%\n")

elif sentiments.index(max(sentiments)) == 2:
	print("\nOverall positive sentiment of: " + str(100 * (pos/NUM_TWEETS)) + "%\n")
# =======================================================================================================================================================