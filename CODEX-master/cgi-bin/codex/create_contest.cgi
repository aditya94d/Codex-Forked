#!C:/python33/python.exe -u
print("Content-type:text/html\n\n")

import cgi,cgitb
import oursql as sql
from os import environ

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

print("<!DOCTYPE html><html><head><title>Admin Panel</title>")

print("""
<style type="text/css">
form
{
	left: 185px;
	top: 300px;
	width: 756px;
	height: 1300px;
	z-index: 3;
	color: #333;
	background-color: #bbbbbb;
	-webkit-border-radius: 15px;
	-moz-border-radius: 15px;
	border-radius: 15px;
	bottom: 200px;
	position: absolute;
	clear: none;
	padding-left: 100px;
}
p
{
	font-family:Arial;
	font-size:20px;
	text-align:left;
}
</style></head>
""")

if len(a) != 1:
	print("""<body><h2 style="color:darkred; text-align:center"><br/><br/>You are trying to access the ADMIN PANEL without AUTHORIZATION</h2></body></html>""")
	conn.close()
	exit(0)

print("""<body><h2 style="color:darkgreen; text-align:center">""")
print("""<br/><br/> <a href="admin_panel.cgi">Admin Panel</a><br/><br/> 
					<a href="home.cgi">Home</a><br/><br/></h2>""")

print("""<form  action="create_contest_confirmation.cgi" method="post" onsubmit="return uploadValidation()" >""")
print("""<h2 style="color:darkgreen; text-align:center; font-family:Arial">CREATE CONTEST</h2><p>&nbsp;</p>""")
print("""<p>      <label for="CdxVer">Codex Version : </label>      <input type="text" name="CdxVer" id="CdxVer" />    </p>""")
print("""<p>      <label for="CdxTag">Tag Line : </label>      <input type="text" name="CdxTag" id="CdxTag" />    </p>""")
print("<p>	  &nbsp;<h3>Begin Time<br/></h3></p>")
print("""<p>      <label for="BeginYear">Year : </label>      <input type="text" name="BeginYear" id="BeginYear" />    </p>""")
print("""<p>      <label for="BeginMonth">Month : </label>      <input type="text" name="BeginMonth" id="BeginMonth" />    </p>""")
print("""<p>      <label for="BeginDay">Date : </label>      <input type="text" name="BeginDay" id="BeginDay" />    </p>""")
print("""<p>      <label for="BeginHour">Hour : </label>      <input type="text" name="BeginHour" id="BeginHour" />    </p>""")
print("""<p>      <label for="BeginMinute">Minute : </label>      <input type="text" name="BeginMinute" id="BeginMinute" />    </p>""")
print("<p>	  &nbsp;<h3>End Time<br/></h3></p>")
print("""<p>      <label for="EndYear">Year : </label>      <input type="text" name="EndYear" id="EndYear" />    </p>""")
print("""<p>      <label for="EndMonth">Month : </label>      <input type="text" name="EndMonth" id="EndMonth" />    </p>""")
print("""<p>      <label for="EndDay">Date : </label>      <input type="text" name="EndDay" id="EndDay" />    </p>""")
print("""<p>      <label for="EndHour">Hour : </label>      <input type="text" name="EndHour" id="EndHour" />    </p>""")
print("""<p>      <label for="EndMinute">Minute : </label>      <input type="text" name="EndMinute" id="EndMinute" />    </p>""")
print("<p>	  &nbsp;<h3>Questions<br/></h3></p>")
print("""<p>      <label for="Q1_code">Problem 1 Code : </label>      <input type="text" name="Q1_code" id="Q1_code" />
					<label for="Q1_val">Value (in Scale of 10) : </label>      <input type="text" name="Q1_val" id="Q1_val" />   </p>""")
print("""<p>      <label for="Q2_code">Problem 2 Code : </label>      <input type="text" name="Q2_code" id="Q2_code" />
					<label for="Q2_val">Value (in Scale of 10) : </label>      <input type="text" name="Q2_val" id="Q2_val" /></p>""")
print("""<p>      <label for="Q3_code">Problem 3 Code : </label>      <input type="text" name="Q3_code" id="Q3_code" />
				<label for="Q3_val">Value (in Scale of 10) : </label>      <input type="text" name="Q3_val" id="Q3_val" />	</p>""")
print("""<p>      <label for="Q4_code">Problem 4 Code : </label>      <input type="text" name="Q4_code" id="Q4_code" />
					<label for="Q4_val">Value (in Scale of 10) : </label>      <input type="text" name="Q4_val" id="Q4_val" /></p>""")
print('<p>&nbsp;</p>')
print(""" <p> <input name="Submit" type="submit" class="button" id="Submit" value="Submit" /> </p>""")
print('</form>')

print("""<script type="text/javascript">""")

print(""" function uploadValidation(){ 
				var ver = document.getElementById("CdxVer").value;
				var tag = document.getElementById("CdxTag").value;
				
				var b_yr = document.getElementById("BeginYear").value;
				var b_mn = document.getElementById("BeginMonth").value;
				var b_dy = document.getElementById("BeginDay").value;
				var b_hr = document.getElementById("BeginHour").value;
				var b_mi = document.getElementById("BeginMinute").value;
				
				var e_yr = document.getElementById("EndYear").value;
				var e_mn = document.getElementById("EndMonth").value;
				var e_dy = document.getElementById("EndDay").value;
				var e_hr = document.getElementById("EndHour").value;
				var e_mi = document.getElementById("EndMinute").value;
				
				var q1 = document.getElementById("Q1_code").value;
				var q2 = document.getElementById("Q2_code").value;
				var q3 = document.getElementById("Q3_code").value;
				var q4 = document.getElementById("Q4_code").value;
				
				var q1v = document.getElementById("Q1_val").value;
				var q2v = document.getElementById("Q2_val").value;
				var q3v = document.getElementById("Q3_val").value;
				var q4v = document.getElementById("Q4_val").value;
				
				if(!ver || !tag || !b_yr || !b_mn || !b_dy || !b_hr || !b_mi || !e_yr || !e_mn || !e_dy || !e_hr || !e_mi || !q1 || !q2 || !q3 || !q4 || !q1v || !q2v || !q3v || !q4v){
					return false;
				}
				return true;
			}""")
print('</script>')			

print('</body></html>')


