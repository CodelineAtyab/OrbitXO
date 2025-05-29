import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

message = input("Enter a message: ")
hashtags = []
for word in message.lower().split():
 if len(word) > 3 and (word not in stop_words and not word.startswith('#')):
  word = word.strip(string.punctuation)
  if word.isalnum():
   hashtags.append(word)

sethashtags = set(hashtags)

for i in sethashtags:
    message = message + (" #" + i)
print(message)
