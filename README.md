# LittleHelpers
Some useful scripts you should know :)

## PDFMerger.py

PDFMerger scans the folder `strMergeFolder` (including all subfolders) for .PDF files. The pdf documents will be added to a list. PyPDF2 combines the files to one large files. There will be added bookmarks in the target file for easy navigation.

### ToDo's

- [ ] Use the argument function for the both folders

## UnzipFiles.py

UnzipFiles scans the folder `strUnzipThisFolder` (including all subfolders) for .zip files. The Zip files will be extracted to `strTargetFolder`added with the filename as subfolder. 

### ToDo's

- [ ] Use the argument function for the both folders

## ShowFolderContent.py

Walks through the folder and subfolder and shows you the content in a text file. There are two arguments needed:

* Folder (absolut)
* abs or rel for the output (Paths absolut or relative)

