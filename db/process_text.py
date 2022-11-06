import uuid


def process_text(text):
    text = text
    return {
        'id': "random" + str(uuid.uuid4()),
        'text': text

    }
