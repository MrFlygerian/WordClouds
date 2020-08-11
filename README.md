# Twitter and WordClouds
 Creating word clouds with the twitter and tweepy API


This is a showcase of how one can create a word cloud with using pseudo-live data in the form of tweets. A bar chart is displayed to add some numerical context to the word cloud. Since this isn't really analytical as oppose to a functionality showcase, there is no error analysis presented.

Both scripts require the input of verified twitter credentials by the user. The search-term script requires a search term as an extra parameter, which can be anything you would usually put in the twitter search box. You will need to have twitter and tweepy installed in your environment as 2 different methods of authentication are used here (this is done for no reason apart from to explore multiple authentication methods). You will also need the libraries nltk, wordcloud and collections.

These scripts were developed using an article written by Sebastian Raschka (the URL is given below). This article steps through the authentication in good detail and covers the basics of the visuals but does no preprocessing. As such, a preprocessor was created in order to clean the data get better results from the word cloud and bar chart. I refrained from using a mask because I thought it superfluous to my purposes, but this is explained in good detail as well. The use of different fonts was cool, so I have included the fonts I used in this repo.

https://www.techtrek.io/generating-word-cloud-from-twitter-feed-with-python/
