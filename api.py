from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "hobbies&pasttime"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/events", methods=["GET"])
def get_events():
    cur = mysql.connection.cursor()
    query="""
    select * from events;
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    
    return make_response(jsonify(data), 200)

@app.route("/members", methods=["GET"])
def get_members():
    cur = mysql.connection.cursor()
    query="""
    select * from members;
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    
    return make_response(jsonify(data), 200)

@app.route("/hobbies_and_pasttime", methods=["GET"])
def get_hobbies_and_pasttime():
    cur = mysql.connection.cursor()
    query="""
    select * from hobbies_and_pasttime;
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    
    return make_response(jsonify(data), 200)

@app.route("/organizations", methods=["GET"])
def get_organizations():
    cur = mysql.connection.cursor()
    query="""
    select * from organizations;
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    
    return make_response(jsonify(data), 200)

@app.route("/memberships", methods=["GET"])
def get_memberships():
    cur = mysql.connection.cursor()
    query="""
    select * from memberships;
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)
    