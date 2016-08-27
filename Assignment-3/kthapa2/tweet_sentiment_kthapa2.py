import sys
import json
from json.decoder import JSONDecodeError

static_sentiment_score_map = {}
tweet_sentiment_score_map = {}


def main():
    if len(sys.argv) < 3:
        print("USAGE : python3 tweet_sentiment_kthapa2.py "
              "<sentiment_file> <tweet_file> > tweet_sentiment_[yourNetID].txt")
        print("Program will exit now...")
        sys.exit(1)

    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    read_sentiment_file(sent_file)
    tweet_string = read_file(tweet_file)
    process_all_tweets(tweet_string)
    happiest_tweets = ((key, tweet_sentiment_score_map[key]) for key in
                       sorted(tweet_sentiment_score_map, key=tweet_sentiment_score_map.get, reverse=True)[:10])
    saddest_tweets = ((key, tweet_sentiment_score_map[key]) for key in
                      sorted(tweet_sentiment_score_map, key=tweet_sentiment_score_map.get, reverse=True)[-10:])
    for tweet, sentiment_score in happiest_tweets:
        print("[" + str(sentiment_score) + "] : [" + repr(tweet) + "]")

    for tweet, sentiment_score in saddest_tweets:
        print("[" + str(sentiment_score) + "] : [" + repr(tweet) + "]")


def read_sentiment_file(sent_file_name):
    sentiment_file_text_data = read_file(sent_file_name)
    sentiment_list = sentiment_file_text_data.split("\n")
    for sentiment_data in sentiment_list:
        term_score = sentiment_data.split("\t")
        static_sentiment_score_map[term_score[0]] = float(term_score[1])
        # print(term_score[0] + " | " + term_score[1])


def read_tweet_file(tweet_file_name):
    tweet_file_text_data = read_file(tweet_file_name)
    tweet_file_text_list = tweet_file_text_data.split("\n")[1:]
    for single_tweet in tweet_file_text_list:
        if single_tweet:
            single_tweet_text = single_tweet.split(",", 1)[1]
            calculate_sentiment_score_for_each_tweet(eval(single_tweet_text))


def calculate_sentiment_score_for_each_tweet(single_tweet):
    single_tweet_text_list = single_tweet.split()
    tweet_sentiment_score = 0
    for single_word in single_tweet_text_list:
        tweet_sentiment_score += static_sentiment_score_map.get(single_word, 0)

    tweet_sentiment_score_map[single_tweet] = tweet_sentiment_score


def process_all_tweets(tweet_string):
    tweet_list = tweet_string.split("\n")
    for tweet_data in tweet_list:
        if tweet_data:
            try:
                tweet_json_data = json.loads(tweet_data)
                tweet_text_part = tweet_json_data["text"]
                calculate_sentiment_score_for_each_tweet(tweet_text_part)
            except JSONDecodeError:
                print("JSON Decode Error")


def read_file(filename):
    f = open(filename, "rU")
    text = f.read()
    f.close()
    return text


if __name__ == '__main__':
    main()
