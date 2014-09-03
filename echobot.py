import anydbm
import os.path
import tweepy

import config

class EchoBot(object):
  def __init__(self, twitter, tweet_store):
    self.tweet_store = tweet_store
    self.twitter = twitter
    self.name = config.BOT
    
  def respond(self):
    for tweet in self.twitter.search(q=self.name):
      if str(tweet.id) not in self.tweet_store:
        self.reply(tweet)
    self.close_db()

  def reply(self, tweet):
    def clean_author(tweet):
      return "@" + tweet.author.screen_name
    def remove_echo(text):
      xs = text.split()
      if self.name in xs:
        xs.remove(self.name)
        return remove_echo(" ".join(xs))
      else:
        return text
    self.twitter.update_status(status="%s %s" % (clean_author(tweet), remove_echo(tweet.text)))
    self.tweet_store[str(tweet.id)] = ""
    self.save_state()
        
  def save_state(self):
    self.tweet_store.sync()

  def close_db(self):
    self.tweet_store.close()

def authenticate_twitter(config):
  auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
  auth.set_access_token(config.token_key, config.token_secret)
  return tweepy.API(auth)

def tweet_store():
  return anydbm.open("tweet_store", "c")
    
def main():
  twitter = authenticate_twitter(config)
  echobot = EchoBot(twitter, tweet_store())
  echobot.respond()

if __name__ == "__main__":
  main()  
