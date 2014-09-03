import cPickle as pickle
import os.path
import time.sleep
import tweepy

from config import *

def load_set():
  if os.path.isfile("responded_to.p"):
    responded_to = pickle.load(open("responded_to.p", "rb"))
  else:
    responded_to = set()
  return responded_to

def dump_set(responded_to):
  pickle.dump(responded_to, open("responded_to.p", "wb"))

def auth():
  auth = tweepy.OAuthHandler(api_key, api_secret)
  auth.set_access_token(token_key, token_secret)
  return tweepy.API(auth)

def search(api):
  return api.search(q=BOT)

def respond(api, responded_to, tweets):
  for tweet in tweets:
    if tweet.id not in responded_to:
      reply(api, responded_to, tweet)

def remove_echo(text):
  xs = text.split()
  if BOT in xs:
    xs.remove(BOT)
    return remove_echo(" ".join(xs))
  else:
    return text

def clean_author(tweet):
  return "@" + tweet.author.screen_name
    
def reply(api, responded_to, tweet):
  api.update_status(status="%s %s" % (clean_author(tweet), remove_echo(tweet.text)))
  responded_to.add(tweet.id)
  dump_set(responded_to)
  
def main():
  responded_to = load_set()
  api = auth()
  respond(api, responded_to, search(api))

if __name__ == "__main__":
  main()  
