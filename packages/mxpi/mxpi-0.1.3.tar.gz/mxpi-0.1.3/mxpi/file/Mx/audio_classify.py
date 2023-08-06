# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
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
"""Main scripts to run audio classification."""

import argparse
import time
from matplotlib import category
import numpy as np
import threading
from scipy.io import wavfile
from Mx.audio_classifier import AudioClassifier
from Mx.audio_classifier import AudioClassifierOptions
from Mx.utils import Plotter

class init():
  def __init__(self,model,max_results) -> None:
      self.model=model
      self.max_results = max_results
  def setUp(self,wav):
    """Initialize the shared variables."""
    # Load the TFLite model to get the audio format required by the model.
    classifier = AudioClassifier(self.model)
    tensor = classifier.create_input_tensor_audio()
    input_size = len(tensor.buffer)
    input_sample_rate = tensor.format.sample_rate
    channels = tensor.format.channels

    # Load the input audio file. Use only the beginning of the file that fits
    # the model input size.
    original_sample_rate, wav_data = wavfile.read(wav, True)

    # Normalize to [-1, 1] and cast to float32
    wav_data = (wav_data / np.iinfo(wav_data.dtype).max).astype(np.float32)

    # Use only the beginning of the file that fits the model input size.
    wav_data = np.reshape(wav_data[:input_size], [input_size, channels])
    tensor.load_from_array(wav_data)
    self._input_tensor = tensor

    
  def run(self,wav):
    self.setUp(wav)
    """Test the max_results option."""
    option = AudioClassifierOptions(max_results=self.max_results)
    classifier = AudioClassifier(self.model, options=option)
    categories = classifier.classify(self._input_tensor)
    sp=[]
    for cat in categories:
      s={'label':cat[0],'score':cat[1]}
      sp.append(s)
    return sp

class init_continue():
  def __init__(self,model,max_results,score_threshold) -> None:
      self.model=model
      self.max_results = max_results
      self.score_threshold=score_threshold
      self.categories=None
      self.cont=SoundThread(self.model,self.max_results,self.score_threshold)
      self.cont.start()

  def get(self):
    self.categories=self.cont.categories
    return self.categories


class SoundThread (threading.Thread):
  def __init__(self, model: str, max_results: int, 
      score_threshold: float,overlapping_factor=0.5, 
      num_threads=4,enable_edgetpu=False):
      threading.Thread.__init__(self)
      self.model=model
      self.max_results=max_results
      self.score_threshold=score_threshold
      self.overlapping_factor=overlapping_factor
      self.num_threads=num_threads
      self.enable_edgetpu=enable_edgetpu
      self.categories=None
      if (self.overlapping_factor <= 0) or (self.overlapping_factor >= 1.0):
        raise ValueError('Overlapping factor must be between 0 and 1.')

      if (self.score_threshold < 0) or (self.score_threshold > 1.0):
        raise ValueError('Score threshold must be between (inclusive) 0 and 1.')

      # Initialize the audio classification model.
      self.options = AudioClassifierOptions(
          num_threads=self.num_threads,
          max_results=self.max_results,
          score_threshold=self.score_threshold,
          enable_edgetpu=self.enable_edgetpu)
      self.classifier = AudioClassifier(self.model, self.options)

      # Initialize the audio recorder and a tensor to store the audio input.
      self.audio_record = self.classifier.create_audio_record()
      self.tensor_audio = self.classifier.create_input_tensor_audio()

      # We'll try to run inference every interval_between_inference seconds.
      # This is usually half of the model's input length to create an overlapping
      # between incoming audio segments to improve classification accuracy.
      self.input_length_in_second = float(len(
          self.tensor_audio.buffer)) / self.tensor_audio.format.sample_rate
      self.interval_between_inference = self.input_length_in_second * (1 - self.overlapping_factor)
      self.pause_time = self.interval_between_inference * 0.1
      self.last_inference_time = time.time()
      # Start audio recording in the background.
      self.audio_record.start_recording()

  def run(self):
      while True:
        # Wait until at least interval_between_inference seconds has passed since
        # the last inference.
        now = time.time()
        diff = now - self.last_inference_time
        if diff < self.interval_between_inference:
          time.sleep(self.pause_time)
          continue
        self.last_inference_time = now

        # Load the input audio and run classify.
        self.tensor_audio.load_from_audio_record(self.audio_record)
        self.categories = self.classifier.classify(self.tensor_audio)
        
if __name__ == '__main__':
  model='file/Mx/model.tflite'
  file='file/Mx/sound.wav'
  max=3
  score_threshold=0.5
  ad=init_continue(model, max, score_threshold)
  while 1:
    print(ad.get())
