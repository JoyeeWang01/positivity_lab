"""
Stop and think: words with which prefix should you remove from tweets?
#, @?
"""
import re #regular expressions module

# Define abbreviations
# as regular expressions together with their expansions
# (\b marks the word boundary):
re_repl = {
    r"\br\b": "are",
    r"\bu\b": "you",
    r"\bhaha\b": "ha",
    r"\bhahaha\b": "ha",
    r"\bdon't\b": "do not",
    r"\bdoesn't\b": "does not",
    r"\bdidn't\b": "did not",
    r"\bhasn't\b": "has not",
    r"\bhaven't\b": "have not",
    r"\bhadn't\b": "had not",
    r"\bwon't\b": "will not",
    r"\bwouldn't\b": "would not",
    r"\bcan't\b": "can not",
    r"\bcannot\b": "can not"
}

emo_repl = {
    # positive emoticons
    "&lt;3": " good ",
    ":d": " good ",  # :D in lower case
    ":dd": " good ", # :DD in lower case
    "8)": " good ",
    ":-)": " good ",
    ":)": " good ",
    ";)": " good ",
    "(-:": " good ",
    "(:": " good ",
    # negative emoticons:
    ":/": " bad ",
    ":&gt;": " sad ",
    ":')": " sad ",
    ":-(": " bad ",
    ":(": " bad ",
    ":S": " bad ",
    ":-S": " bad ",
}

# make sure that e.g. :dd is replaced before :d
emo_repl_order = [k for (k_len,k) in
                  reversed(sorted([(len(k),k) for k in emo_repl.keys()]))]


def clean_tweet(tweet, emo_repl_order, emo_repl, re_repl ):
    tweet = tweet.lower()
    for k in emo_repl_order:
        tweet = tweet.replace(k, emo_repl[k])

    for r, repl in re_repl.items():
        tweet = re.sub(r, repl, tweet)

    return tweet
