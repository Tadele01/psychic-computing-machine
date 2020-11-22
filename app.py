from flask import Flask, request, render_template, jsonify
from wordcloud import WordCloud, STOPWORDS
from flask_cors import CORS, cross_origin
from textblob import TextBlob
import tweepy
import config
import logging
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)
app = Flask(__name__)
cors = CORS(app)
def cluster(twitter_handle):
    user = api.get_user(twitter_handle)

def total_followers(twitter_handle):
    user = api.get_user(twitter_handle)
    total_followers = user.followers_count
    return total_followers
def most_used_word(twitter_handle):
    user = api.get_user(twitter_handle)
    name = user.screen_name
    tweets = api.user_timeline(screen_name=name, count=200,  include_rts = False, tweet_mode = 'extended')
    stopwords = set(STOPWORDS)
    tweets_text = str([tweet.full_text for tweet in tweets])
    user = api.get_user(twitter_handle)
    name = user.screen_name
    stopwords.update(['https', 't', 'co', 'many'])
    word_cloud = WordCloud(stopwords=stopwords, max_words=10, \
                      background_color="azure").generate(tweets_text)
    most_used = list(word_cloud.words_.keys())[0]
    return most_used

@app.route('/sentiment_analysis/<twitter_handle>')
@cross_origin()
def return_sentiment_analysis(twitter_handle):
    user = api.get_user(twitter_handle)
    name = user.screen_name
    tweets = api.user_timeline(screen_name=name, count=200,  include_rts = False, tweet_mode = 'extended')
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
@app.route('/word_cloud/<twitter_handle>')
@cross_origin()
def return_word_cloud(twitter_handle):
    user = api.get_user(twitter_handle)
    name = user.screen_name
    tweets = api.user_timeline(screen_name=name, count=200,  include_rts = False, tweet_mode = 'extended')
    stopwords = set(STOPWORDS)
    tweets_text = str([tweet.full_text for tweet in tweets])
    user = api.get_user(twitter_handle)
    name = user.screen_name
    stopwords.update(['https', 't', 'co', 'many'])
    word_cloud = WordCloud(stopwords=stopwords, max_words=10, \
                      background_color="azure").generate(tweets_text)
    words = word_cloud.words_
    return jsonify(words)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        logging.critical("hi")
        name = request.form['name']
        followers = total_followers(name)
        used_word = most_used_word(name)
        #cluster = cluster(name)
        return render_template('result.html', name=name, followers=followers, most_used=used_word, cluster="postive")
    return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True)