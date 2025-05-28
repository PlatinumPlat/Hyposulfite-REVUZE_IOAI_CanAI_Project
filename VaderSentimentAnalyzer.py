from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
sentence = """The courts are decent but the lessons are a complete waste of time and money.
I used to take lessons here a few years ago and really enjoyed it but most recently in Spring 2024 I found the lessons to be completely useless. There’s not much coaching but rather just you rallying with other people. The coaches just stand there. In addition one of student was injured by another student during the lesson and the coaches did absolutely nothing about it. Instead they made rude comments towards the person that was hurt.
Furthermore when it rains you are left in the dark about whether the class will be cancelled. They emailed me about cancelling the 3-4pm class at 2:30pm however I was in the 4-5pm class. This left people confused about what is happening.
Overall the lessons are disorganized and just a waste of time. There are better places nearby!"""
vs = analyzer.polarity_scores(sentence)
print(vs)
#print(list(vs.values())[3])