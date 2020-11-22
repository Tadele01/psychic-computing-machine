from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
from textblob import TextBlob
import tweepy
import config
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)
app = Flask(__name__)
cors = CORS(app)
@app.route('/sentiment_analysis')
@cross_origin()
def return_sentiment_analysis():
    trump = api.get_user('realDonaldTrump')
    trump_name = trump.screen_name
    #handle = twitter_handle
    tweets = api.user_timeline(screen_name=trump_name, count=200,  include_rts = False, tweet_mode = 'extended')
    tweets_list = [tweet.full_text for tweet in tweets]
    for tweet in tweets_list:
        sentiment = TextBlob(tweet)
    labels = ['Negative', 'Neutral', 'postive']
    values = [0, 0, 0] #initializing count array
    for tweet in tweets_list:
        sentiment = TextBlob(tweet)
        polarity = round((sentiment.polarity +1) *3) %3
        values[polarity] = values[polarity] + 1
    data = {
        "labels": labels,
        "values_": values,
    }
    return jsonify(data)
if __name__ == "__main__":
    app.run(debug=True)