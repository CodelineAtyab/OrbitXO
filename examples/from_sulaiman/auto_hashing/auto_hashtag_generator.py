message_list = input("Enter your text message:\n").lower().strip().split()

stop_words_file = open("examples/from_sulaiman/stop_words_list.txt", "r")
stop_list = stop_words_file.read().split()
stop_words_file.close()

punctuations_file = open("examples/from_sulaiman/punctuations.txt", "r")
punctuations_list = punctuations_file.read().split()
punctuations_file.close()

hashtag_list = []

word_index = 0

while word_index in range(len(message_list)):
    word = message_list[word_index]
    character_index = 0
    while character_index in range(len(word)):
        if word[character_index] in punctuations_list:
            word = word.replace(word[character_index], "")
            character_index -= 1
        character_index += 1
    if word in stop_list or "#" in word:
        message_list.remove(word)
        word_index -= 1
    else:
        hashword = "#" + word
        if len(word) > 3 and word.isalnum() and (hashword) not in hashtag_list:
            hashtag_list.append(hashword)
    word_index += 1

print(" ".join(hashtag_list))

