from flask import Flask, render_template, request, redirect, url_for, g
from mysql.connector import Error
from mysql_link import MysqlLink  # Import your MysqlLink class

app = Flask(__name__)
db_link = MysqlLink()  # Create an instance of MysqlLink


def get_db():
    """Get the database connection."""
    if 'db' not in g or g.db is None or not g.db.is_connected():
        db_link.connect_to_database()  # Ensure a new connection is established if needed
        g.db = db_link.connection
    return g.db


@app.route('/')
def index():
    """Render the index page with members and their count."""
    try:
        cursor = get_db().cursor(dictionary=True)
        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS member_count FROM members")
        member_count = cursor.fetchone()['member_count']

        return render_template('index.html', members=members, member_count=member_count)
    except Error as e:
        print(f"Database error: {e}")
        return render_template('index.html', members=[], member_count=0)


@app.route('/add_member', methods=['POST'])
def add_member():
    """Add a new member to the database."""
    try:
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        membership_duration = request.form['membership_duration']
        paid_fee = request.form['paid_fee']
        phone_number = request.form['phone_number']

        cursor = get_db().cursor()
        query = "INSERT INTO members (name, age, gender, membership_duration, paid_fee, phone_number) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, age, gender, membership_duration, paid_fee, phone_number)
        cursor.execute(query, values)
        db_link.connection.commit()  # Commit the transaction
        cursor.close()
        print(f"Member added: {values}")  # Debugging line to confirm addition
    except Error as e:
        print(f"Error adding member: {e}")
    return redirect(url_for('index'))


@app.route('/delete_member/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    """Delete a member from the database."""
    try:
        cursor = get_db().cursor()
        query = "DELETE FROM members WHERE id = %s"
        cursor.execute(query, (member_id,))
        db_link.connection.commit()
        cursor.close()
        print(f"Deleted member ID: {member_id}")  # Debugging line
    except Error as e:
        print(f"Error deleting member: {e}")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)