from flask import Flask, redirect, url_for, render_template, request, session, flash
import chatbot
from EmailSender import EmailSender_163
import PDF_report

import os
from datetime import timedelta

from keras.models import load_model

new_model = load_model('COVID_CT_CNN_MODEL.h5')
import numpy as np
from keras.preprocessing import image as img

app = Flask(__name__)
app.secret_key = 'hi'
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    return render_template('index.html', url=url_for('main'))


@app.route("/login", methods=["POST", "GET"])
def login():
    if "user" not in session and "email" not in session:
        if request.method == "POST":
            session.permanent = True
            user = request.form['name']
            email = request.form['email']
            session["user"] = user
            session["email"] = email
            return redirect(url_for("user"))
        else:
            return render_template('login.html')
    else:
        flash(f'You have already logged in! Please log out first.')
        return redirect(url_for("user"))


@app.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session and "email" in session:
        user = session["user"]
        email = session["email"]
        if request.method == "POST":
            if "image" in session:
                email_sender = EmailSender_163()
                s = email_sender.send_single_email(email, "Things you need to know about COVID-19", "templates/email.html")
                if s == 1:
                    flash("Email has been sent successfully!")
                else:
                    flash("Aww... Email fails to be sent. ")
                return render_template('User.html', user=user, email=email)
            else:
                flash("Please upload your CT Scan before claiming your report.")
                return render_template('User.html', user=user, email=email)
        else:
            return render_template('User.html', user=user, email=email)
    else:
        flash(f"You haven't logged in yet!")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f'You have been logged out! {user}')
    session.pop("user", None)  # to delete that value from session
    session.pop("email", None)
    if "image" in session:
        session.pop("image", None)
    else:
        flash("Please log in first!")
    return redirect(url_for('login'))


@app.route("/main", methods=['POST', 'GET'])
def main():
    if "user" in session and "email" in session:
        # Chatting part
        bot_msg = "Doc Bot: I am your personal medical assistant, Doc Bot. I will answer your queries about COVID-19 Disease." \
                  " \nIf you want to exit, type 'bye'."
        if request.method == 'POST':
            user_input = request.form['user_input']
            exit_list = ['exit', 'see you later', 'bye', 'quit', 'break', 'goodbye']
            if user_input.lower() in exit_list:
                bot_msg = "Doc Bot: Chat with you later ~"
            else:
                if chatbot.greeting_response(user_input) != None:
                    bot_msg = 'Doc Bot: ' + chatbot.greeting_response(user_input)

                elif chatbot.age_response(user_input) != None:
                    bot_msg ='Doc Bot: ' + chatbot.age_response(user_input)

                elif chatbot.name_response(user_input) != None:
                    bot_msg ='Doc Bot: ' + chatbot.name_response(user_input)

                elif chatbot.joke_response(user_input) != None:
                    bot_msg ='Doc Bot: ' + chatbot.joke_response(user_input)

                else:
                    bot_msg = 'Doc Bot: ' + chatbot.bot_response(user_input)

            return render_template('home.html',
                                   bot_msg=bot_msg,
                                   upload_url=url_for('image_upload'))

        else:

            return render_template('home.html',
                                   bot_msg=bot_msg,
                                   upload_url=url_for('image_upload'))
    else:
        flash(f"Please log in first!")
        return redirect(url_for("login"))


@app.route("/upload", methods=['POST', 'GET'])
def image_upload():
    if "user" in session and "email" in session:
        if request.method == 'POST':
            if request.files:
                image = request.files['image']
                session['image'] = image.filename
                image.save(os.path.join('static/image', image.filename))

                test_image = img.load_img(f'static/image/{image.filename}', target_size=(64, 64))
                test_image = img.img_to_array(test_image)  # making it to 1D array
                test_image = np.expand_dims(test_image, axis=0)  # expanding it to 2D array
                result = new_model.predict(test_image)[0][0]
                prediction = 'Positive' if result == 0 else 'Negative'

                # Process the result
                pdf = PDF_report.PdfReport("my_Report")
                pdf.generate(name= session["user"], image_name= f"{session['image']}", result= prediction)
                url = PDF_report.FileSharer(f"static/{pdf.filename}")


            return render_template('upload.html',
                                   chat_url=url_for('main'),
                                   home_url=url_for('home'),
                                   result=True,
                                   prediction=prediction,
                                   pdf_url= url.share())
        else:
            return render_template('upload.html',
                                   chat_url=url_for('main'),
                                   home_url=url_for('home'),
                                   result=False)
    else:
        flash(f"Please log in first!")
        return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
