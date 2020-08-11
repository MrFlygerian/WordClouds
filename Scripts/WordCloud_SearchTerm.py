# Modules in use now
import twitter

# NLP processing
import nltk
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from string import punctuation
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
import re

# Data visuals
import matplotlib.pyplot as plt
# -----------------------------------------------------

# Collecting words
import collections
# Counting words
import numpy as np
# Load colour map
from matplotlib import cm

# Initialise search term and stop words
search_term = input("Search on Twitter:")
_punctuation = list(punctuation) + ["``", "'s", "'", ".", '"', "n't", ]
extrawords = [w for w in STOPWORDS if w not in stopwords.words('english')]
stop_words = set(
    stopwords.words('english') + ['AT_USER', 'URL', 'rt', search_term.lower(), 'president'] + _punctuation + extrawords)

# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------

# Authenticating Twitter App (credentials will need to be changed other users)
twitter_api = twitter.Api(consumer_key='8i68MvUnFgp3Mqh5jRV34jGh3',
                          consumer_secret='jNPsW7ZKZkKoVLAvFjwgTPHvlw4Hto8jbpnCDcbnnSUm7O8RJX',
                          access_token_key='2378518193-5lkOIoa6OJpm3X0AehYz9EAjws6NjSsjHZS93MM',
                          access_token_secret='DN6j3LxuKWtkKJkGpU16pUr2wqSFYoUs6FwED1SXFjpAw')


# -----------------------------------------------------------------------------------------------------------
# Getting tweets to generate word cloud from
def buildTestSet(search_keyword):
    try:
        tweets_fetched = twitter_api.GetSearch(search_keyword, count=100, lang="en")
        print("Fetched " + str(len(tweets_fetched)) + " tweets for the term " + search_keyword)
        return [status.text for status in tweets_fetched]
    except:
        return None
    pass


# --------------------------------------------------------------------------------------------------------
# Cleaning and vectorising the tweets
def processTweets(DataSet):
    word_soup = []
    i = 0
    while i < len(DataSet):
        tweet = DataSet[i]
        tweet = tweet.lower()  # convert text to lower-case
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)  # remove URLs
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet)  # remove usernames
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)  # remove the # in #hashtag
        tweet = word_tokenize(tweet)  # remove repeated characters (helloooooooo into hello)
        for word in tweet:
            if word not in stop_words:
                word_soup.append(word)  # append each word in each tweet to new word set

        i += 1
    return word_soup


# Get tweets
testDataSet = buildTestSet(search_term)
print(testDataSet[:4])

# Clean the tweets
wordsoup = processTweets(testDataSet)
tag_words = nltk.pos_tag(wordsoup)
nouns = []
for word in tag_words:  # Extra bit to extract the most useful word type from the word soup, which is nouns
    if word[1] == 'NNS' or word[1] == 'NN':
        nouns.append(word[0])

# put all nouns into one string for WordCloud
all_nouns = ' '.join(nouns)

# Generate word cloud
wordcloud = WordCloud(font_path='orange juice 2.0.ttf', stopwords=stop_words, background_color="black", max_words=3000,
                      width=1800, height=1400).generate(all_nouns)

# Show word cloud
plt.figure(figsize=(10, 20))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

# Filter words for use in barchart
counted_words = collections.Counter(nouns)

# Initialise bar chart variables
words = []
counts = []
for letter, count in counted_words.most_common(10):
    words.append(letter)
    counts.append(count)

# Show bar chart
colours = cm.rainbow(np.linspace(0, 1, 10))
plt.title(f'Top words with tweets for {search_term} vs their count')
plt.xlabel('Count')
plt.ylabel('Words')
plt.barh(words, counts, color=colours)
