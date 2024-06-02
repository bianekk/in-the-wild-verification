import os
import shutil
import splitfolders

OUTPUT = "output"

# with open("noise_profiles.txt") as file:
#     noise_profiles = [line.strip() for line in file]

# with open("echo_profiles.txt") as file:
#     echo_profiles = [line.strip() for line in file]

os.makedirs("output", exist_ok=True)

# collecting 250 noised and 250 reverbed profiles

def move_from_folders(root):
    for subdir in os.listdir(root):
        if os.path.isdir(os.path.join(root, subdir)):
            for user_subdir in os.listdir(os.path.join(root, subdir)):
                if os.path.isdir(os.path.join(root, subdir, user_subdir)):
                    for filename in os.listdir(os.path.join(root, subdir, user_subdir)):
                        shutil.move(os.path.join(root, subdir, user_subdir, filename), os.path.join(root, subdir, filename))

def remove_empty_folders(path_abs):
    walk = list(os.walk(path_abs))
    for path, _, _ in walk[::-1]:
        if len(os.listdir(path)) == 0:
            os.remove(path)

def select_to_ouput(type, root):
    with open(f"{type}_profiles.txt") as file:
        profiles = [line.strip() for line in file]
    os.makedirs(f"output/{type}", exist_ok=True)
    i = 0
    for subdir in os.listdir(root):
        if i == 250:
            break
        if os.path.isdir(os.path.join(root, subdir)) and str(subdir) in profiles and len(os.listdir(os.path.join(root, subdir))) > 14:
            shutil.move(os.path.join(root, subdir), os.path.join(f"output/{type}", subdir))
            i = i + 1

def add_clean_profiles():
    noise_profiles = os.listdir("output/noise")
    echo_profiles = os.listdir("output/echo")

    profiles = noise_profiles + echo_profiles
    os.makedirs("output/clean", exist_ok=True)
    i = 0
    for subdir in os.listdir("voxceleb/wav"):
        curr_user = os.path.join(root, subdir)
        if i == 250:
            break
        if os.path.isdir(curr_user) and str(subdir) not in profiles and len(os.listdir(curr_user)) > 14:
            shutil.move(os.path.join(root, subdir), os.path.join("output/clean", subdir))
            i = i + 1


def add_languages():
    noise_profiles = os.listdir("output/noise")
    echo_profiles = os.listdir("output/echo")

    profiles = noise_profiles + echo_profiles

    langs = ['ge', 'pl', 'it']
    os.makedirs("output/language", exist_ok=True)
    i = 0
    for langauge in langs:
        if i != 0 and i % 50 == 0:
                continue
        for subdir in os.listdir(f"wav_{langauge}"):
            curr_user = os.path.join(f"wav_{langauge}", subdir, 'asd')
            if os.path.isdir(curr_user) and str(subdir) not in profiles and len(os.listdir(curr_user)) > 14:
                shutil.move(os.path.join(f"wav_{langauge}", subdir, 'asd'), os.path.join("output/language", subdir))
                i = i + 1
        if i == 150:
            break

if __name__ == '__main__':
    root = "wav"
    # move_from_folders(root)
    # remove_empty_folders(root)
    # select_to_ouput('echo', root)
    # add_clean_profiles()
    # add_languages()
    file_count = sum(len(files) for _, _, files in os.walk('output'))
    print(file_count) # 48 746 