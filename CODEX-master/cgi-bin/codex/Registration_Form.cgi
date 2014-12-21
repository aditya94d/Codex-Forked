#!C:/python33/python.exe -u
print("Content-type:text/html\n\n")

"""
	TO DO:
	------
	The Codex Version is to be implemented dynamically
"""
from os import environ
import cgi, cgitb
import oursql as sql

version = '7.0 Testing'

session_id='None'
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
if len(x)!=0:
	user_name = str(x[0]['user_name'])

	
print("""<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />""")
print("""<title>Register</title>""")

### CSS

print("""
<link rel="stylesheet" type="text/css" href="/css/Registration_Form.css"/>
<style type="text/css">
</style>
<link href="/SpryAssets/SpryMenuBarVertical.css" rel="stylesheet" type="text/css" />
<style type="text/css">
""")

print("#spacing_div {")
print("position: absolute;")
print("left: 186px;")
print("top: 829px;")
print("width: 852px;")
print("height: 178px;")
print("z-index: 8;")
print("}")
print("#apDiv4 {")
print("position: absolute;")
print("left: 276px;")
print("top: 662px;")
print("width: 221px;")
print("height: 17px;")
print("z-index: 9;")
print("}")
print("""</style><script src="/SpryAssets/SpryMenuBar.js" type="text/javascript"></script></head>""")

### END OF CSS and HEAD


print("<body>")
print("""<div id="logo"><img src="/images/codex_logo.jpg" border="0" alt="image"></div>""")

print(""" <div id="header">""")
print("""<div class="text1" id="Name_of_participant"><b style="color:rgb(170,170,170)">GO BACK TO <a style="color:rgb(170,170,170)" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'"  href="home.cgi">HOME</a></b> </div>""")
print('</div>')
	
print("""<div id="Title_text"><h1 style="font-size: 2.5em; margin-top: 0px; color: rgb(0, 0, 0); font-family: Arial, sans-serif; font-style: normal; font-variant: normal; letter-spacing: normal; line-height: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255);">""")
print("REGISTER")
print("</h1></div>")

# home.cgi  --> home
# schedule.cgi --> Contests
# rules.cgi --> Rules
# past_contests.cgi --> practice
#score_board.cgi --> Score Board

print("""<div id="apDiv1">  <ul id="MenuBar1" class="MenuBarVertical"><li><a  href="home.cgi">Home</a></li><li><a href="schedule.cgi">Contests</a></li><li><a href="rules.cgi">Rules</a> </li><li><a href="past_contests.cgi">Practice</a></li><li><a href="score_board.cgi">Score Board</a></li></ul></div>""")

## REGISTRATION FORM
print("""<div id="apDiv2">      <div class="text1" id="div_header" >
									<div align="center" style="color:rgb(200,200,200);margin-top:10px"><b>REGISTRATION</b></div>
								</div> 
								<p>&nbsp;</p>    
								<p>&nbsp;</p>""")
print("""<form action="registration_confirmation.cgi" method="post" onsubmit="return passValidation()" >""")
print("""<p>      <label for="Name">Name : </label>      <input type="text" name="Name" id="Name" />    </p>""")
print("""<p>      <label for="Username">Username : </label>      <input type="text" name="Username" id="Username" />    </p>""")
print("""<p>	<label for="E-Mail">E-Mail :  </label>    <input type="email" name="E-Mail" id="E-Mail" />	</p>""")
print("""<p>      <label for="Institute">Institute :   </label>      <input type="text" name="Institute" id="Institute" />    </p>""")
print(""" <p>      <label for="Password"  >Password :</label>      <input type="password" name="Password" id="Password" />    </p>""")
print("""<p>	<label for="Retype Password">Retype Password :</label>    <input type="password" name="Retype Password" id="Retype Password" />	</p>""")
print(""" <p> <input name="Register" type="submit" class="reg_button" id="Register" value="Register" /> </p>""")
print("</form></div>")

print("""<div id="horizontal_line"><hr/></div>    <div id="line2"><hr/></div>     <div id="spacing_div"></div>""")


### JAVASCRIPT

print("""<script type="text/javascript">""")
print("""var MenuBar1 = new Spry.Widget.MenuBar("MenuBar1", {imgRight:"SpryAssets/SpryMenuBarRightHover.gif"});""")

print("function passValidation() {")
print("""    var pass1 = document.getElementById("Password").value;""")
print("""    var pass2 = document.getElementById("Retype Password").value;""")
print("""	 var user_name = document.getElementById("Username").value;""")
print("""	 var email = document.getElementById("E-Mail").value;""")
print("""    var ok = true;""")
print("""	 if(!user_name) {ok = false; document.getElementById("Username").style.borderColor = "#E34234";}""")
print("""	 if(!email) {ok = false; document.getElementById("E-Mail").style.borderColor = "#E34234";}""")
print("""    if (pass1 != pass2 || !pass1) {""")
print("""        document.getElementById("Password").style.borderColor = "#E34234";""")
print("""        document.getElementById("Retype Password").style.borderColor = "#E34234";""")
print("""        ok = false;""")
print("""    }""")
print("""    return ok;""")
print("}")

print("</script>")
print("<p></p>")

print("""<div id="footer"><p style="text-align:center; color:rgb(170,170,170);font-family:Arial">Copyright &copy; 2014, All rights reserved, Design By <a style="color:rgb(170,170,170)" href="https://www.facebook.com/aditya.dash.520" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'">Aditya Dash</a>, Site By <a style="color:rgb(170,170,170)" href="https://www.facebook.com/sharpandsage" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'">Ganesh Prasad</a></p></div>
""")

print(" </body></html>")

conn.close()