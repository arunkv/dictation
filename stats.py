# Description: Stats tracking for the dictation game

#    Copyright 2024 Arun K Viswanathan
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0

import logging
import os
import pickle
from pathlib import Path

STATS_FILE = Path(__file__).parent / 'cache/stats.pkl'  # Local file to store the game statistics


def load_stats(words):
    # Set up stats tracking
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'rb') as file:
            stats = pickle.load(file)
            logging.debug(f"Loaded stats: {stats}")
    else:
        stats = {}

    # Initialize the stats for the words
    for word in words:
        stats[word] = stats.get(word, 1)
    return stats


def save_stats(stats):
    with open(STATS_FILE, 'wb') as f:
        logging.debug(f"Saved stats: {stats}")
        pickle.dump(stats, f)
