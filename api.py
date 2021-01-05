import sys
import requests
import json
import argparse
import base64
import os
from argparse import ArgumentParser, Action as ParseAction

"""
This class stores the authetification key in a dictionary,
so it can be extracted in the headers parameter in the post request,
separately from the rest of the parsed arguments, which belong
in the body
"""

class StoreDict(ParseAction):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, {'X-Auth-Key' : values})

#Here we implement the necessary arguments, as seen in the documentation
parser = argparse.ArgumentParser(description = 'Parameters for the API')
parser.add_argument('-k','--key' , type=str, required = True, action = StoreDict, help = 'The auth key provided by Klippa.')
#the document and the url are mutually exclusive, however one of them is required
group = parser.add_mutually_exclusive_group(required = True)
group.add_argument('-d','--document', type = str, help = 'the multipart/formdata file')
group.add_argument('-u','--url', type=str, help = 'the url for the file')
#The pdf extraction argument can only take "full" or "fast" as arguments, and "fast" is default
parser.add_argument('-e', '--pdf_text_extraction', type = str, choices = ['full','fast'], default = 'fast',
					help = 'choose whether you want full or fast extraction (default: fast)')
parser.add_argument('-t',  '--template', type = str, help = 'the document template')
parser.add_argument('-p', '--printInFile', type = bool, default = False, 
					help = "Choose whether to print the result in a json file (True) or on the terminal (False). False by default ")
args = parser.parse_args()

if args.document == None:
	x = requests.post("https://custom-ocr.klippa.com/api/v1/parseDocument", headers = args.key, data = vars(args))
else:
	files = {'document' : open(args.document,'rb')}
	x = requests.post("https://custom-ocr.klippa.com/api/v1/parseDocument", headers = args.key, data = vars(args), files = files)

"""
Depending on the value of the printInFile parameter, the code below
will either print the output to a json file as it is, or format it 
for better reading and print it to the terminal
"""
if args.printInFile == True:
	filename = input("What would you like the file to be named? ")
	f = open(filename + ".json","w+")
	f.write(x.text)
else:
	print(json.dumps(x.json(), indent = 4))
	