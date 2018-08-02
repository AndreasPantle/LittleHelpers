#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Unzip every file in folder and subfolder

import os
import sys
import zipfile

strUnzipThisFolder = '/Folder/With/Lots/Of/Zips'
strTargetFolder = '/Unzip/Folder'

def main():
    listZIPFiles = list()

    # get all files in unzip folder
    if os.path.exists(strUnzipThisFolder):
        for strActualFolder, listFolders, listFiles in os.walk(strUnzipThisFolder):
            for strActualFile in listFiles:
                if strActualFile.endswith('.zip'):
                    listZIPFiles.append(strActualFolder + os.path.sep + strActualFile)
                    print('Add: %s' % strActualFile)
    else:
        print('Path: %s doesn\'t exist!' % strUnzipThisFolder)
        sys.exit(1)

    if len(listZIPFiles) != 0:
        for intIndex, strZIPFile in enumerate(listZIPFiles):
            strTargetFolderUnzip = strTargetFolder + os.path.sep + strZIPFile.rsplit(os.path.sep, 1)[-1]
            if not os.path.exists(strTargetFolderUnzip):
                os.makedirs(strTargetFolderUnzip)
                zip_ref = zipfile.ZipFile(strZIPFile, 'r')
                zip_ref.extractall(strTargetFolderUnzip)
                print('Unzip: %s --> %s' % (strZIPFile, strTargetFolderUnzip))

if __name__ == "__main__":
    main()
