"""
Code from: https://colab.research.google.com/github/tensorflow/tensorflow/blob/master/tensorflow/lite/g3doc/convert/metadata_writer_tutorial.ipynb

This script writes metadata to a converted tensorflow lite model.
The metadata is used in the Android app.
Without metadata, the model cannot be imported properly in the front end
For more information check: https://www.tensorflow.org/lite/convert/metadata
"""
from tflite_support.metadata_writers import audio_classifier
from tflite_support.metadata_writers import writer_utils

from Constants import SAMPLE_RATE

AudioClassifierWriter = audio_classifier.MetadataWriter
MODEL_PATH = "model/spectrogram2/converted/model_spec.tflite"
# Task Library expects label files that are in the same format as the one below.
LABEL_FILE = "labels.txt"
# Expected number of channels of the input audio buffer. Note, Task library only
# support single channel so far.
CHANNELS = 1
SAVE_TO_PATH = "model/spectrogram2/converted/model_spec_metadata.tflite"

# Create the metadata writer.
writer = AudioClassifierWriter.create_for_inference(
    writer_utils.load_file(MODEL_PATH), SAMPLE_RATE, CHANNELS, [LABEL_FILE])

# Verify the metadata generated by metadata writer.
print(writer.get_metadata_json())

# Populate the metadata into the model.
writer_utils.save_file(writer.populate(), SAVE_TO_PATH)
