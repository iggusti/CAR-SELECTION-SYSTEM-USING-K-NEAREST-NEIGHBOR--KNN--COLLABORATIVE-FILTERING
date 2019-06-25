import csv
import mysql.connector, cStringIO,base64
def conn():
	db = mysql.connector.connect(
	host="localhost",
	database="cari1088103",
	user="root",
	passwd=""
	)
	return db

def input():
	db = conn()
	mycursor =db.cursor()

	with open('database mobil.csv', 'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			sql = "UPDATE car set jenis = %s where idmobil  = %s "
			args = (row['jenis'],row['idmobil'])
			mycursor.execute(sql,args)
			db.commit()

if __name__ == '__main__':
    input()