#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import os
from lxml import etree
from dateutil.parser import parse
import json
import string
import base64
import mimetypes


def getValidFileName(name):
    # This function eliminates characters that are not valid (given by a frozenset)
    valid_chars = "äöüß_ %s%s" % (string.ascii_letters, string.digits)
    valid_chars = frozenset(valid_chars)
    return ''.join(c if c in valid_chars else '_' for c in name)


class EvernoteAttachmentExtractor:

    datetime_format = '%Y_%m_%d__%H_%M_%S'

    def __init__(self, enexfile, outputpath):
        # Exported evernote note
        self.enexfile = enexfile

        # Output path for storing the data
        self.outputpath = outputpath

    def _load_enex_file(self):
        try:
            parser = etree.XMLParser(huge_tree=True)
            xmltree = etree.parse(self.enexfile, parser)
        except etree.XMLSyntaxError as e:
            print('Could not parse XML! Error: %s' % e)
            sys.exit(1)
        return xmltree

    def extract(self):
        # Get the xml tree of the enex file
        xmltree = self._load_enex_file()

        # Notes of this enex file
        notes = xmltree.xpath('//note')

        # Walk through the notes
        for note in notes:
            # Dictionary which contains the output data
            dictnote = dict()

            # Extract the title
            if note.xpath('title'):
                dictnote['title'] = note.xpath('title')[0].text
                print('Title: ' + dictnote['title'])

            # Output path /PathToEnexFile/Title/...
            dictnote['output'] = self.outputpath + getValidFileName(dictnote['title']) + os.path.sep
            print('Output path: ' + dictnote['output'])

            # Create output path
            if not os.path.exists(dictnote['output']):
                os.makedirs(dictnote['output'])

            # Extract created date
            if note.xpath('created'):
                created = parse(note.xpath('created')[0].text)
                dictnote['created'] = created.strftime(self.datetime_format)
                print('Created: ' + dictnote['created'])

            # Extract updated date
            if note.xpath('updated'):
                updated = parse(note.xpath('updated')[0].text)
                dictnote['updated'] = updated.strftime(self.datetime_format)
                print('Updated: ' + dictnote['updated'])

            # Extract content
            if note.xpath('content'):
                content = note.xpath('content')[0].text
                dictnote['content'] = content
                with open(dictnote['output'] + 'Content.html', 'w') as contentfp:
                    contentfp.write(content)
                contentfp.close()

            # Extract attributes
            if note.xpath('note-attributes'):
                attributes = note.xpath('note-attributes')

                # Walk through attributes
                for attribute in attributes:

                    # Extract the source-url
                    if attribute.xpath('source-url'):
                        dictnote['url'] = attribute.xpath('source-url')[0].text
                        print('URL: ' + dictnote['url'])

                    # Extract the author
                    if attribute.xpath('author'):
                        dictnote['author'] = attribute.xpath('author')[0].text
                        print('Author: ' + dictnote['author'])

            # Extract resources
            if note.xpath('resource'):
                resources = note.xpath('resource')

                # Create a list of resources
                listresources = list()

                # Walk through resource
                for i, resource in enumerate(resources, start=1):

                    # Actual resource dictionary
                    dictresource = dict()

                    # Extract data of resource
                    if resource.xpath('data'):
                        dictresource['data'] = resource.xpath('data')[0].text

                    # Extract the mime type
                    if resource.xpath('mime'):
                        dictresource['mime'] = resource.xpath('mime')[0].text

                    # Get the file extension from the mime type
                    fileextension = mimetypes.guess_extension(dictresource['mime'])

                    if fileextension is None:
                        fileextension = '.unknown'

                    # Output path
                    dictresource['output'] = dictnote['output'] + 'Resource_' + str(i) + fileextension

                    print('Adding resource: ' + str(i) + ' of type: ' + dictresource['mime'] + ' to: ' + dictresource['output'])

                    # Store resource in file
                    open(dictresource['output'], 'wb').write(base64.b64decode(dictresource['data']))

                    # Add the ressource to the list
                    listresources.append(dictresource)

                # Add the list to the note dict
                dictnote['resources'] = listresources

            # Store note dictionary as json
            with open(dictnote['output'] + 'Note.json', 'w') as fp:
                json.dump(dictnote, fp, sort_keys=True, indent=4)
            fp.close()


def main():
    # Check the arguments
    if len(sys.argv) == 1:
        print('Please use an .enex file from Evernote export.')
        sys.exit(0)
    else:
        enexfile = sys.argv[1]
        print('File: %s' % enexfile)

    # Check if enex file is existing
    if not os.path.exists(enexfile):
        print('File does not exist: %s' % enexfile)
        sys.exit(1)

    # Output path (usually the same folder than the enex file
    outputpath = enexfile.rsplit(os.path.sep, 1)[0] + os.path.sep

    # Extract attachments
    theevernoteattachmentextractor = EvernoteAttachmentExtractor(enexfile, outputpath)
    theevernoteattachmentextractor.extract()


if __name__ == "__main__":
    main()
