import csv
from twitter_specials import *

word_counts_dict = {}
with open("labeled_corpus.tsv", encoding="utf-8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\t')
    for row in readCSV:
        line_arr = list(row)

        tweet = line_arr[0]

        tweet = clean_tweet(tweet, emo_repl_order, emo_repl, re_repl)

        words = tweet.split()
        word_set = set()
        for w in words:
            if '#' not in w and '@' not in w:
                word_set.add(w)

        for w in word_set:
            if w not in word_counts_dict:
                word_counts_dict[w] = 0
            word_counts_dict[w] += 1


# create list of tuples to sort
word_freq_sorted = []
for w,count in word_counts_dict.items():
    if count > 1:
        word_freq_sorted.append((count,w))

word_freq_sorted.sort()
print(word_freq_sorted)

word_freq_sorted.reverse()
print(word_freq_sorted)

print(len(word_freq_sorted))
