import csv
from twitter_specials import *
from math import *
import string

word_counts_dict = {} # "word": [positive, negative, neutral, irrelevant, total counts]
category_to_num = {"positive": 0, "negative":1, "neutral":2, "irrelevant": 3}
num_to_category = {0: "positive", 1: "negative", 2: "neutral", 3: "irrelevant"}
total_entries = [0, 0, 0, 0, 0] #[positive, negative, neutral, irrelevant, total counts]

exclude = set(string.punctuation)
def split_words(string):
    split = string.split()
    output = []
    for w in split:
        if '#' not in w and '@' not in w:
            str = ""
            for ch in w:
                if (ch not in exclude):
                    str += ch
            output += [str]
    return output


def preprocessing():
    count = 0
    last_tweet = ''
    with open("labeled_corpus.tsv", encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter='\t')
        for row in readCSV:
            line_arr = list(row)

            tweet = line_arr[0]
            category = str(line_arr[1])

            if (category not in category_to_num):
                last_tweet = last_tweet + " " + tweet + " " + category
                continue

            if (last_tweet != ''):
                tweet = last_tweet + " " + tweet
                last_tweet = ''

            tweet = clean_tweet(tweet, emo_repl_order, emo_repl, re_repl)

            words = split_words(tweet)
            word_set = set()
            for w in words:
                if '#' not in w and '@' not in w:
                    word_set.add(w)

            total_entries[-1] += 1
            total_entries[category_to_num[category]] += 1
            for w in word_set:
                if w not in word_counts_dict:
                    word_counts_dict[w] = [0, 0, 0, 0, 0]
                word_counts_dict[w][-1] += 1 #total count +1
                word_counts_dict[w][category_to_num[category]] += 1 #categorical count +1

    csvfile.close()


probabilities_dict = {} #[positive, negative, neutral, irrelevant]
def probabilities():
    for w, counts in word_counts_dict.items():
        probabilities_dict[w] = [counts[0]/total_entries[0], counts[1]/total_entries[1], counts[2]/total_entries[2], counts[3]/total_entries[3]] #conditional probability for each word
    for i in range(4):
        probabilities_dict[i] = log(total_entries[i]/total_entries[-1]) #prior probabilities with log

result = []
def classifier():
    file_object = open('locations_classified.tsv', 'w', newline='')
    writeTSV = csv.writer(file_object, delimiter='\t')
    with open("geo_twits_squares.tsv", encoding="utf-8") as tsvfile:
        readTSV = csv.reader((line.replace('\0','') for line in tsvfile), delimiter='\t')
        for row in readTSV:
            line_arr = list(row)
            latitude = line_arr[0]
            longitude = line_arr[1]
            tweet = line_arr[2]
            tweet = clean_tweet(tweet, emo_repl_order, emo_repl, re_repl)

            words = split_words(tweet)
            word_set = set()
            for w in words:
                if '#' not in w and '@' not in w:
                    word_set.add(w)

            posterior = [probabilities_dict[0], probabilities_dict[1], probabilities_dict[2], probabilities_dict[3]]

            for w in word_set:
                for i in range(4):
                    try:
                        probabilities_dict[w]
                    except:
                        continue
                    if (probabilities_dict[w][i] != 0):
                        posterior[i] += log(probabilities_dict[w][i])

            m = max(posterior)
            classified = [i for i, j in enumerate(posterior) if j == m]
            writeTSV.writerow([latitude, longitude, num_to_category[classified[0]]])
            #result.append([latitude, longitude, classified[0]])
    file_object.close()
    tsvfile.close()

location_counts_dict = {}
def positivity_score():
    file_object = open('positivity_score.tsv', 'w', newline='')
    writeTSV = csv.writer(file_object, delimiter='\t')
    with open("locations_classified.tsv", encoding="utf-8") as tsvfile:
        readTSV = csv.reader((line.replace('\0','') for line in tsvfile), delimiter='\t')
        for row in readTSV:
            line_arr = list(row)
            latitude = line_arr[0]
            longitude = line_arr[1]
            category = line_arr[2]

            if (latitude, longitude) not in location_counts_dict:
                location_counts_dict[(latitude, longitude)] = [0, 0, 0, 0]
            location_counts_dict[(latitude, longitude)][category_to_num[category]] += 1

    for (location, count) in location_counts_dict.items():
        total = count[0]+count[1]+count[2]+count[3]
        score = (count[0]/total-count[1]/total+1)/2
        writeTSV.writerow([location[0], location[1], score])

    file_object.close()
    tsvfile.close()


def location_data():
    first_line = True
    file_object = open('./public_html/data.js', 'w', newline='')
    file_object.write("var data = [")
    with open("positivity_score.tsv", encoding="utf-8") as tsvfile:
        readTSV = csv.reader((line.replace('\0','') for line in tsvfile), delimiter='\t')
        for row in readTSV:
            line_arr = list(row)
            line_arr[0] = str(float(line_arr[0])+0.05/2)
            line_arr[1] = str(float(line_arr[1])+0.05/2)
            if first_line:
                file_object.write('{"score": ' + line_arr[2] + ', "g": ' + line_arr[1] + ', "t": ' + line_arr[0] + '}')
                first_line = False
            else:
                file_object.write(', {"score": ' + line_arr[2] + ', "g": ' + line_arr[1] + ', "t": ' + line_arr[0] + '}')
    tsvfile.close()
    file_object.write('];')
    file_object.close()

preprocessing() #count tweets in training data
probabilities() #calculate probabilities
classifier() #classify and write locations_classified.tsv
positivity_score() #calculate positivity scores and write positivity_score.tsv
location_data() #write data.js
