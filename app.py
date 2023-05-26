from flask import Flask, render_template, request, url_for, redirect, session, jsonify, Response
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
import json
import webbrowser
import time

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'kuakuis'
mysql = MySQL(app)

app.secret_key = 'ilyasGG'

#ROUTING

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    id_user = session['user']
    cur = mysql.connection.cursor()
    cur.execute('select count(*) from tabel_mapel where id_user = %s', (id_user,))
    tabel_mapel = cur.fetchone()
    tabel_mapel = tabel_mapel[0]
    cur.execute('SELECT count(*) FROM `tabel_soal` INNER JOIN `tabel_mapel` ON tabel_soal.id_mapel = tabel_mapel.id_mapel WHERE tabel_mapel.id_user = %s', (id_user,))
    tabel_soal = cur.fetchone()
    tabel_soal = tabel_soal[0]
    cur.execute('select count(*) from sesi_kuis where id_user = %s', (id_user,))
    tabel_sesi = cur.fetchone()
    tabel_sesi = tabel_sesi[0]
    return render_template('dashboard.html', id = id, tabel_mapel=tabel_mapel, tabel_soal=tabel_soal, tabel_sesi=tabel_sesi)

@app.route('/kuis')
def kuis():
    
    return render_template('kuis.html')

@app.route('/pengajar')
def pengajar():
    
    return render_template('pengajar.html')

@app.route('/panduan')
def panduan():
    
    return render_template('panduan.html')

@app.route('/tentang')
def tentang():
    
    return render_template('tentang.html')

@app.route('/sesibaru')
def sesibaru():

    user = session['user']
    cur = mysql.connection.cursor()
    cur.execute('SELECT `id_sesi`, tabel_mapel.nama_mapel, status_kuis.status from `sesi_kuis` inner join `tabel_mapel` join `status_kuis` on sesi_kuis.id_mapel=tabel_mapel.id_mapel and sesi_kuis.status=status_kuis.id_status where sesi_kuis.id_user =%s and sesi_kuis.status!=3 order by `id_sesi` asc', (user,))
    data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("Select * From tabel_mapel where id_user=%s", (user,))
    mapel = cur.fetchall()
    cur.close()   
    return render_template('sesibaru.html', data = data, mapel = mapel)

@app.route('/kerjakan', methods=["POST"])
def kerjakan():
    nama = request.form["nama"]
    id_sesi = request.form["id_sesi"]
    cur = mysql.connection.cursor()
    cur.execute('Select status, id_mapel From sesi_kuis where id_sesi=%s',(id_sesi,))
    fetch = cur.fetchall()
    cur.close()
    soals = {}
    if fetch != ():
        data = fetch[0]
        status = data[0]
        id_mapel = data[1]
        if status == 2:
            cur = mysql.connection.cursor()
            cur.execute("Select * From tabel_soal where id_mapel=%s",(id_mapel,))
            soal = cur.fetchall()
            x=0
            for i in soal :
                soals[x+1] = {
                    "id_soal": i[0],
                    "no": x+1,
                    "soal": i[2],
                    "jawabanA": i[3],
                    "jawabanB": i[4],
                    "jawabanC": i[5],
                    "jawabanD": i[6],
                    "waktu" : i[8],
                    "id_cpl" : i[9],
                }
                x+=1
            if session.get('nama_peserta') is None and session.get('id_sesi') is None:
                cur2 = mysql.connection.cursor()
                cur2.execute("insert into peserta_kuis (nama_peserta, id_sesi) values (%s, %s)", (nama, id_sesi))
                mysql.connection.commit()
                cur3 = mysql.connection.cursor()
                cur3.execute("Select * From peserta_kuis where nama_peserta=%s AND id_sesi=%s", (nama, id_sesi))
                peserta = cur3.fetchone()
                cur3.close
                session['id_peserta'] = peserta[0]
                session['nama_peserta'] = peserta[1]
                session['id_sesi'] = peserta[2]
                nama_peserta = peserta[1]
            elif session['nama_peserta'] == nama and session.get('id_sesi') == int(id_sesi):
                print(session['nama_peserta'],  session['id_sesi'])
                nama_peserta = session['nama_peserta']
            else:
                cur2 = mysql.connection.cursor()
                cur2.execute("insert into peserta_kuis (nama_peserta, id_sesi) values (%s, %s)", (nama, id_sesi))
                mysql.connection.commit()
                cur3 = mysql.connection.cursor()
                cur3.execute("Select * From peserta_kuis where nama_peserta=%s AND id_sesi=%s", (nama, id_sesi))
                peserta = cur3.fetchone()
                cur3.close
                session['id_peserta'] = peserta[0]
                session['nama_peserta'] = peserta[1]
                session['id_sesi'] = peserta[2]
                nama_peserta = peserta[1]
            return render_template('kerjakankuis.html', soal=json.dumps(soals), nama_peserta=nama_peserta)
        elif status == 1:
            msg = "Status Kuis Belum Dimulai"
            return render_template('kuis.html', msg=msg, nama=nama, id_sesi=id_sesi)
        else:
            msg = "Status Kuis Telah Selesai"
            return render_template('kuis.html', msg=msg, nama=nama, id_sesi=id_sesi)
    else:
        msg = "kode yang anda masukan tidak terdaftar"
        return render_template('kuis.html', msg=msg, nama=nama, id_sesi=id_sesi)
    
@app.route('/mulaikuis', methods=["GET","POST"])
def mulaikuis():
    id_sesi = request.form['id_sesi']
    session['id_sesi'] = id_sesi
    cur = mysql.connection.cursor()
    cur.execute('select id_mapel from sesi_kuis where id_sesi=%s', (id_sesi,))
    data = cur.fetchone()
    data = data[0]
    session['id_mapel'] = data
    cur.execute('SELECT `id_sesi`, tabel_mapel.nama_mapel, status_kuis.status, sesi_kuis.id_mapel from `sesi_kuis` Inner join `tabel_mapel` on sesi_kuis.id_mapel=tabel_mapel.id_mapel Inner join `status_kuis` on sesi_kuis.status=status_kuis.id_status where sesi_kuis.id_sesi =%s', (id_sesi,))
    data = cur.fetchall()
    data = data[0]
    id_mapel = data[3]
    cur.execute('select count(*) as count from tabel_soal where id_mapel = %s', (id_mapel,))
    soal = cur.fetchone()
    jumlah_soal = soal[0]
    cur.close()
    return render_template('mulaikuis.html', data=data, jumlah_soal=jumlah_soal)

@app.route('/hasilkuis', methods=["GET","POST"])
def hasilkuis():
    id_sesi = request.form['id_sesi']
    session['id_sesi'] = id_sesi
    cur = mysql.connection.cursor()
    cur.execute('select id_mapel from sesi_kuis where id_sesi = %s', (id_sesi,))
    id_mapel = cur.fetchone()
    id_mapel = id_mapel[0]
    cur.execute('select count(*) as count from tabel_soal where id_mapel = %s', (id_mapel,))
    soal = cur.fetchone()
    jumlah_soal = soal[0]
    cur.execute('SELECT `id_sesi`, tabel_mapel.nama_mapel, status_kuis.status, sesi_kuis.id_mapel from `sesi_kuis` Inner join `tabel_mapel` on sesi_kuis.id_mapel=tabel_mapel.id_mapel Inner join `status_kuis` on sesi_kuis.status=status_kuis.id_status where sesi_kuis.id_sesi =%s', (id_sesi,))
    data = cur.fetchall()
    data = data[0]
    cur.execute("SELECT `nama_peserta`, status_peserta.status, `score_akhir`, Round(score_akhir / %s * 100) as Nilai_Akhir , FORMAT(score_akhir / %s * 4,2) as Skala_4, Case when Round(score_akhir / %s * 100) >= 80 then 'A' when Round(score_akhir / %s * 100) >= 75 then 'AB' when Round(score_akhir / %s * 100) >= 70 then 'B' when Round(score_akhir / %s * 100) >= 65 then 'BC' when Round(score_akhir / %s * 100) >= 55 then 'C' when Round(score_akhir / %s * 100) >= 40 then 'D' else 'E' end as Grade FROM `peserta_kuis` Inner join `status_peserta` on peserta_kuis.id_status=status_peserta.id where id_sesi = %s order by `nama_peserta` asc", (jumlah_soal,jumlah_soal, jumlah_soal,jumlah_soal ,jumlah_soal , jumlah_soal,jumlah_soal, jumlah_soal, id_sesi,))
    result = cur.fetchall()
    cur.close()
    return render_template('hasilkuis.html',data=data, result=result)

@app.route('/sesiselesai')
def sesiselesai():

    user = session['user']
    cur = mysql.connection.cursor()
    cur.execute('SELECT `id_sesi`, tabel_mapel.nama_mapel, status_kuis.status from `sesi_kuis` inner join `tabel_mapel` join `status_kuis` on sesi_kuis.id_mapel=tabel_mapel.id_mapel and sesi_kuis.status=status_kuis.id_status where sesi_kuis.id_user =%s and sesi_kuis.status=3 order by `id_sesi` asc', (user,))
    data = cur.fetchall()
    cur.close()

    return render_template('sesiselesai.html', data = data)

@app.route('/matapelajaran')
def matapelajaran():
    if session['loggedid'] == False:
        return redirect(url_for('pengajar'))
    else:
        user = session['user']
        print(user)
        cur = mysql.connection.cursor()
        cur.execute("Select * From tabel_mapel where id_user=%s", (user,))
        data = cur.fetchall()
        cur.close()
    return render_template('matapelajaran.html',data=data)

@app.route('/capaianpembelajaran')
def capaianpembelajaran():
    if session['loggedid'] == False:
        return redirect(url_for('pengajar'))
    else:
        user = session['user']
        cur = mysql.connection.cursor()
        cur.execute("Select * From tabel_mapel where id_user=%s", (user,))
        data = cur.fetchall()
        cur.close()    
    return render_template('capaianpembelajaran.html', data=data)

@app.route('/capaianpembelajaranmapel', methods=['GET', 'POST'])
def cpmapel():
    if request.method == 'POST':
        session['soal'] = True
        id_mapel = request.form['id_mapel']
        session['id_mapel'] = id_mapel
    else :
        id_mapel = session['id_mapel']
    cur = mysql.connection.cursor()
    cur.execute("Select * From capaian_pembelajaran where id_mapel=%s",(id_mapel,))
    data = cur.fetchall()
    cur.close()
    if len(data) == 0:
        msg = "Belum Menambahkan Capaian Pembelajaran"
    else :
        msg = ""
    cur2 = mysql.connection.cursor()
    cur2.execute("Select nama_mapel From tabel_mapel where id_mapel=%s", (id_mapel,))
    nama_mapel = cur2.fetchone()
    nama_mapel = nama_mapel[0]
    return render_template('cpmapel.html',data=data , id_mapel=id_mapel, nama_mapel=nama_mapel, msg=msg)

@app.route('/soal')
def soal():
    if session['loggedid'] == False:
        return redirect(url_for('pengajar'))
    else:
        user = session['user']
        print(user)
        cur = mysql.connection.cursor()
        cur.execute("Select * From tabel_mapel where id_user=%s", (user,))
        data = cur.fetchall()
        cur.close()    
    return render_template('soal.html', data=data)

@app.route('/soalmapel', methods=['GET', 'POST'])
def soalmapel():
    if request.method == 'POST':
        session['soal'] = True
        id_mapel = request.form['id_mapel']
        session['id_mapel'] = id_mapel
    else :
        id_mapel = session['id_mapel']
    cur = mysql.connection.cursor()
    cur.execute("Select * From tabel_soal where id_mapel=%s",(id_mapel,))
    data = cur.fetchall()
    cur.close()
    jumlah_soal = len(data)
    if jumlah_soal == 0:
        msg = "Belum Menambahkan Soal"
    else :
        msg = ""

    cur = mysql.connection.cursor()
    cur.execute("Select nama_mapel From tabel_mapel where id_mapel=%s", (id_mapel,))
    nama_mapel = cur.fetchone()
    nama_mapel = nama_mapel[0]
    cur.close()
    
    cur = mysql.connection.cursor()
    cur.execute("select id_cpl, cpl from capaian_pembelajaran where id_mapel=%s", (id_mapel,))
    cpl = cur.fetchall()
    cur.close()
    return render_template('soalmapel.html',data=data ,id_mapel=id_mapel, jumlah_soal=jumlah_soal, nama_mapel=nama_mapel, cpl=cpl, msg=msg)


#INSERT DATA

@app.route('/insertmatapelajaran', methods=["POST"])
def insertmatapelajaran():
    nama_mapel = request.form['matapelajaran']
    id_user = session['user']
    cur = mysql.connection.cursor()
    cur.execute("insert into tabel_mapel (id_user, nama_mapel) values (%s, %s)", (id_user,nama_mapel,))
    mysql.connection.commit()
    return redirect(url_for('matapelajaran'))

@app.route('/insertcpmapel', methods=["POST"])
def insertcpmapel():
    cpl = request.form['cpl']
    id_mapel = session['id_mapel']
    cur = mysql.connection.cursor()
    cur.execute("insert into capaian_pembelajaran (id_mapel, cpl) values (%s, %s)", (id_mapel,cpl,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('cpmapel'))

@app.route('/insertsoal', methods=["POST"])
def insertsoal():
    id_mapel = session['id_mapel']
    soal = request.form['soal']
    j1 = request.form['j1']
    j2 = request.form['j2']
    j3 = request.form['j3']
    j4 = request.form['j4']
    jtrue = request.form['jtrue']
    id_cpl = request.form['cpl']
    waktu = request.form['waktu']
    cur = mysql.connection.cursor()
    cur.execute("insert into tabel_soal (id_mapel, soal, A, B, C, D, jawaban_benar, waktu, id_cpl) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (id_mapel, soal, j1, j2, j3, j4, jtrue, waktu, id_cpl,))
    mysql.connection.commit()
    return redirect(url_for('soalmapel'))

@app.route('/insertsesi', methods=["POST"])
def insertsesi():

    id_mapel = request.form['id_mapel']
    user = session['user']
    cur = mysql.connection.cursor()
    cur.execute("insert into sesi_kuis (id_mapel, id_user) values (%s, %s)", (id_mapel,user))
    mysql.connection.commit()

    return redirect(url_for('sesibaru'))

@app.route('/simpanjawaban', methods=["POST"])
def simpanjawaban():
    id_peserta = session['id_peserta']
    id_sesi = session['id_sesi']
    if request.method == 'POST':
        jawaban = request.form['jawaban']
        id_soal = request.form['id_soal']
        waktu = request.form['waktu']
        score = 0
        status = 0
        cur = mysql.connection.cursor()
        cur.execute("select jawaban_benar from tabel_soal where id_soal = %s", (id_soal,))
        data = cur.fetchall()
        data = data[0][0]
        print(id_soal)
        if (data == jawaban) :
            score = request.form['rasio']
            status = 1
        cur.execute("insert into jawaban_peserta (id_peserta, id_sesi, id_soal, jawaban, waktu, score, status) values (%s, %s, %s, %s, %s, %s, %s)", (id_peserta, id_sesi, id_soal, jawaban, waktu, score, status))
        mysql.connection.commit()
        cur.execute("select score_akhir from peserta_kuis where id_peserta = %s", (id_peserta,))
        total_score = cur.fetchall()
        total_score = total_score[0][0]
        cur.execute("select score from jawaban_peserta where id_peserta = %s and id_soal=%s", (id_peserta, id_soal,))
        score = cur.fetchall()
        score = score[0][0]
        total_score = total_score + score
        cur.execute("update peserta_kuis set score_akhir=%s where id_peserta=%s", (total_score, id_peserta,))
        mysql.connection.commit()
    return Response(status=204)

#UPDATE DATA

@app.route('/updatemapel', methods=["POST"])
def updatemapel():
    id_data = request.form["idmatapelajaran"]
    nama = request.form['updatematapelajaran']
    cur = mysql.connection.cursor()
    cur.execute("update tabel_mapel set nama_mapel=%s where id_mapel=%s", (nama,id_data,))
    mysql.connection.commit()
    return redirect(url_for('matapelajaran'))

@app.route('/updatesoal', methods=["POST"])
def updatesoal():
    id_soal = request.form['id_soal']
    soal = request.form['soal']
    j1 = request.form['j1']
    j2 = request.form['j2']
    j3 = request.form['j3']
    j4 = request.form['j4']
    jtrue = request.form['jtrue']
    id_cpl = request.form['cpl']
    waktu = request.form['waktu']
    cur = mysql.connection.cursor()
    cur.execute("update tabel_soal set soal=%s, A=%s, B=%s, C=%s, D=%s, jawaban_benar=%s, waktu=%s, id_cpl=%s where id_soal=%s", (soal, j1, j2, j3, j4, jtrue, waktu, id_cpl, id_soal))
    mysql.connection.commit()
    return redirect(url_for('soalmapel'))

@app.route('/gantisesi/<string:id_sesi>', methods=["GET" , "POST"])
def gantisesi(id_sesi):
    cur = mysql.connection.cursor()
    cur.execute("update sesi_kuis set status=2 where id_sesi=%s", (id_sesi,))
    mysql.connection.commit()
    return Response(status=204)

@app.route('/nomor_kuis_inc')
def nomor_kuis_inc():
    id_sesi = session['id_sesi']
    id_mapel = session['id_mapel']
    cur = mysql.connection.cursor()
    cur.execute("Select id_mapel From tabel_soal where id_mapel=%s",(id_mapel,))
    data = cur.fetchall()
    maxx = len(data)
    cur.execute('select current_number from sesi_kuis where id_sesi = %s', (id_sesi,))
    current_number = cur.fetchone()
    current_number = current_number[0] + 1
    if maxx + 1 == current_number:
        print("SELEXAI")
        return Response(status=204)
    cur.execute("update sesi_kuis set current_number=%s where id_sesi=%s", (current_number, id_sesi,))
    mysql.connection.commit()
    return Response(status=204)

@app.route('/selesai')
def selesai():
    id_sesi = session['id_sesi']
    session.pop('id_sesi', None)
    id_mapel = session['id_mapel']
    cur = mysql.connection.cursor()
    cur.execute("update sesi_kuis set status='3' where id_sesi=%s",(id_sesi,))
    mysql.connection.commit()
    return sesiselesai()

@app.route('/gantistatuspeserta')
def gantistatuspeserta():
    id_peserta = session['id_peserta']
    cur = mysql.connection.cursor()
    cur.execute("select * from peserta_kuis where id_peserta=%s", (id_peserta,))
    data = cur.fetchall()
    print(data[0][1])
    if data[0][3] == 1:
        cur.execute("update peserta_kuis set id_status=2 where id_peserta=%s", (id_peserta,))
        mysql.connection.commit()
    else:
        cur.execute("update peserta_kuis set id_status=1 where id_peserta=%s", (id_peserta,))
        mysql.connection.commit()
    return Response(status=204)

@app.route('/updatecpl', methods=["POST"])
def updatecpl():
    id_cpl = request.form["idcpl"]
    cpl = request.form['cpl']
    cur = mysql.connection.cursor()
    cur.execute("update capaian_pembelajaran set cpl=%s where id_cpl=%s", (cpl,id_cpl,))
    mysql.connection.commit()
    return redirect(url_for('cpmapel'))



#DELETE DATA

@app.route('/deletematapelajaran/<string:id_mapel>', methods=["GET" , "POST"])
def deletematapelajaran(id_mapel):
    cur = mysql.connection.cursor()
    cur.execute("delete from tabel_mapel where id_mapel=%s", (id_mapel,))
    mysql.connection.commit()
    return redirect(url_for('matapelajaran'))

@app.route('/deletecpl/<string:id_cpl>', methods=["GET" , "POST"])
def deletecpl(id_cpl):
    cur = mysql.connection.cursor()
    cur.execute("delete from capaian_pembelajaran where id_cpl=%s", (id_cpl,))
    mysql.connection.commit()
    return redirect(url_for('cpmapel'))

@app.route('/deletesoal/<string:id_soal>', methods=["GET" , "POST"])
def deletesoal(id_soal):
    cur = mysql.connection.cursor()
    cur.execute("delete from tabel_soal where id_soal=%s", (id_soal,))
    mysql.connection.commit()
    return redirect(url_for('soalmapel'))

@app.route('/deletesesi/<string:id_sesi>', methods=["GET" , "POST"])
def deletesesi(id_sesi):
    cur = mysql.connection.cursor()
    cur.execute("delete from sesi_kuis where id_sesi=%s", (id_sesi,))
    mysql.connection.commit()
    return redirect(url_for('sesiselesai'))

#GET

@app.route('/get_current_number')
def get_current_number():
    id_sesi = session['id_sesi']
    cur=mysql.connection.cursor()
    cur.execute('select current_number from sesi_kuis where id_sesi = %s', (id_sesi,))
    result = cur.fetchall()
    return jsonify(current_number=result)

@app.route('/tabel_peserta')
def peserta_kuis():
    id_sesi = session['id_sesi']
    cur = mysql.connection.cursor()
    cur.execute('SELECT `nama_peserta`, status_peserta.status, `score_akhir` FROM `peserta_kuis` Inner join `status_peserta` on peserta_kuis.id_status=status_peserta.id where id_sesi = %s order by `score_akhir` desc', (id_sesi,))
    result = cur.fetchall()
    return jsonify(result=result) 

@app.route('/tabel_hasil_kuis')
def tabel_soal_akhir():
    id_sesi = session['id_sesi']
    cur = mysql.connection.cursor()
    cur.execute('select distinct id_soal from jawaban_peserta where id_sesi = %s', (id_sesi,))
    data = cur.fetchall()
    data_tabel = {} 
    cur.execute('select count(*) from peserta_kuis where id_sesi = %s', (id_sesi,))
    jumlah_peserta = cur.fetchone()
    jumlah_peserta = jumlah_peserta[0]
    x=0
    for i in data:
        id_soal = i[0]
        cur.execute('select count(*) from jawaban_peserta where id_soal =%s AND id_sesi=%s and status = 1',(id_soal,id_sesi,))
        j_benar = cur.fetchone()
        j_benar = round(j_benar[0]/jumlah_peserta * 100)
        data_tabel[x+1] = {
        "nomor" : x+1,
        "id_soal" : id_soal,
        "jawaban_benar" : j_benar
        }
        x+=1
    return jsonify(data_tabel = data_tabel)

@app.route('/tabel_cpl')
def tabel_cpl():
    id_sesi = session['id_sesi']
    cur = mysql.connection.cursor()
    cur.execute('select distinct tabel_soal.id_cpl from jawaban_peserta INNER JOIN tabel_soal on jawaban_peserta.id_soal = tabel_soal.id_soal where id_sesi = %s', (id_sesi,))
    data = cur.fetchall()
    data_tabel = {}
    x=0
    for i in data:
        id_cpl = i[0]
        cur.execute('select count(*) from jawaban_peserta INNER JOIN tabel_soal on jawaban_peserta.id_soal = tabel_soal.id_soal where id_sesi = %s AND jawaban_peserta.status=1 AND id_cpl=%s',(id_sesi,id_cpl,))
        j_benar = cur.fetchone()
        cur.execute('select count(*) from jawaban_peserta INNER JOIN tabel_soal on jawaban_peserta.id_soal = tabel_soal.id_soal where id_sesi = %s AND id_cpl=%s',(id_sesi,id_cpl,))
        t_jawaban = cur.fetchone()
        j_final = round(j_benar[0]/t_jawaban[0] * 100)
        cur.execute('select cpl from capaian_pembelajaran where id_cpl = %s', (id_cpl,))
        cpl = cur.fetchone()
        data_tabel[id_cpl] = {
            "cpl" : cpl[0],
            "j_benar" : j_final 
        }
        x+=1
    return jsonify(data_tabel = data_tabel)

@app.route('/tabel_jawaban/<int:id_soal>', methods=['GET'])
def tabel_jawaban(id_soal):
    id_sesi = session['id_sesi']
    cur = mysql.connection.cursor()
    cur.execute('SELECT peserta_kuis.nama_peserta, jawaban, tabel_soal.jawaban_benar, Case when jawaban = tabel_soal.jawaban_benar then "Benar" else "Salah" end as jawab FROM `jawaban_peserta` inner join `peserta_kuis` on jawaban_peserta.id_peserta = peserta_kuis.id_peserta inner join `tabel_soal` on jawaban_peserta.id_soal = tabel_soal.id_soal where jawaban_peserta.id_sesi = %s and jawaban_peserta.id_soal = %s', (id_sesi,id_soal,))
    result = cur.fetchall()
    return jsonify(result=result)  

#AKSI LOGIN & LOGOUT

@app.route('/pengajarlogin', methods=["POST"])
def pengajarlogin():
    if request.method == 'POST' and 'nama' in request.form:
        username = request.form['nama']
        password = request.form['password']
        session['username'] = request.form['nama']
        cur = mysql.connection.cursor()
        cur.execute("Select * From user where username = %s AND password = %s", (username, password))
        account = cur.fetchall()    
        if account:
            session['loggedid'] = True
            session['user'] = account[0][0]
            session['nama_user'] = account[0][3]
            return redirect(url_for('dashboard'))
        else:
            msg = "USERNAME dan PASSWORD Salah !!!!"
            return render_template("pengajar.html",msg=msg, username = username, password = password)
        
@app.route('/logout')
def logout():
    session['loggedid'] = False
    return redirect(url_for('index'))

if __name__ == '__main__' :
    app.run(debug=True, host='')