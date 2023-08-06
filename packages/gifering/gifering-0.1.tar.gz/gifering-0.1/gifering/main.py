import os
import argparse
import pathlib
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("webp", type=pathlib.Path, help="folder where all .webp files are located")
parser.add_argument("gif", type=pathlib.Path, help="folder where all previous .gif files are located")
args = parser.parse_args()

# Get all converted gifs names
all_gifs = os.listdir(args.gif)

# Get all file names without .gif extension
all_gifs = [name[:-4] for name in all_gifs]

# Get all files in webp folder
files = os.listdir(args.webp)

# Maintain only .webp files
files = [file for file in files if file[-5:] == '.webp']

for file in files:
    if file[:-5] not in all_gifs:
        image = Image.open(pathlib.Path.joinpath(args.webp, file))
        image.save(pathlib.Path.joinpath(args.gif, f"{file[:-5]}.gif"), 'gif', save_all=True, background=0)

