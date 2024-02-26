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

import yaml
from colorama import Fore, init as colorama_init
from termcolor import colored

from tts import TTSFactory

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import init as pygame_init, mixer as pygame_mixer

CONFIG_FILE = 'words.yaml'
SPEECH_DIR = Path(__file__).parent / 'speech/'
logging.basicConfig(filename='dictation.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def convert_to_lowercase(array):
    return [item.lower() for item in array]


# Load the configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        return config


# Play an MP3 file twice with a 1-second delay
def play_mp3(file_path):
    pygame_mixer.init()
    pygame_mixer.Sound(file_path).play()
    time.sleep(1)
    pygame_mixer.Sound(file_path).play()


def main():
    # Load the game configuration
    data = load_config(CONFIG_FILE)
    grade = data['config']['grade']
    max_words = int(data['config']['max_words'])
    max_attempts = int(data['config']['max_attempts'])
    words = data[grade]

    ai = data['config']['ai']
    ai_options = data.get(ai, {})

    # Select the words for the game
    dictation_words = convert_to_lowercase(words)
    random.seed(time.time())
    dictation_words = random.sample(dictation_words, min(max_words, len(dictation_words)))
    logging.info(dictation_words)

    # Play the dictation game
    factory = TTSFactory.get_tts(name=ai)
    factory.create_tts()

    # Initialize Pygame
    pygame_init()

    colorama_init()
    score = 0

    for word in dictation_words:
        logging.info(f"The word is {word}")
        print(f"Write down the word you hear: ", end="")
        speech_file_path = factory.get_speech_file(word, ai_options)
        tries = 0
        while True:
            try:
                play_mp3(speech_file_path)
            except Exception:
                os.system(f"say {word}")
            user_input = input(Fore.CYAN)
            print(Fore.RESET, end="")
            if user_input.lower() == word:
                score += 1
                print(colored("Correct!", 'green'))
                break
            else:
                tries += 1
                if tries == max_attempts:
                    print(colored(f"Sorry, the word was {word}", 'red'))
                    break
                else:
                    print(colored("Try again: ", 'yellow'), end="")

    print(colored(f"Your score is {score}/{len(dictation_words)}", 'green'))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
