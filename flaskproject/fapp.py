from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user_db'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        
        if 'add_user' in request.form:
            user_id = request.form['user_id']
            username = request.form['username']
            email = request.form['email']
            number = request.form['number']
            course = request.form['course']
            cur.execute("INSERT INTO users (id, name, email, number, course) VALUES (%s, %s, %s, %s, %s)", (user_id, username, email, number, course))
        
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    userDetails = cur.fetchall()
    cur.close()
    
    return render_template('index.html', userDetails=userDetails)

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_email = request.form['new_email']
        new_number = request.form['new_number']
        new_course = request.form['new_course']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET name = %s, email = %s, number = %s, course = %s WHERE id = %s", (new_username, new_email, new_number, new_course, user_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    return render_template('update.html', user=user)


@app.route('/delete/<int:user_id>', methods=['GET'])
def delete(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))


@app.route('/user_details', methods=['GET'])
def user_details():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users ")
    userDetails = cur.fetchall()
    cur.close()
    
    return render_template('user_details.html', userDetails=userDetails)


if __name__ == "__main__":
    app.run(debug=True)
