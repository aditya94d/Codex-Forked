#!C:/python33/python.exe -u
print("Content-type:text/html\n\n")

import time
import cgi,cgitb
import oursql as sql
from os import environ
from datetime import datetime

#cgitb.enable()

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

conn = sql.connect(host='localhost', user='gnsp', passwd='mockingbird', db='codex')
cur = conn.cursor(sql.DictCursor)

cur.execute("SELECT login_data.user_name AS user_name FROM session_info INNER JOIN login_data ON session_info.user_id=login_data.user_id WHERE session_id ='"+str(session_id)+"';",())
x=cur.fetchall()

if len(x):
	user_name = str(x[0]['user_name'])

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
print('</div>')


print("""<div id="Title_text">
  <h1 style="font-size: 2.5em; margin-top: 0px; color: rgb(50, 50, 20); font-family: Arial, sans-serif; font-style: normal; font-variant: normal; letter-spacing: normal; line-height: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255);">Contests</h1>
</div>""")

print("""<div id="apDiv1">
  <ul id="MenuBar1" class="MenuBarVertical">
    <li><a  href="home.cgi">Home</a></li>
    <li><a href="schedule.cgi">Contests</a></li>
    <li><a href="rules.cgi">Rules</a> </li>
    <li><a href="past_contests.cgi">Practice</a></li>
	<li><a href="score_board.cgi">Score Board</a></li>
</ul>
</div>""")

print("""<div id="apDiv2">
  <div class="text1" id="div_header" >
	<div align="center" style="color:rgb(200,200,200);margin-top:10px"><b>CONTESTS</b></div>
	</div>
  <p class="text2">&nbsp;</p>
  <p class="text2">""")

cur.execute('SELECT codex_version, begin_time_y, begin_time_m, begin_time_d,begin_time_hr,begin_time_min,end_time_y,end_time_m,end_time_d,end_time_hr,end_time_min FROM codex_table ORDER BY codex_version DESC;',())
x=cur.fetchall()

now = datetime.now()

def timeLine(begin,end):
	if begin<=now and end >= now:
		return """<b><a style="color:green">Running</a></b>"""
	elif begin > now:
		return """<b><a style="color:blue">Future</a></b>"""
	else:
		return """<b><a style="color:Red">Past</a></b>"""
  
print("""<table border="0" align="center" style="width:700px; color:#4A0A39; font-family:Arial; text-align:center; font-size:17px"><tr><th>CONTEST</th><th>BEGINS</th><th>ENDS</th><th>REMARK</th></tr>""")
for a in x:
	begin_time_y = int(a['begin_time_y'])
	begin_time_m = int(a['begin_time_m'])
	begin_time_d = int(a['begin_time_d'])
	begin_time_hr = int(a['begin_time_hr'])
	begin_time_min = int(a['begin_time_min'])
	end_time_y = int(a['end_time_y'])
	end_time_m = int(a['end_time_m'])
	end_time_d = int(a['end_time_d'])
	end_time_hr = int(a['end_time_hr'])
	end_time_min = int(a['end_time_min'])
	
	codex_version = str(a['codex_version'])
	
	beginTime = datetime(begin_time_y, begin_time_m, begin_time_d, begin_time_hr, begin_time_min)
	endTime = datetime(end_time_y, end_time_m, end_time_d, end_time_hr, end_time_min)
	
	if now >= beginTime and now <= endTime:
		print("""<tr><td><a href = "activity.cgi?mode=contest">CODEX """+codex_version+".0 </a></td><td>"+beginTime.strftime('%Y-%m-%d %H:%M')+"</td><td>"+endTime.strftime('%Y-%m-%d %H:%M')+"</td><td>"+timeLine(beginTime,endTime)+"</td></tr>")
	if now < beginTime:
		print("""<tr><td>CODEX """+codex_version+".0</td><td>"+beginTime.strftime('%Y-%m-%d %H:%M')+"</td><td>"+endTime.strftime('%Y-%m-%d %H:%M')+"</td><td>"+timeLine(beginTime,endTime)+"</td></tr>")
	if now > endTime:
		print("""<tr><td><a href = "score_board.cgi?cdx_ver="""+codex_version+""" ">CODEX """+codex_version+".0 </a></td><td>"+beginTime.strftime('%Y-%m-%d %H:%M')+"</td><td>"+endTime.strftime('%Y-%m-%d %H:%M')+"</td><td>"+timeLine(beginTime,endTime)+"</td></tr>")
print("</table>")
  
print("""  
  </p>
  <p class="text1">&nbsp;</p>
</div>
""")

print("""<div id="horizontal_line"><hr/></div>
<div id="line2"><hr/></div>""")

print("""<div id="footer"><p style="text-align:center; color:rgb(170,170,170);font-family:Arial">Copyright &copy; 2014, All rights reserved, Design By <a style="color:rgb(170,170,170)" href="https://www.facebook.com/aditya.dash.520" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'">Aditya Dash</a>, Site By <a style="color:rgb(170,170,170)" href="https://www.facebook.com/sharpandsage" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'">Ganesh Prasad</a></p></div>
""")

print("""
<div id="spacing_div"></div>
<script type="text/javascript">
var MenuBar1 = new Spry.Widget.MenuBar("MenuBar1", {imgRight:"SpryAssets/SpryMenuBarRightHover.gif"});
</script>
<p></p>
</body>
</html>""")

conn.close()