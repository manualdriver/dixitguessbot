import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

CARDSPATH = os.getenv('CARDPATH')


def setup_deck() -> List[str]:
    image_directory = CARDSPATH
    deck = load_images_from_directory(image_directory)
    return deck

def load_images_from_directory(directory: str) -> List[str]:
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory {directory} does not exist.")
    image_files = sorted(
        os.path.join(directory, filename)
        for filename in os.listdir(directory)
        if filename.lower().endswith((".png", ".jpg", ".jpeg"))
    )
    if not image_files:
        raise FileNotFoundError(f"No image files found in directory {directory}.")
    return image_files

