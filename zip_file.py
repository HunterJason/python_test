#!/usr/bin/env python
# coding=utf-8

__author__ = 'jasonhuang1029'

import zipfile
import os, sys

def zip_dir(dirname, zipdirname):
  filelist = []
  #Check input ...
  fulldirname = os.path.abspath(dirname)
  fullzipfilename = os.path.abspath(zipdirname)
  if not os.path.exists(fulldirname):
    print '%s is not exist, press any key to quit!'%fulldirname
    inputStr = raw_input()
    return
  if os.path.isdir(fullzipfilename):
    tmpbasename = os.path.basename(dirname)
    zipfile_name, extern_name = os.path.splitext(tmpbasename)
    zipfile_name = zipfile_name + '.zip'
    fullzipfilename = os.path.normpath(os.path.join(fullzipfilename,zipfile_name))
  if os.path.exists(fullzipfilename):
    while 1:
      print '%s has already exist, are you sure to modify it? [y/n]'%fullzipfilename
      inputStr = raw_input()
      if inputStr == 'N' or inputStr == 'n':
        return
      elif inputStr == 'Y' or inputStr == 'y':
        break
      else:
        continue

  print 'start to zip %s to %s ...'%(fulldirname,fullzipfilename)
  #Get file(s) to zip ...
  if os.path.isfile(dirname):
    filelist.append(dirname)
    dirname = os.path.dirname(dirname) 
  else:
    for root, dirlist, files in os.walk(dirname):
      for filename in files:
        filelist.append(os.path.join(root,filename))
  return
  #Start to zip file ...
  destZip = zipfile.ZipFile(fullzipfilename, 'w')
  for eachfile in filelist:
    destfile = eachfile[len(dirname):]
    print 'Zip file %s ...'%destfile
    destZip.write(eachfile, destfile)
  destZip.close()

def unzip_dir(zipfilename, unzipdirname):
  fullzipfilename = os.path.abspath(zipfilename)
  fullunzipdirname = os.path.abspath(unzipdirname)
  #Check inpput ...
  if not os.path.exists(fullzipfilename):
    print '%s is not exist, press any key to quit...'%fullzipfilename
    inputStr = raw_input()
    return
  if not os.path.exists(fullunzipdirname):
    os.mkdir(fullunzipdirname)
  else:
    if os.path.isfile(fullunzipdirname):
      while 1:
        print 'File %s is exist, are you sure to delet it first? [Y/N]'%fullunzipdirname
        inputStr = raw_input()
        if inputStr == 'y' or inputStr == 'Y':
          os.remove(fullunzipdirname)
          break
        elif inputStr == 'n' or inputStr == 'N':
          return
        else:
          continue
    elif os.path.isdir(fullunzipdirname):
      zipfilebasename = os.path.basename(fullzipfilename)
      zipfile_name, zipfile_extent_name = os.path.splitext(zipfilebasename)
      fullunzipdirname = os.path.join(fullunzipdirname,zipfile_name)
      if not os.path.exists(fullunzipdirname):
        os.mkdir(fullunzipdirname)
      #print fullunzipdirname
  #Start extract files ...
  srcZip = zipfile.ZipFile(fullzipfilename, 'r')
  for eachfile in srcZip.namelist():
    print 'Unzip file %s ...'%eachfile
    eachfilename = os.path.abspath(os.path.join(fullunzipdirname,eachfile))
    if os.path.exists(eachfilename):
      eachfilename, eachfilename_extent = os.path.splitext(eachfilename)
      eachfilename = eachfilename + '(New)' + eachfilename_extent
    eachdirname = os.path.dirname(eachfilename)
    if not os.path.exists(eachdirname):
      os.makedirs(eachdirname)
    fd = open(eachfilename, 'wb')
    fd.write(srcZip.read(eachfile))
    fd.close()
  srcZip.close()
  print 'Unzip file succeed!'

def print_help(module_name):
  print """
  This program can zip given folder to destination file, or unzip given zipped file to destination folder. 
  Usage: %s [option] [arg]... 
  -z zip: zip given folder to destination file 
  usage: %s -z/zip dirname, zipfilename 
  -u unzip: unzip given zipped file to destination folder, 
  usage: %s -u/-unzip zipfilename, unzipdirname 
  """ %(module_name, module_name, module_name)

if __name__ == '__main__':
  if len(sys.argv) < 4:
    print_help(sys.argv[0])
    sys.exit()
  else:
    if sys.argv[1].startswith('-'):
      option = sys.argv[1][1:]
      if option == 'z' or option == 'zip':
        dirpath = sys.argv[2]
        zipdirpath = sys.argv[3]
        zip_dir(dirpath, zipdirpath)
      elif option == 'u' or option == 'unzip':
        zipfilepath = sys.argv[2]
        unzipdirpath = sys.argv[3]
        unzip_dir(zipfilepath, unzipdirpath)
      else:
        print_help(sys.argv[0])
        sys.exit()
    else:
      print_help(sys.argv[0])
      sys.exit()
