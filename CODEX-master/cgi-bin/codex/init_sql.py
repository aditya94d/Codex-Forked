import oursql as sql

conn = sql.connect(host='localhost', user='gnsp', passwd='mockingbird', db='codex')
cur = conn.cursor(sql.DictCursor)

cur.execute('CREATE TABLE IF NOT EXISTS login_data (user_id INTEGER NOT NULL, user_name VARCHAR(50) NOT NULL, email VARCHAR(50) NOT NULL, password VARCHAR(50) NOT NULL );',())
cur.execute('CREATE TABLE IF NOT EXISTS user_details (user_id INTEGER NOT NULL, name VARCHAR(50), institute VARCHAR(50));',())
cur.execute('CREATE TABLE IF NOT EXISTS session_info (user_id INTEGER NOT NULL, user_name VARCHAR(50) NOT NULL, session_id VARCHAR(40) NOT NULL);',())
cur.execute("""CREATE TABLE IF NOT EXISTS problem_table ( problem_id INTEGER NOT NULL, 
											problem_code VARCHAR(15) NOT NULL, 
											problem_name VARCHAR(50) NOT NULL, 
											problem_location VARCHAR(120) NOT NULL, 
											input_1 VARCHAR(120) NOT NULL, 
											input_2 VARCHAR(120) NOT NULL, 
											input_3 VARCHAR(120) NOT NULL, 
											input_4 VARCHAR(120) NOT NULL,
											input_5 VARCHAR(120) NOT NULL,
											output_1 VARCHAR(120) NOT NULL, 
											output_2 VARCHAR(120) NOT NULL, 
											output_3 VARCHAR(120) NOT NULL, 
											output_4 VARCHAR(120) NOT NULL,
											output_5 VARCHAR(120) NOT NULL,
											editorial VARCHAR(120) NOT NULL);""",())
											
cur.execute('CREATE TABLE IF NOT EXISTS admin_info (user_id INTEGER NOT NULL, user_name VARCHAR(50) NOT NULL);',())
cur.execute("INSERT INTO admin_info VALUES (1,'gnsp');",())

cur.execute('CREATE TABLE practice_table (problem_id INTEGER NOT NULL);',())

cur.execute("""CREATE TABLE IF NOT EXISTS codex_table (	codex_id INTEGER NOT NULL,
														codex_version INTEGER NOT NULL, 
														codex_tag VARCHAR(50) NOT NULL,
														begin_time_y INTEGER(5) NOT NULL,
														begin_time_m TINYINT(3) NOT NULL,
														begin_time_d TINYINT(3) NOT NULL,
														begin_time_hr TINYINT(3) NOT NULL,
														begin_time_min TINYINT(3) NOT NULL,
														end_time_y INTEGER(5) NOT NULL,
														end_time_m TINYINT(3) NOT NULL,
														end_time_d TINYINT(3) NOT NULL,
														end_time_hr TINYINT(3) NOT NULL,
														end_time_min TINYINT(3) NOT NULL,
														q_1_code VARCHAR(15) NOT NULL,
														q_2_code VARCHAR(15) NOT NULL,
														q_3_code VARCHAR(15) NOT NULL,
														q_4_code VARCHAR(15) NOT NULL,
														q_1_value TINYINT(3) NOT NULL,
														q_2_value TINYINT(3) NOT NULL,
														q_3_value TINYINT(3) NOT NULL,
														q_4_value TINYINT(3) NOT NULL,
														begin_time NUMERIC(13,2) NOT NULL,
														end_time NUMERIC(13,2) NOT NULL,
														scoreboard_loc VARCHAR(120));""",())

cur.execute("""CREATE TABLE IF NOT EXISTS current_codex_data ( user_id INTEGER NOT NULL,
																problem_id VARCHAR(15),
																in_file TINYINT(1));""",())

																
conn.close()