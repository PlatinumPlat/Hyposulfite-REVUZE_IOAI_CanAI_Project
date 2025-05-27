from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
sentence = "I buy these crackers every week and this week they’re on for 2 for $5 when the regular price is $1.97, which would make 2 $3.94. I tried to scan one to get the regular price but the original price came as $3.00. Cashier wouldn’t adjust the price even tho it’s clearly printed on the sign."
vs = analyzer.polarity_scores(sentence)
print(vs)
#print(list(vs.values())[3])