import os

import IPython.display as ipd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as skl
import sklearn.utils, sklearn.preprocessing, sklearn.decomposition, sklearn.svm
import librosa
import librosa.display

import utils

plt.rcParams['figure.figsize'] = (17, 5)

# Directory where mp3 are stored.
AUDIO_DIR = "data/fma_medium"

# Load metadata and features.
tracks = utils.load('data/fma_metadata (1)/tracks.csv')
genres = utils.load('data/fma_metadata (1)/genres.csv')
features = utils.load('data/fma_metadata (1)/features.csv')
echonest = utils.load('data/fma_metadata (1)/echonest.csv')

np.testing.assert_array_equal(features.index, tracks.index)
assert echonest.index.isin(tracks.index).all()

tracks.shape, genres.shape, features.shape, echonest.shape

medium = tracks[tracks['set', 'subset'] <= 'medium']
medium = medium['track']['genre_top']

for track_id in medium.index:
    mp3_name = utils.get_audio_path(AUDIO_DIR, track_id)
    png_name = mp3_name.replace(".mp3", ".png").replace("fma_medium", "fma_medium_image")
    print(f"Working on {track_id}: Reading {mp3_name}")

    # if exists in os then skip
    if os.path.exists(png_name):
        print("Image already exists, skipping")
        continue
    
    try:
        # check if file actually exist
        if not os.path.exists(mp3_name):
            print("File unavailable, skipping")
            continue
        
        # Load the file into librosa
        x, sr = librosa.load(mp3_name, sr=None, mono=True)
        S = librosa.feature.melspectrogram(y=x, sr=sr, n_mels=128, fmax=8000)

        plt.figure(figsize=(10, 4))
        librosa.display.specshow(librosa.power_to_db(S, ref=np.max), x_axis=None, y_axis=None, fmax=8000)
        plt.savefig(png_name, bbox_inches='tight', pad_inches=0)
        print(f"Saved file {png_name}")
        
        plt.close()
    
    except Exception as e:
        print(f"An error occurred while processing {track_id}: {e}")
