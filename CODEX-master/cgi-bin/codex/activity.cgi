#!C:/python33/python.exe -u
print("Content-type:text/html\n\n")

import time
import cgi,cgitb
import oursql as sql
from os import environ
from datetime import datetime
import json
import decimal

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def same(given,correct):
	x=''.join(given.split())
	y=''.join(correct.split())
	return x==y
	

cgitb.enable()

session_id='None'
user_name = None
user_id = None

try:
	for cookie in environ['HTTP_COOKIE'].split(';'):
		(key, value ) = cookie.split('=');
		if key == "session_id":
			session_id = value
except:
	pass

form = cgi.FieldStorage()

conn = sql.connect(host='localhost', user='gnsp', passwd='mockingbird', db='codex')
cur = conn.cursor(sql.DictCursor)

print("""<!DOCTYPE html>
<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>CODEX</title>
<link rel="stylesheet" type="text/css" href="/css/Contest_Page.css"/>
<style type="text/css">
</style>
<link href="/SpryAssets/SpryMenuBarVertical.css" rel="stylesheet" type="text/css" />
<style type="text/css">""")

print(HtmlFormatter().get_style_defs())

print("""body {
	margin-bottom: 400px;
}
#apDiv4 {
	position: absolute;
	left: 5px;
	top: 450px;
	width: 482px;
	height: 136px;
	z-index: 9;
}
#Contest_Questions {
	position: absolute;
	left: 5px;
	top: 450px;
	width: 132px;
	height: 145px;
	z-index: 10;
}
</style>
<script src="/SpryAssets/SpryMenuBar.js" type="text/javascript"></script>
</head>
""")

cur.execute("SELECT login_data.user_name AS user_name, login_data.user_id AS user_id FROM session_info INNER JOIN login_data ON session_info.user_id=login_data.user_id WHERE session_id ='"+str(session_id)+"';",())
x=cur.fetchall()

if len(x):
	user_name = str(x[0]['user_name'])
	user_id = int(x[0]['user_id'])

print("""
<body>
<div id="logo">
<img src="/images/codex_logo.jpg" width="150" height="56" alt="image" />
</div>""")

print("""	<div id="apDiv1">
  <ul id="MenuBar1" class="MenuBarVertical">
    <li><a  href="home.cgi">Home</a></li>
    <li><a href="schedule.cgi">Contests</a></li>
    <li><a href="rules.cgi">Rules</a> </li>
    <li><a href="past_contests.cgi">Practice</a></li>
	<li><a href="score_board.cgi">Score Board</a></li>
</ul>
</div>
""")

mode = 'practice'
try:
	mode = str(form.getvalue('mode'))
except:
	pass
	
if mode=='practice':
	show = 'problem'
	try:
		p_code = str(form.getvalue('p_code'))
		show = str(form.getvalue('show'))
	except:
		pass
		
	cur.execute("SELECT problem_name AS pn, problem_id AS pid FROM problem_table WHERE problem_code = '"+p_code+"';",())
	data = cur.fetchall()
	try:
		title = str(data[0]['pn'])
		pid = str(data[0]['pid'])
	except:
		pass
		
	rcvd = None
	try:
		rcvd = form['OutFile']
	except:
		pass
	
	cur.execute("SELECT * FROM practice_table WHERE problem_id = "+pid+";",())
	check = cur.fetchall()
	if len(check)!=1:
		print("""<div id="Title_text"><h1 style="color:red">Bitch Please... Don't make me look bad with your feeble hacking skills... ~GnsP</h1></div>""")
		exit(0)
		
	message = 'CODEX IS RUNNING ON BETA'
	print("""<div id="header">""")
	try:
		cur.execute("""SELECT output_1 AS f FROM problem_table WHERE problem_code='{pCode}';""".format(pCode=p_code),())
		data = cur.fetchall()
		correct = str( open ( str( data[0]['f'] ), 'r').read() )
		given = str ( rcvd.file.read().decode() )
		if same(given,correct):
			print("""<div id="message" class="text2" style="color:yellowgreen;"><b>Congrats !!! Your Solution is CORRECT. </b></div>
					""".format(msg=message))
		else:
			print("""<div id="message" class="text2" style="color:#ff5555;"><b>Sorry, Your Solution is WRONG. </b></div>
					""".format(msg=message))
	except:
		print("""<div id="message" class="text2" style="color:gold;"><b>{msg}</b></div>
		""".format(msg=message))
		
	if user_name != None:
		print("""<div class="text1" id="Name_of_participant"><b style="color:rgb(170,170,170)">Logged in as : """+user_name+""" (<a style="color:rgb(170,170,170)" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'"  href="saybye.cgi">logout</a>)</b> </div>""")
	else:
		print("""<div class="text1" id="Name_of_participant"><b style="color:rgb(170,170,170)">Not Logged in ... <a style="color:rgb(170,170,170)" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'" href="login.cgi">login or register</a></b></div>""")
	
	print("""<div class="text3" id="count_down"><b style="color:orange">PRACTICE MODE</b></div>""")
	
	print('</div>')
		
	print("""<div id="Title_text">
		<h1 style="font-size: 2.5em; margin-top: 0px; color: rgb(0, 0, 0); font-family: Arial, sans-serif; font-style: normal; font-variant: normal; letter-spacing: normal; line-height: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255);">PRACTICE</h1>
		<h2 style="color: rgb(0, 0, 0); font-family: Arial, sans-serif; font-style: normal; font-variant: normal; white-space: normal;">{Title}</h2>
		</div>
		""".format(Title=title))
	
	cur.execute("SELECT problem_location AS pl, editorial AS ed FROM problem_table WHERE problem_code = '"+p_code+"';",())
	data = cur.fetchall()
	try:
		pl = str(data[0]['pl'])
		ed = str(data[0]['ed'])
		problem_content = str ( open(pl,'r').read() ).replace('\<','&lt;').replace('\>','&gt;').replace('\n','<br/>').replace('\t','&nbsp;&nbsp;&nbsp;&nbsp').replace(' ','&nbsp;')
		editorial_content_raw = str ( open(ed,'r').read() ).replace('\<','&lt;')
		editorial_content = highlight(editorial_content_raw, PythonLexer(), HtmlFormatter())
	except:
		problem_content = ''
		editorial_content = ''
	print("""<div id="apDiv4"></div>
			<div id="Contest_Questions">
			  <ul id="MenuBar2" class="MenuBarVertical">
				<li><a  href="activity.cgi?mode=practice&p_code={pCode}&show=problem" >Problem</a></li>
				<li><a  href="activity.cgi?mode=practice&p_code={pCode}&show=editorial">Editorial</a></li>
			  </ul>
			</div>""".format(pCode=p_code))
	
	if show=='problem':
		Value = 'PROBLEM STATEMENT'
		Content = problem_content
	else:
		Value = 'EDITORIAL'
		Content = editorial_content
	
	print("""<div align="center"></div>
				<div id="Question_Box">
				  <div class="text3" id="div_header" >
					<div align="center" style="color:rgb(200,200,200);margin-top:10px"><b>{value}</b></div>
				  </div>
				  <p align="left" class="text2">&nbsp;</p>
				  <div align="left" class="text2" style="text-align:justify;color:#333;line-height:30px">
				 {content}</div>
				</div>""".format(content=Content,value=Value))
				
	print("""<div align="center"></div>
		<div id="register">
		  <div id="div_header" class="text1">
			<div align="center" style="color:lightgreen;margin-top:10px"><b>SUBMISSION</b></div>
		  </div>
		  <p align="center"></p>
		  <div align="center">
		  </div>
		  <form id="Submit" name="Submit" enctype="multipart/form-data" method="post" action="activity.cgi" onsubmit="return practiceValidation()">
			<input type="hidden" name="mode" value="practice">
			<input type="hidden" name="show" value="problem">
			<input type="hidden" name="p_code" value="{val}">
			<div align="center">
			  <input type="submit" name="register_button" class="reg_button blue" value="SUBMIT" />
			</div>
		  <p align="center"></p>
		  <div align="center"></div>
			<a href="download_input_file.cgi?mode=practice&p_code={pCode}" class="download_bar" > <h3>DOWNLOAD INPUT FILE</h3></a>
			
			<div id="upload_output_block" style="display:block; background-color:#AAA; color:#444">
			<p><br/></p>
			<h3 style="font-family:Verdana, Geneva, sans-serif">UPLOAD OUTPUT FILE</h3>
			<div align="center"><input type="file" name="OutFile" id="OutFile" /></div>
			<p><br/></p>
			</div>
			
		  </form>
		</div>""".format(val=p_code,pCode=p_code))
	
	print("""<div align="right"></div>
		<div id="horizontal_line"><hr/></div>
		<div id="line2"><hr/></div>
		<div id="footer"><p style="text-align:center; color:rgb(170,170,170);font-family:Arial">Copyright &copy; 2014, All rights reserved, Design By <a style="color:rgb(170,170,170)" href="https://www.facebook.com/aditya.dash.520" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'">Aditya Dash</a>, Site By <a style="color:rgb(170,170,170)" href="https://www.facebook.com/sharpandsage" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'">Ganesh Prasad</a></p></div>

		<script type="text/javascript">
		var MenuBar1 = new Spry.Widget.MenuBar("MenuBar1", {imgRight:"SpryAssets/SpryMenuBarRightHover.gif"});
		var MenuBar2 = new Spry.Widget.MenuBar("MenuBar2", {imgRight:"SpryAssets/SpryMenuBarRightHover.gif"});
		function practiceValidation(){
			var out = document.getElementById("OutFile").value;
			if(!out){
				document.getElementById("upload_output_block").style.color="darkred";
				return false;
			}
			return true;
		}
		</script>

		</body>
		</html>""")

else:
	now = datetime.now()
	y = int( now.year )
	m = int( now.month )
	d = int( now.day )
	hr = int( now.hour )
	min = int( now.minute )
	
	ts = float(time.mktime(now.timetuple()))
	
	cur.execute(" SELECT * FROM codex_table WHERE begin_time <= {TS} AND end_time >= {Ts};".format(TS=ts,Ts=ts),())
	data = cur.fetchall()
	
	if len(data) < 1 :
		message = 'Sorry . NO CONTEST is Running right now . '
		print("""<div id="header">""")
		print("""<div id="message"><p class="text2" style="color:#ff5555;"><b>{msg}</b></p></div>
			""".format(msg=message))
			
		if user_name != None:
			print("""<div class="text1" id="Name_of_participant"><b style="color:rgb(170,170,170)">Logged in as : """+user_name+""" (<a style="color:rgb(170,170,170)" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'"  href="saybye.cgi">logout</a>)</b> </div>""")
		else:
			print("""<div class="text1" id="Name_of_participant"><b style="color:rgb(170,170,170)">Not Logged in ... <a style="color:rgb(170,170,170)" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'" href="login.cgi">login or register</a></b></div>""")
		print('</div></body></html>')
		conn.close()
		exit(0)
	
	try:
		b_y = int( data[0]['begin_time_y'] )
		b_m = int( data[0]['begin_time_m'] )
		b_d = int( data[0]['begin_time_d'] )
		b_hr = int( data[0]['begin_time_hr'] )
		b_min = int( data[0]['begin_time_min'] )
		e_y = int( data[0]['end_time_y'] )
		e_m = int( data[0]['end_time_m'] )
		e_d = int( data[0]['end_time_d'] )
		e_hr = int( data[0]['end_time_hr'] )
		e_min = int( data[0]['end_time_min'] )
		
		cdx_id = int(data[0]['codex_id'])
		cdx_ver = str(data[0]['codex_version'])
		cdx_tag = str(data[0]['codex_tag'])
		
		q1 = str(data[0]['q_1_code'])
		q2 = str(data[0]['q_2_code'])
		q3 = str(data[0]['q_3_code'])
		q4 = str(data[0]['q_4_code'])
		
		q1_val = int(data[0]['q_1_value'])
		q2_val = int(data[0]['q_2_value'])
		q3_val = int(data[0]['q_3_value'])
		q4_val = int(data[0]['q_4_value'])
		
		scoreboard_loc = str(data[0]['scoreboard_loc'])
	except:
		print("""<div id="Title_text">
		<h1 style="font-size: 2.5em; margin-top: 0px; color: rgb(240, 30, 10); font-family: Arial, sans-serif; font-style: normal; font-variant: normal; letter-spacing: normal; line-height: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255);">ERROR OCCURED...</h1>
		</div></body></html>
		""")
		conn.close()
		exit(0)
	
	score_board_file = open(scoreboard_loc,'r')
	score_board_str = score_board_file.read()
	score_board_dict = json.loads(score_board_str)
	score_board_file.close()
	
	p_code = q1
	try:
		p_code__ = form.getvalue('show')
		if p_code__ != None:
			p_code=str(p_code__)
	except:
		pass
	
	outFile = None
	srcFile = None
	try:
		if form['OutFile'].filename != None and form['SrcFile'].filename != None:
			program = str(form['SrcFile'].file.read().decode())
			outFile = form['OutFile']
	except:
		pass
		
	cur.execute("SELECT problem_name AS pn, problem_id AS pid, problem_location AS pl FROM problem_table WHERE problem_code = '"+p_code+"';",())
	data = cur.fetchall()

	try:
		pn = str(data[0]['pn'])
		pid = int(data[0]['pid'])
		pl = str(data[0]['pl'])
		problem_content = str ( open(pl,'r').read() ).replace('\<','&lt;').replace('\>','&gt;').replace('\n','<br/>').replace('\t','&nbsp;&nbsp;&nbsp;&nbsp').replace(' ','&nbsp;')
	except:
		print("""<div id="Title_text">
		<h1 style="font-size: 2.5em; margin-top: 0px; color: rgb(240, 30, 10); font-family: Arial, sans-serif; font-style: normal; font-variant: normal; letter-spacing: normal; line-height: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255);">ERROR OCCURED...</h1>
		</div></body></html>
		""")
		conn.close()
		exit(0)
	
	#### Message Bar and Enforcing Log in
		
	message = 'CODEX IS RUNNING ON BETA'
	print("""<div id="header">""")
	
	if user_name != None:
		print("""<div class="text1" id="Name_of_participant"><b style="color:rgb(170,170,170)">Logged in as : """+user_name+""" (<a style="color:rgb(170,170,170)" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'"  href="saybye.cgi">logout</a>)</b> </div>""")
	else:
		message = 'YOU MUST LOG IN TO PARTICIPATE'
		print("""<div class="text1" id="Name_of_participant"><b style="color:rgb(170,170,170)">Not Logged in ... <a style="color:rgb(170,170,170)" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'" href="login.cgi">login or register</a></b></div>""")
	
	countdown = int((datetime(e_y,e_m,e_d,e_hr,e_min)-now).seconds)	
	total_time = int((datetime(e_y,e_m,e_d,e_hr,e_min)-datetime(b_y,b_m,b_d,b_hr,b_min)).seconds)	
	Min = countdown//60
	Sec = countdown%60
	print("""<div id="count_down" class="text3" style="color:orange"><b>{min} : {sec}</b></div>""".format(min=Min,sec=Sec))
	
	#####		Match the input-output file from current_codex_data table
	#####		if correct delete entry from curren_codex_data table
	#####		
	#####		update score_board
	#####		save src file in src_dump__
	
	src_dump_path = 'E:\\CODEX_SITE\\src_dump__\\'
	
	if outFile != None:
		cur.execute("SELECT in_file FROM current_codex_data WHERE user_id={uid} AND problem_id='{pCode}';".format(uid=str(user_id),pCode=p_code),())
		x=cur.fetchall()
		
		if len(x)==1:
			f_no = int( x[0]['in_file'])
			cur.execute("""SELECT output_{fno} AS f FROM problem_table WHERE problem_code='{pCode}';""".format(fno=str(f_no),pCode=p_code),())
			data = cur.fetchall()
			correct = str( open ( str( data[0]['f'] ), 'r').read() )
			given = str ( outFile.file.read().decode() )
			if same(given,correct):
				print("""<div id="message" class="text2" style="color:yellowgreen;"><b>Congrats !!! Your Solution is CORRECT. </b></div>""")
				cur.execute("DELETE FROM current_codex_data WHERE user_id={uid} AND problem_id='{pCode}';".format(uid=str(user_id),pCode=p_code),())
				
				full_mark_value = 0
				if p_code==q1:
					full_mark_value = q1_val
				elif p_code==q2:
					full_mark_value = q2_val
				elif p_code==q3:
					full_mark_value = q3_val
				else:
					full_mark_value = q3_val
					
				marks = round( (0.9*countdown + 0.1*total_time)*full_mark_value*100/total_time, 2)
				
				if user_name+'_____score' in score_board_dict:
					if user_name+'_____'+p_code not in score_board_dict:
						score_board_dict[user_name+'_____'+p_code]=marks
						score_board_dict[user_name+'_____score'] += marks
					else:
						pass
				else:
					score_board_dict[user_name+'_____'+p_code]=marks
					score_board_dict[user_name+'_____score'] = marks
				
				score_board_str = json.dumps(score_board_dict)
				score_board_file = open(scoreboard_loc,'w')
				score_board_file.write(score_board_str)
				score_board_file.close()
				
				open(src_dump_path+cdx_ver+'_'+user_name+'_'+p_code+'.txt','w').write(program)
			else:
				print("""<div id="message" class="text2" style="color:#ff5555;"><b>Sorry, Your Solution is WRONG. </b></div>""")
		else:
			print("""<div id="message" class="text2" style="color:orangered;"><b>PLEASE DO NOT CHEAT. DOWNLOAD INPUT FIRST.</b></div>""")
	else:
		print("""<div id="message" class="text2" style="color:gold;"><b>{msg}</b></div>
		""".format(msg=message))
	
	print('</div>')
	
	print("""<div id="Title_text">
		<h1 style="font-size: 2.5em; margin-top: 0px; color: rgb(0, 0, 0); font-family: Arial, sans-serif; font-style: normal; font-variant: normal; letter-spacing: 10px; line-height: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255);">CODEX  {ver}.0</h1>
		<h2 style="color: rgb(0, 0, 0); font-family: Arial, sans-serif; font-style: normal; font-variant: normal; white-space: normal;">{tag}</h2>
		</div>
		""".format(ver=cdx_ver,tag=cdx_tag))
	
	### Questions of the contest
	cur.execute("SELECT problem_name AS pn, problem_code AS pc FROM problem_table WHERE problem_code = '"+q1+"' OR problem_code = '"+q2+"' OR problem_code = '"+q3+"' OR problem_code = '"+q4+"' ;",())
	data = cur.fetchall()
	n1 = str( data[0]['pn']).upper()
	n2 = str( data[1]['pn']).upper()
	n3 = str( data[2]['pn']).upper()
	n4 = str( data[3]['pn']).upper()
	
	print("""<div id="apDiv4"></div>
			<div id="Contest_Questions">
			  <ul id="MenuBar2" class="MenuBarVertical">
				<li><a  href="activity.cgi?mode=contest&show={Q1}">1. {N1}</a></li>
				<li><a  href="activity.cgi?mode=contest&show={Q2}">2. {N2}</a></li>
				<li><a  href="activity.cgi?mode=contest&show={Q3}">3. {N3}</a></li>
				<li><a  href="activity.cgi?mode=contest&show={Q4}">4. {N4}</a></li>
			  </ul>
			</div>""".format(Q1=q1,Q2=q2,Q3=q3,Q4=q4,N1=n1,N2=n2,N3=n3,N4=n4))

	
	print("""<div align="center"></div>
				<div id="Question_Box">
				  <div class="text3" id="div_header" >
					<div align="center" style="color:rgb(200,200,200);margin-top:10px"><b>{value}</b></div>
				  </div>
				  <p align="left" class="text2">&nbsp;</p>
				  <div align="left" class="text2" style="text-align:justify;color:#333;line-height:30px">
				 {content}</div>
				</div>""".format(content=problem_content,value=pn.upper()))
	
	if user_name != None:
		print("""<div align="center"></div>
			<div id="register">
			  <div id="div_header" class="text1">
				<div align="center" style="color:lightgreen;margin-top:10px"><b>SUBMISSION</b></div>
			  </div>
			  <p align="center"></p>
			  <div align="center">
			  </div>
			  <form id="Submit" name="Submit" enctype="multipart/form-data" method="post" action="activity.cgi" onsubmit="return submitValidation()">
				<input type="hidden" name="mode" value="contest">
				<input type="hidden" name="show" value={val}>
				<div align="center">
				  <input type="submit" name="register_button" class="reg_button blue" value="SUBMIT" />
				</div>
			  <p align="center"></p>
			  <div align="center"></div>
				<a href="download_input_file.cgi?mode=contest&p_code={pCode}" class="download_bar" > <h3>DOWNLOAD INPUT FILE</h3></a>
				
			<div id="upload_out_block" style="display:block; background-color:#AAA">
			<p></p>
			<h3 style="color:#444; font-family:Verdana, Geneva, sans-serif">UPLOAD OUTPUT FILE</h3>
			<div align="center"><input type="file" name="OutFile" id="OutFile" /></div>
			<p></p>
			</div>
			
			<div id="upload_src_block" style="display:block; background-color:#AAA">
			<p></p>
			<h3 style="color:#444; font-family:Verdana, Geneva, sans-serif">UPLOAD SOURCE FILE</h3>
			<div align="center"><input type="file" name="SrcFile" id="SrcFile" /></div>
			<p></p>
			</div>
				
			</form>
			</div>""".format(val=p_code,pCode=p_code))
			
	print("""<div id="score_board" class="text3">""")
	##SCORE-BOARD GOES HERE
	print("""<div class="text1" id="div_header" >
			<div align="center" style="color:coral;margin-top:10px"><b>SCORE BOARD</b></div>
			</div>
			<p>&nbsp;</p>
			<table align="center"><col width="75px"><col width="150px"><col width="75px">
			<tr><th>RANK</th><th>USER NAME</th><th>SCORE</th></tr>
		""")
	
	score_list=[]
	for key in score_board_dict:
		if key[-10:]=='_____score':
			score_list.append((key[:-10],score_board_dict[key]))
	scoreList = sorted(score_list,key=lambda x:x[1],reverse=True)
	
	for i in range(len(scoreList)):
		if scoreList[i][0]==user_name:
			print("""<tr style="color:green"><th>"""+str(i+1)+"</th><th>"+scoreList[i][0]+"</th><th>"+str(scoreList[i][1])+"</th></tr>")
		else:
			print("<tr><td>"+str(i+1)+"</td><td>"+scoreList[i][0]+"</td><td>"+str(scoreList[i][1])+"</td></tr>")
	
	print("</table>")
	print('<p>&nbsp;</p>')
	print('</div>')
	
	print("""<div align="right"></div>
		<div id="horizontal_line"><hr/></div>
		<div id="line2"><hr/></div>
		<div id="footer"><p style="text-align:center; color:rgb(170,170,170);font-family:Arial">Copyright &copy; 2014, All rights reserved, Design By <a style="color:rgb(170,170,170)" href="https://www.facebook.com/aditya.dash.520" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'">Aditya Dash</a>, Site By <a style="color:rgb(170,170,170)" href="https://www.facebook.com/sharpandsage" onMouseOver="this.style.color='rgb(255,255,255)'" onMouseOut="this.style.color='rgb(170,170,170)'">Ganesh Prasad</a></p></div>

		<script type="text/javascript">
		
		var countDown = """+str(countdown)+""";
		var area=document.getElementById("count_down");

		setInterval (function() {
			countDown=countDown-1;
			M=parseInt(countDown/60);
			S=countDown%60;
			area.innerHTML = "<b>"+M+" : "+S+"</b>";
		},1000)
		
		function submitValidation(){
			var src = document.getElementById("SrcFile").value;
			var out = document.getElementById("OutFile").value;
			if(!src){
				document.getElementById("upload_src_block").style.color="darkred";
				return false;
			}
			if(!out){
				document.getElementById("upload_out_block").style.color="darkred";
				return false;
			}
			return true;
		}
		</script>

		</body>
		</html>""")	
		
conn.close()
	
	
