# Description: A simple dictation game that uses OpenAI's text to speech API to generate speech for the words

#    Copyright 2024 Arun K Viswanathan
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0

import logging
import os
import random
import time
from pathlib import Path

import pygame
import yaml
from openai import OpenAI
from termcolor import colored

WORDS_FILE = 'words.yaml'
SPEECH_DIR = Path(__file__).parent / 'speech/'
logging.basicConfig(filename='dictation.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def convert_to_lowercase(array):
    return [item.lower() for item in array]


# Load the words from the yaml file
def load_config_from_yaml(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        return config


def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.Sound(file_path).play()
    time.sleep(1)
    pygame.mixer.Sound(file_path).play()


def speech_file_for_word(input_word, ai_voice):
    return SPEECH_DIR / f"{input_word}-{ai_voice}.mp3"


# Convert the words into speech using OpenAI's text to speech API
# Needs the OPENAI_API_KEY environment variable to be set
def generate_speech(spoken_words, ai_voice='alloy'):
    client = OpenAI()
    os.makedirs(SPEECH_DIR, exist_ok=True)
    for spoken_word in spoken_words:
        speech_file = speech_file_for_word(spoken_word, ai_voice)
        if not os.path.isfile(speech_file):
            with client.audio.speech.with_streaming_response.create(
                    model="tts-1-hd",
                    voice=ai_voice,
                    input=spoken_word
            ) as response:
                response.stream_to_file(speech_file_path)
                logging.info(f"{spoken_word}-{ai_voice}.mp3 generated successfully!")
        else:
            logging.warning(f"{spoken_word}-{ai_voice}.mp3 already exists")


# Load the game configuration
data = load_config_from_yaml(WORDS_FILE)
word_section = data['config']['default']
max_words = int(data['config']['max_words'])
max_attempts = int(data['config']['max_attempts'])
words = data[word_section]
openai_voice = data['config']['openai_voice']

# Select the words for the game
dictation_words = convert_to_lowercase(words)
dictation_words = random.sample(dictation_words, min(max_words, len(dictation_words)))
logging.info(dictation_words)

# Convert the words into speech
generate_speech(dictation_words, openai_voice)

# Play the dictation game
pygame.init()
score = 0

for word in dictation_words:
    logging.info(f"The word is {word}")
    print(f"Write down the word you hear: ", end="")
    speech_file_path = speech_file_for_word(word, openai_voice)
    tries = 0
    while True:
        play_mp3(speech_file_path)
        user_input = input()
        if user_input.lower() == word:
            score += 1
            print(colored("Correct!", 'green'))
            break
        else:
            tries += 1
            if tries == max_attempts:
                print(colored(f"Sorry, the word was {word}"), 'red')
                break
            else:
                print(colored("Try again: ", 'yellow'), end="")

print(colored(f"Your score is {score}/{len(dictation_words)}", 'green'))
