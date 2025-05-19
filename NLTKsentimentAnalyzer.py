import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
SIA = SentimentIntensityAnalyzer()

reviewsList = ["I love this product! It's amazing.", "Bad bananas. Expensive no frills.", "I received a chair on time. It was mid, kinda floppy."]

for i in reviewsList:
    sentiment_score = SIA.polarity_scores(i)
    print(sentiment_score)
