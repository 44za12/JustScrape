from flask import Flask, render_template, flash, request, send_from_directory
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, ValidationError
import json
from random import randint
import os
import justscrape as s
from flask_mail import Message, Mail
app = Flask(__name__)
app.config.update(dict(
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'YOUR_EMAIL_ADDRESS_HERE',
    MAIL_PASSWORD = 'YOUR_EMAIL_PASSWORD_HERE'
))
mail = Mail(app)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
def pageNumberCheck(form, field):
    if not field.data.isdigit():
        raise ValidationError('Enter a number in pages field')
class IndexForm(Form):
    url = TextField('url', validators=[validators.Required(),validators.URL(require_tld=True,message="Please enter a valid URL")])
    pages = TextField('pages',validators=[pageNumberCheck])
class ContactForm(Form):
  name = TextField("name",  [validators.Required("Please enter your name.")])
  email = TextField("email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("submit")
@app.route("/", methods=['GET', 'POST'])
def index():
    form = IndexForm(request.form)
    print(form.errors)
    if request.method == 'POST':
        url=request.form['url']
        if request.form['pages'] != '':
          pages=request.form['pages']
        else:
          pages=1
        if form.validate():
            filepath = s.scrape(url,pages)
            flash(filepath)
        else:
            flash('Error: A valid URL and pagenumber as an integer is required.')
    return render_template('index.html', form=form)
@app.route("/about", methods=['GET', 'POST'])
def about():
     return render_template('about.html')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm(request.form)
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='YOUR_EMAIL_ADDRESS_HERE', recipients=['YOUR_EMAIL_ADDRESS_HERE'])
      msg.body = """
      From: %s &lt;%s&gt;
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      return render_template('contact.html', form=form, success=True)
  elif request.method == 'GET':
    return render_template('contact.html', form=form)
@app.route('/download/<path:filename>')
def download(filename,methods=['GET','POST']):
    root_dir = os.getcwd()
    return send_from_directory(
        directory= root_dir,filename=filename
    )
if __name__ == "__main__":
    app.run(debug=True)