#!C:/python33/python.exe -u
print("Content-type:text/html\n\n")

import cgi,cgitb
import oursql as sql
import os
from os import environ

problem_directory_path = 'E:\\CODEX_SITE\\problems__\\'

cgitb.enable()
form = cgi.FieldStorage()
q_code = form.getvalue('QCode')
q_name = form.getvalue('QName')
q_file = form['QFile']
in_1 = form['InFile1']
out_1 = form['OutFile1']
in_2 = form['InFile2']
out_2 = form['OutFile2']
in_3 = form['InFile3']
out_3 = form['OutFile3']
in_4 = form['InFile4']
out_4 = form['OutFile4']
in_5 = form['InFile5']
out_5 = form['OutFile5']
editorial = form['Editorial']

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


cur.execute("SELECT problem_id FROM problem_table WHERE problem_code = '"+str(q_code)+"';")
x=cur.fetchall()

if len(x) != 0:
	print("""<h2 style="color:darkred; text-align:center"><br/><br/>Problem Code already exists... Give an Unique Problem Code</h2>""")
	print("</body></html>")
	conn.close()
	exit(0)

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

open(q_file_loc,'w').write(q_file.file.read().decode())
open(in_1_loc,'w').write(in_1.file.read().decode())
open(in_2_loc,'w').write(in_2.file.read().decode())
open(in_3_loc,'w').write(in_3.file.read().decode())
open(in_4_loc,'w').write(in_4.file.read().decode())
open(in_5_loc,'w').write(in_5.file.read().decode())
open(out_1_loc,'w').write(out_1.file.read().decode())
open(out_2_loc,'w').write(out_2.file.read().decode())
open(out_3_loc,'w').write(out_3.file.read().decode())
open(out_4_loc,'w').write(out_4.file.read().decode())
open(out_5_loc,'w').write(out_5.file.read().decode())
open(editorial_loc,'w').write(editorial.file.read().decode())

cur.execute('SELECT MAX(problem_id) AS res FROM problem_table;',())
x=cur.fetchall()
try:
	problem_id = int(x[0]['res'])+1
except:
	problem_id = 0
	
cur.execute('INSERT INTO problem_table VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);',(problem_id, q_code, q_name, q_file_loc, in_1_loc, in_2_loc, in_3_loc, in_4_loc, in_5_loc, out_1_loc, out_2_loc, out_3_loc, out_4_loc, out_5_loc, editorial_loc))

print("""<h2 style="color:darkgreen; text-align:center"><br/><br/>Problem UPLOADED Successfully </h2>""")
print("</body></html>")

conn.close()