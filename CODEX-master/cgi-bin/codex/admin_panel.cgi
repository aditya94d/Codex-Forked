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

print("<!DOCTYPE html><html><head><title>Admin Panel</title></head>")

if len(a) != 1:
	print("""<body><h2 style="color:darkred; text-align:center"><br/><br/>You are trying to access the ADMIN PANEL without AUTHORIZATION</h2></body></html>""")
	conn.close()
	exit(0)

print("""<body><h2 style="color:darkgreen; text-align:center"><br/><br/>Welcome to ADMIN PANEL""")
print("""<br/><br/> <a href="create_contest.cgi">Create Contest</a><br/><br/> 
					<a href="upload_question.cgi">Upload Question</a><br/><br/>
					<a href="admin_console.cgi">Admin CONSOLE</a><br/><br/>
					<a href="manage_problems.cgi">Manage Problems</a><br/><br/>
					<a href="home.cgi">Home</a><br/><br/></h2>""")
print('</body></html>')





