# Description: Factory class that creates a text-to-speech (TTS) client and generates speech for the words

#    Copyright 2024 Arun K Viswanathan
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0


import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path

from openai import OpenAI

SPEECH_DIR = Path(__file__).parent / 'speech/'
logging.basicConfig(filename='tts.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class TTSFactory(ABC):
    @abstractmethod
    def create_tts(self):
        pass

    @abstractmethod
    def get_speech_file(self, input_word: str, ai_options: dict) -> Path:
        pass


class OpenAITTSFactory(TTSFactory):
    DEFAULT_MODEL = "tts-1"
    DEFAULT_VOICE = 'alloy'

    name: str = None
    client: OpenAI = None

    def create_tts(self):
        self.name = "OpenAI"
        self.client = OpenAI()

    # Convert the word into speech using OpenAI's text to speech API
    # Needs the OPENAI_API_KEY environment variable to be set
    def get_speech_file(self, input_word: str, ai_options: dict) -> Path:
        ai_model = ai_options.get('model', self.DEFAULT_MODEL)
        ai_voice = ai_options.get('voice', self.DEFAULT_VOICE)
        speech_dir: Path = SPEECH_DIR / f"{self.name}"
        os.makedirs(speech_dir, exist_ok=True)
        speech_file: Path = speech_dir / f"{input_word}-{ai_voice}.mp3"
        logging.info(f"Speech file for {input_word} is {speech_file}")
        if not os.path.isfile(speech_file):
            with self.client.audio.speech.with_streaming_response.create(
                    model=ai_model,
                    voice=ai_voice,
                    input=input_word
            ) as response:
                response.stream_to_file(speech_file)
                logging.info(f"{speech_file} generated successfully!")
        else:
            logging.warning(f"{speech_file} already exists")
        return speech_file
