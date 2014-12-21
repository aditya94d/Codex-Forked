#!C:/python33/python.exe -u
print("Content-type:text/html\n\n")

import oursql as sql
import cgi, cgitb
from os import environ

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

cur.execute("DELETE FROM session_info WHERE session_id ='"+str(session_id)+"';",())

print("""<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url=home.cgi" /><title>Logging Out</title></head>
<body>Redirecting to home... If not automatically redirected , REFRESH the page...</body></html>""")
conn.close()