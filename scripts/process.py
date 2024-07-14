import json
import nltk
import pymorphy2
import re
import sys

from nltk.tokenize import word_tokenize

nltk.download('punkt')

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"
                           u"\U0001F300-\U0001F5FF"
                           u"\U0001F680-\U0001F6FF"
                           u"\U0001F1E0-\U0001F1FF"
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def preprocess(text):
    text = text.replace("\n\n", ' ')
    text = text.replace("\n", ' ')
    text = remove_emoji(text)
    split = text.split()
    filtered = [part if '/' not in part else '' for part in split]
    text = ' '.join(filtered).lower()
    return text

nltk.download('punkt')

def process(text):
    morph = pymorphy2.MorphAnalyzer()
    processed_tokens = []
    for token in word_tokenize(text):
        parsed_token = morph.parse(token)[0]
        processed_tokens.append({'token': token, 'normal_form': parsed_token.normal_form, 'speech_part': parsed_token.tag.POS, 'case': parsed_token.tag.case, 'number': parsed_token.tag.number,
                            'gender': parsed_token.tag.gender, 'tense': parsed_token.tag.tense})
    return processed_tokens

with open(sys.argv[1]) as input:
    with open('processed.json', 'w+', encoding='utf-8') as output:        
        i = 0
        content = json.load(input)
        for row in content:
            row['processed'] = process(row['text'])
            if i%100 == 0:
                print(i)
            i+=1
        json.dump(content, output, ensure_ascii=False, indent=4)            