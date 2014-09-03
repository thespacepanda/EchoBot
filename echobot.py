import anydbm
import os.path
import tweepy

import config

class EchoBot(object):
  def __init__(self):
    def auth():
      auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
      auth.set_access_token(config.token_key, config.token_secret)
      return tweepy.API(auth)
    self.tweet_store = anydbm.open("tweet_store", "c")
    self.twitter = auth()
    self.name = config.BOT
    
  def respond(self):
    for tweet in self.twitter.search(q=self.name):
      if str(tweet.id) not in self.tweet_store.keys():
        self.reply(tweet)
    self.save_state()

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
        
  def save_state(self):
    self.tweet_store.close()

def main():
  echobot = EchoBot()
  echobot.respond()

if __name__ == "__main__":
  main()  
