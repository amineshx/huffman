from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField

class Huffman(FlaskForm):
    charchain = StringField(label='Donner la chaine de caracteres: ')
    submit = SubmitField(label='submit')

class Shanonfano(FlaskForm):
    charchain = StringField(label='Donner la chaine de caracteres: ')
    submit = SubmitField(label='submit')    

class Prefix(FlaskForm):
    codes = StringField(label='Donner les codes: ')
    probabilities = StringField(label='Donner les proba: ')
    submit = SubmitField(label='submit')

