from flask import Flask, render_template, redirect, url_for, request, session, g, jsonify
import mysql.connector, ast, os, cStringIO, base64, io, json, ast
from PIL import Image

Image.LOAD_TRUNCATED_IMAGES = True

application = Flask(__name__)
application.secret_key = "01234546"


def conn():
    db = mysql.connector.connect(host="localhost",
                                 database="cari",
                                 user="root",
                                 passwd="")
    return db


# =============== Login ===============================
@application.route("/", methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('menu'))
    myresult = []
    if request.method == 'POST':
        db = conn()
        mycursor = db.cursor()
        if request.form['Simpan'] == "login":
            sql = "select * from user_profile where nama = '" + request.form[
                'username'] + "' and password= '" + request.form[
                    'password'] + "'"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            #print  len(myresult)
            if len(myresult) > 0:
                #print  myresult[0][0]
                session['login'] = True
                session['id'] = myresult[0][0]
                session['user'] = request.form['username']
                #simuser(session['id'])
                #simmobil(session['id'])
                return redirect(url_for('menu'))
        else:
            sql = "insert into user_profile(nama, password, usia, jk, pendapatan, pekerjaan, anggaran) values (%s, %s, %s, %s, %s, %s, %s)"
            args = (request.form['nama'], request.form['passworddaftar'],
                    request.form['usia'], request.form['jk'],
                    request.form['pendapatan'], request.form['pekerjaan'],
                    request.form['anggaran'])
            mycursor.execute(sql, args)
            db.commit()

            sql = "select * from user_profile where nama = '" + request.form[
                'nama'] + "' and password= '" + request.form[
                    'passworddaftar'] + "'"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            #print  len(myresult)
            if len(myresult) > 0:
                #print  myresult[0][0]
                session['login'] = True
                session['id'] = myresult[0][0]
                session['user'] = request.form['nama']
                #simuser(session['id'])
                #simmobil(session['id'])
                return redirect(url_for('menu'))
    return render_template("loginform.html")


@application.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


# ====================================================================


# =========== Logout ================================================
@application.route("/logout", methods=['GET', 'POST'])
def logout():
    session['user'] = None
    g.user = None
    return redirect(url_for('login'))


# ====================================================================


def pilih():
    db = conn()
    mycursor = db.cursor()
    kirim = []
    data = ["merk", "jenis", "varian", "transmisi", "warna"]
    for i in data:
        sql = "SELECT %s FROM car GROUP BY %s HAVING ( COUNT(%s) > 0 )" % (
            i, i, i)
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        kiriman = []
        for i in myresult:
            kiriman2 = []
            for ii in i:
                kiriman2.append(str(ii).capitalize())
            kiriman.append(kiriman2)
        kirim.append(kiriman)
    return kirim


def pilihuser(kode):
    db = conn()
    mycursor = db.cursor()
    kirim = []
    data = ["merk", "jenis", "varian", "transmisi", "warna"]
    for i in data:
        sql = "SELECT %s FROM car %s GROUP BY %s HAVING ( COUNT(%s) > 0 )" % (
            i, kode, i, i)
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        kiriman = []
        for i in myresult:
            kiriman2 = []
            for ii in i:
                kiriman2.append(str(ii).capitalize())
            kiriman.append(kiriman2)
        kirim.append(kiriman)
    return kirim


def pilihratinguser(kode):
    db = conn()
    mycursor = db.cursor()
    kirim = []
    data = ["merk", "jenis", "varian", "transmisi", "warna"]
    for i in data:
        sql = "SELECT a.%s FROM car %s GROUP BY a.%s HAVING ( COUNT(a.%s) > 0 )" % (
            i, kode, i, i)
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        kiriman = []
        for i in myresult:
            kiriman2 = []
            for ii in i:
                kiriman2.append(str(ii).capitalize())
            kiriman.append(kiriman2)
        kirim.append(kiriman)
    return kirim


def pilihcari(kode):
    db = conn()
    mycursor = db.cursor()
    kirim = []
    data = ["merk", "jenis", "varian", "transmisi", "warna"]
    for i in data:
        sql = "SELECT %s FROM car where idmobil in (%s) GROUP BY %s HAVING ( COUNT(%s) > 0 )" % (
            i, kode, i, i)
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        kiriman = []
        for i in myresult:
            kiriman2 = []
            for ii in i:
                kiriman2.append(str(ii).capitalize())
            kiriman.append(kiriman2)
        kirim.append(kiriman)
    return kirim


def dataharga():
    db = conn()
    mycursor = db.cursor()
    data = []
    sql = "SELECT * FROM hargamobil"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    data.append(myresult)
    return data


@application.route('/menu', methods=['GET', 'POST'])
def menu():
    if g.user:
        if session['user'] == "superuser":
            return render_template("mainadmin.html")
        db = conn()
        mycursor = db.cursor()
        sql = "SELECT a.idmobil FROM car as a inner join rating as b on a.idmobil = b.car_id where b.user_id = %s" % (
            session['id'])
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        if len(myresult) < 3:
            return redirect(url_for('DataUserLogin'))  #PilihMobilRegis
        simuser(session['id'])
        simmobil(session['id'])
        #cekmaeuser()
        #cekmaemobil()
        return redirect(url_for('PredRatingCar'))
    return redirect(url_for('login'))


@application.route('/datauser', methods=['GET', 'POST'])
def datauser():
    if g.user:
        myresult = []
        if request.method == 'POST':
            db = conn()
            mycursor = db.cursor()
            sql = "INSERT into user_profile(nama, password, usia, jk, pendapatan, pekerjaan, anggaran) values (%s, %s, %s, %s, %s, %s, %s)"
            args = (request.form['nama'], request.form['password'],
                    request.form['usia'], request.form['jk'],
                    request.form['pendapatan'], request.form['pekerjaan'],
                    request.form['anggaran'])
            mycursor.execute(sql, args)
            db.commit()
            #print mycursor.rowcount, "record inserted."
        return render_template("datauser.html")
    return redirect(url_for('menu'))


@application.route('/DataUserLogin', methods=['GET', 'POST'])
def DataUserLogin():
    simuser(session['id'])
    simmobil(session['id'])
    #cekmaeuser()
    #cekmaemobil()
    if g.user:
        myresult = []
        db = conn()
        mycursor = db.cursor()
        if request.method == 'POST':
            if request.form['Simpan'] == "Simpan":
                sql = "UPDATE `user_profile` SET usia = %s , jk = %s , pendapatan = %s , pekerjaan = %s , anggaran = %s WHERE id = %s"
                args = (request.form['usia'], request.form['jk'],
                        request.form['pendapatan'], request.form['pekerjaan'],
                        request.form['anggaran'], session['id'])
                mycursor.execute(sql, args)
            elif request.form['Simpan'] == 'SimpanPass':
                #print "masuk ke sini"
                sql = "UPDATE `user_profile` SET password = %s WHERE id = %s"
                args = (request.form['passwordbaru'], session['id'])
                mycursor.execute(sql, args)
            db.commit()
        sql = "SELECT * from user_profile where id = %s" % (session['id'])
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        lis1 = str(myresult)
        lis2 = ast.literal_eval(lis1)
        return render_template("DataUserLogin.html", post=lis2)
    return redirect(url_for('menu'))


@application.route('/tableuser', methods=['GET', 'POST'])
def tableuser():
    if g.user:
        myresult = []
        db = conn()
        mycursor = db.cursor()
        if request.method == 'POST':
            if request.form['Simpan'] == "Simpan":
                sql = "UPDATE `user_profile` SET usia = %s , jk = %s , pendapatan = %s , pekerjaan = %s , anggaran = %s WHERE id = %s"
                args = (request.form['usia'], request.form['jk'],
                        request.form['pendapatan'], request.form['pekerjaan'],
                        request.form['anggaran'], request.form['kodeuser'])
                mycursor.execute(sql, args)
            elif request.form['Simpan'] == 'SimpanPass':
                ###print "masuk ke sini"
                sql = "UPDATE `user_profile` SET password = %s WHERE id = %s"
                args = (request.form['passwordbaru'], request.form['kodeuser'])
                mycursor.execute(sql, args)
            else:
                sql = "DELETE FROM user_profile WHERE id = %s" % (
                    request.form['kodeuser'])
                mycursor.execute(sql)
            db.commit()
        sql = "select * from user_profile"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        lis1 = str(myresult)
        lis2 = ast.literal_eval(lis1)
        return render_template("tableuser.html", post=lis2)
    return redirect(url_for('menu'))


@application.route('/ModalUser/<kode>', methods=['GET', 'POST'])
def ModalUser(kode):
    myresult = []
    db = conn()
    mycursor = db.cursor()
    sql = "select * from user_profile where id = %s" % (kode)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    lis1 = str(myresult)
    lis2 = ast.literal_eval(lis1)
    return render_template("ModalUser.html", post=lis2, kode=kode)


@application.route('/datamobil', methods=['GET', 'POST'])
def datamobil():
    if g.user:
        myresult = []
        if request.method == 'POST':
            db = conn()
            mycursor = db.cursor()
            gas = 0
            dis = 0
            if request.form['fuel'] == "1":
                gas = 1
                dis = 0
            else:
                gas = 0
                dis = 1
            #sql ="insert into car(mesin, tipe, merk, warna, harga, model) values ('"+request.form['mesin']+"', '"+request.form['merk']+"', '"+request.form['tipe']+"', '"+request.form['warna']+"', '"+ request.form['harga']+"', '"+ request.form['model']+"')"
            sql = "insert into car(merk, jenis, varian, cc, transmisi, harga, warna, keterangan, kelebihan, kekurangan, image, seater, aftersale, gasoline, diesel) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            args = (request.form['merk'], request.form['jenis'],
                    request.form['varian'], request.form['cc'],
                    request.form['transmisi'], request.form['harga'],
                    request.form['warna'], request.form['keterangan'],
                    request.form['kelebihan'], request.form['kekurangan'],
                    request.form['image'], request.form['seater'],
                    request.form['aftersale'], gas, dis)
            mycursor.execute(sql, args)
            db.commit()
            ###print mycursor.rowcount, "record inserted."
        return render_template("datamobil.html")
    return redirect(url_for('menu'))


@application.route('/tablemobil', methods=['GET', 'POST'])
def tablemobil():
    if g.user:
        myresult = []
        db = conn()
        mycursor = db.cursor()
        if request.method == 'POST':
            if request.form['Simpan'] == "Simpan":
                gas = 0
                dis = 0
                if request.form['fuel'] == "1":
                    gas = 1
                    dis = 0
                else:
                    gas = 0
                    dis = 1
                #sql ="insert into car(mesin, tipe, merk, warna, harga, model) values ('"+request.form['mesin']+"', '"+request.form['merk']+"', '"+request.form['tipe']+"', '"+request.form['warna']+"', '"+ request.form['harga']+"', '"+ request.form['model']+"')"
                sql = "UPDATE  car set merk = %s, jenis = %s, varian = %s, cc = %s, transmisi = %s, harga = %s, warna = %s, keterangan = %s, kelebihan = %s, kekurangan = %s, image = %s, seater = %s, aftersale = %s, gasoline = %s, diesel = %s where idmobil = %s"
                args = (request.form['merk'], request.form['jenis'],
                        request.form['varian'], request.form['cc'],
                        request.form['transmisi'], request.form['harga'],
                        request.form['warna'], request.form['keterangan'],
                        request.form['kelebihan'], request.form['kekurangan'],
                        request.form['image'], request.form['seater'],
                        request.form['aftersale'], gas, dis,
                        request.form['kodemob'])
                mycursor.execute(sql, args)
            else:
                sql = "DELETE FROM car WHERE idmobil = %s" % (
                    request.form['kodemob'])
                mycursor.execute(sql)
            db.commit()
        sql = "select * from car"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        post = []
        z = 0
        for i in myresult:
            z = z + 1
            filename = "static/image/" + str(i[0]) + ".png"
            try:
                pilImg = Image.open(cStringIO.StringIO(str(i[12])))
                pilImg.thumbnail((200, 300), Image.ANTIALIAS)
                pilImg.save(filename)
            except IOError:
                print "=====Error========"
                print i
                print "=================="
            post.append([
                i[0],
                str(i[1]).capitalize(),
                str(i[2]).capitalize(),
                str(i[3]).capitalize(), i[4],
                str(i[5]).capitalize(), i[6],
                str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                i[13], i[14], i[15], i[16]
            ])
        ###print post
        return render_template("tablemobil.html", post=post)
    return redirect(url_for('menu'))


@application.route('/ModalMobil/<kode>', methods=['GET', 'POST'])
def ModalMobil(kode):
    myresult = []
    db = conn()
    mycursor = db.cursor()
    sql = "SELECT * from car where idmobil = %s" % (kode)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    post = []
    z = 0
    for i in myresult:
        z = z + 1
        filename = "static/image/" + str(i[0]) + ".png"
        try:
            pilImg = Image.open(cStringIO.StringIO(str(i[12])))
            pilImg.thumbnail((200, 300), Image.ANTIALIAS)
            pilImg.save(filename)
        except IOError:
            print "=====Error========"
            print i
            print "=================="
        post.append([
            i[0],
            str(i[1]).capitalize(),
            str(i[2]).capitalize(),
            str(i[3]).capitalize(), i[4],
            str(i[5]).capitalize(), i[6],
            str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename, i[13],
            i[14], i[15], i[16]
        ])
    ###print post
    return render_template("ModalMobil.html", post=post, kode=kode)


@application.route('/mobiluser', methods=['GET', 'POST'])
def mobiluser():
    if g.user:
        myresult = []
        db = conn()
        mycursor = db.cursor()
        sql = "select * from car where harga > (select b.harga1 from user_profile as a inner join hargamobil as b on a.anggaran=b.Ket where a.nama = '%s') and harga < (select b.harga2 from user_profile as a inner join hargamobil as b on a.anggaran=b.Ket where a.nama = '%s')" % (
            session['user'], session['user'])
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        post = []
        z = 0
        kirim = pilih()
        for i in myresult:
            z = z + 1
            pilImg = Image.open(cStringIO.StringIO(str(i[12])))
            pilImg.thumbnail((200, 300), Image.ANTIALIAS)
            filename = "static/image/" + str(i[0]) + ".png"
            pilImg.save(filename)
            post.append([
                i[0],
                str(i[1]).capitalize(),
                str(i[2]).capitalize(),
                str(i[3]).capitalize(), i[4],
                str(i[5]).capitalize(), i[6],
                str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                i[13], i[14], i[15], i[16]
            ])
        return render_template("mobiluser.html", post=post, kirim=kirim)
    return redirect(url_for('menu'))


@application.route('/listallmobiluser', methods=['GET', 'POST'])
def listallmobiluser():
    if g.user:
        db = conn()
        mycursor = db.cursor()
        sql = "SELECT a.idmobil FROM car as a inner join rating as b on a.idmobil = b.car_id where b.user_id = %s" % (
            session['id'])
        mycursor.execute(sql)
        myresult9 = mycursor.fetchall()
        if len(myresult9) < 3:
            return redirect(url_for('PilihMobilRegis'))
        myresult = []
        kirim = []
        hasilcari = ""
        if request.method == 'POST':
            if request.form["merk"] == "":
                merk = "%"
            else:
                merk = request.form["merk"]
                hasilcari = hasilcari + merk + " / "

            if request.form["jenis"] == "":
                jenis = "%"
            else:
                jenis = request.form["jenis"]
                hasilcari = hasilcari + jenis + " / "

            if request.form["varian"] == "":
                varian = "%"
            else:
                varian = request.form["varian"]
                hasilcari = hasilcari + varian + " / "

            if request.form["cc"] == "":
                cc = "%"
            else:
                cc = request.form["cc"]
                hasilcari = hasilcari + cc + " / "

            if request.form["transmisi"] == "":
                transmisi = "%"
            else:
                transmisi = request.form["transmisi"]
                hasilcari = hasilcari + transmisi + " / "

            if request.form["harga"] == "":
                harga = "%"
            else:
                harga = request.form["harga"]
                hasilcari = hasilcari + harga + " / "

            if request.form["warna"] == "":
                warna = "%"
            else:
                warna = request.form["warna"]
                hasilcari = hasilcari + warna + " / "

            if request.form["seater"] == "":
                seater = "%"
            else:
                seater = request.form["seater"]
                hasilcari = hasilcari + seater + " / "

            if request.form["aftersale"] == "":
                aftersale = "%"
            else:
                aftersale = request.form["aftersale"]
                hasilcari = hasilcari + aftersale + " / "

            if request.form["fuel"] == "":
                gasoline = "%"
            else:
                gasoline = request.form["fuel"]
                hasilcari = hasilcari + gasoline + " / "

            #hasilcari=merk+" / "+jenis+" / "+varian+" / "+cc+" / "+transmisi+" / "+harga+" / "+warna
            res = listallmobilusercari(merk, jenis, varian, cc, transmisi,
                                       harga, warna, seater, aftersale,
                                       gasoline)
            myresult = res[0][0]
            s = ""
            for t in res[1][0]:
                s += str(t[0]) + ","
            kodeid = s[:-1]
            ##print kodeid
            kirim = pilihcari(kodeid)
            post = []
            post2 = []
            z = 0
            kirim2 = pilih()
            ##print kirim2
            ##print myresult
            for i in myresult:
                z = z + 1
                pilImg = Image.open(cStringIO.StringIO(str(i[12])))
                pilImg.thumbnail((200, 300), Image.ANTIALIAS)
                filename = "static/image/" + str(i[0]) + ".png"
                pilImg.save(filename)
                post.append([
                    i[0],
                    str(i[1]).capitalize(),
                    str(i[2]).capitalize(),
                    str(i[3]).capitalize(), i[4],
                    str(i[5]).capitalize(), i[6],
                    str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                    i[13], i[14], i[15], i[16]
                ])
                if z <= 10:
                    post2.append([
                        i[0],
                        str(i[1]).capitalize(),
                        str(i[2]).capitalize(),
                        str(i[3]).capitalize(), i[4],
                        str(i[5]).capitalize(), i[6],
                        str(i[7]).capitalize(), i[8], i[9], i[10], i[11],
                        filename, i[13], i[14], i[15], i[16]
                    ])
            return render_template("listallmobiluser.html",
                                   post=post,
                                   kirim=kirim,
                                   kirim2=kirim2,
                                   hasilcari=hasilcari,
                                   post2=post2)
        else:
            db = conn()
            mycursor = db.cursor()
            sql = "select * from car"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            sqlpilihuser = " as a inner join rating as b on a.idmobil=b.car_id inner join user_profile as c on b.user_id=c.id where harga > (select b.harga1 from user_profile as a inner join hargamobil as b on a.anggaran=b.Ket where a.nama = '%s') and harga < (select b.harga2 from user_profile as a inner join hargamobil as b on a.anggaran=b.Ket where a.nama = '%s')  and c.nama = '%s' " % (
                session['user'], session['user'], session['user'])
            kirim = pilih()
            post = []
            post2 = []
            z = 0
            kirim2 = pilih()
            ###print kirim2[4]
            for i in myresult:
                z = z + 1
                pilImg = Image.open(cStringIO.StringIO(str(i[12])))
                pilImg.thumbnail((200, 300), Image.ANTIALIAS)
                filename = "static/image/" + str(i[0]) + ".png"
                pilImg.save(filename)
                post.append([
                    i[0],
                    str(i[1]).capitalize(),
                    str(i[2]).capitalize(),
                    str(i[3]).capitalize(), i[4],
                    str(i[5]).capitalize(), i[6],
                    str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                    i[13], i[14], i[15], i[16]
                ])
                #if z<=10:
                #	post2.append([i[0], str(i[1]).capitalize(), str(i[2]).capitalize(), str(i[3]).capitalize(), i[4], str(i[5]).capitalize(), i[6], str(i[7]).capitalize(), i[8], i[9], i[10],i[11], filename,i[13],i[14],i[15],i[16]])
            return render_template("listallmobiluser.html",
                                   post=post,
                                   kirim=kirim,
                                   kirim2=kirim2,
                                   hasilcari=hasilcari,
                                   post2=post2)
    return redirect(url_for('menu'))


@application.route('/PilihMobilRegis', methods=['GET', 'POST'])
def PilihMobilRegis():
    if g.user:
        if request.method == 'POST':
            db = conn()
            mycursor = db.cursor()
            sql = "SELECT * from rating where car_id = %s and user_id=%s" % (
                session['kodemob'], session['id'])
            mycursor.execute(sql)
            myresult1 = mycursor.fetchall()
            if len(myresult1) == 0:
                sql = "insert into rating(user_id, car_id, ratings) values (%s, %s, %s)"
                args = (session['id'], session['kodemob'],
                        request.form['rating'])
                mycursor.execute(sql, args)
            else:
                sql = "UPDATE rating set ratings = %s where car_id= %s and user_id=%s" % (
                    request.form['rating'], session['kodemob'], session['id'])
                mycursor.execute(sql)
            db.commit()
            sql = "SELECT avg(ratings) from rating where car_id = %s" % (
                session['kodemob'])
            mycursor.execute(sql)
            myresult1 = mycursor.fetchall()
            if len(myresult1) > 0:
                sql = "UPDATE car set rating = %s where idmobil  = %s "
                args = (myresult1[0][0], session['kodemob'])
                mycursor.execute(sql, args)
                db.commit()
        myresult = []
        db = conn()
        mycursor = db.cursor()
        sql = "select * from car"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        post = []
        z = 0
        kirim = pilih()
        kirim2 = pilih()

        for i in myresult:
            z = z + 1
            pilImg = Image.open(cStringIO.StringIO(str(i[12])))
            pilImg.thumbnail((200, 300), Image.ANTIALIAS)
            filename = "static/image/" + str(i[0]) + ".png"
            pilImg.save(filename)
            post.append([
                i[0],
                str(i[1]).capitalize(),
                str(i[2]).capitalize(),
                str(i[3]).capitalize(), i[4],
                str(i[5]).capitalize(), i[6],
                str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                i[13], i[14], i[15], i[16]
            ])

        sql = "SELECT a.idmobil FROM car as a inner join rating as b on a.idmobil = b.car_id where b.user_id = %s" % (
            session['id'])
        mycursor.execute(sql)
        myresult2 = mycursor.fetchall()
        jml = len(myresult2)
        if jml >= 3:
            simuser(session['id'])
            simmobil(session['id'])
        return render_template("PilihMobilRegis.html",
                               post=post,
                               kirim=kirim,
                               kirim2=kirim2,
                               jml=jml)
    return redirect(url_for('menu'))


@application.route('/ModalPilihMobilRegis/<kode>', methods=['GET', 'POST'])
def ModalPilihMobilRegis(kode):
    kode = kode
    myresult = []
    db = conn()
    mycursor = db.cursor()
    session['kodemob'] = kode
    sql = "SELECT ratings from rating where car_id = %s and user_id=%s" % (
        kode, session['id'])
    mycursor.execute(sql)
    myresult1 = mycursor.fetchall()
    rat = 0
    if len(myresult1) > 0:
        rat = myresult1[0][0]
    sql = "SELECT * from car where idmobil ='%s'" % (kode)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    post = []
    z = 0
    for i in myresult:
        z = z + 1
        pilImg = Image.open(cStringIO.StringIO(str(i[12])))
        pilImg.thumbnail((200, 300), Image.ANTIALIAS)
        filename = "static/image/" + str(i[0]) + ".png"
        pilImg.save(filename)
        post.append([
            i[0],
            str(i[1]).capitalize(),
            str(i[2]).capitalize(),
            str(i[3]).capitalize(), i[4],
            str(i[5]).capitalize(), i[6],
            str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename, i[13],
            i[14], i[15], i[16]
        ])
    return render_template("ModalPilihMobilRegis.html",
                           post=post,
                           rat=rat,
                           kode=kode)


#@application.route('/listallmobilusercari/<merk>/<jenis>/<varian>/<cc>/<transmisi>/<harga>/<warna>', methods=['GET', 'POST'])
def listallmobilusercari2(merk, jenis, varian, cc, transmisi, harga, warna,
                          seater, aftersale, gasoline):
    myresult = []
    db = conn()
    mycursor = db.cursor()
    ###print harga
    if harga == "%":
        ###print "kadieu"
        sql = "select * from car where merk like '%s' and jenis like '%s' and varian like '%s' and cc like '%s' and transmisi like '%s' and harga like '%s' and warna like '%s' and seater like '%s' and aftersale like '%s' and gasoline like '%s'" % (
            merk, jenis, varian, cc, transmisi, harga, warna, seater,
            aftersale, gasoline)
    else:
        ###print "kaditu"
        sql = "select * from car where merk like '%s' and jenis like '%s' and varian like '%s' and cc like '%s' and transmisi like '%s'  and warna like '%s' and harga > (select harga1 from  hargamobil where Ket = '%s') and harga < (select harga2 from  hargamobil where Ket = '%s') and seater like '%s' and aftersale like '%s' and gasoline like '%s'" % (
            merk, jenis, varian, cc, transmisi, warna, harga, harga, seater,
            aftersale, gasoline)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


def listallmobilusercari(merk, jenis, varian, cc, transmisi, harga, warna,
                         seater, aftersale, gasoline):
    db = conn()
    mycursor = db.cursor()
    if merk == "%":
        merk = ""
    else:
        merk = merk.upper()

    if jenis == "%":
        jenis = ""
    else:
        jenis = jenis.upper()

    if varian == "%":
        varian = ""
    else:
        varian = varian.upper()

    if cc == "%":
        cc = ""

    if transmisi == "%":
        transmisi = ""
    else:
        transmisi = transmisi.upper()

    if harga == "%":
        harga = ""

    if warna == "%":
        warna = ""
    else:
        warna = warna.upper()

    if seater == "%":
        seater = ""

    if aftersale == "%":
        aftersale = ""

    if gasoline == "%":
        gasoline = ""

    ab = ("", "", merk, jenis, varian, cc, transmisi, warna, harga, seater,
          aftersale, gasoline)

    sql = "SELECT (idmobil),(rating),upper(merk),upper(jenis),upper(varian),cc,upper(transmisi),upper(warna),harga,seater,aftersale,gasoline from car"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    latih = 0
    a = 0
    b = 0
    c = 0
    d = []
    m = []
    for h in myresult:
        uji = 0
        a = 0
        d = []
        kolom = 0
        #print "Pengolahan Jarak Euclid ke-"+str(latih+1)
        for k in ab:
            if k != "":
                #print "Data testing  ke-"+str(uji+1)
                #print "Data training ke-"+str(latih+1)
                b = 0
                c = 0
                atas = 0
                bawahdepan = 0
                bawahbelakang = 0
                bawah = 0
                test = []
                train = []
                cossim = 0
                if (kolom == 2) or (kolom == 3) or (kolom == 4) or (
                        kolom == 6) or (kolom == 7):
                    #print "   Data testing  : "+str(k)
                    for j in k:
                        #print "      > ord("+str(j)+") = "+str(ord(j))
                        test.append(ord(j))
                        bawahdepan = bawahdepan + (ord(j)**2)
                    #print "   Data training : "+str(h[a])
                    for i in h[a]:
                        #print "      > ord("+str(i)+") = "+str(ord(i))
                        train.append(ord(i))
                        bawahbelakang = bawahbelakang + (ord(i)**2)
                    for asci in range(len(test)):
                        try:
                            atas = float(atas) + (float(test[asci]) *
                                                  float(train[asci]))
                        except:
                            atas = atas
                    bawahdepan = float(bawahdepan)**0.5
                    bawahbelakang = float(bawahbelakang)**0.5
                    bawah = float(bawahdepan) * float(bawahbelakang)
                    atas = round(atas, 3)
                    bawah = round(bawah, 3)
                    cossim = float(atas) / float(bawah)
                    #print "   Similarity = "+str(cossim)
                    #print ""
                    d.append(1 - cossim)
                if (kolom == 5) or (kolom == 8) or (kolom == 9) or (
                        kolom == 10) or (kolom == 11):
                    b = float(k)
                    c = float(h[a])
                    #print "   Data testing  : "+str(b)
                    #print "   Data training : "+str(c)
                    if kolom == 5:
                        sql = "SELECT MAX(cc) FROM car"
                        mycursor.execute(sql)
                        maksi = mycursor.fetchall()
                        sql = "SELECT MIN(cc) FROM car"
                        mycursor.execute(sql)
                        minim = mycursor.fetchall()
                    elif kolom == 8:
                        sql = "SELECT MAX(harga) FROM car"
                        mycursor.execute(sql)
                        maksi = mycursor.fetchall()
                        sql = "SELECT MIN(harga) FROM car"
                        mycursor.execute(sql)
                        minim = mycursor.fetchall()
                    elif kolom == 9:
                        sql = "SELECT MAX(seater) FROM car"
                        mycursor.execute(sql)
                        maksi = mycursor.fetchall()
                        sql = "SELECT MIN(seater) FROM car"
                        mycursor.execute(sql)
                        minim = mycursor.fetchall()
                    elif kolom == 10:
                        sql = "SELECT MAX(aftersale) FROM car"
                        mycursor.execute(sql)
                        maksi = mycursor.fetchall()
                        sql = "SELECT MIN(aftersale) FROM car"
                        mycursor.execute(sql)
                        minim = mycursor.fetchall()
                    else:
                        sql = "SELECT MAX(gasoline) FROM car"
                        mycursor.execute(sql)
                        maksi = mycursor.fetchall()
                        sql = "SELECT MIN(gasoline) FROM car"
                        mycursor.execute(sql)
                        minim = mycursor.fetchall()
                    jmaksimal = abs(b - maksi[0][0])
                    jminimal = abs(b - minim[0][0])
                    if jmaksimal > jminimal:
                        distance = abs(b - c) / jmaksimal
                    else:
                        distance = abs(b - c) / jminimal
                    #print "   Jarak      = "+str(distance)
                    #print ""
                    d.append(distance)
            a = a + 1
            kolom = kolom + 1
            uji = uji + 1
        latih = latih + 1
        f = 0
        for g in d:
            f = f + (g**2)
        n = 0
        n = f**0.5
        m.append(n)
    #print "Jarak Euclidean = "
    #print str(m)
    tigadata = {}
    duadata = {}
    a = 0
    for o in m:
        tigadata[(myresult[a][0])] = {'rat': (myresult[a][1]), 'euc': o}
        duadata[(myresult[a][0])] = o
        a = a + 1
    duaakhir = sorted(sorted(duadata.items(), key=lambda t: t[0]),
                      key=lambda t: t[1])
    tigaakhir = sorted(sorted(tigadata.keys(),
                              key=lambda t: (tigadata[t]['rat']),
                              reverse=True),
                       key=lambda t: float(tigadata[t]['euc']))
    #print "Jarak Euclidean setelah disorting = "
    #print str(duaakhir)
    p5 = (((duaakhir[len(duaakhir) - 1][1]) -
           (duaakhir[0][1])) * 0.05) + (duaakhir[0][1])
    p10 = (((duaakhir[len(duaakhir) - 1][1]) -
            (duaakhir[0][1])) * 0.1) + (duaakhir[0][1])
    p20 = (((duaakhir[len(duaakhir) - 1][1]) -
            (duaakhir[0][1])) * 0.2) + (duaakhir[0][1])
    p40 = (((duaakhir[len(duaakhir) - 1][1]) -
            (duaakhir[0][1])) * 0.4) + (duaakhir[0][1])
    p80 = (((duaakhir[len(duaakhir) - 1][1]) -
            (duaakhir[0][1])) * 0.8) + (duaakhir[0][1])
    #print ""
    #print "Awal             : "+str(duaakhir[0][1])
    #print ""
    #print "Akhir            : "+str((duaakhir[len(duaakhir)-1][1]))
    #print ""
    ulangp5 = 0
    ulangp10 = 0
    ulangp20 = 0
    ulangp40 = 0
    ulangp80 = 0
    i = 0
    for i in range(len(duaakhir)):
        if duaakhir[i][1] <= p5:
            ulangp5 = ulangp5 + 1
        if duaakhir[i][1] <= p10:
            ulangp10 = ulangp10 + 1
        if duaakhir[i][1] <= p20:
            ulangp20 = ulangp20 + 1
        if duaakhir[i][1] <= p40:
            ulangp40 = ulangp40 + 1
        if duaakhir[i][1] <= p80:
            ulangp80 = ulangp80 + 1
    #print "Jarak Maksi 5%   : "+str(p5) +"     , Jumlah Anggota   : "+str(ulangp5)
    #print ""
    #print "Jarak Maksi 10%  : "+str(p10)+"     , Jumlah Anggota   : "+str(ulangp10)
    #print ""
    #print "Jarak Maksi 20%  : "+str(p20)+"     , Jumlah Anggota   : "+str(ulangp20)
    #print ""
    #print "Jarak Maksi 40%  : "+str(p40)+"     , Jumlah Anggota   : "+str(ulangp40)
    #print ""
    #print "Jarak Maksi 80%  : "+str(p80)+"     , Jumlah Anggota   : "+str(ulangp80)
    r = []
    ka = 0
    #print "ID hasil seleksi (40%) Jarak Euclidean terdekat"
    for isi in tigaakhir:
        for q in duaakhir:
            if q[0] == isi:
                if q[1] <= p5:
                    sql = "select * from car where idmobil =%s" % (q[0])
                    mycursor.execute(sql)
                    myresult = mycursor.fetchall()
                    r.append(myresult[0])
                    #print " IDMobil = "+str(q[0])
        ka = ka + 1
        if ka == 10:
            for lokasi in duaakhir:
                if isi == lokasi[0]:
                    #print ""
                    #print "K=10     : "+str(lokasi[1])
                    akurasi10 = (1 - (
                        (lokasi[1] - duaakhir[0][1]) /
                        (duaakhir[len(duaakhir) - 1][1] - duaakhir[0][1]))
                                 ) * 100
            #print ""
            #print "Persentase Akurasi k=10   : "+str(akurasi10)
        if ka == 50:
            for lokasi in duaakhir:
                if isi == lokasi[0]:
                    #print ""
                    #print "K=50     : "+str(lokasi[1])
                    akurasi50 = (1 - (
                        (lokasi[1] - duaakhir[0][1]) /
                        (duaakhir[len(duaakhir) - 1][1] - duaakhir[0][1]))
                                 ) * 100
            #print ""
            #print "Persentase Akurasi k=50   : "+str(akurasi50)
        if ka == 100:
            for lokasi in duaakhir:
                if isi == lokasi[0]:
                    #print ""
                    #print "K=100    : "+str(lokasi[1])
                    akurasi100 = (1 - (
                        (lokasi[1] - duaakhir[0][1]) /
                        (duaakhir[len(duaakhir) - 1][1] - duaakhir[0][1]))
                                  ) * 100
            #print ""
            #print "Persentase Akurasi k=100  : "+str(akurasi100)
        if ka == 500:
            for lokasi in duaakhir:
                if isi == lokasi[0]:
                    #print ""
                    #print "K=500    : "+str(lokasi[1])
                    akurasi500 = (1 - (
                        (lokasi[1] - duaakhir[0][1]) /
                        (duaakhir[len(duaakhir) - 1][1] - duaakhir[0][1]))
                                  ) * 100
            #print ""
            #print "Persentase Akurasi k=500  : "+str(akurasi500)
        if ka == 1000:
            for lokasi in duaakhir:
                if isi == lokasi[0]:
                    #print ""
                    #print "K=1000   : "+str(lokasi[1])
                    akurasi1000 = (1 - (
                        (lokasi[1] - duaakhir[0][1]) /
                        (duaakhir[len(duaakhir) - 1][1] - duaakhir[0][1]))
                                   ) * 100
            #print ""
            #print "Persentase Akurasi k=1000 : "+str(akurasi1000)
    res = []
    res.append([r])
    res.append([r])
    ##print ""
    ##print ""
    ##print ""
    ##print ""
    ##print "---- FINISH ----"
    return res


def listallmobilusercarirelated(merk, jenis, varian, cc, transmisi, harga,
                                warna, seater, aftersale, gasoline):
    db = conn()
    mycursor = db.cursor()
    if merk == "%":
        merk = ""
    else:
        merk = merk.upper()

    if jenis == "%":
        jenis = ""
    else:
        jenis = jenis.upper()

    if varian == "%":
        varian = ""
    else:
        varian = varian.upper()

    if cc == "%":
        cc = ""

    if transmisi == "%":
        transmisi = ""
    else:
        transmisi = transmisi.upper()

    if harga == "%":
        harga = ""

    if warna == "%":
        warna = ""
    else:
        warna = warna.upper()

    if seater == "%":
        seater = ""

    if aftersale == "%":
        aftersale = ""

    if gasoline == "%":
        gasoline = ""

    ab = ("", "", merk, jenis, varian, cc, transmisi, warna, harga, seater,
          aftersale, gasoline)
    sql = "select upper(idmobil),upper(rating),upper(merk),upper(jenis),upper(varian),cc,upper(transmisi),upper(warna),harga,seater,aftersale,gasoline from car"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    latih = 0
    a = 0
    b = 0
    c = 0
    d = []
    m = []
    for h in myresult:
        uji = 0
        a = 0
        d = []
        kolom = 0
        for k in ab:
            if k != "":
                b = 0
                c = 0
                atas = 0
                bawahdepan = 0
                bawahbelakang = 0
                bawah = 0
                test = []
                train = []
                cossim = 0
                if (kolom == 2) or (kolom == 3) or (kolom == 4) or (
                        kolom == 6) or (kolom == 7):
                    for j in k:
                        test.append(ord(j))
                        bawahdepan = bawahdepan + (ord(j)**2)
                    for i in h[a]:
                        train.append(ord(i))
                        bawahbelakang = bawahbelakang + (ord(i)**2)
                    for asci in range(len(test)):
                        try:
                            atas = float(atas) + (float(test[asci]) *
                                                  float(train[asci]))
                        except:
                            atas = atas
                    bawahdepan = float(bawahdepan)**0.5
                    bawahbelakang = float(bawahbelakang)**0.5
                    bawah = float(bawahdepan) * float(bawahbelakang)
                    atas = round(atas, 3)
                    bawah = round(bawah, 3)
                    cossim = float(atas) / float(bawah)
                    d.append(1 - cossim)
                if (kolom == 5) or (kolom == 8) or (kolom == 9) or (
                        kolom == 10) or (kolom == 11):
                    b = float(k)
                    c = float(h[a])
                    if kolom == 5:
                        sql = "SELECT MAX(cc) FROM car"
                        mycursor.execute(sql)
                        maksi = mycursor.fetchall()
                        sql = "SELECT MIN(cc) FROM car"
                        mycursor.execute(sql)
                        minim = mycursor.fetchall()
                    elif kolom == 8:
                        sql = "SELECT MAX(harga) FROM car"
                        mycursor.execute(sql)
                        maksi = mycursor.fetchall()
                        sql = "SELECT MIN(harga) FROM car"
                        mycursor.execute(sql)
                        minim = mycursor.fetchall()
                    elif kolom == 9:
                        sql = "SELECT MAX(seater) FROM car"
                        mycursor.execute(sql)
                        maksi = mycursor.fetchall()
                        sql = "SELECT MIN(seater) FROM car"
                        mycursor.execute(sql)
                        minim = mycursor.fetchall()
                    elif kolom == 10:
                        sql = "SELECT MAX(aftersale) FROM car"
                        mycursor.execute(sql)
                        maksi = mycursor.fetchall()
                        sql = "SELECT MIN(aftersale) FROM car"
                        mycursor.execute(sql)
                        minim = mycursor.fetchall()
                    else:
                        sql = "SELECT MAX(gasoline) FROM car"
                        mycursor.execute(sql)
                        maksi = mycursor.fetchall()
                        sql = "SELECT MIN(gasoline) FROM car"
                        mycursor.execute(sql)
                        minim = mycursor.fetchall()
                    jmaksimal = abs(b - maksi[0][0])
                    jminimal = abs(b - minim[0][0])
                    if jmaksimal > jminimal:
                        distance = abs(b - c) / jmaksimal
                    else:
                        distance = abs(b - c) / jminimal
                    d.append(distance)
            a = a + 1
            kolom = kolom + 1
            uji = uji + 1
        latih = latih + 1
        f = 0
        for g in d:
            f = f + (g**2)
        n = 0
        n = f**0.5
        m.append(n)
    tigadata = {}
    duadata = {}
    a = 0
    for o in m:
        tigadata[(myresult[a][0])] = {'rat': (myresult[a][1]), 'euc': o}
        duadata[(myresult[a][0])] = o
        a = a + 1
    duaakhir = sorted(sorted(duadata.items(), key=lambda t: t[0]),
                      key=lambda t: t[1])
    tigaakhir = sorted(sorted(tigadata.keys(),
                              key=lambda t: (tigadata[t]['rat']),
                              reverse=True),
                       key=lambda t: float(tigadata[t]['euc']))
    p = (((duaakhir[len(duaakhir) - 1][1]) -
          (duaakhir[0][1])) * 0.2) + (duaakhir[0][1])
    r = []
    for isi in tigaakhir:
        for q in duaakhir:
            if q[0] == isi:
                if q[1] <= p:
                    sql = "select * from car where idmobil =%s" % (q[0])
                    mycursor.execute(sql)
                    myresult = mycursor.fetchall()
                    r.append(myresult[0])
    res = []
    res.append([r])
    return res


@application.route('/listsugestlmobiluser', methods=['GET', 'POST'])
def listsugestlmobiluser():
    if g.user:
        db = conn()
        mycursor = db.cursor()
        sql = "SELECT a.idmobil FROM car as a inner join rating as b on a.idmobil = b.car_id where b.user_id = %s" % (
            session['id'])
        mycursor.execute(sql)
        myresult9 = mycursor.fetchall()
        if len(myresult9) < 3:
            return redirect(url_for('PilihMobilRegis'))
        myresult = []
        kirim = []
        hasilcari = ""
        if request.method == 'POST':
            if request.form["merk"] == "":
                merk = "%"
            else:
                merk = request.form["merk"]
                hasilcari = hasilcari + merk + " / "

            if request.form["jenis"] == "":
                jenis = "%"
            else:
                jenis = request.form["jenis"]
                hasilcari = hasilcari + jenis + " / "

            if request.form["varian"] == "":
                varian = "%"
            else:
                varian = request.form["varian"]
                hasilcari = hasilcari + varian + " / "

            if request.form["cc"] == "":
                cc = "%"
            else:
                cc = request.form["cc"]
                hasilcari = hasilcari + cc + " / "

            if request.form["transmisi"] == "":
                transmisi = "%"
            else:
                transmisi = request.form["transmisi"]
                hasilcari = hasilcari + transmisi + " / "

            if request.form["harga"] == "":
                harga = "%"
            else:
                harga = request.form["harga"]
                hasilcari = hasilcari + harga + " / "

            if request.form["warna"] == "":
                warna = "%"
            else:
                warna = request.form["warna"]
                hasilcari = hasilcari + warna + " / "

            if request.form["seater"] == "":
                seater = "%"
            else:
                seater = request.form["seater"]
                hasilcari = hasilcari + seater + " / "

            if request.form["aftersale"] == "":
                aftersale = "%"
            else:
                aftersale = request.form["aftersale"]
                hasilcari = hasilcari + aftersale + " / "

            if request.form["fuel"] == "":
                gasoline = "%"
            else:
                gasoline = request.form["fuel"]
                hasilcari = hasilcari + gasoline + " / "

            #hasilcari=merk+"/"+jenis+"/"+varian+"/"+cc+"/"+transmisi+"/"+harga+"/"+warna
            res = listallmobilusercari(merk, jenis, varian, cc, transmisi,
                                       harga, warna, seater, aftersale,
                                       gasoline)
            myresult = res[0][0]
            s = ""
            for t in res[1][0]:
                s += str(t[0]) + ","
            kodeid = s[:-1]
            ##print kodeid
            kirim = pilihcari(kodeid)
            post = []
            post2 = []
            z = 0
            kirim2 = pilih()
            ##print kirim2
            ##print myresult
            for i in myresult:
                z = z + 1
                pilImg = Image.open(cStringIO.StringIO(str(i[12])))
                pilImg.thumbnail((200, 300), Image.ANTIALIAS)
                filename = "static/image/" + str(i[0]) + ".png"
                pilImg.save(filename)
                post.append([
                    i[0],
                    str(i[1]).capitalize(),
                    str(i[2]).capitalize(),
                    str(i[3]).capitalize(), i[4],
                    str(i[5]).capitalize(), i[6],
                    str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename
                ])
                if z <= 10:
                    post2.append([
                        i[0],
                        str(i[1]).capitalize(),
                        str(i[2]).capitalize(),
                        str(i[3]).capitalize(), i[4],
                        str(i[5]).capitalize(), i[6],
                        str(i[7]).capitalize(), i[8], i[9], i[10], i[11],
                        filename, i[13], i[14], i[15], i[16]
                    ])
            return render_template("listallmobiluser.html",
                                   post=post,
                                   kirim=kirim,
                                   kirim2=kirim2,
                                   hasilcari=hasilcari,
                                   post2=post2)
        else:
            db = conn()
            mycursor = db.cursor()
            sql = "select * from car where harga < (select b.harga2 from user_profile as a inner join hargamobil as b on a.anggaran=b.Ket where a.nama = '%s')" % (
                session['user'])
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            sqlpilihuser = " where harga < (select b.harga2 from user_profile as a inner join hargamobil as b on a.anggaran=b.Ket where a.nama = '%s')" % (
                session['user'])
            kirim = pilihuser(sqlpilihuser)
            post = []
            post2 = []
            z = 0
            kirim2 = pilih()
            for i in myresult:
                z = z + 1
                pilImg = Image.open(cStringIO.StringIO(str(i[12])))
                pilImg.thumbnail((200, 300), Image.ANTIALIAS)
                filename = "static/image/" + str(i[0]) + ".png"
                pilImg.save(filename)
                post.append([
                    i[0],
                    str(i[1]).capitalize(),
                    str(i[2]).capitalize(),
                    str(i[3]).capitalize(), i[4],
                    str(i[5]).capitalize(), i[6],
                    str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                    i[13], i[14], i[15], i[16]
                ])
            return render_template("listallmobiluser.html",
                                   post=post,
                                   kirim=kirim,
                                   kirim2=kirim2,
                                   hasilcari=hasilcari,
                                   post2=post2)
    return redirect(url_for('menu'))


@application.route('/listratinglmobiluser', methods=['GET', 'POST'])
def listratinglmobiluser():
    if g.user:
        db = conn()
        mycursor = db.cursor()
        sql = "SELECT a.idmobil FROM car as a inner join rating as b on a.idmobil = b.car_id where b.user_id = %s" % (
            session['id'])
        mycursor.execute(sql)
        myresult9 = mycursor.fetchall()
        if len(myresult9) < 3:
            return redirect(url_for('PilihMobilRegis'))
        myresult = []
        kirim = []
        hasilcari = ""
        if request.method == 'POST':
            if request.form["merk"] == "":
                merk = "%"
            else:
                merk = request.form["merk"]
                hasilcari = hasilcari + merk + " / "

            if request.form["jenis"] == "":
                jenis = "%"
            else:
                jenis = request.form["jenis"]
                hasilcari = hasilcari + jenis + " / "

            if request.form["varian"] == "":
                varian = "%"
            else:
                varian = request.form["varian"]
                hasilcari = hasilcari + varian + " / "

            if request.form["cc"] == "":
                cc = "%"
            else:
                cc = request.form["cc"]
                hasilcari = hasilcari + cc + " / "

            if request.form["transmisi"] == "":
                transmisi = "%"
            else:
                transmisi = request.form["transmisi"]
                hasilcari = hasilcari + transmisi + " / "

            if request.form["harga"] == "":
                harga = "%"
            else:
                harga = request.form["harga"]
                hasilcari = hasilcari + harga + " / "

            if request.form["warna"] == "":
                warna = "%"
            else:
                warna = request.form["warna"]
                hasilcari = hasilcari + warna + " / "

            if request.form["seater"] == "":
                seater = "%"
            else:
                seater = request.form["seater"]
                hasilcari = hasilcari + seater + " / "

            if request.form["aftersale"] == "":
                aftersale = "%"
            else:
                aftersale = request.form["aftersale"]
                hasilcari = hasilcari + aftersale + " / "

            if request.form["fuel"] == "":
                gasoline = "%"
            else:
                gasoline = request.form["fuel"]
                hasilcari = hasilcari + gasoline + " / "

            #hasilcari=merk+" / "+jenis+" / "+varian+" / "+cc+" / "+transmisi+" / "+harga+" / "+warna
            res = listallmobilusercari(merk, jenis, varian, cc, transmisi,
                                       harga, warna, seater, aftersale,
                                       gasoline)
            myresult = res[0][0]
            s = ""
            for t in res[1][0]:
                s += str(t[0]) + ","
            kodeid = s[:-1]
            ##print kodeid
            kirim = pilihcari(kodeid)
            post = []
            post2 = []
            z = 0
            kirim2 = pilih()
            ##print kirim2
            ##print myresult
            for i in myresult:
                z = z + 1
                pilImg = Image.open(cStringIO.StringIO(str(i[12])))
                pilImg.thumbnail((200, 300), Image.ANTIALIAS)
                filename = "static/image/" + str(i[0]) + ".png"
                pilImg.save(filename)
                post.append([
                    i[0],
                    str(i[1]).capitalize(),
                    str(i[2]).capitalize(),
                    str(i[3]).capitalize(), i[4],
                    str(i[5]).capitalize(), i[6],
                    str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                    i[13], i[14], i[15], i[16]
                ])
                if z <= 10:
                    post2.append([
                        i[0],
                        str(i[1]).capitalize(),
                        str(i[2]).capitalize(),
                        str(i[3]).capitalize(), i[4],
                        str(i[5]).capitalize(), i[6],
                        str(i[7]).capitalize(), i[8], i[9], i[10], i[11],
                        filename, i[13], i[14], i[15], i[16]
                    ])
            return render_template("listallmobiluser.html",
                                   post=post,
                                   kirim=kirim,
                                   kirim2=kirim2,
                                   hasilcari=hasilcari,
                                   post2=post2)
        else:
            db = conn()
            mycursor = db.cursor()
            sql = "SELECT * from car as a inner join rating as b on a.idmobil=b.car_id inner join user_profile as c on b.user_id=c.id where c.id = '%s'" % (
                session['id'])
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            sqlpilihuser = " as a inner join rating as b on a.idmobil=b.car_id inner join user_profile as c on b.user_id=c.id where  c.id = '%s' " % (
                session['id'])
            kirim = pilihratinguser(sqlpilihuser)
            post = []
            post2 = []
            z = 0
            kirim2 = pilih()
            ##print kirim2[4]
            for i in myresult:
                z = z + 1
                pilImg = Image.open(cStringIO.StringIO(str(i[12])))
                pilImg.thumbnail((200, 300), Image.ANTIALIAS)
                filename = "static/image/" + str(i[0]) + ".png"
                pilImg.save(filename)
                post.append([
                    i[0],
                    str(i[1]).capitalize(),
                    str(i[2]).capitalize(),
                    str(i[3]).capitalize(), i[4],
                    str(i[5]).capitalize(), i[6],
                    str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                    i[13], i[14], i[15], i[16]
                ])
            return render_template("listallmobiluser.html",
                                   post=post,
                                   kirim=kirim,
                                   kirim2=kirim2,
                                   hasilcari=hasilcari,
                                   post2=post2)
    return redirect(url_for('menu'))


@application.route('/listallmobilusersinggle/<kode>', methods=['GET', 'POST'])
def listallmobilusersinggle(kode):
    if g.user:
        myresult = []
        db = conn()
        mycursor = db.cursor()
        sql = "select * from car where idmobil=%s" % (kode)
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        post = []
        z = 0
        for i in myresult:
            z = z + 1
            pilImg = Image.open(cStringIO.StringIO(str(i[12])))
            pilImg.thumbnail((200, 300), Image.ANTIALIAS)
            filename = "static/image/" + str(i[0]) + ".png"
            pilImg.save(filename)
            sql = "select ratings from rating where car_id = %s and user_id=%s" % (
                i[0], session['id'])
            mycursor.execute(sql)
            myresult1 = mycursor.fetchall()
            rat = 0
            if len(myresult1) > 0:
                rat = myresult1[0][0]
            post.append([
                i[0],
                str(i[1]).capitalize(),
                str(i[2]).capitalize(),
                str(i[3]).capitalize(), i[4],
                str(i[5]).capitalize(), i[6],
                str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                i[13], i[14], i[15], i[16]
            ])

        merk = myresult[0][1]
        jenis = myresult[0][2]
        varian = myresult[0][3]
        cc = "%"
        transmisi = myresult[0][5]
        harga = "%"
        warna = myresult[0][7]
        seater = "%"
        aftersale = "%"
        gasoline = "%"

        res2 = listallmobilusercarirelated(merk, jenis, varian, cc, transmisi,
                                           harga, warna, seater, aftersale,
                                           gasoline)
        myresult2 = res2[0][0]
        relatedpost = []
        for i in myresult2:
            z = z + 1
            pilImg = Image.open(cStringIO.StringIO(str(i[12])))
            pilImg.thumbnail((200, 300), Image.ANTIALIAS)
            filename = "static/image/" + str(i[0]) + ".png"
            pilImg.save(filename)
            if z <= 11:
                relatedpost.append([
                    i[0],
                    str(i[1]).capitalize(),
                    str(i[2]).capitalize(),
                    str(i[3]).capitalize(), i[4],
                    str(i[5]).capitalize(), i[6],
                    str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                    i[13], i[14], i[15], i[16]
                ])

        return render_template("listallmobilusersinggle.html",
                               post=post,
                               rat=rat,
                               relatedpost=relatedpost)
    return redirect(url_for('menu'))


@application.route('/rating2', methods=['GET', 'POST'])
def rating2():
    if g.user:
        return render_template("rating.html")
    return redirect(url_for('menu'))


@application.route('/rating/<kode>', methods=['GET', 'POST'])
def rating(kode):
    if g.user:
        myresult = []
        db = conn()
        mycursor = db.cursor()
        if request.method == 'POST':
            sql = "SELECT * from rating where car_id = %s and user_id=%s" % (
                kode, session['id'])
            mycursor.execute(sql)
            myresult1 = mycursor.fetchall()
            if len(myresult1) == 0:
                sql = "insert into rating(user_id, car_id, ratings) values (%s, %s, %s)"
                args = (session['id'], kode, request.form['rating'])
                mycursor.execute(sql, args)
            else:
                sql = "UPDATE rating set ratings = %s where car_id= %s and user_id=%s" % (
                    request.form['rating'], kode, session['id'])
                mycursor.execute(sql)
            db.commit()
            sql = "SELECT avg(ratings) from rating where car_id = %s" % (kode)
            mycursor.execute(sql)
            myresult1 = mycursor.fetchall()
            if len(myresult1) > 0:
                sql = "UPDATE car set rating = %s where idmobil  = %s "
                args = (myresult1[0][0], kode)
                mycursor.execute(sql, args)
                db.commit()
            simuser(session['id'])
            simmobil(session['id'])
        sql = "SELECT ratings from rating where car_id = %s and user_id=%s" % (
            kode, session['id'])
        mycursor.execute(sql)
        myresult1 = mycursor.fetchall()
        rat = 0
        if len(myresult1) > 0:
            rat = myresult1[0][0]
        sql = "SELECT * from car where idmobil ='%s'" % (kode)
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        post = []
        z = 0
        for i in myresult:
            z = z + 1
            pilImg = Image.open(cStringIO.StringIO(str(i[12])))
            pilImg.thumbnail((200, 300), Image.ANTIALIAS)
            filename = "static/image/" + str(i[0]) + ".png"
            pilImg.save(filename)
            post.append([
                i[0],
                str(i[1]).capitalize(),
                str(i[2]).capitalize(),
                str(i[3]).capitalize(), i[4],
                str(i[5]).capitalize(), i[6],
                str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                i[13], i[14], i[15], i[16]
            ])
        ##print mycursor.rowcount, "record inserted."
        merk = myresult[0][1]
        jenis = myresult[0][2]
        varian = myresult[0][3]
        cc = "%"
        transmisi = myresult[0][5]
        harga = "%"
        warna = myresult[0][7]
        seater = "%"
        aftersale = "%"
        gasoline = "%"

        res2 = listallmobilusercarirelated(merk, jenis, varian, cc, transmisi,
                                           harga, warna, seater, aftersale,
                                           gasoline)
        myresult2 = res2[0][0]
        relatedpost = []
        for i in myresult2:
            z = z + 1
            pilImg = Image.open(cStringIO.StringIO(str(i[12])))
            pilImg.thumbnail((200, 300), Image.ANTIALIAS)
            filename = "static/image/" + str(i[0]) + ".png"
            pilImg.save(filename)
            if z <= 11:
                relatedpost.append([
                    i[0],
                    str(i[1]).capitalize(),
                    str(i[2]).capitalize(),
                    str(i[3]).capitalize(), i[4],
                    str(i[5]).capitalize(), i[6],
                    str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                    i[13], i[14], i[15], i[16]
                ])
        return render_template("rating.html",
                               post=post,
                               rat=rat,
                               relatedpost=relatedpost)
    return redirect(url_for('menu'))


@application.route('/tablemobillogin', methods=['GET', 'POST'])
def tablemibillogin():
    if g.user:
        myresult = []
        db = conn()
        mycursor = db.cursor()
        sql = "SELECT * from car where harga > (select b.harga1 from user_profile as a inner join hargamobil as b on a.anggaran=b.Ket where a.nama = '%s') and harga < (select b.harga2 from user_profile as a inner join hargamobil as b on a.anggaran=b.Ket where a.nama = '%s')" % (
            session['user'], session['user'])

        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        #lis1 = str(myresult)
        #lis2 = ast.literal_eval(lis1)
        ###print myresult[0][0]
        post = []
        z = 0
        for i in myresult:
            #dirc="../static/image/kosong.png"#+str(z)+'.jpg'
            z = z + 1
            #img=Image.open(i[11])
            #dirc.save("static\image", format)
            pilImg = Image.open(cStringIO.StringIO(str(i[12])))
            pilImg.thumbnail((200, 300), Image.ANTIALIAS)

            #imgdata = base64.b64decode(pilImg)
            #file_like=io.BytesIO(imgdata)
            #filename = 'cek.png'  # I assume you have a way of picking unique filenames
            #with open(filename, 'wb') as f:
            #    f.write(pilImg)
            #pilImg.show()
            filename = "static/image/" + str(i[0]) + ".png"
            pilImg.save(filename)
            post.append([
                i[0],
                str(i[1]).capitalize(),
                str(i[2]).capitalize(),
                str(i[3]).capitalize(), i[4],
                str(i[5]).capitalize(), i[6],
                str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                i[13], i[14], i[15], i[16]
            ])

        ##print "================="
        ##print session['user']
        ##print "================="
        return render_template("mobiluser.html", post=post)
    return redirect(url_for('menu'))


@application.route('/regis', methods=['GET', 'POST'])
def regis():
    return render_template("regis.html")


# Metode 2 =======================================================================================
def simattmetode2(kode):
    usia = {
        '19 - 30 tahun': 1,
        '31 - 40 tahun': 2,
        '41 - 50 tahun': 3,
        '51 - 60 tahun': 4,
        'lebih dari 60 tahun': 5
    }
    jk = {'Laki-laki': 2, 'Perempuan': 1}
    pendapatan = {
        'Kurang dari Rp.8 juta': 1,
        'Antara Rp.8 juta hingga Rp.15 juta': 2,
        'Lebih dari Rp.15 juta': 3
    }
    pekerjaan = {
        'Pelajar': 1,
        'Wiraswasta': 2,
        'Pegawai Negeri Sipil': 4,
        'Pegawai Swasta': 3,
        'Professional': 5
    }
    anggaran = {
        'Kurang dari Rp.200 juta': 1,
        'Rp.200 juta - Rp.400 juta': 2,
        'Rp.400 juta - Rp.600 juta (tepat Rp.400 juta tidak termasuk)': 3,
        'Rp.600 juta - Rp.800 juta (tepat Rp.600 juta pas tidak termasuk)': 4,
        'Lebih dari Rp.800 juta': 5
    }

    data = []
    data2 = []
    data3 = []

    db = conn()
    mycursor = db.cursor()
    sql = "SELECT * from user_profile where id =%s" % (kode)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for a in myresult:
        data.append([
            usia[a[3]], jk[a[4]], pendapatan[a[5]], pekerjaan[a[6]],
            anggaran[a[7]]
        ])
    #jika user 1 harus di tambahkan
    sql = "SELECT * from rating where user_id = %s" % (kode)
    mycursor.execute(sql)
    myresult3 = mycursor.fetchall()
    if len(myresult3) > 0:
        #sql2="SELECT * from user_profile where `usia` <> '0'"
        sql2 = "SELECT * from (SELECT a.id as id, a.nama as nama, a.password as password, a.usia as usia, a.jk as jk, a.pendapatan as pendapatan, a.pekerjaan as pekerjaan, a.anggaran as anggaran, b.ratings as ratings from user_profile as a left join rating as b on a.id=b.user_id where `usia` <> '0' group by a.id) as c where c.ratings <> 'null' and c.usia <> '0' and c.id <> '0'"
        ##print "000001"
    else:
        #sql2="SELECT * from user_profile where `usia` <> '0' and id <> %s" %(kode)
        sql2 = "SELECT * from (SELECT a.id as id, a.nama as nama, a.password as password, a.usia as usia, a.jk as jk, a.pendapatan as pendapatan, a.pekerjaan as pekerjaan, a.anggaran as anggaran, b.ratings as ratings from user_profile as a left join rating as b on a.id=b.user_id where `usia` <> '0' group by a.id) as c where c.ratings <> 'null' and c.usia <> '0' and c.id <> '0' and c.id <> %s" % (
            kode)
        ##print "0000002"

    mycursor.execute(sql2)
    myresult2 = mycursor.fetchall()
    for a in myresult2:
        data2.append([
            usia[a[3]], jk[a[4]], pendapatan[a[5]], pekerjaan[a[6]],
            anggaran[a[7]]
        ])

    for a in range(0, len(data2)):
        atas = ((data[0][0] * data2[a][0]) + (data[0][1] * data2[a][1]) +
                (data[0][2] * data2[a][2]) + (data[0][3] * data2[a][3]) +
                (data[0][4] * data2[a][4]))
        bawah1 = (((data[0][0]**2) + (data[0][1]**2) + (data[0][2]**2) +
                   (data[0][3]**2) + (data[0][4]**2))**0.5)
        bawah2 = (((data2[a][0]**2) + (data2[a][1]**2) + (data2[a][2]**2) +
                   (data2[a][3]**2) + (data2[a][4]**2))**0.5)
        hasil = atas / (bawah1 * bawah2)
        data3.append([myresult[0][0], myresult2[a][0], str(hasil)])
    return data3


def ratingattmetode2(kode):
    data = []
    db = conn()
    mycursor = db.cursor()

    sql = "SELECT a.user_id,c.nama,a.car_id,a.ratings from rating as a inner join car as b on a.car_id = b.idmobil inner join user_profile as c on a.user_id=c.id and c.usia <> '0' and c.id <> '0' where a.user_id =%s" % (
        kode)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    sql2 = "SELECT a.user_id, COUNT(a.user_id) as jumlah from rating as a inner join car as b on a.car_id = b.idmobil inner join user_profile as c on a.user_id=c.id  where c.usia <> '0' and c.id <> '0' group by a.user_id HAVING ( COUNT(a.user_id) > 0 )"
    mycursor.execute(sql2)
    myresult2 = mycursor.fetchall()

    sql3 = "SELECT a.user_id,c.nama,a.car_id, a.ratings from rating as a inner join car as b on a.car_id = b.idmobil inner join user_profile as c on a.user_id=c.id where c.usia <> '0' and c.id <> '0'"
    mycursor.execute(sql3)
    myresult3 = mycursor.fetchall()

    user = []
    kode1 = ""
    kode2 = ""
    i = 0
    j = 0
    data = []
    kosong = []
    isi = []
    for a in myresult2:
        i = i + a[1]
        user2 = []
        for b in range(i - a[1], i):
            user2.append(myresult3[b])  #array satu user dan semua ratignya
        user.append(user2)  #array kumpulan user dan semua ratingnya
    k = 0
    for a in user:  #mengambil satu persatu user dan dan semua ratingnya
        k = 0
        atas = 0
        bawah1 = 0
        hasil = 0
        for b in a:  #mengambil satu user dan satu persatu ratingnya
            bawah2 = 0
            for c in myresult:  #mengambil baris pada user login
                if b[2] == c[
                        2]:  #id_car pada array b(user yang diambil) sama dengan id_car pada array c(user login)
                    atas = atas + (b[3] * c[3])
                bawah2 = bawah2 + (c[3]**2)
            bawah1 = bawah1 + (b[3]**2)
            k = k + 1
        if atas > 0:
            bawah1 = bawah1**0.5
            bawah2 = bawah2**0.5
            hasilbawah = bawah1 * bawah2
            hasil = float(float(atas) / float(hasilbawah))
        data.append([a[0], str(hasil)])
    return data  #berisi data user dan similarity rating terhadap user login


def simuser(kode):
    simatt = simattmetode2(kode)
    simrating = ratingattmetode2(kode)
    db = conn()
    mycursor = db.cursor()
    sql = "TRUNCATE TABLE `similarity`"
    #sql ="DELETE FROM similarity WHERE `idmobil` = 1"
    mycursor.execute(sql)
    db.commit()
    print ""
    print "===== Prediksi User Based ====="
    print "  Jumlah Sim Att : " + str(len(simatt))
    print "  Jumlah Sim Rat : " + str(len(simrating))
    print "==============================="
    data = []
    for a in range(0, len(simatt)):
        if len(simrating) == 0:
            break
        total = float((float(simatt[a][2]) * float(0.4)) +
                      (float(simrating[a][1]) * float(0.6)))
        data.append(
            (simatt[a][0], simatt[a][1], simatt[a][2], simrating[a][1], total))
    args = str(data)[1:][:len(str(data)) - 2]
    sql = "INSERT into similarity(user_id,user_id2,sim_att,sim_rating,sim_tot) values " + (
        args)
    mycursor.execute(sql, args)
    db.commit()
    simpred(kode)


def simpred(kode):
    data = []
    db = conn()
    mycursor = db.cursor()
    sql = "TRUNCATE TABLE `prediction`"
    mycursor.execute(sql)
    db.commit()
    sql = "SELECT AVG(ratings) FROM rating where user_id = %s" % (kode)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    sql = "SELECT * from (SELECT b.user_id as user_id, b.car_id as car_id, b.ratings as ratings from  user_profile as a \
         inner join rating as b on a.id = b.user_id and a.usia <> '0' and a.id <> '0' \
         inner join car as c on b.car_id = c.idmobil \
         where a.id<>0 GROUP BY b.car_id having(COUNT(b.car_id) > 0)) as d \
         where d.user_id <> %s" % (kode
                                   )  #user_id | car_id (berurutan) | ratings
    mycursor.execute(sql)
    myresult2 = mycursor.fetchall()
    if myresult[0][0] == None:
        Ru1 = 0
    else:
        Ru1 = myresult[0][0]
    data = []
    n = 0
    args = ""
    for a in myresult2:
        n += 1
        sql = "SELECT user_id, car_id, ratings from rating where car_id = %s" % (
            a[1])  #mengambil car_id pada setiap baris myresult2
        mycursor.execute(sql)
        myresult3 = mycursor.fetchall()
        atas1 = 0
        bawah1 = 0
        for b in myresult3:
            if b[0] != 0:  #mengambil user_id dari myresult3
                sql = "SELECT sim_tot from similarity where user_id = %s and user_id2 = %s" % (
                    kode, b[0])
                mycursor.execute(sql)
                myresult4 = mycursor.fetchall()
                #print "atas1"+str(atas1)
                #print "b2"+str(b[0])
                #print "Ru1"+str(Ru1)
                #print "myresult4"+str(float(myresult4[0][0]))
                atas1 = float(
                    float(atas1) +
                    float((float(b[2] - Ru1)) * float(myresult4[0][0])))
                bawah1 = float(float(bawah1) + float(myresult4[0][0]))
        hasil1 = float(float(atas1) / float(bawah1))
        hasil2 = float(float(Ru1) + float(hasil1))
        data.append((kode, myresult3[0][1], hasil2))
    args = str(data)[1:][:len(str(data)) - 2]
    #print "======================"
    #print args
    #print "Setelah ini error"
    if args != "":
        sql = "INSERT into prediction(user_id,car_id,pre_rating) values " + (
            args)
        mycursor.execute(sql)
        db.commit()


def ratingattmetode3(kode):
    db = conn()
    mycursor = db.cursor()
    sql = "SELECT user_id, car_id, ratings from rating where user_id = %s order by user_id asc" % (
        kode)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    sql = "SELECT idmobil from car where rating > 0"
    mycursor.execute(sql)
    myresult4 = mycursor.fetchall()
    ##print len(myresult4)
    gini = 0
    i = 0
    data = []
    for a in myresult:
        for b in myresult4:
            sql = "SELECT e.user_id, e.car_id, e.ratings , (SELECT AVG(ratings) from rating where user_id = e.user_id) as Rata from (SELECT d.user_id, b.car_id, b.ratings from \
            (select a.user_id as user_id, a.car_id as car_id, a.ratings as ratings from rating as a where car_id=%s) as b \
            inner join \
            (select c.user_id as user_id, c.car_id as car_id, c.ratings as ratings from rating as c where car_id=%s ) as d \
            on b.user_id=d.user_id) as e " % (a[1], b[0])
            mycursor.execute(sql)
            myresult2 = mycursor.fetchall()
            atas = 0
            bawah1 = 0
            bawah2 = 0
            hasilbawah = 0
            hasilakhir = 0

            #print str(gini+1)
            myresult7 = []
            myresult8 = []
            muter = 0
            for c in myresult2:
                sql = "SELECT a.user_id as user_id, a.car_id as car_id, a.ratings as ratings from rating as a \
                where car_id=%s and user_id=%s" % (a[1], c[0])
                mycursor.execute(sql)
                myresult7 = mycursor.fetchall()
                sql = "SELECT c.user_id as user_id, c.car_id as car_id, c.ratings as ratings from rating as c \
                where car_id=%s and user_id=%s" % (b[0], c[0])
                mycursor.execute(sql)
                myresult8 = mycursor.fetchall()
                atas = float(atas + ((float(myresult7[0][2]) - float(c[3])) *
                                     (float(myresult8[0][2]) - float(c[3]))))
                #print "rating depan    "+str(myresult7[0][2])+" user = " + str(myresult7[0][0])+" mobil = " + str(myresult7[0][1])
                #print "rating belakang "+str(myresult8[0][2])+" user = " + str(myresult8[0][0])+" mobil = " + str(myresult8[0][1])
                #print "uta2 "+str(myresult2[0][0])
                #print "atas = (" + str(float(myresult7[0][2])) + "-" + str(c[3]) + ") * (" + str(float(myresult8[0][2])) + " - " + str(float(c[3])) + ")"
                bawah1 = bawah1 + ((myresult7[0][2] - float(c[3]))**2)
                #print "bawah1 =(" + str(myresult7[0][2])+ "-" + str(c[3])+")^2"
                #print "hasil bawah1 = " + str(bawah1)
                bawah2 = bawah2 + ((myresult8[0][2] - float(c[3]))**2)
                #print "bawah2=(" + str(myresult8[0][2])+ "-" + str(c[3])+")^2"
                #print "hasil bawah2 = " + str(bawah2)
                muter = muter + 1
            hasilbawah = float(float((bawah1**0.5)) * float((bawah2**0.5)))
            #print "hasil atas = " + str(atas)
            #print "hasil bawah = " + str(hasilbawah)
            if len(myresult7) > 0 and len(myresult8) > 0:
                if muter == 1:
                    hasilakhir = 1
                    #print "a"
                elif hasilbawah == 0:
                    hasilakhir = 1
                    #print "b"
                else:
                    hasilakhir = float(float(atas) / float(hasilbawah))
                    hasilakhir = "{:,.7f}".format(hasilakhir)
                    #print "c"
            else:
                if hasilbawah != 0:
                    hasilakhir = float(float(atas) / float(hasilbawah))
                    hasilakhir = "{:,.7f}".format(hasilakhir)
                    #print "d"
                    #print "cek 1"
                else:
                    #print "cek 2"
                    hasilakhir = 0
                    #print "e"
                    #if myresult7[0][2]!=0.0:
                    ##print "rating depan    "+str(myresult7[0][2])+" user = " + str(myresult7[0][0])+" mobil = " + str(myresult7[0][1])
                    #else:
                    # #print "lol"
                    #hasilakhir=0
            #print "hasil akhir = " + str(hasilakhir)
            #print ""
            gini = gini + 1
            data.append([b[0], str(hasilakhir)])
    return data


def simattmetode3(kode):
    warna = {"gray": 1, "silver": 2, "white": 3, "black": 4}
    trans = {"automatic": 1, "manual": 2}
    mobil = {
        "toyota": 1,
        "Daihatsu": 2,
        "mitsubishi": 3,
        "Honda": 4,
        "suzuki": 5,
        "isuzu": 6,
        "Datsun": 7,
        "nissan": 8,
        "wuling": 9,
        "mazda": 10,
        "kia": 11,
        "BMW": 12,
        "Chevrolet": 13,
        "ford": 14,
        "jeep": 15,
        "land rover": 16,
        "lexus": 17,
        "mercedes benz": 18,
        "mini cooper": 19,
        "hyundai": 20
    }
    seat = {2: 1, 4: 2, 5: 3, 7: 4, 8: 5, 9: 6}
    fuel = {1: 1, 0: 2}

    db = conn()
    mycursor = db.cursor()
    sql = "SELECT a.user_id, b.cc, b.warna, b.harga, b.transmisi, b.idmobil, b.aftersale, b.seater, b.gasoline, b.merk from rating as a inner join car as b on b.rating > 0 and a.car_id=b.idmobil where a.user_id = %s" % (
        kode)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    ##print myresult

    sql = "SELECT idmobil, cc, warna, harga, transmisi, diesel, aftersale, seater, gasoline, merk from car where rating > 0"
    mycursor.execute(sql)
    myresult2 = mycursor.fetchall()
    #dist=[]
    sim = []
    for b in range(0, len(myresult)):
        dat_cc1 = 0
        if myresult[b][1] <= 1500:
            dat_cc1 = 1
        elif 1500 < myresult[b][1] <= 2000:
            dat_cc1 = 2
        elif 2000 < myresult[b][1] <= 2500:
            dat_cc1 = 3
        elif 2500 < myresult[b][1] <= 3000:
            dat_cc1 = 4
        elif myresult[b][1] > 3000:
            dat_cc1 = 5

        dat_warna1 = warna[myresult[b][2]]

        dat_harga1 = 0
        if myresult[b][3] < 200000000:
            dat_harga1 = 1
        elif 200000000 <= myresult[b][3] < 300000000:
            dat_harga1 = 2
        elif 300000000 <= myresult[b][3] < 450000000:
            dat_harga1 = 3
        elif 450000000 <= myresult[b][3] < 650000000:
            dat_harga1 = 4
        elif myresult[b][3] >= 650000000:
            dat_harga1 = 5

        dat_trans1 = trans[myresult[b][4]]

        dat_hargapurna1 = 0
        if myresult[b][6] < 100000000:
            dat_hargapurna1 = 1
        elif 100000000 <= myresult[b][6] < 200000000:
            dat_hargapurna1 = 2
        elif 200000000 <= myresult[b][6] < 350000000:
            dat_hargapurna1 = 3
        elif 350000000 <= myresult[b][6] < 500000000:
            dat_hargapurna1 = 4
        elif myresult[b][6] >= 500000000:
            dat_hargapurna1 = 5

        dat_seat1 = seat[myresult[b][7]]

        dat_fuel1 = fuel[myresult[b][8]]

        dat_mobil1 = mobil[myresult[b][9]]

        for a in myresult2:
            dat_cc2 = 0
            if a[1] <= 1500:
                dat_cc2 = 1
            elif 1500 < a[1] <= 2000:
                dat_cc2 = 2
            elif 2000 < a[1] <= 2500:
                dat_cc2 = 3
            elif 2500 < a[1] <= 3000:
                dat_cc2 = 4
            elif a[1] > 3000:
                dat_cc2 = 5

            dat_warna2 = warna[a[2]]

            dat_harga2 = 0
            if a[3] < 200000000:
                dat_harga2 = 1
            elif 200000000 <= a[3] < 300000000:
                dat_harga2 = 2
            elif 300000000 <= a[3] < 450000000:
                dat_harga2 = 3
            elif 450000000 <= a[3] < 650000000:
                dat_harga2 = 4
            elif a[3] >= 650000000:
                dat_harga2 = 5

            dat_trans2 = trans[a[4]]

            dat_hargapurna2 = 0
            if a[6] < 100000000:
                dat_hargapurna2 = 1
            elif 100000000 <= a[6] < 200000000:
                dat_hargapurna2 = 2
            elif 200000000 <= a[6] < 350000000:
                dat_hargapurna2 = 3
            elif 350000000 <= a[6] < 500000000:
                dat_hargapurna2 = 4
            elif a[6] >= 500000000:
                dat_hargapurna2 = 5

            dat_seat2 = seat[a[7]]

            dat_fuel2 = fuel[a[8]]

            dat_mobil2 = mobil[a[9]]

            dat_mobil3 = ""
            if dat_mobil1 == dat_mobil2:
                dat_mobil3 = 1
            else:
                dat_mobil3 = 0

            dat_harga3 = ""
            if dat_harga1 == dat_harga2:
                dat_harga3 = 1
            else:
                dat_harga3 = 0

            dat_trans3 = ""
            if dat_trans1 == dat_trans2:
                dat_trans3 = 1
            else:
                dat_trans3 = 0

            dat_warna3 = ""
            if dat_warna1 == dat_warna2:
                dat_warna3 = 1
            else:
                dat_warna3 = 0

            dat_cc3 = ""
            if dat_cc1 == dat_cc2:
                dat_cc3 = 1
            else:
                dat_cc3 = 0

            dat_seat3 = ""
            if dat_seat1 == dat_seat2:
                dat_seat3 = 1
            else:
                dat_seat3 = 0

            dat_fuel3 = ""
            if dat_fuel1 == dat_fuel2:
                dat_fuel3 = 1
            else:
                dat_fuel3 = 0

            dat_hargapurna3 = ""
            if dat_hargapurna1 == dat_hargapurna2:
                dat_hargapurna3 = 1
            else:
                dat_hargapurna3 = 0

            data1 = (dat_mobil3 * (16.5 / 100)) + (
                dat_harga3 * (15.7 / 100)) + (dat_trans3 * (15.7 / 100)) + (
                    dat_warna3 * (15.3 / 100)) + (dat_cc3 * (15.1 / 100)) + (
                        dat_seat3 *
                        (13.4 / 100)) + (dat_fuel3 *
                                         (7.5 / 100)) + (dat_hargapurna3 *
                                                         (0.8 / 100))
            ##print "data 1 = " + str(data1)
            #hasil= 1+data1
            ##print "hasil = " + str(hasil)
            #data2 = float(float(1)/float(hasil))
            #data2 = "{:,.2f}".format(data2)
            #dist.append([data1])
            sim.append([myresult[b][5], a[0], data1])
    return sim


def simmobil(kode):
    ##print "asup ke simattmetode3(kode)"
    simatt = simattmetode3(kode)
    ##print "asup ke ratingattmetode3(kode)"
    simrating = ratingattmetode3(kode)
    print ""
    print "===== Prediksi Item Based ====="
    print "  Jumlah Sim Att : " + str(len(simatt))
    #print simatt
    print "  Jumlah Sim Rat : " + str(len(simrating))
    #print simrating
    print "==============================="
    print ""
    db = conn()
    mycursor = db.cursor()
    sql = "TRUNCATE TABLE similarity_car"
    mycursor.execute(sql)
    db.commit()
    data = []
    for a in range(0, len(simatt)):
        if len(simrating) == 0:
            break
    #total=0
    #if float(simrating[a][1]) > 0:
        total = float((float(simatt[a][2]) * float(0.4)) +
                      (float(simrating[a][1]) * float(0.6)))
        #print ""
        #print str(a+1)
        #print "(" + str(float(simatt[a][2])) + "*" + str(float(0.4)) +")+(" + str(float(simrating[a][1])) + "*" + str(float(0.6))
        #print "total =" + str (total)
        data.append(
            (simatt[a][0], simatt[a][1], simatt[a][2], simrating[a][1], total))
    args = str(data)[1:][:len(str(data)) - 2]
    sql = "INSERT into similarity_car(idmobil,idmobil2,sim_att,sim_rating,sim_tot) values " + (
        args)
    mycursor.execute(sql, args)
    db.commit()
    simpred_car(kode)


def simpred_car(kode):
    data = []
    db = conn()
    mycursor = db.cursor()

    sql = "TRUNCATE TABLE prediction_car"
    mycursor.execute(sql)
    db.commit()

    sql = "SELECT * from (SELECT b.user_id as user_id, b.car_id as car_id, b.ratings as ratings from  user_profile as a \
         inner join rating as b on a.id = b.user_id \
         inner join car as c on b.car_id = c.idmobil \
         where a.id<>0 GROUP BY b.car_id having(COUNT(b.car_id) > 0)) as a"

    #where a.user_id <> %s" %(kode)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    sql = "SELECT user_id, car_id, ratings from rating where user_id = %s" % (
        kode)
    mycursor.execute(sql)
    myresult2 = mycursor.fetchall()
    #print "prediksi rating"
    urut = 0
    for a in myresult:
        atas = 0
        bawah = 0
        hasil = 0
        #print ""
        #print str(urut+1)
        for b in myresult2:
            sql = "SELECT sim_tot from similarity_car where idmobil = %s and idmobil2 = %s" % (
                b[1], a[1])
            mycursor.execute(sql)
            myresult3 = mycursor.fetchall()
            if len(myresult3) == 0:
                continue
            if len(myresult3) > 0:
                if myresult3[0][0] > 0:
                    atas = float(float(atas) + float(myresult3[0][0] * b[2]))
                    bawah = float(float(bawah) + float(myresult3[0][0]))
                    #print "myresult3 = " + str(myresult3[0][0])
                    #print "b2        = " + str(b[2])
            if bawah != 0:
                hasil = float(atas / bawah)
            else:
                hasil = atas
            #print "atas      = " + str(atas)
            #print "bawah     = " + str(bawah)
        urut = urut + 1
        #print "hasil     = " + str(hasil)
        data.append((kode, a[1], hasil))
    args = str(data)[1:][:len(str(data)) - 2]
    sql = "INSERT into prediction_car(user_id,car_id,pre_rating) values " + (
        args)
    mycursor.execute(sql, args)
    db.commit()


@application.route('/PredRatingCar', methods=['GET', 'POST'])
def PredRatingCar():
    if g.user:
        if request.method == 'POST':
            myresult = []
            kirim = []
            hasilcari = ""
        if request.method == 'POST':
            if request.form["merk"] == "":
                merk = "%"
            else:
                merk = request.form["merk"]
                hasilcari = hasilcari + merk + " / "

            if request.form["jenis"] == "":
                jenis = "%"
            else:
                jenis = request.form["jenis"]
                hasilcari = hasilcari + jenis + " / "

            if request.form["varian"] == "":
                varian = "%"
            else:
                varian = request.form["varian"]
                hasilcari = hasilcari + varian + " / "

            if request.form["cc"] == "":
                cc = "%"
            else:
                cc = request.form["cc"]
                hasilcari = hasilcari + cc + " / "

            if request.form["transmisi"] == "":
                transmisi = "%"
            else:
                transmisi = request.form["transmisi"]
                hasilcari = hasilcari + transmisi + " / "

            if request.form["harga"] == "":
                harga = "%"
            else:
                harga = request.form["harga"]
                hasilcari = hasilcari + harga + " / "

            if request.form["warna"] == "":
                warna = "%"
            else:
                warna = request.form["warna"]
                hasilcari = hasilcari + warna + " / "

            if request.form["seater"] == "":
                seater = "%"
            else:
                seater = request.form["seater"]
                hasilcari = hasilcari + seater + " / "

            if request.form["aftersale"] == "":
                aftersale = "%"
            else:
                aftersale = request.form["aftersale"]
                hasilcari = hasilcari + aftersale + " / "

            if request.form["fuel"] == "":
                gasoline = "%"
            else:
                gasoline = request.form["fuel"]
                hasilcari = hasilcari + gasoline + " / "

            #hasilcari=merk+" / "+jenis+" / "+varian+" / "+cc+" / "+transmisi+" / "+harga+" / "+warna
            ##print hasilcari
            res = listallmobilusercari(merk, jenis, varian, cc, transmisi,
                                       harga, warna, seater, aftersale,
                                       gasoline)
            myresult = res[0][0]
            s = ""
            for t in res[1][0]:
                s += str(t[0]) + ","
            kodeid = s[:-1]
            ##print kodeid
            kirim = pilihcari(kodeid)
            post = []
            post2 = []
            z = 0
            kirim2 = pilih()
            ##print kirim2
            ##print myresult
            for i in myresult:
                z = z + 1
                pilImg = Image.open(cStringIO.StringIO(str(i[12])))
                pilImg.thumbnail((200, 300), Image.ANTIALIAS)
                filename = "static/image/" + str(i[0]) + ".png"
                pilImg.save(filename)
                post.append([
                    i[0],
                    str(i[1]).capitalize(),
                    str(i[2]).capitalize(),
                    str(i[3]).capitalize(), i[4],
                    str(i[5]).capitalize(), i[6],
                    str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                    i[13], i[14], i[15], i[16]
                ])
                if z <= 10:
                    post2.append([
                        i[0],
                        str(i[1]).capitalize(),
                        str(i[2]).capitalize(),
                        str(i[3]).capitalize(), i[4],
                        str(i[5]).capitalize(), i[6],
                        str(i[7]).capitalize(), i[8], i[9], i[10], i[11],
                        filename, i[13], i[14], i[15], i[16]
                    ])
            return render_template("listallmobiluser.html",
                                   post=post,
                                   kirim=kirim,
                                   kirim2=kirim2,
                                   hasilcari=hasilcari,
                                   post2=post2)
        else:
            ##print "lain kadieu cuk"
            myresult = []
            db = conn()
            mycursor = db.cursor()
            sql = "SELECT a.car_id, c.merk, c.jenis, c.varian, c.cc, c.transmisi, c.harga, c.warna, c.keterangan, c.kelebihan, c.kekurangan, c.rating, c.image, a.pre_rating, c.seater, c.aftersale, c.gasoline, c.diesel FROM `prediction_car` as a \
				 inner join car as c on a.car_id=c.idmobil\
				 left join (select * from rating where user_id =%s) as b on a.car_id=b.car_id where b.user_id is null \
				 ORDER BY `pre_rating` desc limit 10" % (session['id'])
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            predcar = []
            z = 0
            for i in myresult:
                z = z + 1
                pilImg = Image.open(cStringIO.StringIO(str(i[12])))
                pilImg.thumbnail((200, 300), Image.ANTIALIAS)
                filename = "static/image/" + str(i[0]) + ".png"
                pilImg.save(filename)
                predcar.append([
                    i[0],
                    str(i[1]).capitalize(),
                    str(i[2]).capitalize(),
                    str(i[3]).capitalize(), i[4],
                    str(i[5]).capitalize(), i[6],
                    str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                    i[13], i[14], i[15], i[16]
                ])

            myresult = []
            sql = "SELECT a.car_id, c.merk, c.jenis, c.varian, c.cc, c.transmisi, c.harga, c.warna, c.keterangan, c.kelebihan, c.kekurangan, a.pre_rating, c.image, c.seater, c.aftersale, c.gasoline, c.diesel FROM `prediction` as a \
				 inner join car as c on a.car_id=c.idmobil\
				 left join (select * from rating where user_id =%s) as b on a.car_id=b.car_id where b.user_id is null \
				 ORDER BY `pre_rating` desc limit 10" % (session['id'])
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            preduser = []
            z = 0
            for i in myresult:
                z = z + 1
                pilImg = Image.open(cStringIO.StringIO(str(i[12])))
                pilImg.thumbnail((200, 300), Image.ANTIALIAS)
                filename = "static/image/" + str(i[0]) + ".png"
                pilImg.save(filename)
                preduser.append([
                    i[0],
                    str(i[1]).capitalize(),
                    str(i[2]).capitalize(),
                    str(i[3]).capitalize(), i[4],
                    str(i[5]).capitalize(), i[6],
                    str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                    i[13], i[14], i[15], i[16]
                ])

            myresult = []
            sql = "SELECT * from car order by rating desc limit 10"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            ratcar = []
            z = 0
            for i in myresult:
                z = z + 1
                ##print i[0]
                pilImg = Image.open(cStringIO.StringIO(str(i[12])))
                pilImg.thumbnail((200, 300), Image.ANTIALIAS)
                filename = "static/image/" + str(i[0]) + ".png"
                pilImg.save(filename)
                ratcar.append([
                    i[0],
                    str(i[1]).capitalize(),
                    str(i[2]).capitalize(),
                    str(i[3]).capitalize(), i[4],
                    str(i[5]).capitalize(), i[6],
                    str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename,
                    i[13], i[14], i[15], i[16]
                ])
            kirim2 = pilih()
            return render_template("menu.html",
                                   predcar=predcar,
                                   preduser=preduser,
                                   ratcar=ratcar,
                                   kirim2=kirim2)
    return redirect(url_for('menu'))


def cekmaeuser():
    data = []
    db = conn()
    mycursor = db.cursor()

    sql = "SELECT * from prediction a \
		inner join rating_test c on a.user_id=c.user_id and a.car_id=c.car_id"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    jum = 0
    for i in myresult:
        print str(i[2]) + "-" + str(i[5]) + "=" + str(abs(i[2] - i[5]))
        jum = jum + abs(i[2] - i[5])
    if len(myresult) == 0:
        print "MAE = 0.0"
    else:
        print "MAE = " + str(jum / len(myresult))


def cekmaemobil():
    data = []
    db = conn()
    mycursor = db.cursor()

    sql = "SELECT * from prediction_car a \
		inner join rating_test c on a.user_id=c.user_id and a.car_id=c.car_id"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    jum = 0
    for i in myresult:
        print str(i[2]) + "-" + str(i[5]) + "=" + str(abs(i[2] - i[5]))
        jum = jum + abs(i[2] - i[5])
    ##print str(jum)
    ##print str(len(myresult))
    if len(myresult) == 0:
        print "MAE = 0.0"
    else:
        print "MAE = " + str(jum / len(myresult))


@application.route('/background_process1', methods=['GET', 'POST'])
def background_process1():
    myresult = []
    db = conn()
    mycursor = db.cursor()
    sql = "select * from car where harga > (select b.harga1 from user_profile as a inner join hargamobil as b on a.anggaran=b.Ket where a.nama = '%s') and harga < (select b.harga2 from user_profile as a inner join hargamobil as b on a.anggaran=b.Ket where a.nama = '%s')" % (
        session['user'], session['user'])
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    post = []
    z = 0
    kirim = pilih()
    for i in myresult:
        z = z + 1
        pilImg = Image.open(cStringIO.StringIO(str(i[12])))
        pilImg.thumbnail((200, 300), Image.ANTIALIAS)
        filename = "static/image/" + str(i[0]) + ".png"
        pilImg.save(filename)
        post.append([
            i[0],
            str(i[1]).capitalize(),
            str(i[2]).capitalize(),
            str(i[3]).capitalize(), i[4],
            str(i[5]).capitalize(), i[6],
            str(i[7]).capitalize(), i[8], i[9], i[10], i[11], filename, i[13],
            i[14], i[15], i[16]
        ])
    hasil = [post, kirim]
    hasil2 = json.dumps(hasil)
    return hasil2


@application.route('/background_process', methods=['GET', 'POST'])
def background_process():
    db = conn()
    mycursor = db.cursor()
    kirim = []
    data = ["merk", "jenis", "varian", "cc", "transmisi", "harga", "warna"]
    #data2=[]
    merk = "%" + request.args.get('merk', '%', type=str) + "%"
    jenis = "%" + request.args.get('jenis', '%', type=str) + "%"
    varian = "%" + request.args.get('varian', '%', type=str) + "%"
    cc = "%" + request.args.get('cc', '%', type=str) + "%"
    transmisi = "%" + request.args.get('transmisi', '%', type=str) + "%"
    harga = "%" + request.args.get('harga', '%', type=str) + "%"
    warna = "%" + request.args.get('warna', '%', type=str) + "%"
    ##print '============='
    ##print warna
    ##print merk
    ##print '============='
    for i in data:
        #sql="SELECT %s FROM car where merk like '%" + merk + "%' and jenis like '%" + jenis + "%' and varian like '%" + varian + "%' and cc like '%" + cc + "%' and transmisi like '%" + transmisi + "%' and harga like '%" + harga + "%' and warna like '%" + warna + "%' GROUP BY %s HAVING ( COUNT(%s) > 0 )" %(i,i,i)
        sql = "SELECT %s FROM car where upper(merk) like upper('%s') and upper(jenis) like upper('%s') and upper(varian) like upper('%s') and upper(transmisi) like upper('%s') and  upper(warna) like upper('%s') GROUP BY %s HAVING ( COUNT(%s) > 0 )" % (
            i, merk, jenis, varian, transmisi, warna, i, i)
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        kirim.append(myresult)
    ##print '============='
    ##print kirim
    lis = str(kirim)
    ##print '============='
    ##print lis
    kirim = json.dumps(kirim)
    ##print '============='
    return kirim

    #lang = request.args.get('merk', 0, type=str)
    #if lang.lower() == 'python':
    #	return jsonify(result='You are wise')
    #else:
    #	return jsonify(result='Try again.')


if __name__ == "__main__":
    application.run(debug=True)
    application.run(host='0.0.0.0')
#idmobil
#merk
#jenis
#varian
#cc
#transmisi
#harga
#warna
#keterangan
#kelebihan
#kekurangan
#image
