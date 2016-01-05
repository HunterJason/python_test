#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'jasonhuang1029'

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.utils import parseaddr, formataddr
import smtplib
import mimetypes
import os, sys 


def callback(progress, total):
  percent = 100. * progress / total
  sys.stdout.write('\r')
  sys.stdout.write('%s bytes sent of %s [%2.0f%%]'%(progress, total, percent))
  sys.tdout.flush()
  if percent >= 100:
    sys.stdout.write('\n')

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send(files2send):
  from_addr = '18801799470@163.com'
  password = raw_input('%s\'s Password: '%from_addr)
  to_addr = 'jasonhuang1029@icloud.com'
  smtp_server = 'smtp.163.com'

  msg = MIMEMultipart()

  msg.attach(MIMEText('Hello, Master! This is from my python program,below is the attachment you need,please download it...\r\n\r\n', 'plain', 'utf-8'))
  msg['From'] = _format_addr('jasonhuang <%s>' % from_addr)
  msg['To'] = _format_addr('huangjie <%s>' % to_addr)
  msg['Subject'] = Header('recieve from my python program', 'utf-8').encode()

  for file_name in files2send:
    if not os.path.isfile(file_name):
      print '%s is not file, then next...'%file_name
      continue
    with open(file_name,'rb') as f:
      ctype,encoding = mimetypes.guess_type(file_name)
      if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
      maintype,subtype = ctype.split('/',1)
      basename = os.path.basename(file_name)
      mime = MIMEBase(maintype,subtype,filename=basename)
      mime.add_header('Content-Disposition','attachment',filename = basename)
      #mime.add_header('Content-ID','<0>')
      #mime.add_header('X-Attachment-ID','0')
      mime.set_payload(f.read())
      f.close()
      print 'sending %s...'%file_name
      encoders.encode_base64(mime)
      msg.attach(mime)
  try:
    server = smtplib.SMTP(smtp_server, 25)
    server.callback = callback
    server.set_debuglevel(0)#'0' 关闭调试 '1' 打开
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
  except Exception, e:
    print e
    sys.exit()

if __name__ == '__main__':
  if len(sys.argv) >= 2:
    list = []
    for i in range(1,len(sys.argv)):
      list.append(sys.argv[i])
    send(list)
  else:
    print 'no selected files to send'
    sys.exit()

