# Copyright 2022 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests for the AudioClassifier wrapper."""

import csv
import unittest

from Mx.audio_classifier import AudioClassifier
from Mx.audio_classifier import AudioClassifierOptions
from Mx.audio_classifier import Category
import numpy as np
from scipy.io import wavfile

_MODEL_FILE = 'file/Mx/model.tflite'
_GROUND_TRUTH_FILE = 'ground_truth.csv'
_AUDIO_FILE = 'file/Mx/sound.wav'
_ACCEPTABLE_ERROR_RANGE = 0.01


class AudioClassifierTest(unittest.TestCase):

  def setUp(self):
    """Initialize the shared variables."""
    super().setUp()
    # Load the TFLite model to get the audio format required by the model.
    classifier = AudioClassifier(_MODEL_FILE)
    tensor = classifier.create_input_tensor_audio()
    input_size = len(tensor.buffer)
    input_sample_rate = tensor.format.sample_rate
    channels = tensor.format.channels

    # Load the input audio file. Use only the beginning of the file that fits
    # the model input size.
    original_sample_rate, wav_data = wavfile.read(_AUDIO_FILE, True)

    # Ensure that the WAV file's sampling rate matches with the model
    # requirement.
    self.assertEqual(
        original_sample_rate, input_sample_rate,
        'The test audio\'s sample rate does not match with the model\'s requirement.'
    )

    # Normalize to [-1, 1] and cast to float32
    wav_data = (wav_data / np.iinfo(wav_data.dtype).max).astype(np.float32)

    # Use only the beginning of the file that fits the model input size.
    wav_data = np.reshape(wav_data[:input_size], [input_size, channels])
    tensor.load_from_array(wav_data)
    self._input_tensor = tensor

    
  def test_max_results_option(self):
    """Test the max_results option."""
    max_results = 3
    option = AudioClassifierOptions(max_results=max_results)
    classifier = AudioClassifier(_MODEL_FILE, options=option)
    categories = classifier.classify(self._input_tensor)
    print(categories)
    self.assertLessEqual(
        len(categories), max_results, 'Too many results returned.')


# pylint: enable=g-unreachable-test-method

if __name__ == '__main__':
  unittest.main()
