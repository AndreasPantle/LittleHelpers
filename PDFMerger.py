#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import PyPDF2

strMergeFolder = '/YourPath/With/The/PDF/Files'
strOutputFile = '/Output/File.pdf'

def main():
    listPDFFiles = list()

    # get all files in merge folder
    if os.path.exists(strMergeFolder):
        # Get the files in this folder
        for strActualFolder, listFolders, listFiles in os.walk(strMergeFolder):
            for strActualFile in listFiles:
                if strActualFile.endswith('.pdf'):
                    listPDFFiles.append(strActualFile)
                    print('Add: %s' % strActualFile)
    else:
        print('Path doesn\'t exist!')
        sys.exit(1)

    if len(listPDFFiles) != 0:
        pdfMerger = PyPDF2.PdfFileMerger()

        for intIndex, strPDFFile in enumerate(listPDFFiles, start=0):
            strFile = strMergeFolder + os.path.sep + strPDFFile
            pdfMerger.append(open(strFile, 'rb'), bookmark=strPDFFile, pages=None, import_bookmarks=True)

        pdfMerger.write(strOutputFile)
        pdfMerger.close()

if __name__ == '__main__':
    main()
