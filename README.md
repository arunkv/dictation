# Dictation Game

**Dictation game for kids to practice their spelling.**

* Uses either OpenAI's TTS API or Google's TTS API to generate audio for the words. 
* [The Sound of Learning: Using OpenAI’s Text-to-Speech API for a Simple Dictation Game for Kids](https://arunkv.medium.com/the-sound-of-learning-using-openais-text-to-speech-api-for-a-simple-dictation-game-for-kids-e237db497ad1)

## Required Packages
* `pygame` (https://www.pygame.org/)
* `pyyaml` (https://pyyaml.org/)
* `termcolor` (https://pypi.org/project/termcolor/)
* `colorama` (https://pypi.org/project/colorama/)
* `openai` (https://pypi.org/project/openai/)
* `google-cloud-texttospeech` (https://pypi.org/project/google-cloud-texttospeech/)

## Usage
* `python dictation_game.py [--grade {grade1|grade3}]`
* Use grades as named in `words.yaml` configuration file
* To use OpenAI's Text-to-Speech:
  * OpenAI's TTS API (https://platform.openai.com/docs/guides/text-to-speech)
  * Needs valid OpenAPI API key set as `OPENAI_API_KEY` environment variable (https://platform.openai.com/api-keys)
* To use Google's Text-to-Speech::
  * Google's TTS API (https://cloud.google.com/text-to-speech/docs)
  * Enable Cloud Text-to-Speech API (https://console.cloud.google.com/flows/enableapi?apiid=texttospeech.googleapis.com)
  * Authenticate via `gcloud auth application-default login`

## Attributions
* Uses [`Jingle_Win_Synth_06.wav`](https://freesound.org/people/LittleRobotSoundFactory/sounds/274181/) from `LittleRobotSoundFactory` under CC BY 4.0 DEED Attribution 4.0 International license