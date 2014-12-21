#!C:/python33/python.exe -u
print("Content-type:text/html\n\n")

import cgi, cgitb
from os import environ
import oursql as sql
import os

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

message=""

cgitb.enable()
form=cgi.FieldStorage()
try:
	pid = int(form.getvalue('add'))
	cur.execute('INSERT INTO practice_table VALUES('+str(pid)+');',())
	message = "PROBLEM ID : {id} was ADDED to Practice Successfully".format(id=str(pid))
except:
	pass
	
try:
	pid = int(form.getvalue('revoke'))
	cur.execute('DELETE FROM practice_table WHERE problem_id ='+str(pid)+';',())
	message = "Practice for PROBLEM ID : {id} was REVOKED Successfully".format(id=str(pid))
except:
	pass
	
try:
	pid = int(form.getvalue('del'))
	
	problem_directory_path = 'E:\\CODEX_SITE\\problems__\\'
	cur.execute("SELECT problem_code AS pc FROM problem_table WHERE problem_id ="+str(pid)+";",())
	m=cur.fetchall()
	q_code = str(m[0]['pc'])
	
	q_file_loc = problem_directory_path+q_code+'_statement.txt'
	in_1_loc = problem_directory_path+q_code+'_in_1.in'
	in_2_loc = problem_directory_path+q_code+'_in_2.in'
	in_3_loc = problem_directory_path+q_code+'_in_3.in'
	in_4_loc = problem_directory_path+q_code+'_in_4.in'
	in_5_loc = problem_directory_path+q_code+'_in_5.in'
	out_1_loc = problem_directory_path+q_code+'_out_1.out'
	out_2_loc = problem_directory_path+q_code+'_out_2.out'
	out_3_loc = problem_directory_path+q_code+'_out_3.out'
	out_4_loc = problem_directory_path+q_code+'_out_4.out'
	out_5_loc = problem_directory_path+q_code+'_out_5.out'
	editorial_loc = problem_directory_path+q_code+'_editorial.txt'
	
	os.remove(q_file_loc)
	os.remove(in_1_loc)
	os.remove(in_2_loc)
	os.remove(in_3_loc)
	os.remove(in_4_loc)
	os.remove(in_5_loc)
	os.remove(out_1_loc)
	os.remove(out_2_loc)
	os.remove(out_3_loc)
	os.remove(out_4_loc)
	os.remove(out_5_loc)
	os.remove(editorial_loc)
	
	cur.execute('DELETE FROM problem_table WHERE problem_id ='+str(pid)+';',())
	cur.execute('DELETE FROM practice_table WHERE problem_id ='+str(pid)+';',())
	message = "PROBLEM ID : {id} was DELETED Successfully".format(id=str(pid))
except:
	pass

print("""<body><h2 style="color:rgb(100,100,100); text-align:center">{m}</h2>""".format(m=message))
print("""<body><h2 style="color:darkgreen; text-align:center">""")
print("""<br/><br/> <a href="admin_panel.cgi">Admin Panel</a><br/><br/> 
					<a href="home.cgi">Home</a><br/><br/></h2>""")

cur.execute('SELECT problem_id AS id, problem_code AS pc, problem_name AS pn FROM problem_table ;',())
x=cur.fetchall()
print("""<table border="0" align="center" style="width:900px; color:#4A0A39; font-family:Arial; text-align:center; font-size:17px"><tr><th>PROBLEM CODE</th><th>PROBLEM NAME</th><th>ADD TO PRACTICE</th><th>REMOVE FROM PRACTICE</th><th>DELETE</th></tr>""")
for a in x:
	pid = int(a['id'])
	cur.execute('SELECT problem_id FROM practice_table WHERE problem_id = '+str(pid)+';')
	m=cur.fetchall()
	if len(m)==0:
		print("""<tr><td>"""+str(a['pc'])+"</td><td>"+str(a['pn'])+"""</td><td><a href="manage_problems.cgi?add="""+str(pid)+""" ">ADD</a></td><td></td><td><a href="manage_problems.cgi?del="""+str(pid)+""" ">DELETE</a></td></tr>""")
	else:
		print("""<tr><td>"""+str(a['pc'])+"</td><td>"+str(a['pn'])+"""</td><td></td><td><a href="manage_problems.cgi?revoke="""+str(pid)+""" ">REVOKE</a></td><td><a href="manage_problems.cgi?del="""+str(pid)+""" ">DELETE</a></td></tr>""")

print("</table></body></html>")
conn.close()