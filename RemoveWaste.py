#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import shutil


folders_to_remove = ['.AppleDB', '.AppleDesktop', '.AppleDouble', 'Network Trash Folder', 'Temporary Items', '.Trash-1000']
files_to_remove = ['.DS_Store', '._.DS_Store']


def main():
    # Check the arguments
    if len(sys.argv) == 1:
        print('Please define a folder to run within!')
        exit(0)
    else:
        folder = sys.argv[1]
        print('Folder: %s' % folder)

    # Check if folder is existing
    if os.path.isdir(folder):
        # Start with removing waste
        for folder, foldernames, filenames in os.walk(folder, topdown=False): # topdown=False walks from bottom up
            for file in filenames:
                if file in files_to_remove:
                    removefile = folder + os.path.sep + file
                    print('Remove file: %s' % removefile)
                    try:
                        os.remove(removefile)
                    except OSError:
                        print('Failed to remove file: %s' % removefile)

            folder_last = folder.rsplit(os.path.sep, 1)[-1]
            if folder_last in folders_to_remove:
                print('Remove folder: %s' % folder)
                try:
                    shutil.rmtree(folder)
                except OSError:
                    print('Failed to remove folder: %s' % folder)
    else:
        # Folder does not exist!
        print('Folder: %s is not existing!' % folder)
        exit(1)


if __name__ == "__main__":
    main()
