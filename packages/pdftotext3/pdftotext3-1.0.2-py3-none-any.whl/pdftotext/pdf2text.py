# PDFtoTEXT
# Copyright (c) 2021 ANISH M < aneesh25861@gmail.com >

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

''' This program converts all PDF files in current working directory to text Files.'''

import os
import subprocess
import platform
import webbrowser
from sys import exit
from time import sleep
from shutil import move

pkg=''
mode=platform.system().lower()

def tesseract(i):
    if mode == 'windows':
      os.system('"C:\\Program Files\\Tesseract-OCR\\tesseract" ' +i+' '+i[:-3] +' 2>tmp')
      os.remove('tmp')
    
    else:
      x = subprocess.run(['tesseract',i,i[:-3]],capture_output=True)

def pdf2image(file):
    if mode == 'windows':
      x = subprocess.run(['magick','convert','-density','300','-trim',file,'-quality','100',file[:-3]+'.png'])
    else:
      x = subprocess.run(['pdftocairo',file,'-png'])

def main():
 # Detect if platform is using apt or dnf package manager.
 try:
  subprocess.run(['apt','-v'],capture_output=True).stdout
  pkg='apt'
 except Exception as e:
   try:
     subprocess.run(['dnf','--version'],capture_output=True).stdout
     pkg='dnf'
   except Exception as e:
     try:
       subprocess.run(['pacman','--version'],capture_output=True).stdout
       pkg='pacman'
     except Exception as e:
       print('Platform not supported!')  
       sleep(5)
       exit(1)
    
     if mode !='windows':
       print('Platform not supported!')  
       sleep(5)
       exit(1)

 if mode != 'windows':    
  try:
      x = subprocess.run(['tesseract','-v'],capture_output=True)
  except Exception as e:
      print('Tesseract Not Found!\n Trying to Install it...')
      if pkg == 'apt':
         subprocess.run(['sudo','apt','update','&&','sudo','apt','install','tesseract-ocr']).stdout
      elif pkg == 'dnf':
         subprocess.run(['sudo','dnf','install','tesseract']).stdout
      elif pkg == 'pacman':
         subprocess.run(['sudo','pacman','-S','tesseract'],capture_output=True).stdout


  try:
      x = subprocess.run(['pdftocairo','-v'],capture_output=True)
  except Exception as e:
      print('pdftocairo Not Found!\n Trying to Install it...')
      if pkg == 'apt':
         subprocess.run(['sudo','apt','update','&&','sudo','apt','install','poppler-utils']).stdout
      elif pkg == 'dnf':
         subprocess.run(['sudo','dnf','install','poppler-utils']).stdout
      elif pkg == 'pacman':
         subprocess.run(['sudo','pacman','-S','poppler'],capture_output=True).stdout
 else:
  
   x = os.system('"C:\\Program Files\\Tesseract-OCR\\tesseract" -v > tmp')
   os.remove('tmp')
   if x != 0:
      print('Tesseract Not Found! Please Install it ...')
      webbrowser.open("https://github.com/UB-Mannheim/tesseract/wiki")

   try:
      x = subprocess.run(['magick','-version'],capture_output=True)
   except Exception as e:
      print('Imagemagick Not Found!\n Please install it...')
      webbrowser.open("https://imagemagick.org/script/download.php#windows")
      webbrowser.open("https://www.ghostscript.com/download/gsdnld.html")

 #Loop to get names of all PDF files in current working Directory.
 for i in os.listdir():
   if i[-3:].lower() == 'pdf':
     
      print('\nProcessing',i)
      #create an output folder.
      os.mkdir(i+'_output')
     
      #Move PDF file to output folder.
      move(i,i+'_output')
     
      #Change directory to output folder.
      os.chdir(i+'_output')
     
      #Convert PDF file to PNG images using pdftocairo tool in poppler-utils.
      print('\nConverting PDF file into PNGs...')
      pdf2image(i)

      #Loop to get names of all PNG image files in current working directory.
      for i in os.listdir():
        if i[-3:].lower()=='png':
          print('Extracting Text from ',i)
          #Pass the image to Tesseract ocr to recover text from images.
          tesseract(i)
     
          #Delete the image generated during Conversion of PDF to Text files.
          os.remove(i)
         
      #Return to current working Directory.
      os.chdir('..')
      print('Cleaning up PNGs...')
 print('\nDone!')     
