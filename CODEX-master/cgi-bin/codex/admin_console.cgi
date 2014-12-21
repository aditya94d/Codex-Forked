#!C:/python33/python.exe -u
print("Content-type:text/html\n\n")

import cgi,cgitb
import oursql as sql
from os import environ
import sys
import os
import json
import math
import random

session_id='None'
user_name = None

try:
	for cookie in environ['HTTP_COOKIE'].split(';'):
		(key, value ) = cookie.split('=');
		if key == "session_id":
			session_id = value
except:
	user_name = None
	
conn = sql.connect(host='localhost', user='gnsp', passwd='mockingbird', db='codex')
cur = conn.cursor(sql.DictCursor)

cur.execute("SELECT login_data.user_name AS user_name FROM session_info INNER JOIN login_data ON session_info.user_id=login_data.user_id WHERE session_id ='"+str(session_id)+"';",())
x=cur.fetchall()

if len(x):
	user_name = str(x[0]['user_name'])

cur.execute("SELECT user_id FROM admin_info WHERE user_name = '"+user_name+"';",())
a=cur.fetchall()

print("""<!DOCTYPE html>
<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>ADMIN CONSOLE</title>
<link rel="stylesheet" type="text/css" href="/css/admin_console.css"/>
<link href="/SpryAssets/SpryMenuBarVertical.css" rel="stylesheet" type="text/css" />
<script src="/SpryAssets/SpryMenuBar.js" type="text/javascript"></script>
</head>""")


if len(a) != 1:
	print("""<body><h2 style="color:darkred; text-align:center"><br/><br/>You are trying to access the ADMIN PANEL without AUTHORIZATION</h2></body></html>""")
	conn.close()
	exit(0)

form = cgi.FieldStorage()

command = 'nop'
if form.getvalue('comm') != None:
	command=str(form.getvalue('comm'))
	
Content = '> '+command+'\n\n'
cmd_list = command.split('# ')
if cmd_list[0] == 'FILE':
	Content += str(open(cmd_list[1],'r').read()).replace('>','&gt;').replace('<','&lt;')
	Content +='\n\n'
	Content += ('-'*110)
	Content +='\n\n'
	
elif cmd_list[0] == 'SQL':
	cur.execute(cmd_list[1],())
	if cmd_list[1].split()[0] == 'SELECT' or cmd_list[1].split()[0] == 'select':
		data = cur.fetchall()
		for a in data:
			val = [str(key)+':'+str(a[key]) for key in a]
			Content += '\t'.join(val)
			Content += '\n'
	Content +='\nQUERY EXECUTED SUCCESSFULLY ...  ...  ...\n'
	Content += ('-'*110)
	Content +='\n\n'
	
elif cmd_list[0] == 'PYTHON':
	sys.stdout=open('E:\\CODEX_SITE\\cgi-bin\\codex\\python_log.glog','w')
	try:
		eval(cmd_list[1])
	except:
		print('\nERROR OCCURED... ... ...')
	sys.stdout=sys.__stdout__
	output = open('E:\\CODEX_SITE\\cgi-bin\\codex\\python_log.glog','r').read()
	Content += output
	Content +='\nQUERY EXECUTED SUCCESSFULLY ...  ...  ...\n'
	Content += ('-'*110)
	Content +='\n\n'
	
elif cmd_list[0] == 'COMMENT':
	Content +='\n'+cmd_list[1]+'\n'
	Content += ('-'*110)
	Content +='\n\n'

elif cmd_list[0] == 'CLEAR':
	command_log = open('E:\\CODEX_SITE\\cgi-bin\\codex\\command_log.glog','w')
	command_log.close()
	Content = ''
	
else:
	Content +='\nBAD COMMAND OR FILE NAME ...  ...  ...\n'
	Content += ('-'*110)
	Content +='\n\n'
	
command_log = open('E:\\CODEX_SITE\\cgi-bin\\codex\\command_log.glog','r+')
oldContent = command_log.read()
Content = Content+'\n'+oldContent
command_log.write(Content)
command_log.close()

print("<body>")

print(""" <div id="header">""")
print("""<div class="text1" id="Name_of_participant"><b><a style="color:rgb(170,170,170)" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'" href="admin_panel.cgi">ADMIN PANEL</a></b></div>""")

print("""<div id="message" class="text2" style="color:yellowgreen"><b>
<form action="admin_console.cgi" method="post">
<label for="comm">COMMAND: </label><input type="text" name="comm" id="comm" style="width:750px" />
<input name="Submit" type="submit" id="Submit" value="SEND" /></form>
</b></div>""")
	
print('</div>')

print("""<div id="apDiv2">
	 <p class="text1">&nbsp;</p>
	 <p class="text1">&nbsp;</p>
	 <pre style="margin-left:30px;margin-right:30px; font-size:18px">{text}</pre></div></body></html>""".format(text=Content))
	 
conn.close()