#!C:/python33/python.exe -u

import time
import cgi,cgitb
import oursql as sql
from os import environ
import hashlib

version = '7.0 Testing'
session_id='None'
user_name = None

try:
	for cookie in environ['HTTP_COOKIE'].split(';'):
		(key, value ) = cookie.split('=');
		if key == "session_id":
			session_id = value
except:
	user_name = None

	
form = cgi.FieldStorage()
new_user_name = form.getvalue('Username')
new_password = form.getvalue('Password')

conn = sql.connect(host='localhost', user='gnsp', passwd='mockingbird', db='codex')
cur = conn.cursor(sql.DictCursor)

if new_user_name and new_password:
	cur.execute("SELECT user_id FROM login_data WHERE user_name = '"+str(new_user_name)+"' AND password = '"+str(new_password)+"';",())
	x=cur.fetchall()

	user_id = None
	if len(x)!=0:
		user_id = int(x[0]['user_id'])
		cur.execute("DELETE FROM session_info WHERE user_id = "+str(user_id)+";",())
		session_id = str(hashlib.md5(str.encode(repr(time.time())+new_user_name)).hexdigest())
		cur.execute('INSERT INTO session_info VALUES (?,?,?);',(user_id,new_user_name,session_id))
		print("Set-Cookie:session_id={val};".format(val=session_id))
		print("Set-Cookie:path=/;")
		
cur.execute("SELECT login_data.user_name AS user_name FROM session_info INNER JOIN login_data ON session_info.user_id=login_data.user_id WHERE session_id ='"+str(session_id)+"';",())
x=cur.fetchall()

if len(x):
	user_name = str(x[0]['user_name'])	
	
print("Content-type:text/html\n\n")
print("<!DOCTYPE html><html><head>")
print("""
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Home</title>

<link rel="stylesheet" type="text/css" href="/css/DBMS_FE.css"/>
<style type="text/css">
</style>
<link href="/SpryAssets/SpryMenuBarVertical.css" rel="stylesheet" type="text/css" />
<style type="text/css">
body {
	margin-bottom: 400px;
}
#apDiv4 {
	position: absolute;
	left: 214px;
	top: 613px;
	width: 481px;
	height: 136px;
	z-index: 9;
}
</style>
<script src="/SpryAssets/SpryMenuBar.js" type="text/javascript"></script>
</head>""")

print("""<body>
<div id="logo">
<img src="/images/codex_logo.jpg" width="150" height="56" alt="image" />
</div>""")

print(""" <div id="header">""")
if user_name != None:
	print("""<div class="text1" id="Name_of_participant"><b style="color:rgb(170,170,170)">Logged in as : """+user_name+""" (<a style="color:rgb(170,170,170)" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'"  href="saybye.cgi">logout</a>)</b> </div>""")
else:
	print("""<div class="text1" id="Name_of_participant"><b style="color:rgb(170,170,170)">Not Logged in ... <a style="color:rgb(170,170,170)" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'" href="login.cgi">login or register</a></b></div>""")
print('</div>')

print("""<div id="Title_text">
  <h1 style="font-size: 2.5em; margin-top: 0px; color: rgb(0, 10, 20); font-family: Arial, sans-serif; font-style: normal; font-variant: normal; letter-spacing: normal; line-height: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255);">CODEX</h1>
</div>""")

print("""<div id="apDiv1">
  <ul id="MenuBar1" class="MenuBarVertical">
    <li><a  href="home.cgi">Home</a></li>
    <li><a href="schedule.cgi">Contests</a></li>
    <li><a href="rules.cgi">Rules</a> </li>
    <li><a href="past_contests.cgi">Practice</a></li>
	<li><a href="score_board.cgi">Score Board</a></li>
</ul>
</div>
<div id="apDiv4"></div>
<div align="center">""")

welcome_title = ' ABOUT CODEX'
welcome_text = 'CODEX is an initiative towards the initiation and propagation of a healthy Coding Culture among the students of National Institute of Technology, Rourkela. We are to host short Coding contests every week, so that people can practice and gain confidence to participate in various coding contests like Google Code Jam and ACM ICPC etc. '

print("""</div>
<div id="Contest_Description">
    <div class="text1" id="div_header" >
	<div align="center" style="color:rgb(200,200,200);margin-top:10px"><b>{welcomeTitle}</b></div>
	</div>
	<p align="center" class="text2">&nbsp;</p>
  <p align="center" class="text2">
  {welcomeText}
  </p>
</div>
<div align="center"></div>""".format(welcomeTitle = welcome_title, welcomeText = welcome_text))

if user_name == None:
	print("""<div id="register_box">
	  <div class="text1" id="div_header" >
	<div align="center" style="color:yellowgreen;margin-top:10px"><b>REGISTRATION</b></div>
	</div>
	  <div align="center"><p>&nbsp;</p></div>
	  <form  action="Registration_Form.cgi" id="form1" name="form1" method="post" >
		<div align="center" >
		  <input type="submit" name="register_button" class="reg_button" value="Register"  />
		</div>
	  </form>
	  <form  action="login.cgi" id="form2" name="form2" method="post" >
		<p>
		  <input name="Login" type="submit" class="reg_button" id="Login" value="Sign In" />
		</p>
	  </form>
	  <p align="center">&nbsp;</p>
	  <div align="center"></div></div>""")
else:
	print("""<div id="register_box">
	  <div class="text1" id="div_header" >
	<div align="center" style="color:yellow;margin-top:10px"><b>LOGGED IN</b></div>
	</div>
	  <div align="center"><p>&nbsp;</p></div>
	  <form  action="schedule.cgi" id="form1" name="form1" method="post" >
		<div align="center" >
		  <input type="submit" name="register_button" class="reg_button" value="Participate"  />
		</div>
	  </form>
	  <form  action="past_contests.cgi" id="form2" name="form2" method="post" >
		<p>
		  <input name="Login" type="submit" class="reg_button" id="Login" value="Practice" />
		</p>
	  </form>""")
	cur.execute("SELECT user_id FROM admin_info WHERE user_name = '"+user_name+"';",())
	a=cur.fetchall()
	if len(a) == 1:
		print("""<form  action="admin_panel.cgi" id="form2" name="form2" method="post" >
		<p>
		  <input name="Login" type="submit" class="reg_button" id="Login" value="Admin Panel" />
		</p>
	  </form>""")
	print("""
	  <p align="center">&nbsp;</p>
	  <div align="center"></div></div>""")

  
print("""<div align="right">
</div>
<div id="horizontal_line"><hr/></div>
<div id="line2"><hr/></div>""")

print("""<script type="text/javascript">
var MenuBar1 = new Spry.Widget.MenuBar("MenuBar1", {imgRight:"SpryAssets/SpryMenuBarRightHover.gif"});
</script>""")

print("""<div id="footer"><p style="text-align:center; color:rgb(170,170,170);font-family:Arial">Copyright &copy; 2014, All rights reserved, Design By <a style="color:rgb(170,170,170)" href="https://www.facebook.com/aditya.dash.520" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'">Aditya Dash</a>, Site By <a style="color:rgb(170,170,170)" href="https://www.facebook.com/sharpandsage" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'">Ganesh Prasad</a></p></div>
""")

print("""</body>
</html>
""")

conn.close()