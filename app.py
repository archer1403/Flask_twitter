import json
import threading

import twint
from flask import Flask, render_template, request
from twitter_scraper import get_profile_details
from threading import Thread
from classify.predict_class import classify

app = Flask(__name__)


# finder_box_tweets
def get_data_tweets(key, tweets_count, date_from, date_to):
    c = twint.Config()
    # c.Username = key
    c.Search = "(from:" + key + ") -filter:links -filter:replies"
    c.Until = date_to
    c.Since = date_from
    c.Count = True
    c.Limit = tweets_count
    c.Store_object = True
    c.Hide_output = True
    if len(twint.output.tweets_list) != 0:
        twint.output.tweets_list = []
    twint.run.Search(c)
    tweets = twint.output.tweets_list
    return tweets


# finder_box_topics
def get_data_topics(key, tweets_count, date_from, date_to):
    c = twint.Config()
    c.Search = key
    c.Until = None
    c.Since = None
    c.Count = True
    c.Limit = tweets_count
    c.Store_object = True
    c.Hide_output = True
    if len(twint.output.tweets_list) != 0:
        twint.output.tweets_list = []
    twint.run.Search(c)
    topics = twint.output.tweets_list
    return topics

# finder_replies_tweets_15
def get_rep_twe(key, tweest_count):
    re, tw = 0, 0
    list = []
    c = twint.Config()
    c.Search = "(from:" + key + ")"
    c.Count = True
    c.Limit = tweest_count
    c.Store_object = True
    c.Hide_output = True
    if len(twint.output.tweets_list) != 0:
        twint.output.tweets_list = []
    twint.run.Search(c)
    re_tw_s = twint.output.tweets_list
    for re_tw in re_tw_s:
        re += re_tw.replies_count
        tw += re_tw.retweets_count
    list.append(re, tw)
    return list




# controller
def con_get_profiles(twitter_username):
    user = json.loads(get_profile_details(twitter_username=twitter_username, filename=''))
    return user


# controller
def con_get_tweets(key, tweets_count, date_from, date_to):
    # tweets = json.loads(scrape_keyword(keyword=key, browser="firefox", tweets_count=tweets_count, until=date_to, since=date_from, output_format="json", filename="", headless=False))
    tweets = get_data_tweets(key, tweets_count, date_from, date_to)
    return tweets


# controller
def con_get_topics(key, tweets_count, date_from, date_to):
    topics = get_data_topics(key, tweets_count, date_from, date_to)
    return topics


# route
@app.route("/")
def main():
    return render_template('index.html')


@app.route("/get_profiles", methods=['GET', 'POST'])
def get_profiles():
    if request.method == 'POST':
        users = con_get_profiles(request.form.get('username'))
        # re_tw = get_rep_twe(request.form.get('username'), int(15))
        return render_template('result.html', users=users)
    else:
        return render_template('profiles.html')


@app.route("/get_tweets", methods=['GET', 'POST'])
def get_tweets():
    if request.method == 'POST':
        key = request.form.get('key')
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')
        tweets_count = request.form.get('counts')
        # print('tweets_count: ',len(tweets_count))
        tweets = con_get_tweets(key, int(tweets_count), date_from, date_to)
        # print('tweets: ',len(tweets))
        if tweets == []:
            message = 'Không có dữ liệu'
            return render_template('tweets.html', message=message)
        elif tweets != []:
            return render_template('table.html', tweets=tweets)
    else:
        return render_template('tweets.html')


@app.route("/get_topic", methods=['GET', 'POST'])
def get_topics():
    if request.method == 'POST':
        key = request.form.get('key')
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')
        tweets_count = request.form.get('counts')
        topics = con_get_topics(key, int(tweets_count), date_from, date_to)
        print(topics)
        if topics == []:
            message = 'Không có dữ liệu'
            return render_template('topics.html.html', message=message)
        elif topics != []:
            return render_template('table.html', tweets=topics)
    else:
        return render_template('topics.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(debug=True)
