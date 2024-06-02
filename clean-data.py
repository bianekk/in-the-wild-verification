import os
import shutil
import splitfolders
import pandas as pd

"""Script for moving *.wav files into parent user directory
Run after downloading and unpacking *.zip file from Google Drive
"""

def remove_empty_folders(path_abs):
    walk = list(os.walk(path_abs))
    for path, _, _ in walk[::-1]:
        if len(os.listdir(path)) == 0:
            shutil.rmtree(path)


def split_users_for_tests(root, users_no = 25):
    os.makedirs('test_users', exist_ok=True) # folder to save files
    subfolders = ['clean', 'noise', 'echo', 'language']

    for sub in subfolders:
        sub_root = f'{root}/{sub}'
        test_users = os.listdir(sub_root)[:users_no+1]
        for user in test_users:
            shutil.move(os.path.join(sub_root, user), os.path.join('test_users', sub, user))


def split_train_test(root):
    splitfolders.ratio(root, output='split_data', seed=1337, ratio=(.7, .3), move=True) 


def user_metadata(root):
    subfolders = ['clean', 'noise', 'echo', 'language']
    user_df = pd.DataFrame(columns=['ID', 'type'])
    for sub in subfolders:
        for subdir in os.listdir(f'{root}/{sub}'):
            if os.path.isdir(os.path.join(f'{root}/{sub}', subdir)):
                user_df.loc[len(user_df)] = [subdir, sub]
    
    user_df.to_csv("users_raw.csv", index=None)


def move_from_subfolders(root):
    subfolders = ['clean', 'noise', 'echo', 'language']
    for sub in subfolders:
        for user in os.listdir(os.path.join(root, sub)):
            if os.path.isdir(os.path.join(root, sub, user)):
                shutil.move(os.path.join(root, sub, user), os.path.join(root, user))

def drop_sparse_profiles(root, min_samples = 10):
    for user in os.listdir(os.path.join(root)):
        if os.path.isdir(os.path.join(root, user)) and len(os.listdir(os.path.join(root, user))) < min_samples:
            # print(len(os.listdir(os.path.join(root, user))))
            shutil.rmtree(os.path.join(root, user))

if __name__ == "__main__":
    """Insert your data folder here"""
    ROOT = "output"
    # remove_empty_folders(ROOT)
    os.makedirs('split_data', exist_ok=True) # folder to save files
    # user_metadata(ROOT)
    #split_users_for_tests(ROOT)
    #move_from_subfolders(ROOT)
    # split_train_test(ROOT)
    drop_sparse_profiles('split_data/val', min_samples=5)

