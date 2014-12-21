#!C:/python33/python.exe -u
print("Content-Type:application/octet-stream; name=\"input.in\"")
print("Content-Disposition: attachment; filename=\"input.in\"\n")

import cgi,cgitb
import os
import oursql as sql
import random
from os import environ

cgitb.enable()

form=cgi.FieldStorage()
mode = str (form.getvalue('mode'))
p_code = str(form.getvalue('p_code'))

conn = sql.connect(host='localhost', user='gnsp', passwd='mockingbird', db='codex')
cur = conn.cursor(sql.DictCursor)

session_id='None'
try:
	for cookie in environ['HTTP_COOKIE'].split(';'):
		(key, value ) = cookie.split('=');
		if key == "session_id":
			session_id = value
except:
	pass


if mode == 'practice':
	cur.execute("SELECT input_1 FROM problem_table WHERE problem_code='{pCode}';".format(pCode=p_code),())
	x=cur.fetchall()
	file_loc = str(x[0]['input_1'])
	fo = open(file_loc, "r")
	s = str(fo.read());
	p=s.split('\n\n')
	for a in p:
		print(a)
	fo.close()

else:
	n=random.randint(1,4)
	cur.execute("SELECT input_"+str(n)+" AS inp FROM problem_table WHERE problem_code='{pCode}';".format(pCode=p_code),())
	x=cur.fetchall()
	file_loc = str(x[0]['inp'])
	fo = open(file_loc, "r")
	s = str(fo.read());
	p=s.split('\n\n')
	for a in p:
		print(a)
	cur.execute("SELECT user_id FROM session_info WHERE session_id = '"+session_id+"';",())
	x=cur.fetchall()
	uid=int(x[0]['user_id'])
	cur.execute("SELECT user_id FROM current_codex_data WHERE problem_id = '"+p_code+"' AND user_id = "+str(uid)+";",())
	x=cur.fetchall()
	if len(x)!=0:
		cur.execute("DELETE FROM current_codex_data WHERE problem_id = '"+p_code+"' AND user_id = "+str(uid)+";",())
	cur.execute("INSERT INTO current_codex_data VALUES ({user_id},'{problem_id}',{in_file});".format(user_id=str(uid),problem_id=p_code,in_file=str(n)),())
	fo.close()
	
conn.close()