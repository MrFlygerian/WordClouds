# Twitter management
import tweepy, random
from tweepy import OAuthHandler

# Word processing
import nltk
from nltk.corpus import stopwords
from string import punctuation
import re
from nltk.tokenize import word_tokenize

nltk.download('stopwords')

# Visuals
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# Counting and collecting words
import collections

# Initialise stopwords
_punctuation = list(punctuation) + ["``", "'s", "'", ".", '"', "n't", ]
extrawords = [w for w in STOPWORDS if w not in stopwords.words('english')]
_stopwords = set(stopwords.words('english') + _punctuation + extrawords + ['rt', 'co', 'https'])


# -------------------------------------------------------------------------------------------------------
# Colour function to greyscale wordcloud
def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)


# Preprocess tweets
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
            if word not in _stopwords:
                word_soup.append(word)  # append each word in each tweet to new word set

        i += 1
    return word_soup


# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
# Define credentials to authenticate (credentials will need to be changed for other users)
consumer_key = '8i68MvUnFgp3Mqh5jRV34jGh3'
consumer_secret = 'jNPsW7ZKZkKoVLAvFjwgTPHvlw4Hto8jbpnCDcbnnSUm7O8RJX'
access_token_key = '2378518193-5lkOIoa6OJpm3X0AehYz9EAjws6NjSsjHZS93MM'
access_token_secret = 'DN6j3LxuKWtkKJkGpU16pUr2wqSFYoUs6FwED1SXFjpAw'

# Pass credentials through to be authenticated
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

# Define access api
api = tweepy.API(auth)

# Get tweets
tweets = []
for status in api.user_timeline()[:]:
    tweets.append(api.get_status(status.id).text)

# Process tweets for use in WordCloud
wordsoup = processTweets(tweets)
tag_words = nltk.pos_tag(wordsoup)
nouns = []
for word in tag_words:  # Extra bit to extract the most useful word type from the word soup, which is noun
    if word[1] == 'NNS' or word[1] == 'NN':
        nouns.append(word[0])

all_tweets = ' '.join(nouns)

# Generate WordCloud
wordcloud = WordCloud(font_path='GatsbyFLF-BoldItalic.ttf', stopwords=_stopwords, background_color='black', mask=None,
                      max_words=500, width=1800, height=1400).generate(all_tweets)

# Show WordCloud
plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3))
plt.axis('off')
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
colours = cm.viridis(np.linspace(0, 1, 10))
plt.title('Top words from the TL vs their count')
plt.xlabel('Count')
plt.ylabel('Words')
plt.barh(words, counts, color=colours)
plt.show()
