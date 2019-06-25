import mysql.connector, cStringIO,base64
from PIL import Image

def conn():
    db = mysql.connector.connect(
        host="localhost",
        database="cari1088103",
        user="root",
        passwd=""
        )
    return db

def main():
    db = conn()
    mycursor =db.cursor()
    for i in range(0,1089):
        sql="SELECT avg(ratings) from rating where car_id = %s" %(i)
        mycursor.execute(sql)
        myresult1 = mycursor.fetchall()

        sql = "UPDATE car set rating = %s where idmobil  = %s "
        args = (myresult1[0][0], i)
        mycursor.execute(sql,args)
        db.commit()

if __name__ == '__main__':
    main()