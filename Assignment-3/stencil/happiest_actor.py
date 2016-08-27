import sys
import csv

static_sentiment_score_map = {}
actor_sentiment_score_map = {}
actor_tweet_count_map = {}
actor_average_sentiment_score_map = {}


def main():
    if len(sys.argv) < 3:
        print("USAGE : python3 happiest_actor_kthapa2.py <sentiment_file> <tweet_csv_file> > happiest_actor_[yourNetID].txt")
        print("Program will exit now...")
        sys.exit(1)

    sent_file = sys.argv[1]
    csv_file = sys.argv[2]
    read_sentiment_file(sent_file)
    read_csv_file(csv_file)
    calculate_average_sentiment_score_for_each_actor()
    actor_tweets = ((key, actor_average_sentiment_score_map[key]) for key in
                    sorted(actor_average_sentiment_score_map, key=actor_average_sentiment_score_map.get,
                           reverse=True))
    for actor_name, sentiment_score in actor_tweets:
        print("[" + str(sentiment_score) + "] : [" + repr(actor_name) + "]")


def read_sentiment_file(sent_file_name):
    sentiment_file_text_data = read_file(sent_file_name)
    sentiment_list = sentiment_file_text_data.split("\n")
    for sentiment_data in sentiment_list:
        term_score = sentiment_data.split("\t")
        static_sentiment_score_map[term_score[0]] = float(term_score[1])
        # print(term_score[0] + " | " + term_score[1])


def read_csv_file(csv_file_name):
    with open(csv_file_name) as csv_file:
        csv_file_reader = csv.reader(csv_file, delimiter=",")

        # Skip First Row, i.e. Headers of the CSV file.
        next(csv_file_reader, None)

        # Now iterate over all the rows of the csv file.
        for single_tweet in csv_file_reader:
            if len(single_tweet) > 1:
                user_name = single_tweet[0]
                if user_name not in actor_tweet_count_map:
                    actor_tweet_count_map[user_name] = 0
                single_tweet_text = single_tweet[1]
                tweet_score = calculate_sentiment_score_for_each_tweet(eval(single_tweet_text))
                actor_sentiment_score_map[user_name] = actor_sentiment_score_map.get(user_name, 0) + tweet_score
                actor_tweet_count_map[user_name] += 1


def calculate_sentiment_score_for_each_tweet(single_tweet):
    single_tweet_text_list = single_tweet.split()
    tweet_sentiment_score = 0
    for single_word in single_tweet_text_list:
        tweet_sentiment_score += static_sentiment_score_map.get(single_word, 0)

    return tweet_sentiment_score


def calculate_average_sentiment_score_for_each_actor():
    for actor_name in actor_sentiment_score_map:
        actor_average_sentiment_score_map[actor_name] = float(
            actor_sentiment_score_map[actor_name] / actor_tweet_count_map[actor_name])


def read_file(filename):
    f = open(filename, "rU")
    text = f.read()
    f.close()
    return text


if __name__ == '__main__':
    main()
