import os
import psycopg2
from flask import Flask, render_template,request, url_for, redirect
from app import app
from app.frm_data import EditForm,CariForm

def get_db_connection():
    conn=psycopg2.connect(host='localhost',
                          database='testing',
                          user='postgres',
                          password='postgres123')
    return conn

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("home.html")

@app.route("/tampil_data", methods=["GET","POST"])
def tampil_data():
    conn = get_db_connection()
    cur = conn.cursor()
    form_cari=CariForm()

    wherenya_1=""

    if request.method=="POST":
       details=request.form
       ynama_situ=details["wnama_situ"]

       if len(ynama_situ)>0:
          wherenya_1=" where k1_nama_danau_situ like '%"+ynama_situ+"%'"
       else:
          wherenya_1=""

    cur.execute("select ogc_fid,k1_nama_danau_situ,k2_alamat,k16_berapa_kedalaman_air_rata_rata_situ_meter,"
                "k17_berapa_kedalaman_air_maksimum_situ_meter,k18_adakah_pembatas_situ,k3_titik_lokasi_lat,"
                "k3_titik_lokasi_peta_lon,foto_inlet_situ from situ "+wherenya_1+" order by ogc_fid")
    dataku = cur.fetchall()

    # Data Peta
    cur.execute("select ogc_fid,k1_nama_danau_situ,k2_alamat,k3_titik_lokasi_lat,k3_titik_lokasi_peta_lon,"
                "foto_inlet_situ from situ"+wherenya_1)
    datapeta = cur.fetchall()

    cur.close()
    conn.close()
    return render_template("tampil_data.html", dataku=dataku,datapeta=datapeta,form_cari=form_cari)

@app.route("/edit_data/<id>",methods=["GET","POST"])
def edit_data(id):
    conn = get_db_connection()
    cur = conn.cursor()
    form=EditForm()
    cur.execute("select ogc_fid,k1_nama_danau_situ,k2_alamat,k16_berapa_kedalaman_air_rata_rata_situ_meter,"
                "k17_berapa_kedalaman_air_maksimum_situ_meter,k18_adakah_pembatas_situ,"
                "k3_titik_lokasi_peta_lon,k3_titik_lokasi_lat,foto_inlet_situ from situ where ogc_fid='"+id+"'")
    hasilnya=cur.fetchall()
    for rows in hasilnya:
        xnama_situ=rows[1]
        xalamat_situ=rows[2]
        xair_rata_rata=rows[3]
        xair_max=rows[4]
        xpembatas=rows[5]
        xlon = rows[6]
        xlat = rows[7]

    if request.method=="POST":
       details=request.form
       xnama_situ = details["znama_situ"]
       xalamat_situ = details["zalamat_situ"]
       xair_rata_rata = details["zair_rata_rata"]
       xair_max = details["zair_max"]
       xpembatas = details["zpembatas"]
       xlon = details["zlon"]
       xlat = details["zlat"]

       cur.execute("update situ set k1_nama_danau_situ=%s,k2_alamat=%s,k3_titik_lokasi_peta_lon=%s,"
                   "k3_titik_lokasi_lat=%s,k16_berapa_kedalaman_air_rata_rata_situ_meter=%s,"
                   "k17_berapa_kedalaman_air_maksimum_situ_meter=%s,k18_adakah_pembatas_situ=%s"
                   "where ogc_fid=%s",((xnama_situ,xalamat_situ,xlon,xlat,xair_rata_rata,xair_max,xpembatas,id)))
       cur.connection.commit()
       cur.close()
       return render_template("info/sukses_edit.html")
    else:
       form.znama_situ.data=xnama_situ
       form.zalamat_situ.data=xalamat_situ
       form.zair_rata_rata.data=xair_rata_rata
       form.zair_max.data=xair_max
       form.zpembatas.data=xpembatas
       form.zlon.data = xlon
       form.zlat.data = xlat
    return render_template("edit_data.html",form=form)

@app.route("/hapus_data/<id>",methods=["GET","POST"])
def hapus_data(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("delete from situ where ogc_fid='"+id+"'")
    cur.connection.commit()
    cur.close()
    return render_template("info/sukses_hapus_data.html")

@app.route("/entry_data",methods=["GET","POST"])
def entry_data():
    conn = get_db_connection()
    cur = conn.cursor()
    form=EditForm()

    if request.method=="POST":
        details=request.form
        xnama_situ = details["znama_situ"]
        xalamat_situ = details["zalamat_situ"]
        xair_rata_rata = details["zair_rata_rata"]
        xair_max = details["zair_max"]
        xpembatas = details["zpembatas"]
        xlon = details["zlon"]
        xlat = details["zlat"]
        xinlet_situ=details["zinlet_situ"]

        cur.execute("select max(ogc_fid) from situ")
        hasil=cur.fetchall()
        for rows in hasil:
            nilai_max=rows[0]

        nilai_max_baru=nilai_max+1
        cur.execute("insert into situ (ogc_fid,k1_nama_danau_situ,k2_alamat,k16_berapa_kedalaman_air_rata_rata_situ_meter,"
                    "k17_berapa_kedalaman_air_maksimum_situ_meter,k18_adakah_pembatas_situ,k3_titik_lokasi_peta_lon,"
                    "k3_titik_lokasi_lat) values (%s,%s,%s,%s,%s,%s,%s,%s)",((nilai_max_baru,xnama_situ,xalamat_situ,
                     xair_rata_rata,xair_max,xpembatas,xlon,xlat)))
        cur.connection.commit()
        cur.close()
        return render_template("info/sukses_entry.html")

    return render_template("entry_data.html",form=form)






