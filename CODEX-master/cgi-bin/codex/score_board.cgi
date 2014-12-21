#!C:/python33/python.exe -u
print("Content-type:text/html\n\n")

import time
import cgi,cgitb
import oursql as sql
from os import environ
from datetime import datetime
import json

cgitb.enable()

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

cur.execute("SELECT max(codex_version) AS res FROM codex_table;",())
x=cur.fetchall()

cdx_ver=0
if len(x) > 0:
	if x[0]['res'] != None:
		cdx_ver = int(x[0]['res'])
	
form=cgi.FieldStorage()
try:
	cdx_ver = int(float(form.getvalue('cdx_ver')))
except:
	pass
	
score_board_dict = {}
score_board_str = None
if cdx_ver != None:
	cur.execute(" SELECT scoreboard_loc FROM codex_table WHERE codex_version={v};".format(v=cdx_ver),())
	data=cur.fetchall()
	
	if len(data) > 0:
		scoreboard_loc = str(data[0]['scoreboard_loc'])
		score_board_file = open(scoreboard_loc,'r')
		score_board_str = score_board_file.read()
		score_board_dict = json.loads(score_board_str)
		score_board_file.close()
	else:
		pass
	
print("""<!DOCTYPE html>
<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Contests</title>
<link rel="stylesheet" type="text/css" href="/css/DBMS_FE2.css"/>
<link href="/SpryAssets/SpryMenuBarVertical.css" rel="stylesheet" type="text/css" />
<script src="/SpryAssets/SpryMenuBar.js" type="text/javascript"></script>
</head>""")

print("""<body>
<div id="logo"><img src="/images/codex_logo.jpg" width="150" height="56" alt="image" /></div>""")

print(""" <div id="header">""")
if user_name != None:
	print("""<div class="text1" id="Name_of_participant"><b style="color:rgb(170,170,170)">Logged in as : """+user_name+""" (<a style="color:rgb(170,170,170)" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'"  href="saybye.cgi">logout</a>)</b> </div>""")
else:
	print("""<div class="text1" id="Name_of_participant"><b style="color:rgb(170,170,170)">Not Logged in ... <a style="color:rgb(170,170,170)" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'" href="login.cgi">login or register</a></b></div>""")

print("""<div id="message" class="text2" style="color:yellowgreen;"><b>
<form action="score_board.cgi" method="post">
<label for="cdx_ver">SEARCH CODEX VERSION: </label><input type="text" name="cdx_ver" id="cdx_ver" />
<input name="Submit" type="submit" class="reg_button" id="Submit" value="SUBMIT" /></form>
</b></div>""")
	
print('</div>')

print("""<div id="Title_text">
  <h1 style="font-size: 2.5em; margin-top: 0px; color: rgb(0, 0, 0); font-family: Arial, sans-serif; font-style: normal; font-variant: normal; letter-spacing: 10px; line-height: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255);">SCORE BOARD : CODEX {v}.0</h1>
</div>""".format(v=cdx_ver))

print("""<div id="apDiv1">
  <ul id="MenuBar1" class="MenuBarVertical">
    <li><a  href="home.cgi">Home</a></li>
    <li><a href="schedule.cgi">Contests</a></li>
    <li><a href="rules.cgi">Rules</a> </li>
    <li><a href="past_contests.cgi">Practice</a></li>
	<li><a href="score_board.cgi">Score Board</a></li>
</ul>
</div>""")


if score_board_str != None:
	print("""<div id="apDiv2">
	  <div class="text1" id="div_header" >
		<div align="center" style="color:rgb(200,200,200);margin-top:10px"><b>SCORE BOARD</b></div>
		</div>
	  <p class="text2">&nbsp;</p>
	  <table border="0" align="center" style="width:700px; color:#4A0A39; font-family:Arial; text-align:center; font-size:17px">
		<tr><th>RANK</th><th>USER NAME</th><th>SCORE</th></tr>""")

	score_list=[]
	for key in score_board_dict:
		if key[-10:]=='_____score':
			score_list.append((key[:-10],score_board_dict[key]))
	scoreList = sorted(score_list,key=lambda x:x[1],reverse=True)
	
	for i in range(len(scoreList)):
		if scoreList[i][0]==user_name:
			print("""<tr style="color:green"><th>"""+str(i+1)+"</th><th>"+scoreList[i][0]+"</th><th>"+str(scoreList[i][1])+"</th></tr>")
		else:
			print("<tr><td>"+str(i+1)+"</td><td>"+scoreList[i][0]+"</td><td>"+str(scoreList[i][1])+"</td></tr>")
	
	print("</table>")
	print('<p>&nbsp;</p>')
	print('</div>')
	
else:
	print("""<div id="apDiv2">
	  <div class="text1" id="div_header" >
		<div align="center" style="color:orangered;margin-top:10px"><b>NO DATA FOUND</b></div>
		</div></div>""")
		
print("""<div align="right"></div>
		<div id="horizontal_line"><hr/></div>
		<div id="line2"><hr/></div>
		<div id="footer"><p style="text-align:center; color:rgb(170,170,170);font-family:Arial">Copyright &copy; 2014, All rights reserved, Design By <a style="color:rgb(170,170,170)" href="https://www.facebook.com/aditya.dash.520" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'">Aditya Dash</a>, Site By <a style="color:rgb(170,170,170)" href="https://www.facebook.com/sharpandsage" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'">Ganesh Prasad</a></p></div>
		</body></html>""")
		
