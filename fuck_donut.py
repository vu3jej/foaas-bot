#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

# This script combines Fuck Off As A Service(FOAAS)[http://foaas.com/] and Twitter for some fun!
# There are still few kinks to work out. It works, though ;) 

from apscheduler.schedulers.blocking import BlockingScheduler
from foaas import fuck
import tweepy
import logging
import re

def save_id(statefile, id):

    # Write the id of the tweet last replied to on to a file
    last_id  = get_last_id(statefile)
    if last_id < id:
        with open(statefile, 'w') as f:
            f.write(id)

def get_last_id(statefile):
    
    # Get the id of the tweet last replied to
    with open(statefile, 'r') as f:
        id = int(f.read())
    return id

def no_fucks_given(twitter):

    # Generate the fucks and post it on Twitter
    mentions = []
    for mention in tweepy.Cursor(twitter.mentions_timeline).items():
        mentions.append(mention)

        for mention in reversed(mentions):
            last_id = get_last_id(last_fuck_given)
            screen_name = mention.user.screen_name
            name = mention.user.name
            tweet_id = mention.id_str

            if last_id < int(tweet_id):
                pattern = re.compile(r'(\s\-\sF_BOT)')
                reply = '@' + screen_name + ' ' + fuck.random(name = name, from_ = 'F_BOT').text
                reply = pattern.sub('', reply)

                # Shorten if message is more than 140 characters
                if len(reply) > 140:
                    reply = reply[0:137] + '...'

                # Reply to the tweet with id of tweet_id
                twitter.update_status(reply, tweet_id)

                # Save the tweet_id into a file to avoid spamming in the future
                save_id(last_fuck_given, tweet_id)

def main():

    try:
    
        # Authentication for the application
        keys = {
        'consumer_key': 'YOUR CONSUMER_KEY',
        'consumer_secret': 'YOUR CONSUMER_SECRET',
        'access_token_key': 'YOUR ACCESS_TOKEN',
        'access_token_secret': 'YOUR ACCESS_TOKEN_SECRET'
        }

        consumer_key = keys['consumer_key']
        consumer_secret = keys['consumer_secret']
        access_token = keys['access_token_key']
        access_token_secret = keys['access_token_secret']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.secure = True
        auth.set_access_token(access_token, access_token_secret)
        
        api = tweepy.API(auth, retry_count = 3, wait_on_rate_limit = True)

        # Give few fucks
        params = [api]
        scheduler = BlockingScheduler()
        scheduler.add_job(no_fucks_given, 'interval', args = params, minutes = 2)
        scheduler.start()

    except Exception as e:
        print e

if __name__ == '__main__':
    # Logging(apscheduler requires it)
    logging.basicConfig(filename = 'no_fucks_given.log')

    # File to save the id of the last tweet replied to
    last_fuck_given='last_id.txt'
    
    # Let's start, shall we?
    main()