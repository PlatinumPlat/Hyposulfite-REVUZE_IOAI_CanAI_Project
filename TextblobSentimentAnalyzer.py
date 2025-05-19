from textblob import TextBlob

reviewsList = ["I love this product! It's amazing.", "Bad bananas. Expensive no frills.", "I received a chair on time. It was mid, kinda floppy."]

for i in reviewsList:
    blob = TextBlob(i)
    sentiment = blob.sentiment
    print(sentiment)