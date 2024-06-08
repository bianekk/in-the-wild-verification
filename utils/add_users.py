import os
import librosa
import soundfile as sf
from tqdm import tqdm
import torch
from denoising import filter_butter
from speech_model.hparam import hparam as hp
from speech_model.utils import mfccs_and_spec
from speech_model.speech_embedder_net import SpeechEmbedder

def load_model():
    model = SpeechEmbedder()
    model.load_state_dict(torch.load(hp.model.model_path))
    model.eval()
    return model

def compute_embedding(model, audio_input):
    _, mel_db, _ = mfccs_and_spec(audio_input, wav_process = True)
    mel_db = torch.Tensor(mel_db)
    enrollment_batch = torch.reshape(mel_db, (1, mel_db.size(0), mel_db.size(1)))
    embedding = model(torch.Tensor(enrollment_batch))
    return embedding

def denoise_user(user_folder: str, denoise_folder: str):
    for user_file in os.listdir(user_folder):
        os.makedirs(denoise_folder, exist_ok=True)
        if user_file.endswith('wav'):
            filename = user_file
            try:
                audio, sr = librosa.load(os.path.join(user_folder, user_file), sr=16000)
                d_audio = filter_butter(audio, sr)
                sf.write(os.path.join(denoise_folder, filename), d_audio, sr)
            except EOFError: # some files are corrupted
                continue

def export_embeddings(model, denoise_folder: str, output_folder: str):
    user_embeddings = []
    for user_file in os.listdir(denoise_folder):
        if user_file.endswith('wav'):
            try:
                embedding = compute_embedding(model, os.path.join(denoise_folder, user_file))
                user_embeddings.append(embedding)
            except EOFError: # some files are corrupted
                continue
    user_embeddings = torch.stack(user_embeddings)
    os.makedirs(output_folder, exist_ok=True)
    torch.save(user_embeddings, os.path.join(output_folder, 'tensor.pt'))



if __name__ == "__main__":
    """
    Script for embedding test users
    Embeddings for each user are of shape [256, N] where N is the number of their samples 
    """
    OUT_DIR = "test_users_embeddings"
    SOURCE_DIR = "test_users"
    DENOISE_DIR = "denoised"
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(DENOISE_DIR, exist_ok=True)
    subfolders = ['clean', 'echo', 'language', 'noise']

    model = load_model()
    for sub in subfolders:
        print(f"=== Encoding {sub} users ===")
        sub_root = f'{SOURCE_DIR}/{sub}'
        test_users = os.listdir(sub_root)
        
        for user in tqdm(test_users):
            if os.path.isdir(os.path.join(SOURCE_DIR, sub, user)):
                # first denoising
                denoise_user(os.path.join(sub_root, user), os.path.join(DENOISE_DIR, sub, user))
                # embedding later
                # note: if you do not want to denoise, comment the previous line and replace the below line with this
                # export_embeddings(model, os.path.join(SOURCE_DIR, sub, user), os.path.join(OUT_DIR, sub, user))
                export_embeddings(model, os.path.join(DENOISE_DIR, sub, user), os.path.join(OUT_DIR, sub, user))