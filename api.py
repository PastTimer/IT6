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
    response.headers['Content-Type'] = 'application/xml'
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
    hobby_desc = info["hobby_desc"]
    cur.execute(
        """ INSERT INTO hobbies_and_pasttime (hobby_code, hobby_desc) VALUES (%s, %s)""",
        (hobby_code, hobby_desc),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    response.headers['Content-Type'] = 'application/xml'
    return make_response(
        jsonify({"message": "Value added successfully", 
                 "rows_affected": rows_affected}), 201,)

@app.route("/organizations/add", methods=["POST"])
def add_organizations():
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Content-Type must be application/json"}), 415)
    cur = mysql.connection.cursor()
    info = request.get_json()
    organization_id = info["organization_id"]
    organization_details = info["organization_details"]
    cur.execute(
        """ INSERT INTO organizations (organization_id, organization_details) VALUES (%s, %s)""",
        (organization_id, organization_details),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    response.headers['Content-Type'] = 'application/xml'
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
    response.headers['Content-Type'] = 'application/xml'
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
    response.headers['Content-Type'] = 'application/xml'
    return make_response(
        jsonify({"message": "Value added successfully", 
                 "rows_affected": rows_affected}), 201,)
    
##PUT
@app.route("/members/update/<int:id>", methods=["PUT"])
def update_members(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    first_name = info["first_name"]
    last_name = info["last_name"]
    address = info["address"]
    other_details = info["other_details"]
    cur.execute(
        """ UPDATE members SET first_name = %s, last_name = %s, address = %s, other_details = %s WHERE member_id = %s """,
        (first_name, last_name, address, other_details, id),)
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response.headers['Content-Type'] = 'application/xml'
    return make_response(
        jsonify({"message": "Value updated successfully", 
                 "rows_affected": rows_affected}),200,)

@app.route("/hobbies_and_pasttime/update/<id>", methods=["PUT"])
def update_hobbies(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    hobby_desc = info["hobby_desc"]
    cur.execute(
        """ UPDATE hobbies_and_pasttime SET hobby_desc = %s WHERE hobby_code = %s """,
        (hobby_desc, id),)
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response.headers['Content-Type'] = 'application/xml'
    return make_response(
        jsonify({"message": "Value updated successfully", 
                 "rows_affected": rows_affected}),200,)

@app.route("/organizations/update/<id>", methods=["PUT"])
def update_organizations(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    organization_details = info["organization_details"]
    cur.execute(
        """ UPDATE organizations SET organization_details = %s WHERE organization_id = %s """,
        (organization_details, id),)
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response.headers['Content-Type'] = 'application/xml'
    return make_response(
        jsonify({"message": "Value updated successfully", 
                 "rows_affected": rows_affected}),200,)

@app.route("/events/update/<int:id>", methods=["PUT"])
def update_events(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    event_name = info["event_name"]
    event_description = info["event_description"]
    location = info["location"]
    other_details = info["other_details"]
    cur.execute(
        """ UPDATE events SET event_name = %s, event_description = %s, location = %s, other_details = %s WHERE event_id = %s """,
        (event_name, event_description, location, other_details, id),)
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response.headers['Content-Type'] = 'application/xml'
    return make_response(
        jsonify({"message": "Value updated successfully", 
                 "rows_affected": rows_affected}),200,)

@app.route("/memberships/update/<int:id>", methods=["PUT"])
def update_membersships(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    level_of_ability = info["level_of_ability"]
    hobby_code = info["hobby_code"]
    member_id = info["member_id"]
    organisation_id = info["organisation_id"]
    cur.execute(
        """ UPDATE memberships SET level_of_ability = %s, hobby_code = %s, member_id = %s, organisation_id = %s WHERE membership_id = %s """,
        (level_of_ability, hobby_code, member_id, organisation_id, id),)
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response.headers['Content-Type'] = 'application/xml'
    return make_response(
        jsonify({"message": "Value updated successfully", 
                 "rows_affected": rows_affected}),200,)

##DELETE
@app.route("/members/del/<int:id>", methods=["DELETE"])
def delete_member(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM members where member_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response.headers['Content-Type'] = 'application/xml'
    return make_response(
        jsonify(
            {"message": "Value deleted successfully", "rows_affected": rows_affected}),200,)

@app.route("/hobbies_and_pasttime/del/<id>", methods=["DELETE"])
def delete_hobby(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM hobbies_and_pasttime where hobby_code = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response.headers['Content-Type'] = 'application/xml'
    return make_response(
        jsonify(
            {"message": "Value deleted successfully", "rows_affected": rows_affected}),200,)

@app.route("/organizations/del/<id>", methods=["DELETE"])
def delete_org(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM organizations where organization_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response.headers['Content-Type'] = 'application/xml'
    return make_response(
        jsonify(
            {"message": "Value deleted successfully", "rows_affected": rows_affected}),200,)

@app.route("/events/del/<int:id>", methods=["DELETE"])
def delete_event(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM events where event_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response.headers['Content-Type'] = 'application/xml'
    return make_response(
        jsonify(
            {"message": "Value deleted successfully", "rows_affected": rows_affected}),200,)

@app.route("/memberships/del/<int:id>", methods=["DELETE"])
def delete_memberships(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM memberships where membership_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response.headers['Content-Type'] = 'application/xml'
    return make_response(
        jsonify(
            {"message": "Value deleted successfully", "rows_affected": rows_affected}),200,)

##URI
@app.route("/members/format", methods=["GET"])
def get_params():
    format_type = request.args.get('format', 'json')
    data = {"format": format_type, "foo": "bar"}
    if format_type.lower() == 'xml':
        response = make_response("<data><format>xml</format><foo>bar</foo></data>")
        response.headers['Content-Type'] = 'application/xml'
    else:
        response = jsonify(data)
    return response

if __name__ == "__main__":
    app.run(debug=True)
