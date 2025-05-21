import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import string
hashtags = []
stop_words = set(stopwords.words('english'))

user_input = input("Enter a text: ")
user_inputs = user_input.lower().split()
for word in user_inputs:
    if word not in stop_words and (len(word) >= 4 and not word.startswith("#")):
     hashtags.append("#" + word.strip(string.punctuation))
    

# set_hastags = set(hashtags)
# for words in set_hastags:
#    user_input += (" #" + words)
print(user_input+str(hashtags))

    