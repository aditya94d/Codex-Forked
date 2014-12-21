#!C:/python33/python.exe -u
print("Content-type:text/html\n\n")

import cgi,cgitb
import oursql as sql
import os
import json
from os import environ
import time
from datetime import datetime


score_directory_path = 'E:\\CODEX_SITE\\score__\\'

cgitb.enable()
form = cgi.FieldStorage()
ver = int(form.getvalue('CdxVer'))
tag = form.getvalue('CdxTag')
b_yr = int(form.getvalue('BeginYear'))
b_mn = int(form.getvalue('BeginMonth'))
b_dy = int(form.getvalue('BeginDay'))
b_hr = int(form.getvalue('BeginHour'))
b_mi = int(form.getvalue('BeginMinute'))
e_yr = int(form.getvalue('EndYear'))
e_mn = int(form.getvalue('EndMonth'))
e_dy = int(form.getvalue('EndDay'))
e_hr = int(form.getvalue('EndHour'))
e_mi = int(form.getvalue('EndMinute'))
q1 = form.getvalue('Q1_code')
q2 = form.getvalue('Q2_code')
q3 = form.getvalue('Q3_code')
q4 = form.getvalue('Q4_code')
q1v = int(form.getvalue('Q1_val'))
q2v = int(form.getvalue('Q2_val'))
q3v = int(form.getvalue('Q3_val'))
q4v = int(form.getvalue('Q4_val'))

b_time = datetime(b_yr,b_mn,b_dy,b_hr,b_mi)
e_time = datetime(e_yr,e_mn,e_dy,e_hr,e_mi)

b = float(time.mktime(b_time.timetuple()))
e = float(time.mktime(e_time.timetuple()))

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

print("""<body><h2 style="color:darkgreen; text-align:center">""")
print("""<br/><br/> <a href="admin_panel.cgi">Admin Panel</a><br/><br/> 
					<a href="home.cgi">Home</a><br/><br/></h2>""")


cur.execute("SELECT codex_id FROM codex_table WHERE codex_version = "+str(ver)+";")
x=cur.fetchall()

if len(x) != 0:
	print("""<h2 style="color:darkred; text-align:center"><br/><br/>Codex """+str(ver)+"""already exists</h2>""")
	print("</body></html>")
	conn.close()
	exit(0)
	
cur.execute("SELECT problem_id FROM problem_table WHERE problem_code = '"+str(q1)+"' OR problem_code = '"+str(q2)+"' OR problem_code = '"+str(q3)+"' OR problem_code = '"+str(q4)+"';")
x=cur.fetchall()

if len(x) != 4:
	print("""<h2 style="color:darkred; text-align:center"><br/><br/>Please provide 4 UNIQUE and EXISTING Problems  </h2>""")
	print("</body></html>")
	conn.close()
	exit(0)

score_loc = score_directory_path+'codex_'+str(ver)+'.scr'
open(score_loc,'w').write('{}')


cur.execute('SELECT MAX(codex_id) AS res FROM codex_table;',())
x=cur.fetchall()
try:
	cdx_id = int(x[0]['res'])+1
except:
	cdx_id = 0
	
cur.execute('INSERT INTO codex_table VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);',(cdx_id,ver,tag,b_yr,b_mn,b_dy,b_hr,b_mi,e_yr,e_mn,e_dy,e_hr,e_mi,q1,q2,q3,q4,q1v,q2v,q3v,q4v,b,e,score_loc))

print("""<h2 style="color:darkgreen; text-align:center"><br/><br/>Contest CREATED Successfully </h2>""")
print("</body></html>")

conn.close()