import pysndfx
import librosa
import numpy as np
import os
if os.path.basename(os.getcwd()) != 'in-the-wild-verification':
    os.chdir(os.path.dirname(os.getcwd()))

def add_reverb(audio_array: np.array, out_folder: str = None, name: str = None):
    """Function to add reverb (echo) to a *.wav file
    Args:
        file -- numpy array 
        out_folder -- if specified, files will be saved there
        name -- name of the output file
    Returns the processed file and its samplerate
    """
    fx = (
        pysndfx.AudioEffectsChain()
        .delay()
    )   
    y = fx(audio_array)
    if out_folder:
        path = os.path.join(out_folder, name)
        fx(audio_array, path)
    
    return y


if __name__ == "__main__":
    INPUT = "data/id10001/00002.wav"
    sample_file, sr = librosa.load(INPUT, sr=None)
    sample_file = librosa.resample(sample_file, orig_sr=sr, target_sr=44100) # resampling due to some issues along the way
    add_reverb(sample_file, out_folder='data/tests', name='01.wav')