from flask import Flask, render_template, request
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
import smtplib
from email.message import EmailMessage


app = Flask(__name__)
bootstrap = Bootstrap5(app)

app.config['SECRET_KEY'] = "secretkey"
my_email = "your_own@gmail.com"
PASSWORD_EMAIL = "your_own_password"


class ContactForm(FlaskForm):
    name = StringField(label="", validators=[DataRequired()], render_kw={"placeholder": "Name"})
    email = EmailField(label="", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    message = TextAreaField(label="", validators=[DataRequired()], render_kw={"placeholder": "Message"})
    send = SubmitField("Send")


@app.route("/")
def home():
    return render_template("index.html", active_page="home")


@app.route("/about")
def about():
    return render_template("about.html", active_page="about")


@app.route("/projects")
def projects():
    return render_template("projects.html", active_page="projects")


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if request.method == "POST" and form.validate_on_submit():
        msg = EmailMessage()
        msg["From"] = my_email
        msg["Subject"] = "You've got new message from Portfolio"
        msg["To"] = my_email
        msg.set_content(f"Name: {form.name.data}\nEmail: {form.email.data}\nMessage: {form.message.data}")
        print(msg)
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=PASSWORD_EMAIL)
            connection.send_message(msg=msg)
        return render_template("contact.html", active_page="contact", form=form, message_sent=True)

    return render_template("contact.html", active_page="contact", form=form, message_sent=False)


if __name__ == "__main__":
    app.run(debug=True, port=2000)
