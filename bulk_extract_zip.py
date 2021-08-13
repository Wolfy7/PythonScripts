"""
Unpacks all zip archives found in the folder
"""

from zipfile import ZipFile
import glob
import sys

folder = '.'
if len(sys.argv) > 1:
    folder = sys.argv[1]

for zip_file in glob.glob(folder + '\*.zip'):
    with ZipFile(zip_file, 'r') as zip:
        zip.extractall()