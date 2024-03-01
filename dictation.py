# Description: A simple dictation game that uses OpenAI's text to speech API to generate speech for the words

#    Copyright 2024 Arun K Viswanathan
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0

import argparse
import logging
import nltk
import os
import pickle
import random
import time
from pathlib import Path

import yaml
from colorama import Fore, init as colorama_init
from pygame import init as pygame_init, mixer as pygame_mixer, error as pygame_error
from termcolor import colored

from tts import TTSFactory

CONFIG_FILE = 'words.yaml'
CACHE_DIR = Path(__file__).parent / 'cache'
STATS_FILE = CACHE_DIR / 'stats.pkl'  # Local file to store the game statistics
SPEECH_DIR = CACHE_DIR / 'speech/'
WIN_SOUND_FILE = Path(__file__).parent / 'sounds/win.wav'
logging.basicConfig(filename='dictation.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Load the configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        return config


# Play a sound file.
# If times > 1, the sound is played multiple times with a 1-second delay
def play_sound_file(file_path, times=1):
    pygame_mixer.init()
    while times > 0:
        pygame_mixer.Sound(file_path).play()
        times = times - 1
        if times > 0:
            time.sleep(1)
        else:
            time.sleep(0.25)


def get_words_for_grade(data, grade_override):
    grade = grade_override or data['config']['grade']
    if grade is None or grade == 'nltk':
        try:
            words = nltk.corpus.words.words()
        except LookupError:
            nltk.download('words')
            logging.info("Downloading NLTK words corpus")
            words = nltk.corpus.words.words()
            logging.info(f"NLTK words corpus downloaded with {len(words)} words")
    else:
        words = list(set(data[grade]))  # Remove duplicates
    return words


def dictation_game(grade_override=None):
    # Load the game configuration
    data = load_config(CONFIG_FILE)
    words = get_words_for_grade(data, grade_override)
    max_words = int(data['config']['max_words'])
    max_attempts = int(data['config']['max_attempts'])
    ai = data['config']['ai']
    ai_options = data.get(ai, {})

    # Initialize the TTS engine
    factory = TTSFactory.get_tts(name=ai)
    factory.create_tts()

    # Initialize Pygame
    pygame_init()

    # Initialize colorama
    colorama_init()

    # Set up stats tracking
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'rb') as file:
            stats = pickle.load(file)
            logging.debug(f"Loaded stats: {stats}")
    else:
        stats = {}
    for word in words:
        stats[word] = stats.get(word, 1)

    # Select the words for the game
    dictation_words = [item.lower() for item in words]
    random.seed(time.time())
    word_weights = [1 / (stats.get(word, 1)) for word in dictation_words]
    dictation_words = random.choices(dictation_words, weights=word_weights, k=min(max_words, len(dictation_words)))
    logging.info(dictation_words)

    # Play the dictation game
    score = 0
    try:
        for word in dictation_words:
            logging.info(f"The word is {word}")

            print(f"Write down the word you hear: ", end="")
            speech_file_path = factory.get_speech_file(word, ai_options)
            tries = 0
            while True:
                # Play the word and track as used
                try:
                    stats[word] = stats.get(word, 0) + 1
                    play_sound_file(speech_file_path, 2)
                except pygame_error as e:
                    logging.error(f"Error playing {speech_file_path}: {e}")
                    os.system(f"say {word}")

                # Get user input and compare
                user_input = input(Fore.CYAN).strip().lower()
                print(Fore.RESET, end="")
                if user_input.lower() == word:
                    score += 1
                    play_sound_file(WIN_SOUND_FILE)
                    print(colored("Correct!", 'green'))
                    break
                else:
                    tries += 1
                    # Decrease the word's usage so that it is played more often
                    stats[word] = max(1, stats.get(word, 0) - 1)
                    if tries == max_attempts:
                        print(colored(f"Sorry, the word was {word}", 'red'))
                        break
                    else:
                        print(colored("Try again: ", 'yellow'), end="")
        with open(STATS_FILE, 'wb') as f:
            logging.debug(f"Saved stats: {stats}")
            pickle.dump(stats, f)
    except KeyboardInterrupt:
        with open(STATS_FILE, 'wb') as f:
            logging.debug(f"Saved stats (interrupted): {stats}")
            pickle.dump(stats, f)

    print(colored(f"\nYour score is {score}/{len(dictation_words)}", 'green'))


def main():
    parser = argparse.ArgumentParser(description="Dictation game.")
    parser.add_argument("--grade", help="The grade for the dictation game")
    args = parser.parse_args()
    dictation_game(args.grade)
    logging.shutdown()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
