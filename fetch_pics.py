#!/usr/bin/env python
# coding=utf-8

__authort__ = 'jasonhuang1029'

import os, re
import shutil
from os.path import join, getsize
import sys

save_dir = '/tmp/pics/'

def fetch_pics(dst_dir):
  if os.path.isdir(dst_dir) == 0:
    print dst_dir + ' is not dirctory'
    return
  if os.path.exists(save_dir) == 0:
    os.mkdir(save_dir)
  num = 0
  re_file = re.compile('.*\.jpg')
  for root, dirs, files in os.walk(dst_dir):
    for name in files:
      path_name = join(root, name)
      if os.path.isfile(path_name):
        re_files = re_file.findall(path_name)
        if len(re_files) == 1:
          #print re_files
          try:
            num = num + getsize(re_files[0])
            if num < 3000000000:
              shutil.copy(re_files[0], save_dir)
            else:
              print 'pics is over 3000000000 byte'
              break
          except:
              print 'error'
              pass
  print 'files saved in ' + save_dir + ' ,total size is: %d byte'%num
if __name__ == '__main__':
    if len(sys.argv) == 2:
      fetch_pics(sys.argv[1])
