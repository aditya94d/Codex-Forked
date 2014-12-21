#!C:/python33/python.exe -u
print("Content-type:text/html\n\n")

import time
import cgi,cgitb
import oursql as sql

print("<!DOCTYPE html><html><head>")
print("<title>Confirmation</title>")

print("<style>")
print("th,td")
print("{")
print("padding:10px;")
print("}")
print("</style>")

print("</head>")

print("""<body><h1 style="margin:50px; color:#3B0C39; font-family:Arial; text-align:center">"""+time.strftime("%A, %B %d, %Y")+"<br/>"+time.strftime("%I:%M:%S %p")+"</h1>")
print("""<p style="margin:20px 250px 20px 250px; color:#3B0C39; font-family:Arial; font-size:28px; text-align:center">""")

form = cgi.FieldStorage()
name = form.getvalue('Name')
user_name = form.getvalue('Username')
email = form.getvalue('E-Mail')
institute = form.getvalue('Institute')
password = form.getvalue('Password')

conn = sql.connect(host='localhost', user='gnsp', passwd='mockingbird', db='codex')
cur = conn.cursor(sql.DictCursor)

cur.execute("SELECT user_id FROM login_data WHERE user_name = '"+str(user_name)+"' OR email= '"+str(email)+"';")
x=cur.fetchall()

if len(x) != 0:
	print("Username or E-Mail already exists</p>")
	print("""<br/><br/><h1 style="text-align:center; font-family:Arial; color:darkred"><a href="Registration_Form.cgi">BACK</a></h1>""")
	print("</body></html>")
	conn.close()
	exit(0)
	
cur.execute('SELECT MAX(user_id) AS res FROM login_data;',())
x=cur.fetchall()
try:
	user_id = int(x[0]['res'])+1
except:
	user_id = 0

cur.execute('INSERT INTO login_data VALUES (?,?,?,?);',(user_id,user_name,email,password))
cur.execute('INSERT INTO user_details VALUES (?,?,?);',(user_id,name,institute))


print("You have been REGISTERED Successfully</p>")
print("<br/><br/>")

cur.execute('SELECT login_data.user_id AS user_id,name,user_name,email,institute FROM login_data INNER JOIN user_details ON login_data.user_id=user_details.user_id WHERE login_data.user_id = '+str(user_id)+' ;',())
x = cur.fetchall()
print("""<table border="0" align="center" style="width:700px; color:#4A0A39; font-family:Arial; text-align:center; font-size:24px"><tr><th>UserID</th><th>Name</th><th>Username</th><th>Email</th><th>Institute</th></tr>""")
for a in x:
	print("<tr><td>"+str(int(a['user_id']))+"</td><td>"+a['name']+"</td><td>"+a['user_name']+"</td><td>"+a['email']+"</td><td>"+a['institute']+"</td></tr>")
print("</table>")


print("""<br/><br/><h1 style="text-align:center; font-family:Arial; color:darkred"><a href="home.cgi">HOME</a></h1>""")

print("</body></html>")
conn.close()