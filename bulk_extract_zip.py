"""
Unpacks all zip archives found in the folder
"""

from zipfile import ZipFile
import glob
import sys
import os

folder = '.'
if len(sys.argv) > 1:
    folder = sys.argv[1]

archive_counter = 0
for zip_file in glob.glob(folder + '\*.zip'):
    folder_name, extension = os.path.splitext(os.path.basename(zip_file))
    print(f"Unpacking {folder_name}{extension} ...")
    with ZipFile(zip_file, 'r') as zip:
        zip.extractall(folder + "\\" + folder_name)
    archive_counter += 1

print(f"Finished unpacking {archive_counter} archive(s)")
