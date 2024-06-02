"""This script creates an augmented copy of a sound files
dataset. It adds reverb (echo) to all sound files in the provided data_dir.
Args:
    data_dir: path to the directory with sound files (WAV)
        the directory at path data_dir should have the following structure:
        data_dir_name
        |
        |---profile_name_1
           |
           |---file_1.wav
           |---file_2.wav
           |--- ...
        |---profile_name_2
        |--- ...
    output_dir: path to the directory to put output files in
Example:
    python add_echos.py split_data/train output/ 
Notes:
    data_dir must exist
    files in data_dir are assumed to be WAV files
"""

import argparse
import os
import numpy as np
import pysndfx
import librosa
from tqdm import tqdm
import soundfile as sf

parser = argparse.ArgumentParser()
parser.add_argument("--data_dir", default='data/')
parser.add_argument("--output_dir", default='output_reverb/')

args = parser.parse_args()
os.makedirs(os.path.join(args.output_dir), exist_ok=True)

for path in (args.data_dir, args.output_dir):
    assert os.path.isdir(path), f"Invalid path: {path}"


def add_reverb(audio_array: np.array, out_file: str = None):
    """Function to add reverb (echo) to a *.wav file
    Args:
        file -- numpy array 
        out_file -- if specified, files will be saved there
    Returns the processed file
    """
    fx = (
        pysndfx.AudioEffectsChain()
        .delay()
    )   
    y = fx(audio_array)
    if out_file:
        y = librosa.resample(y, orig_sr=44100, target_sr=16000)
        # fx(audio_array, out_file)
        sf.write(out_file, y, 16000)
    
    return y



def process_profile(profile_name: str):
    """For a profile dir, creates profile dir
    in the output dir, augments profile sounds with reverb
    and adds augmented sounds to the output profile
    """
    os.makedirs(os.path.join(args.output_dir, profile_name), exist_ok=True)
    profile_path = os.path.join(args.data_dir, profile_name)
    for fname in os.listdir(profile_path):

        if not fname.endswith(".wav"):
            continue

        sample_file, sr = librosa.load(os.path.join(profile_path, fname), sr=None)
        sample_file = librosa.resample(
            sample_file, 
            orig_sr=sr, 
            target_sr=44100) # resampling due to some issues along the way
        
        add_reverb(sample_file, out_file=os.path.join(args.output_dir, profile_name, fname))


if __name__ == '__main__':

    # creating mixed sounds and saving to output_dir
    print("Creating reverbed sounds ...")
    for profile_name in tqdm(os.listdir(args.data_dir)):

        process_profile(
            profile_name=profile_name,
        )