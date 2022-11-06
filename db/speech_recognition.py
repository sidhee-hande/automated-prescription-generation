import os
import azure.cognitiveservices.speech as speechsdk
from config import SPEECH_KEY, SPEECH_REGION
import time


def recognize_from_microphone(speech_recognizer):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        if speech_recognition_result.text == "":
            stop_cb()

    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(
            speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(
            cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(
                cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")


speech_config = speechsdk.SpeechConfig(
    subscription=SPEECH_KEY, region=SPEECH_REGION)
speech_config.speech_recognition_language = "en-US"

audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config, audio_config=audio_config)

done = False

total_text = []


def save_all_text(evt):
    total_text.append(evt.result.text)
    # print(total_text)


def stop_cb(evt):
    print('CLOSING on {}'.format(evt))

    speech_recognizer.stop_continuous_recognition()
    # nonlocal done
    done = True
    with open('convo.txt', 'w') as f:
        for text in total_text:
            f.write(text+" ")

    # print(total_text)


def recognized_event(evt):
    print('RECOGNIZED: {}'.format(evt))
    if (evt.result.text == "Stop recognizing."):
        stop_cb(evt)


def begin_recognizing():
    speech_recognizer.recognizing.connect(
        lambda evt: print('RECOGNIZING: {}'.format(evt)))

    speech_recognizer.recognized.connect(lambda evt: save_all_text(evt))
    speech_recognizer.recognized.connect(
        lambda evt: recognized_event(evt)

    )
    speech_recognizer.session_started.connect(
        lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(
        lambda: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(
        lambda evt: print('CANCELED {}'.format(evt)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)


# recognize_from_microphone(speech_recognizer)
