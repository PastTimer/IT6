from flask import Flask, make_response, jsonify, request, render_template_string
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "hobbies&pasttime"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

###Default
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def data_fetch(query, params=None):
    cur = mysql.connection.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

###GET
@app.route("/events", methods=["GET"])
def get_events():
    data = data_fetch("""select * from events;""")
    return make_response(jsonify(data), 200)

@app.route("/members", methods=["GET"])
def get_members():
    data = data_fetch("""select * from members;""")
    return make_response(jsonify(data), 200)

@app.route("/hobbies_and_pasttime", methods=["GET"])
def get_hobbies_and_pasttime():
    data = data_fetch("""select * from hobbies_and_pasttime;""")
    return make_response(jsonify(data), 200)

@app.route("/organizations", methods=["GET"])
def get_organizations():
    data = data_fetch("""select * from organizations;""")
    return make_response(jsonify(data), 200)

@app.route("/memberships", methods=["GET"])
def get_memberships():
    data = data_fetch("""select * from memberships;""")
    return make_response(jsonify(data), 200)

@app.route("/events/<int:id>", methods=["GET"])
def get_event_by_id(id):
    data = data_fetch("""select * from events where event_id = %s;""", (id,))
    return make_response(jsonify(data), 200)

###GET FANCY
@app.route("/hobbies_and_pasttime/<id>/members", methods=["GET"])
def get_members_by_hobby(id):
    data = data_fetch("""
        SELECT m.first_name, m.last_name
        FROM members m
        INNER JOIN memberships ms ON m.member_id = ms.member_id
        INNER JOIN hobbies_and_pasttime h ON ms.hobby_code = h.hobby_code
        WHERE h.hobby_code = %s
        GROUP BY m.first_name, m.last_name;
    """, (id,))
    return make_response(jsonify({"hobby_code": id, "count": len(data), "members": data}), 200)

###POST
@app.route("/members/add", methods=["POST"])
def add_member():
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Content-Type must be application/json"}), 415)
    cur = mysql.connection.cursor()
    info = request.get_json()
    first_name = info["first_name"]
    last_name = info["last_name"]
    address = info["address"]
    other_details = info["other_details"]
    cur.execute(
        """ INSERT INTO members (first_name, last_name, address, other_details) VALUES (%s, %s, %s, %s)""",
        (first_name, last_name, address, other_details),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify({"message": "Value added successfully", 
                 "rows_affected": rows_affected}), 201,)

@app.route("/hobbies_and_pasttime/add", methods=["POST"])
def add_hobby():
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Content-Type must be application/json"}), 415)
    cur = mysql.connection.cursor()
    info = request.get_json()
    hobby_code = info["hobby_code"]
    hobby_desc = info["hobby_description"]
    cur.execute(
        """ INSERT INTO hobbies_and_pasttime (hobby_code, hobby_desc) VALUES (%s, %s)""",
        (hobby_code, hobby_desc),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify({"message": "Value added successfully", 
                 "rows_affected": rows_affected}), 201,)

@app.route("/organizations/add", methods=["POST"])
def add_organizations():
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Content-Type must be application/json"}), 415)
    cur = mysql.connection.cursor()
    info = request.get_json()
    organization_id = info["organization_code"]
    organization_details = info["organization_description"]
    cur.execute(
        """ INSERT INTO organizations (organization_id, organization_details) VALUES (%s, %s)""",
        (organization_id, organization_details),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify({"message": "Value added successfully", 
                 "rows_affected": rows_affected}), 201,)

@app.route("/events/add", methods=["POST"])
def add_events():
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Content-Type must be application/json"}), 415)
    cur = mysql.connection.cursor()
    info = request.get_json()
    event_name = info["event_name"]
    event_description = info["event_description"]
    location = info["location"]
    other_details = info["other_details"]
    cur.execute(
        """ INSERT INTO events (event_name, event_description, location, other_details) VALUES (%s, %s, %s, %s)""",
        (event_name, event_description, location, other_details),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify({"message": "Value added successfully", 
                 "rows_affected": rows_affected}), 201,)

@app.route("/memberships/add", methods=["POST"])
def add_memberships():
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Content-Type must be application/json"}), 415)
    cur = mysql.connection.cursor()
    info = request.get_json()
    level_of_ability = info["level_of_ability"]
    hobby_code = info["hobby_code"]
    member_id = info["member_id"]
    organisation_id = info["organisation_id"]
    cur.execute(
        """ INSERT INTO memberships (level_of_ability, hobby_code, member_id, organisation_id) VALUES (%s, %s, %s, %s)""",
        (level_of_ability, hobby_code, member_id, organisation_id),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify({"message": "Value added successfully", 
                 "rows_affected": rows_affected}), 201,)

if __name__ == "__main__":
    app.run(debug=True)
