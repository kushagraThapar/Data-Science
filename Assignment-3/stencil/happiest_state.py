import sys
import json
from json import JSONDecodeError

static_sentiment_score_map = {}
state_sentiment_score_map = {}
state_abbreviation_map = {}
state_sentiment_tweet_count = {}
state_average_sentiment_score_map = {}

# Global constants
COUNTRY_CODE = "US"
PLACE_CITY = "city"
PLACE_ADMIN = "admin"
state_abbreviations_text = "AL:Alabama,AK:Alaska,AZ:Arizona,AR:Arkansas,CA:California,CO:Colorado," \
                           "CT:Connecticut,DE:Delaware,DC:District of Columbia,FL:Florida,GA:Georgia," \
                           "HI:Hawaii,ID:Idaho,IL:Illinois,IN:Indiana,IA:Iowa,KS:Kansas,KY:Kentucky," \
                           "LA:Louisiana,ME:Maine,MT:Montana,NE:Nebraska,NV:Nevada,NH:New Hampshire," \
                           "NJ:New Jersey,NM:New Mexico,NY:New York,NC:North Carolina," \
                           "ND:North Dakota,OH:Ohio,OK:Oklahoma,OR:Oregon,MD:Maryland," \
                           "MA:Massachusetts,MI:Michigan,MN:Minnesota,MS:Mississippi,MO:Missouri," \
                           "PA:Pennsylvania,RI:Rhode Island,SC:South Carolina,SD:South Dakota," \
                           "TN:Tennessee,TX:Texas,UT:Utah,VT:Vermont,VA:Virginia,WA:Washington," \
                           "WV:West Virginia,WI:Wisconsin,WY:Wyoming"


def main():
    if len(sys.argv) < 3:
        print("USAGE : python3 happiest_state_kthapa2.py <sentiment_file> <tweet_file> > happiest_state_[yourNetID].txt")
        print("Program will exit now...")
        sys.exit(1)

    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    fill_state_abbreviation_map()
    read_sentiment_file(sent_file)
    tweet_string = read_file(tweet_file)
    process_all_tweets(tweet_string)
    calculate_average_sentiment_score_for_each_state()
    happiest_tweets = ((key, state_average_sentiment_score_map[key]) for key in
                       sorted(state_average_sentiment_score_map, key=state_average_sentiment_score_map.get,
                              reverse=True))
    for state, sentiment_score in happiest_tweets:
        print("[" + "%.6f" % float(sentiment_score) + "] : [" + str(state) + "]")


def read_sentiment_file(sent_file_name):
    sentiment_file_text_data = read_file(sent_file_name)
    sentiment_list = sentiment_file_text_data.split("\n")
    for sentiment_data in sentiment_list:
        term_score = sentiment_data.split("\t")
        static_sentiment_score_map[term_score[0]] = float(term_score[1])
        # print(term_score[0] + " | " + term_score[1])


def calculate_sentiment_score_for_single_tweet(single_tweet):
    single_tweet_text_list = single_tweet.split()
    tweet_sentiment_score = 0
    for single_word in single_tweet_text_list:
        tweet_sentiment_score += static_sentiment_score_map.get(single_word, 0)

    return tweet_sentiment_score


def process_all_tweets(tweet_string):
    tweet_list = tweet_string.split("\n")
    for tweet_data in tweet_list:
        if tweet_data:
            try:
                tweet_json_data = json.loads(tweet_data)
                find_state_from_tweet_json(tweet_json_data)
            except JSONDecodeError:
                print("JSON Decode Error")


def find_state_from_tweet_json(tweet_json_data):
    tweet_text_part = tweet_json_data["text"]
    tweet_sentiment_score = calculate_sentiment_score_for_single_tweet(tweet_text_part)
    tweet_places_data = tweet_json_data["place"]
    if tweet_places_data is not None and tweet_places_data["country_code"] == COUNTRY_CODE:
        state_name = None
        full_name_array_data = tweet_places_data["full_name"].split(",")
        if tweet_places_data["place_type"] == PLACE_CITY:
            state_name = full_name_array_data[-1].strip(" \n\r\t")
            # print("[" + state_name + "]")
        elif tweet_places_data["place_type"] == PLACE_ADMIN:
            # print("[" + full_name_array_data[0].strip(" \n\t\r").lower() + "]")
            state_name = state_abbreviation_map[full_name_array_data[0].strip(" \n\t\r")]

        if state_name is not None:
            state_sentiment_score_map[state_name] = state_sentiment_score_map.get(state_name, 0) + tweet_sentiment_score
            state_sentiment_tweet_count[state_name] = state_sentiment_tweet_count.get(state_name, 0) + 1


def fill_state_abbreviation_map():
    state_abbreviations = state_abbreviations_text.split(",")
    for state_abbreviation_mapping in state_abbreviations:
        state_abbreviation_mapping_list = state_abbreviation_mapping.split(":")
        state_short_name = state_abbreviation_mapping_list[0].strip(" \n\t\r")
        state_full_name = state_abbreviation_mapping_list[1].strip(" \n\t\r")
        state_abbreviation_map[state_full_name] = state_short_name

        # for state_full_name in state_abbreviation_map:
        #     print("[" + state_full_name + "] -> [" + state_abbreviation_map[state_full_name] + "]")


def calculate_average_sentiment_score_for_each_state():
    for state_name in state_sentiment_score_map:
        state_average_sentiment_score_map[state_name] = float(
            state_sentiment_score_map[state_name] / state_sentiment_tweet_count[state_name])


def read_file(filename):
    f = open(filename, "rU")
    text = f.read()
    f.close()
    return text


if __name__ == '__main__':
    main()
