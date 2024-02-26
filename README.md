# Dictation Game

Simple game that helps children practice dictaion.
* Uses either OpenAI's TTS API or Google's TTS API to generate audio for the words. 
* [The Sound of Learning: Using OpenAI’s Text-to-Speech API for a Simple Dictation Game for Kids](https://arunkv.medium.com/the-sound-of-learning-using-openais-text-to-speech-api-for-a-simple-dictation-game-for-kids-e237db497ad1)

## Required Packages
* `pygame` (https://www.pygame.org/)
* `pyyaml` (https://pyyaml.org/)
* `termcolor` (https://pypi.org/project/termcolor/)
* `openai` (https://pypi.org/project/openai/)
* `google-cloud-texttospeech` (https://pypi.org/project/google-cloud-texttospeech/)

## APIs
To use OpenAI's TTS:
* OpenAI's TTS-API (https://platform.openai.com/docs/guides/text-to-speech)
* Needs valid OpenAPI API key set as `OPENAI_API_KEY` environment variable (https://platform.openai.com/api-keys)

To use Google's TTS::
* Google's TTS-API (https://cloud.google.com/text-to-speech/docs)
* Enable Cloud Text-to-Speech API (https://console.cloud.google.com/flows/enableapi?apiid=texttospeech.googleapis.com)
* Authenticate via `gcloud auth application-default login`