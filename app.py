from flask import *
from flask_mail import Mail, Message
import sqlite3, os

app = Flask(__name__)

DATABASE = "personal.db"

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def fetchall_to_dict(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    result_list = [dict(zip(columns, row)) for row in rows]
    return result_list# Configure Flask-Mail

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'garyaxelmuliyono@gmail.com'  # Replace with your Gmail address
app.config['MAIL_PASSWORD'] = "aaa"   # Replace with your Gmail password
app.config['MAIL_DEFAULT_SENDER'] = 'garyaxelmuliyono@gmail.com'  # Replace with your Gmail address

mail = Mail(app)

@app.route('/',methods=['GET','POST'])
def root():
    if request.method == 'GET':
        db = get_db()
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        expData = fetchall_to_dict(cursor, 'SELECT * FROM Experience')
        eduData = fetchall_to_dict(cursor, 'SELECT * FROM Education')
        conn.close()
        for item in expData + eduData:
            if item['description']:
                if item['description'][:4] == 'http':
                    item['link'] = item['description'].split('|')[0]
                    item['label'] = item['description'].split('|')[1]
                    item['description'] = item['description'].split('|')[2]
        db.close()
        print(get_flashed_messages())
        return render_template('home.html',expData = expData, eduData = eduData, messages = get_flashed_messages())
    else:
        full_name = request.form.get('fullName')
        email = request.form.get('email')
        message = request.form['message']
        subject = 'Contact Form Submission from salmonkarp.com'
        body = f'Name: {full_name}\nEmail: {email}\nMessage: {message}'
        msg = Message(subject, recipients=['garyaxelmuliyono@gmail.com'])  # Replace with your email address
        msg.body = body
        try:
            mail.send(msg)
            response = {
                'script': 'document.getElementById("contact-form").reset(); alert("Message submitted successfully!");'
            }
            return jsonify(response)
        except Exception as e:
            response = {
                'script': f'alert("Error sending email: {str(e)}");'
            }
            return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)