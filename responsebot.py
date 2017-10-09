#!/usr/bin/python
# Calvin Cloutier
# Simple twitter bot to rewtweet a users tweet in reverse. Mostly to mess around with Twitters API

import tweepy, time
from credentials import *
import argparse

# Authorization
try:
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
except tweepy.TweepError:
		print "Auothorizing the handler failed!"
		exit(1)

try:
		auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
except tweepy.TweepError:
		print "Auothorizing the tokens failed!"
		exit(1)

api = tweepy.API(auth)

global lasttweet
lasttweet = None

# Parse user options
parser = argparse.ArgumentParser(description="Twitter bot to retweet a users tweet in reverse")
parser.add_argument("-u", "--user", dest='user', help="User whos most recent tweet you want to retweet", required=True)
parser.add_argument("-n", "--number", dest='tweetnum', help="the tweet number you want to retweet from top up. ex -n=0 is the most recent tweet", required=True, type=int)
args = parser.parse_args()

# Get the most recent tweet that is less than 140 characters total (to exclude retweets)
def lastTweet():
		tweets = []
		# 200 is max allowed
		recenttweet =  api.user_timeline(args.user, count=200, include_rts=False, exclude_replied=True)
		tweets.extend(recenttweet)

		# Get the actual tweet we want from the list
		toreverse = tweets[args.tweetnum]

		# Can't retweet anything that is more than 140 chars
		if len(toreverse.text) > 140:
				print "ERROR: Tweet length is too long. Please pick another one"
				exit(1)

		return toreverse

def makeNewTweet(oldtweet):
		tweetlen = len(oldtweet.text)
		newtweet = ''
		i = 0
		# Make the new tweet the reverse of my last tweet
		for letter in oldtweet.text:
				newtweet += oldtweet.text[tweetlen-1]
				i = i + 1
				tweetlen = tweetlen - 1

		return newtweet

# Get my most recent tweet
mylasttweet = lastTweet()
#print(mylasttweet)
mynewtweet = makeNewTweet(mylasttweet)
#print(mynewtweet)
api.update_status(status=mynewtweet)

