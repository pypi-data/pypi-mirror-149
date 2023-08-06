"""
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

bad_words = ['basemap', 'Basemap','projection']

def replace(file_path, bad_words):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if not any(bad_word in line for bad_word in bad_words):
                    new_file.write(line)
    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

print('Disable basemap from track_iss')
replace('liveisstracker/track_iss.py',bad_words)
"""
