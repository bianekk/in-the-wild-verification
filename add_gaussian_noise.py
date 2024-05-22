"""This script creates an augmented copy of a sound files
dataset. It mixes each audio file with a random gaussian noise

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
    --noise_scale: the target ratio between the mean of noise absolute value and the mean
        of sound absolute value,
        default: 0.5

Example:
    python add_gaussian_noise.py split_data/train output/ --noise_scale 0.5

Notes:
    each provided directory as an argument must exist
    files in data_dir are assumed to be WAV files

"""

import argparse
import os
import random
import numpy as np
from pydub import AudioSegment
from pydub.utils import ratio_to_db
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("data_dir")
parser.add_argument("output_dir")
parser.add_argument("--noise_scale", default=0.5)

args = parser.parse_args()

for path in (args.data_dir, args.output_dir):
    assert os.path.isdir(path), f"Invalid path: {path}"


def add_gaussian_noise(
    segment: AudioSegment,
    ratio: float,
) -> AudioSegment:
    """Adds Gaussian noise to given
    audio segment

    At first, Gaussian noise N(0,1) is generated.
    Next, it is scaled so that
    abs(noise)_mean / abs(segment)_mean = ratio

    Args:
        segment: pydub.AudioSegment object to add noise to
        ratio: float from range (0,1), ratio between mean
            means as described above

    Returns:
        pydub.AudioSegment: audio segment with added noise
    """
    # convert segment to numpy array and get its length
    segment_arr = np.array(
        segment.get_array_of_samples()
    ).astype(np.float64)
    segment_len = segment_arr.shape[0]

    # generate noise N(0,1) with number of samples same as segment
    noise_base = np.random.normal(0, 1, size=segment_len)

    # scale the noise
    segment_mean = np.mean(np.abs(segment_arr))
    noise_mean = np.mean(np.abs(noise_base))
    noise_scaled = (segment_mean * ratio / noise_mean) * noise_base

    # create noise object
    noise_segment = AudioSegment(
        noise_scaled.astype(np.int16).tobytes(),
        frame_rate=segment.frame_rate,
        sample_width=segment.sample_width,
        channels=segment.channels
    )

    return segment.overlay(
        noise_segment
    )


def process_profile(profile_name: str):
    """For a profile dir, creates profile dir
    in the output dir, augments profile sounds with Gaussian noises
    and adds augmented sounds to the output profile
    """
    os.makedirs(os.path.join(args.output_dir, profile_name))
    profile_path = os.path.join(args.data_dir, profile_name)
    for fname in os.listdir(profile_path):

        if not fname.endswith(".wav"):
            continue

        sound = AudioSegment.from_wav(
            os.path.join(profile_path, fname)
        )
        sound_with_noise = add_gaussian_noise(
            sound, ratio=float(args.noise_scale)
        )
        sound_with_noise.export(
            out_f=os.path.join(args.output_dir, profile_name, fname),
            format="wav"
        )


if __name__ == '__main__':

    # creating mixed sounds and saving to output_dir
    print("Creating mixed sounds ...")
    for profile_name in tqdm(os.listdir(args.data_dir)):

        process_profile(
            profile_name=profile_name,
        )
