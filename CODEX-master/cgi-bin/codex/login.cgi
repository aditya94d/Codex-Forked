#!C:/python33/python.exe -u
print("Content-type:text/html\n\n")

import cgi,cgitb
import oursql as sql
from os import environ

version = '7.0 Testing'

session_id='None'
try:
	for cookie in environ['HTTP_COOKIE'].split(';'):
		(key, value ) = cookie.split('=');
		if key == "session_id":
			session_id = value
except:
	user_name = None
	
print("<!DOCTYPE html><html><head>")
print("""<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Login</title>
<link rel="stylesheet" type="text/css" href="/css/Login_Page.css"/>

<link href="/SpryAssets/SpryMenuBarVertical.css" rel="stylesheet" type="text/css" />
<style type="text/css">
#spacing_div {
	position: absolute;
	left: 186px;
	top: 829px;
	width: 852px;
	height: 178px;
	z-index: 8;
}
#apDiv4 {
	position: absolute;
	left: 276px;
	top: 662px;
	width: 221px;
	height: 17px;
	z-index: 9;
}
</style>
<script src="/SpryAssets/SpryMenuBar.js" type="text/javascript"></script>
</head>
""")

print("""<div id="logo">
<img src="/images/codex_logo.jpg" width="150" height="56" alt="image" />
</div>""")

print(""" <div id="header">""")
print("""<div class="text1" id="Name_of_participant"><b style="color:rgb(170,170,170)">GO BACK TO <a style="color:rgb(170,170,170)" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'"  href="home.cgi">HOME</a></b> </div>""")
print('</div>')

print("""<div id="Title_text">
  <h1>{contestName}</h1>
</div>""".format(contestName = 'LOG IN'))


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

print("""<div id="apDiv2">
	<div class="text1" id="div_header" >
		<div align="center" style="color:rgb(200,200,200);margin-top:10px"><b>LOG IN</b></div>
	</div>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
  <form action="home.cgi" method="post"  class="form_ele">
    <p>
      <label for="Username">Username : </label>
      <input type="text" name="Username" id="Username" />
    </p>
    <p>
      <label for="Password"  >Password :</label>
      <input type="password" name="Password" id="Password" />
    </p>
  <p>&nbsp;</p>
    <input name="Register" type="submit" class="reg_button" id="Register" value="Login" />
  </form>
</div>""")

print("""<div id="horizontal_line"><hr/></div>
<div id="line2"><hr/></div>""")

print("""<div id="spacing_div"></div>""")

print("""<div id="footer"><p style="text-align:center; color:rgb(170,170,170);font-family:Arial">Copyright &copy; 2014, All rights reserved, Design By <a style="color:rgb(170,170,170)" href="https://www.facebook.com/aditya.dash.520" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'">Aditya Dash</a>, Site By <a style="color:rgb(170,170,170)" href="https://www.facebook.com/sharpandsage" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'">Ganesh Prasad</a></p></div>
""")

print("""<script type="text/javascript">
var MenuBar1 = new Spry.Widget.MenuBar("MenuBar1", {imgRight:"SpryAssets/SpryMenuBarRightHover.gif"});
</script>
<p></p>
</html>""")
conn.close()