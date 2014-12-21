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
	height: 1100px;
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

print("""<form enctype="multipart/form-data" action="question_upload_confirmation.cgi" method="post" onsubmit="return uploadValidation()" >""")
print("""<h2 style="color:darkgreen; text-align:center; font-family:Arial">Upload Question</h2><p>&nbsp;</p>""")
print("""<p>      <label for="QCode">Question Code : </label>      <input type="text" name="QCode" id="QCode" />    </p>""")
print("""<p>      <label for="QName">Question Name : </label>      <input type="text" name="QName" id="QName" />    </p>""")
print("""<p>      <label for="QFile">Problem Statement File : </label>      <input type="file" name="QFile" id="QFile" />    </p>""")
print('<p>&nbsp;</p>')
print("""<p>      <label for="InFile1">Input File(1) : </label>      <input type="file" name="InFile1" id="InFile1" />    </p>""")
print("""<p>      <label for="OutFile1">Output File(1) : </label>      <input type="file" name="OutFile1" id="OutFile1" />    </p>""")
print('<p>&nbsp;</p>')
print("""<p>      <label for="InFile2">Input File(2) : </label>      <input type="file" name="InFile2" id="InFile2" />    </p>""")
print("""<p>      <label for="OutFile2">Output File(2) : </label>      <input type="file" name="OutFile2" id="OutFile2" />    </p>""")
print('<p>&nbsp;</p>')
print("""<p>      <label for="InFile3">Input File(3) : </label>      <input type="file" name="InFile3" id="InFile3" />    </p>""")
print("""<p>      <label for="OutFile3">Output File(3) : </label>      <input type="file" name="OutFile3" id="OutFile3" />    </p>""")
print('<p>&nbsp;</p>')
print("""<p>      <label for="InFile4">Input File(4) : </label>      <input type="file" name="InFile4" id="InFile4" />    </p>""")
print("""<p>      <label for="OutFile4">Output File(4) : </label>      <input type="file" name="OutFile4" id="OutFile4" />    </p>""")
print('<p>&nbsp;</p>')
print("""<p>      <label for="InFile5">Input File(5) : </label>      <input type="file" name="InFile5" id="InFile5" />    </p>""")
print("""<p>      <label for="OutFile5">Output File(5) : </label>      <input type="file" name="OutFile5" id="OutFile5" />    </p>""")
print('<p>&nbsp;</p>')
print("""<p>      <label for="Editorial">Editorial : </label>      <input type="file" name="Editorial" id="Editorial" />    </p>""")
print(""" <p> <input name="Upload" type="submit" class="button" id="Upload" value="Upload" /> </p>""")
print('</form>')

print("""<script type="text/javascript">""")

print(""" function uploadValidation(){ 
				var qcode = document.getElementById("QCode").value;
				var qname = document.getElementById("QName").value;
				var qfile = document.getElementById("QFile").value;
				var in_1 = document.getElementById("InFile1").value;
				var out_1 = document.getElementById("OutFile1").value;
				var in_2 = document.getElementById("InFile2").value;
				var out_2 = document.getElementById("OutFile2").value;
				var in_3 = document.getElementById("InFile3").value;
				var out_3 = document.getElementById("OutFile3").value;
				var in_4 = document.getElementById("InFile4").value;
				var out_4 = document.getElementById("OutFile4").value;
				var in_5 = document.getElementById("InFile5").value;
				var out_5 = document.getElementById("OutFile5").value;
				var in_1 = document.getElementById("InFile1").value;
				var editorial = document.getElementById("Editorial").value;
				if(!qcode || !qname || !qfile || !in_1 || !out_1 || !in_2 || !out_2 || !in_3 || !out_3 || !in_4 || !out_4 || !in_5 || !out_5 || !editorial){
					return false;
				}
				return true;
			}""")
print('</script>')			

print('</body></html>')

conn.close()



