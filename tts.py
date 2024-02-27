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

from google.cloud import texttospeech
from openai import OpenAI

SPEECH_DIR = Path(__file__).parent / 'speech/'

class TTSFactory(ABC):
    @staticmethod
    def get_tts(name: str):
        if name == "openai":
            return OpenAITTSFactory()
        elif name == "google":
            return GoogleTTSFactory()
        else:
            return None

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
        self.name = "openai"
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


class GoogleTTSFactory(TTSFactory):
    DEFAULT_GENDER = 'neutral'

    name: str = None
    client: texttospeech.TextToSpeechClient = None
    audio_config: texttospeech.AudioConfig = None

    def create_tts(self):
        self.name = "google"
        self.client = texttospeech.TextToSpeechClient()
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    # Convert the word into speech using Google's text to speech API
    # Needs Cloud Text-to-Speech API to be enabled
    # Authentication to be set up by running `gcloud auth application-default login`

    def get_speech_file(self, input_word: str, ai_options: dict) -> Path:
        ai_gender_name = ai_options.get('gender', self.DEFAULT_GENDER).lower()
        ai_gender = {
            'male': texttospeech.SsmlVoiceGender.MALE,
            'female': texttospeech.SsmlVoiceGender.FEMALE,
            'neutral': texttospeech.SsmlVoiceGender.NEUTRAL,
        }.get(ai_gender_name, texttospeech.SsmlVoiceGender.NEUTRAL)
        speech_dir: Path = SPEECH_DIR / f"{self.name}"
        os.makedirs(speech_dir, exist_ok=True)
        speech_file: Path = speech_dir / f"{input_word}-{ai_gender_name}.mp3"
        if not os.path.isfile(speech_file):
            synthesis_input = texttospeech.SynthesisInput(text=input_word)
            voice = texttospeech.VoiceSelectionParams(
                language_code='en-US',
                ssml_gender=ai_gender,
            )
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=self.audio_config
            )
            with open(speech_file, 'wb') as out:
                out.write(response.audio_content)
        return speech_file

