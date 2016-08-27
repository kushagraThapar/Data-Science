import sys
import json
from json.decoder import JSONDecodeError

words_map = {}
words_frequency_map = {}
stop_words_set = set()
total_words = 0


def main():
    if len(sys.argv) < 3:
        print("USAGE : python3 frequency_kthapa2.py <stopword_file> <tweet_file> > term_freq_[yourNetID].txt")
        print("Program will exit now...")
        sys.exit(1)

    stopword_file = sys.argv[1]
    tweet_file = sys.argv[2]
    stopword_text = read_file(stopword_file)
    fill_stopword_set(stopword_text)
    tweet_string = read_file_bytes(tweet_file)
    fill_words_map(tweet_string)
    fill_words_frequency_map()


def fill_words_frequency_map():
    # Sort the words map according to the number of occurrences of each word.
    sorted_words_map = ((key, words_map[key]) for key in sorted(words_map, key=words_map.get, reverse=True))
    print("Total Words [" + str(total_words) + "]")
    for single_word, count in sorted_words_map:
        words_frequency_map[single_word] = float(count / total_words)
        # print(single_word + " " + "%.8f" % words_frequency_map[single_word])
        print("[ " + single_word + " ], [ " + str(count) + " ], [ " + "%.8f" % words_frequency_map[single_word] + " ]")


def fill_words_map(tweet_string):
    tweet_list = tweet_string.split("\n")
    combined_tweet_text = ""
    for tweet_data in tweet_list:
        if tweet_data:
            try:
                tweet_json_data = json.loads(tweet_data)
                tweet_text_part = tweet_json_data["text"]
                combined_tweet_text += tweet_text_part + " "
            except JSONDecodeError:
                print("JSON Decode Error")

    split_and_fill_tweet_text(combined_tweet_text)


def split_and_fill_tweet_text(combined_tweet_text):
    tweet_text_words = combined_tweet_text.split()
    for single_word in tweet_text_words:
        single_word = single_word.lower()
        if single_word not in stop_words_set:
            global total_words
            total_words += 1
            if single_word not in words_map:
                words_map[single_word] = 1
            else:
                words_map[single_word] += 1
                # else:
                #   It is a stop word, so skip it.


def fill_stopword_set(stopword_text):
    stopwords_list = stopword_text.split("\n")
    for stopword in stopwords_list:
        stop_words_set.add(stopword)


def read_file(filename):
    f = open(filename, "rU")
    text = f.read()
    f.close()
    return text


def read_file_bytes(filename):
    f = open(filename, "rU")
    text = f.read()
    # print(text)
    f.close()
    return text


if __name__ == '__main__':
    main()
