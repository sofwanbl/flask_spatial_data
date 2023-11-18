from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField, TextAreaField, RadioField
from wtforms.validators import DataRequired

class EditForm(FlaskForm):
    znama_situ=StringField("Nama Situ")
    zalamat_situ=TextAreaField("Alamat Situ")
    zair_rata_rata=StringField("Kedalaman Air rata-rata")
    zair_max=StringField("Kedalaman Air Max")
    zpembatas=RadioField("Adakah Pembatas", choices=[("Ya","Ya"),("Tidak","Tidak")])
    zlat = StringField("Latitude",default=0)
    zlon = StringField("Longitude", default=0)
    zinlet_situ=StringField("Foto Inlet Situ")
    submit=SubmitField("Edit")
    submit_entry=SubmitField("Simpan")

class CariForm(FlaskForm):
    wnama_situ = StringField("Nama Situ")
    submit_cari = SubmitField("Cari")