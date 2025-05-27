def text_message(message):
    if len(message)<= 280:
        return message
    else:
        return message[:277] + "..."