from flask import Flask, make_response, jsonify, request, render_template_string, Response, session, g
from flask_mysqldb import MySQL
import dicttoxml
from xml.dom.minidom import parseString
import jwt
from datetime import datetime, timedelta
from functools import wraps


app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "hobbies&pasttime"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config['SECRET_KEY'] = 'super_duper_secret_key'
app.config['SESSION_COOKIE_NAME'] = 'session_cookie_name'
app.config['SESSION_COOKIE_PATH'] = '/'


mysql = MySQL(app)

###Default
def data_fetch(query, params=None):
    cur = mysql.connection.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

def format_response(data, format):
    if format == "xml":
        xml = dicttoxml.dicttoxml(data, custom_root='response', attr_type=False)
        dom = parseString(xml)
        xml_str = dom.toprettyxml()
        return Response(xml_str, mimetype='application/xml')
    else:
        return make_response(jsonify(data), 200)

def generate_jwt_token(user_id):
    secret_key = app.config['SECRET_KEY']
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)}
    return jwt.encode(payload, secret_key, algorithm='HS256')

def decode_jwt_token(token):
    secret_key = app.config['SECRET_KEY']
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = decode_jwt_token(token)
            current_user = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token is expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'root' and password == 'root':
            user_id = 1
            token = generate_jwt_token(user_id)
            session['token'] = token 
            return jsonify({'message': 'Login successful', 'token': token}), 200
        else:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route("/logout", methods=['POST'])
def logout():
    session.pop('token', None)
    return jsonify({'message': 'Logged out successfully'}), 200


###GET
@app.route("/events", methods=["GET"])
@token_required
def get_events():
    data = data_fetch("""select * from events;""")
    response_format = request.args.get('format', 'json')
    return format_response(data, response_format)

@app.route("/members", methods=["GET"])
@token_required
def get_members():
    data = data_fetch("""select * from members;""")
    response_format = request.args.get('format', 'json')
    return format_response(data, response_format)

@app.route("/hobbies_and_pasttime", methods=["GET"])
@token_required
def get_hobbies_and_pasttime():
    data = data_fetch("""select * from hobbies_and_pasttime;""")
    response_format = request.args.get('format', 'json')
    return format_response(data, response_format)

@app.route("/organizations", methods=["GET"])
@token_required
def get_organizations():
    data = data_fetch("""select * from organizations;""")
    response_format = request.args.get('format', 'json')
    return format_response(data, response_format)

@app.route("/memberships", methods=["GET"])
@token_required
def get_memberships():
    data = data_fetch("""select * from memberships;""")
    response_format = request.args.get('format', 'json')
    return format_response(data, response_format)

###GET SPECIFIC (SEARCH)
@app.route("/events/<int:id>", methods=["GET"])
@token_required
def get_event_by_id(id):
    data = data_fetch("""select * from events where event_id = %s;""", (id,))
    response_format = request.args.get('format', 'json')
    return format_response(data, response_format)

@app.route("/hobbies_and_pasttime/<id>", methods=["GET"])
@token_required
def get_hobby_by_id(id):
    data = data_fetch("""select * from hobbies_and_pasttime where hobby_code = %s;""", (id,))
    response_format = request.args.get('format', 'json')
    return format_response(data, response_format)

@app.route("/members/<int:id>", methods=["GET"])
@token_required
def get_member_by_id(id):
    data = data_fetch("""select * from members where member_id = %s;""", (id,))
    response_format = request.args.get('format', 'json')
    return format_response(data, response_format)

@app.route("/memberships/<int:id>", methods=["GET"])
@token_required
def get_memebership_by_id(id):
    data = data_fetch("""select * from memberships where membership_id = %s;""", (id,))
    response_format = request.args.get('format', 'json')
    return format_response(data, response_format)

@app.route("/organizations/<id>", methods=["GET"])
@token_required
def get_org_by_id(id):
    data = data_fetch("""select * from organizations where organization_id = %s;""", (id,))
    response_format = request.args.get('format', 'json')
    return format_response(data, response_format)

###GET FANCY
@app.route("/hobbies_and_pasttime/<id>/members", methods=["GET"])
@token_required
def get_members_by_hobby(id):
    data = data_fetch("""
        SELECT m.first_name, m.last_name
        FROM members m
        INNER JOIN memberships ms ON m.member_id = ms.member_id
        INNER JOIN hobbies_and_pasttime h ON ms.hobby_code = h.hobby_code
        WHERE h.hobby_code = %s
        GROUP BY m.first_name, m.last_name;
    """, (id,))
    response_format = request.args.get('format', 'json')
    return format_response({"hobby_code": id, "count": len(data), "members": data}, response_format)

###POST
@app.route("/members/add", methods=["POST"])
@token_required
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
        """INSERT INTO members (first_name, last_name, address, other_details) VALUES (%s, %s, %s, %s)""",
        (first_name, last_name, address, other_details),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response = make_response(
        jsonify({"message": "Value added successfully", "rows_affected": rows_affected}), 201
    )
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route("/hobbies_and_pasttime/add", methods=["POST"])
@token_required
def add_hobby():
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Content-Type must be application/json"}), 415)
    cur = mysql.connection.cursor()
    info = request.get_json()
    hobby_code = info["hobby_code"]
    hobby_desc = info["hobby_desc"]
    cur.execute(
        """INSERT INTO hobbies_and_pasttime (hobby_code, hobby_desc) VALUES (%s, %s)""",
        (hobby_code, hobby_desc),
    )
    mysql.connection.commit()

    rows_affected = cur.rowcount
    cur.close()
    response = make_response(
        jsonify({"message": "Value added successfully", "rows_affected": rows_affected}), 201
    )
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route("/organizations/add", methods=["POST"])
@token_required
def add_organizations():
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Content-Type must be application/json"}), 415)
    cur = mysql.connection.cursor()
    info = request.get_json()
    organization_id = info["organization_id"]
    organization_details = info["organization_details"]
    cur.execute(
        """INSERT INTO organizations (organization_id, organization_details) VALUES (%s, %s)""",
        (organization_id, organization_details),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response = make_response(
        jsonify({"message": "Value added successfully", "rows_affected": rows_affected}), 201
    )
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route("/events/add", methods=["POST"])
@token_required
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
    response = make_response(
        jsonify({"message": "Value added successfully", "rows_affected": rows_affected}), 201
    )
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route("/memberships/add", methods=["POST"])
@token_required
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
        """INSERT INTO memberships (level_of_ability, hobby_code, member_id, organisation_id) VALUES (%s, %s, %s, %s)""",
        (level_of_ability, hobby_code, member_id, organisation_id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response = make_response(
        jsonify({"message": "Value added successfully", "rows_affected": rows_affected}), 201
    )
    response.headers['Content-Type'] = 'application/xml'
    return response
    
##PUT
@app.route("/members/update/<int:id>", methods=["PUT"])
@token_required
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
    response = make_response(
        jsonify({"message": "Value updated successfully", 
                 "rows_affected": rows_affected}),200,)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route("/hobbies_and_pasttime/update/<id>", methods=["PUT"])
@token_required
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
    response = make_response(
        jsonify({"message": "Value updated successfully", 
                 "rows_affected": rows_affected}),200,)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route("/organizations/update/<id>", methods=["PUT"])
@token_required
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
    response = make_response(
        jsonify({"message": "Value updated successfully", 
                 "rows_affected": rows_affected}),200,)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route("/events/update/<int:id>", methods=["PUT"])
@token_required
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
    response = make_response(
        jsonify({"message": "Value updated successfully", 
                 "rows_affected": rows_affected}),200,)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route("/memberships/update/<int:id>", methods=["PUT"])
@token_required
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
    response = make_response(
        jsonify({"message": "Value updated successfully", 
                 "rows_affected": rows_affected}),200,)
    response.headers['Content-Type'] = 'application/xml'
    return response

##DELETE
@app.route("/members/del/<int:id>", methods=["DELETE"])
@token_required
def delete_member(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM members where member_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response = make_response(
        jsonify({"message": "Value deleted successfully", 
                 "rows_affected": rows_affected}),200,)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route("/hobbies_and_pasttime/del/<id>", methods=["DELETE"])
@token_required
def delete_hobby(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM hobbies_and_pasttime where hobby_code = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response = make_response(
        jsonify({"message": "Value deleted successfully", 
                 "rows_affected": rows_affected}),200,)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route("/organizations/del/<id>", methods=["DELETE"])
@token_required
def delete_org(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM organizations where organization_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response = make_response(
        jsonify({"message": "Value deleted successfully", 
                 "rows_affected": rows_affected}),200,)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route("/events/del/<int:id>", methods=["DELETE"])
@token_required
def delete_event(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM events where event_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response = make_response(
        jsonify({"message": "Value deleted successfully", 
                 "rows_affected": rows_affected}),200,)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route("/memberships/del/<int:id>", methods=["DELETE"])
@token_required
def delete_memberships(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM memberships where membership_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    response = make_response(
        jsonify({"message": "Value deleted successfully", 
                 "rows_affected": rows_affected}),200,)
    response.headers['Content-Type'] = 'application/xml'
    return response

##URI
@app.route("/actors/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)

if __name__ == "__main__":
    app.run(debug=True)
