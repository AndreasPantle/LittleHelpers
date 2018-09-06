# -*- coding: utf-8 -*-

# Walks through the folder and subfolder and shows you the content

import sys
import os

lFilter = ['.svn', '.sv', '.idea', '.ide', '.sv']

def main():
    # We need one folder
    if len(sys.argv) != 3:
        print('Please add a folder and mode (abs/rel).')
        sys.exit(1)

    sFolder = sys.argv[1]
    sMode = sys.argv[2]

    # Is the folder existing
    if not os.path.exists(sFolder):
        print('Folder: %s is not existing!' % sFolder)
        sys.exit(1)
    else:
        print('Using folder: %s' % sFolder)

    lFolderContent = list()

    for sActualFolder, lFolders, lFiles in os.walk(sFolder):
        for sFile in lFiles:
            # Check file filter
            if any(sFile in s for s in lFilter):
                continue

            # Check folder filter
            if any(s in sActualFolder for s in lFilter):
                continue

            sAppendFile = ''

            if sMode == 'abs':
                sAppendFile = sActualFolder + os.path.sep + sFile

            if sMode == 'rel':
                if sActualFolder != sFolder:
                    sAppendFile = sActualFolder.strip(sFolder) + os.path.sep + sFile
                else:
                    sAppendFile = sFile

            lFolderContent.append(sAppendFile)

    if len(lFolderContent) == 0:
        print('Folder is empty.')
        sys.exit(0)
    else:
        print('Entries in folder: %i' % len(lFolderContent))

    # get the actual path
    sActualPath = os.path.dirname(os.path.realpath(__file__))
    sOutputFile = sActualPath + os.path.sep + 'ShowFolderContent.txt'

    with open(sOutputFile, 'w') as fOutputFile:
        for sElement in lFolderContent:
            fOutputFile.write('\'%s\'\n' % sElement)
    fOutputFile.close()

if __name__ == "__main__":
    main()
