"""
Saves all images found the folder reduce by half size to the folder
"""

from PIL import Image, UnidentifiedImageError
import glob
import sys
import os

valid_images = ["jpg", "png"]

folder = '.'
if len(sys.argv) > 1:
    folder = sys.argv[1]

for images in [glob.glob(f'{folder}\*.{ext}') for ext in valid_images]:
    for img in images:
        try:
            image = Image.open(img, mode='r')
        except FileNotFoundError as e:
            print(e)
            continue
        except UnidentifiedImageError as e:
            print(e)
            continue
        except ValueError as e:
            print(e)
            continue
        except TypeError as e:
            print(e)
            continue

        image_name = os.path.basename(image.filename)
        #new_image = image.resize((image.size[0]//2, image.size[1]//2))
        new_image = image.reduce(2)
        try:
            new_image.save("reduced_" + image_name)
            new_image.close()
        except ValueError as e:
            print(e)
        except OSError as e:
            print(e)
        finally:
            image.close()
