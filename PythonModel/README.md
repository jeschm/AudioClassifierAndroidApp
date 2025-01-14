# Python Backend for Audio Classification
This folder contains the Python backend that was used for the implementation and training of two different neural network models.
The two models are then used in an Android App for audio classification.
For more information about the Android App please check [this link](https://github.com/jeschm/AudioClassifierAndroidApp/tree/main/AndroidApp).

##General Comments
Since the task is to create a model that predicts the class of the last two seconds of audio input from an 
Android device, we use the following parameter in the whole application:
* `SAMPLE_RATE` refers to the sample rate of the audio input and it is 16'000 or 16kHz since this is supported by 
  the microphone on the tested Android device
* `AUDIO_PIECE_LENGTH` refers to the size of one audio input piece and it is 32'000 since we use a frequency of 
  16kHz and a sample length of 2 seconds
* `N_MELS` refers to the number of mels that are used for the creation of the mel spectrograms and it is 128
* Model related parameter such as batch size or number of training epochs are taken directly from the papers

## Installation and Run Instructions
All requirements are stored in the requirements.txt file. 
In order to install them, please run the command `pip install`.

To create the models please run the following scripts and adapt the paths directly in the scripts:

1. `TrainModel.py`
2. `ConvertModelToTFLite.py`
3. `WriteMetadataToModel.py`

After running all three scripts, copy the tensorflow lite model that contains the metadata 
(e.g. `model/melspectrogram/converted/model_mel_metadata.tflite`) to your Android App.

## Script Explanation
This section gives a short introduction to each script.
All scripts can be run without arguments and the parameters can be changed directly in the scripts.

### Constants.py
This file contains all global constants that are used by multiple scripts such as the sample rate of audio samples
or the length of audio pieces used by the model.
In addition, it contains helper methods.
Constants can be changed but must always be the same as in the front end to get meaningful results.

### labels.txt
This file contains all labels that should be predicted by the model.
It is used for the generation of the metadata.
The labels must be ordered according to the folder structure containing the data.
This means, that the first label in this file is the name of the first data folder (e.g. "silence").

### TrainModel.py
This file contains the two models that are trained on the data sets.
Training parameters and the used data can be changed directly in this file.

The first model, a 1D convolutional neuronal network, was taken from [Adboli et al.](https://arxiv.org/abs/1904.08990)
It works with the raw audio input from the .wav files.
The model was trained for 100 epochs and the batch size was 100.
For more information about the model, please check the mentioned paper.

The second model, a 2D convolution neuronal network, was taken from: [Mushtaq et al.](https://doi.org/10.1016/j.apacoust.2020.107581)
It works with mel spectrograms that are generated by the [Librosa](https://librosa.org) library.
The model was trained for 50 epochs and the batch size was 64.
For more information about the model, please check the mentioned paper.

Both models are saved for further processing.

### ConvertModelToTFLite.py
This file contains a script that transforms a tensorflow model (.pb) to a tensorflow lite (.tflite) model.
The lite models are needed by the front end.
Please adapt the path to the model that you want to convert directly in this script.

The code is taken from: [https://www.tensorflow.org/lite/convert](https://www.tensorflow.org/lite/convert)
### WriteMetadataToModel.py
This script writes metadata to the tensorflow lite model since this is required by the front end.
Please adapt the path to the model that you want to write metadata to directly in this script.

The code is taken from: [https://colab.research.google.com/github/tensorflow/tensorflow/blob/master/tensorflow/lite/g3doc/convert/metadata_writer_tutorial.ipynb](https://colab.research.google.com/github/tensorflow/tensorflow/blob/master/tensorflow/lite/g3doc/convert/metadata_writer_tutorial.ipynb)

### PlotSignalMelSpec.py
This script plots a sample audio signal for visual inspection as a spectrogram and a mel spectrogram.
The sample is a one dimensional array taken from `SampleSignal.py`.

### SampleSignal.py
This file contains a sample audio signal that can be plotted in the script `PlotSignalMelSpec.py`.

### TestSignalModel.py
This script takes one audio sample as input and predicts the labels for it with the one-dimensional Signal model.
If an audio sample is longer that the sample length that was used for the model creation, it is cut into smaller pieces of the required length.
For all pieces, the prediction is then run.

The prediction function is called with the raw audio input from the .wav file without further pre-processing.
The script handles the input processing and cutting of audio sample by itself.

### TestMelSpecModel.py
This script takes one audio sample as input and predicts the labels for it with the two-dimensional Mel Spectrogram model.
If an audio sample is longer that the sample length that was used for the model creation, it is cut into smaller pieces of the required length.

For all pieces, a mel spectrogram is computed by the [Librosa](https://librosa.org) library.
This mel spectrogram is then used for running the model prediction.
The model runs the prediction for each audio piece.
The script handles the input processing, cutting of audio sample, and computation of mel spectrograms by itself.

## Data 
Since the task is to predict three different classes, the training data must also cover these three classes.
The data for the training of the model was taken from the following resources:

Speech: [The Flickr 8k Audio Caption Corpus](https://dagshub.com/michizhou/Flickr-Audio-Caption-Corpus)

Song: [CSD: Children's Song Dataset for Singing Voice Research](https://zenodo.org/record/4785016#.YYkpOtZBxqv) 
and [VocalSet: A Singing Voice Dataset](https://zenodo.org/record/1193957)

Silence: Privately recorded with the tool [Audacity](https://www.audacityteam.org/).

Since the audio data was not always in the right form, pre-processing has been applied to the data with the tool [Audacity](https://www.audacityteam.org/).
The audio data was converted from stereo to mono, converted to a sample rate of 16kHz and for the song and speech 
data sets, silence was manually removed (e.g. at the beginning of an audio sample).
In addition, since not all speech audio samples were long enough (2 seconds), several speech audio samples were 
combined into one file to get samples of the required length.
This resulted in several speech audio files that consist of multiple speech samples (in a serial form).

The data is organised in two folders: `data_short` and `data_long`.
The `data_long` folder contains all available pre-processed audio sample and is used for the actual training of the model.
The `data_short` folder contains only a small subset of all available pre-processed data.
It is mainly used for testing the whole pipeline since it requires less time.

## References and Resources
This list contains all resources that were used for the project:

* [Tensorflow Metadata Writer Information](https://www.tensorflow.org/lite/convert/metadata)
* [Tensorflow Metadata Converter (Code)](https://colab.research.google.com/github/tensorflow/tensorflow/blob/master/tensorflow/lite/g3doc/convert/metadata_writer_tutorial.ipynb)
* [Tensorflow Lite Model Converter](https://www.tensorflow.org/lite/convert)
* [1D CNN Model for Spectrogram Data](https://github.com/Logan97117/environmental_sound_classification_1DCNN)
* [2D CNN Model for Mel Spectrogram Data](https://doi.org/10.1016/j.apacoust.2020.107581)
* [Audacity](https://www.audacityteam.org/)
* [Librosa](https://librosa.org)
* [Tensorflow](http://www.tensorflow.org/)
* [matplotlib](https://matplotlib.org/)
* [numpy](https://numpy.org/)
* [scikit_learn](https://github.com/tqdm/tqdm)
* [tqdm](https://github.com/tqdm/tqdm)

The following list presents all references that were used in this project:

<a id="1">[1]</a> 
Sajjad Abdoli and Patrick Cardinal and Alessandro Lameiras Koerich. 
End-to-End Environmental Sound Classification using a 1D Convolutional Neural Network.
Expert Systems with Applications,
Volume 136, pages 252-263,2019. 
doi: https://doi.org/10.1016/j.eswa.2019.06.040.

<a id="1">[1]</a> 
Soonbeom Choi and Wonil Kim and Saebyul Park and Sangeon Yong and Juhan Nam.
Children’s Song Dataset for Singing Voice Research. 
21th International Society for Music Information Retrieval Conference (ISMIR), 2020. 
URL: https://zenodo.org/record/4785016#.YYkpOtZBxqv.

<a id="2">[2]</a>
David Harwath and James Glass.
Deep Multimodal Semantic Embeddings for Speech and Images.
2015 IEEE Automatic Speech Recognition and Understanding Workshop, 
pages 237-244, 2015.
doi: https://doi.org/10.1109/ASRU.2015.7404800.

<a id="3">[3]</a>
Micah Hodosh and Peter Young and Julia Hockenmaier.
Framing Image Description as a Ranking Task: Data, Models and Evaluation Metrics.
Journal of Artificial Intelligence Research, 
Volume 47, pages 853-899, 2013. 
doi: https://doi.org/10.1613/jair.3994.

<a id="4">[4]</a> 
Zohaib Mushtaq and Shun-Feng Su and Quoc-Viet Tran. 
Spectral images based environmental sound classification using CNN with meaningful data augmentation.
Applied Acoustics,
Volume 172, 2021. 
doi: https://doi.org/10.1016/j.apacoust.2020.107581.

<a id="5">[5]</a> 
Julia Wilkins and Seetharaman Prem and Alison Wahl and Bryan Pardo.
VocalSet: A Singing Voice Dataset.
19th International Society for Music Information Retrieval Conference (ISMIR), 
pages 468-474, 2018.
URL: https://zenodo.org/record/1193957.
