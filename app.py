from flask import Flask, render_template, request, jsonify, redirect
import sqlite3 as sql
import mimetypes
from passlib.hash import bcrypt
import random
import string
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"

username = "guest"
password = ""
selected_buggy = 1


# ------------------------------------------------------------
# validate integer - num:number, lower:lower bound check
# ------------------------------------------------------------
def validate_integer(num, lower):
    try:
        val = int(num)
        if val >= lower:
            return True
        else:
            return False
    except ValueError:
        return False


# ------------------------------------------------------------
# get cost of buggy based on the buggy ID
# ------------------------------------------------------------
def get_buggy_cost(buggy_id):
    try:
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()

            cur.execute("SELECT total_cost FROM Buggy WHERE id=?", (buggy_id,))
            for row in cur.fetchall():
                cost = int(row[0])
        return cost
    except:
        print("Could not locate the record in the database")
    finally:
        con.close()


# ------------------------------------------------------------
# get a single buggy record based on the buggy ID
# ------------------------------------------------------------
def get_buggy_record(buggy_id):
    try:
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()

            # Get record of buggy
            record = []
            cur.execute("SELECT * FROM Buggy WHERE id=?", (buggy_id,))
            for row in cur.fetchall():
                record = row
        return record
    except:
        print("Could not locate the record in the database")
    finally:
        con.close()


# ------------------------------------------------------------
# get the buggy_id of the last buggy
# ------------------------------------------------------------
def get_last_buggy_id():
    try:
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()
            # Get buggy id of the last record
            cur.execute("SELECT id FROM Buggy ORDER BY id DESC LIMIT 1")
            for row in cur.fetchall():
                buggy_id = row[0]
            buggy_id = int(buggy_id)
            return buggy_id
    except:
        return 0
    finally:
        con.close()


# ------------------------------------------------------------
# Validate consumable power types
# ------------------------------------------------------------
def valid_power_type(power_type, power_units):
    try:
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()

            power_type = str(power_type)
            cur.execute("SELECT consumable FROM Motive_Power WHERE power_type=?", (power_type,))

            for row in cur.fetchall():
                consumable = str(row[0])

            power_units = int(power_units)

            if consumable == 'false' and power_units > 1:
                return False
            return True
    except:
        return 0
    finally:
        con.close()


# ------------------------------------------------------------
# calculate cost of the buggy
# ------------------------------------------------------------
def calc_cost():
    try:
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()

            # Get buggy id of the last record
            cur.execute("SELECT id FROM Buggy ORDER BY id DESC LIMIT 1")
            for row in cur.fetchall():
                buggy_id = row[0]
            buggy_id = str(buggy_id)

            # Get record of last buggy
            record = []
            cur.execute("SELECT * FROM Buggy WHERE id=?", (buggy_id,))
            for row in cur.fetchall():
                record = row

            total_cost = 0

            # Cost for primary power type and power units
            cur.execute("SELECT cost FROM Motive_Power WHERE power_type=?", (record[2],))
            #Alternative method
            #cur.execute("SELECT cost FROM 'Motive Power' WHERE power_type=:pt", {"pt": record[2]})
            for row in cur.fetchall():
                total_cost += row[0] * record[3]

            # Cost for aux power type and aux power units
            cur.execute("SELECT cost FROM Motive_Power WHERE power_type=?", (record[4],))
            for row in cur.fetchall():
                total_cost += row[0] * record[5]

            # Cost for hamster booster
            cur.execute("SELECT cost FROM Extras WHERE perk='hamster_booster'")
            for row in cur.fetchall():
                total_cost += row[0] * record[6]

            # Cost for tyre type
            cur.execute("SELECT cost FROM Tyre WHERE type=?", (record[10],))
            for row in cur.fetchall():
                total_cost += row[0] * record[11]

            # Cost for armour
            cur.execute("SELECT cost FROM Armour WHERE type=?", (record[12],))
            for row in cur.fetchall():
                if record[1] == 4:
                    total_cost += row[0]
                else:
                    extra_wheels = record[1] - 4
                    total_cost += row[0] * (1 + (extra_wheels/10))

            # Cost for offensive capability
            cur.execute("SELECT cost FROM Offensive_Capability WHERE type=?", (record[13],))
            for row in cur.fetchall():
                total_cost += row[0] * record[14]

            # Cost for fireproof
            cur.execute("SELECT cost FROM Extras WHERE perk='fireproof'")
            for row in cur.fetchall():
                if record[15] == 1:
                    total_cost += row[0]

            # Cost for insulated
            cur.execute("SELECT cost FROM Extras WHERE perk='insulated'")
            for row in cur.fetchall():
                if record[16] == 1:
                    total_cost += row[0]

            # Cost for antibiotic
            cur.execute("SELECT cost FROM Extras WHERE perk='antibiotic'")
            for row in cur.fetchall():
                if record[17] == 1:
                    total_cost += row[0]

            # Cost for banging
            cur.execute("SELECT cost FROM Extras WHERE perk='banging'")
            for row in cur.fetchall():
                if record[18] == 1:
                    total_cost += row[0]

            # Update cost in buggy table after calculation
            cur.execute("UPDATE Buggy set total_cost=? WHERE id=?", (total_cost, buggy_id))
            con.commit()
    except:
        print("Exception")
    finally:
        con.close()


# ------------------------------------------------------------
# return buggy records owned by a user
# ------------------------------------------------------------
def get_user_buggies():
    try:
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()

        # Get privilege level of user from database table User
        cur.execute("SELECT privilege_level FROM User WHERE username=?", (username,))
        for row in cur.fetchall():
            privilege_level = row[0]

        if privilege_level == "admin":
            return get_records()        # fetch all buggy records
        else:
            # Get all the buggy id's owned by a user
            # select Buggy.* from Buggy left join Ownership on  Buggy.id=Ownership.buggy_id where username="username"
            cur.execute("SELECT Buggy.* FROM Buggy LEFT JOIN Ownership ON Buggy.id=Ownership.buggy_id \
                        WHERE Ownership.username=?", (username,))
            records = cur.fetchall()
            return records

    except:
        print("Exception: in database operation")
    finally:
        con.close()


# ------------------------------------------------------------
# the login page
# ------------------------------------------------------------
@app.route('/')
def home():
    mimetypes.add_type("text/css", ".css", True)
    return render_template('login.html', server_url=BUGGY_RACE_SERVER_URL)


# ------------------------------------------------------------
# the index page
# ------------------------------------------------------------
@app.route('/index')
def index():
    mimetypes.add_type("text/css", ".css", True)
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

# ------------------------------------------------------------
# the register page
# ------------------------------------------------------------
@app.route('/register')
def register_page():
    mimetypes.add_type("text/css", ".css", True)
    return render_template('register.html', server_url=BUGGY_RACE_SERVER_URL)


# ------------------------------------------------------------
# the forgot password page
# ------------------------------------------------------------
@app.route('/forgot-pass')
def forgot_password_page():
    mimetypes.add_type("text/css", ".css", True)
    return render_template('forgot-pass.html', server_url=BUGGY_RACE_SERVER_URL)


# ------------------------------------------------------------
# the change password page
# ------------------------------------------------------------
@app.route('/change-pass')
def change_password_page():
    mimetypes.add_type("text/css", ".css", True)
    return render_template('change-pass.html', server_url=BUGGY_RACE_SERVER_URL)


# ------------------------------------------------------------
# login processing username, password are stored globally
# ------------------------------------------------------------
@app.route('/login', methods=['POST', 'GET'])
def login():
    global username
    global password

    username = str(request.form['u'])   # Gets username from user
    password = str(request.form['p'])   # Gets password from user

    pwd_hash = bcrypt.hash(password)    # Generate password hash using bcrypt

    try:
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()

        # Get privilege level of user from database table User
        cur.execute("SELECT privilege_level FROM User WHERE username=?", (username,))
        for row in cur.fetchall():
            privilege_level = row[0]

        # Get password from database table User
        cur.execute("SELECT password FROM User WHERE username=?", (username,))

        # Check privilege level of user and gives appropriate response for each case
        if privilege_level == "admin" or privilege_level == "user":
            for row in cur.fetchall():
                if bcrypt.verify(password, row[0]):
                    return render_template('index.html')    # successful login

        # reload login page for incorrect password
        return render_template('login.html')
    except:
        # report exception
        print("Exception - in login")
        return render_template('login.html')
    finally:
        con.close()


# ---------------------------------------------------------------------
# registers a user and adds their credentials to database table User
# ---------------------------------------------------------------------
@app.route('/register', methods=['POST', 'GET'])
def register():
    new_username = str(request.form['u'])   # Gets username from user
    new_password = str(request.form['p'])   # Gets password from user
    new_email = str(request.form['e'])      # Gets email from user

    pwd_hash = bcrypt.hash(new_password)    # Generate password hash using bcrypt

    try:
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()

        # Insert user credentials to database table User
        cur.execute(''' INSERT INTO User (username, password, privilege_level, email) VALUES (?, ?, ?, ?)''',
                    (new_username, pwd_hash, "user", new_email))

        # Get password from database table User
        cur.execute("SELECT password FROM User WHERE username=?", (username,))
        con.commit()

        # loads login page after successfully registering a user
        return render_template('login.html')
    except:
        # report exception
        print("Exception - in register")
        con.rollback()
        return render_template('register.html')
    finally:
        con.close()


# ------------------------------------------------------------
# sends an email with a new password to the user
# ------------------------------------------------------------
@app.route('/forgot-pass', methods=['POST', 'GET'])
def send_email():
    name = str(request.form['u'])  # Get username from user

    try:
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()

        # Get user email from database table User
        cur.execute("SELECT email FROM User WHERE username=?", (name,))
        for row in cur.fetchall():
            email = row[0]

        # Generate random password of length 10
        choice = string.ascii_letters + string.digits + string.punctuation
        new_password = (''.join((random.choice(choice) for i in range(10))))

        # Generate password hash using bcrypt for the random password
        pwd_hash = bcrypt.hash(new_password)

        # Set up the SMTP server
        s = smtplib.SMTP(host="smtp.office365.com", port=587)
        s.starttls()
        s.login("aisha.buggy@outlook.com", "%Buggy123%")

        # Set Template object of the contents of the file specified by the filename
        with open('message.txt', 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
        message_template = Template(template_file_content)

        msg = MIMEMultipart()   # Create message
        message = message_template.substitute(USERNAME=name, NEW_PASSWORD=new_password)

        msg['From'] = "aisha.buggy@outlook.com"   # Sender email address
        msg['To'] = email  # Recipient email address
        msg['Subject'] = "Buggy Admin - Your new password"  # Subject of email

        msg.attach(MIMEText(message, 'plain'))
        s.send_message(msg)
        del msg
        s.quit()

        # Update user's password in the database table User with the new random password hash
        cur.execute("UPDATE User set password=? WHERE username=?", (pwd_hash, name))
        con.commit()

        # Load login page after successfully sending the user an email with their new password
        return render_template('login.html')
    except:
        # Report exception
        print("Exception - in forgot-pass")
        con.rollback()
        return render_template('forgot-pass.html')
    finally:
        con.close()


# ------------------------------------------------------------
# change a user's password
# ------------------------------------------------------------
@app.route('/change-pass', methods=['POST', 'GET'])
def change_pass():
    global username
    global password

    old_password = str(request.form['op'])   # Get old password from user
    first_new_pwd = str(request.form['np1'])  # Get first entry of new password from user
    second_new_pwd = str(request.form['np2'])  # Get second entry of new password from user

    if first_new_pwd == second_new_pwd and password == old_password:
        pwd_hash = bcrypt.hash(first_new_pwd)    # Generate hash of new password using bcrypt
    else:
        return render_template('change-pass.html')

    try:
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()

        # Update user's password with hash of new password in database table User
        cur.execute("UPDATE User set password=? WHERE username=?", (pwd_hash, username))
        con.commit()

        # load login page after successfully updating password
        return render_template('login.html')
    except:
        # report exception
        print("Exception - in change password")
        return render_template('change-pass.html')
    finally:
        con.close()


# ------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
# ------------------------------------------------------------
@app.route('/new', methods=['POST', 'GET'])
def create_buggy():
    mimetypes.add_type("text/css", ".css", True)
    msg = []
    buggy_id = DEFAULT_BUGGY_ID
    valid_wheels = True
    valid_power = True
    valid_aux_power = True
    valid_hamster = True
    valid_tyres = True
    valid_attacks = True
    all_valid = False

    msg.append("Invalid data input, record not written to database")

    if request.method == 'GET':
        buggy_id = get_last_buggy_id() + 1
        return render_template("buggy-form.html", buggy=buggy_id, title="Make buggy")
    elif request.method == 'POST':
        try:
            qty_wheels = request.form['qty_wheels'].strip()
            valid_wheels = validate_integer(qty_wheels, 4)
            if not valid_wheels or int(qty_wheels) % 2 != 0:
                msg.append("Wheels - The number of wheels must be an even integer greater or equal to 4")
                valid_wheels = False

            power_type = (request.form['power_type']).lower()

            power_units = request.form['power_units'].strip()
            valid_power = validate_integer(power_units, 1)
            if not valid_power:
                msg.append("Power unit - Value must be an integer greater than or equal to 1")

            if not valid_power_type(power_type, power_units):
                msg.append("Power type/unit - Consumable primary power type can only have one power unit")

            aux_power_type = request.form['aux_power_type'].lower()

            aux_power_units = request.form['aux_power_units'].strip()
            valid_aux_power = validate_integer(aux_power_units, 0)
            if not valid_aux_power:
                msg.append("Aux Power - Value must be an integer greater than or equal to 0")

            if aux_power_type != "none" and int(aux_power_units) == 0:
                msg.append("Aux Power Units - Cannot be zero when aux power type is chosen")
                valid_aux_power = False

            if not valid_power_type(aux_power_type, aux_power_units):
                msg.append("Power type/unit - Consumable auxiliary power type can only have one auxiliary power unit")

            hamster_booster = request.form['hamster_booster'].strip()
            valid_hamster = validate_integer(hamster_booster, 0)
            if not valid_hamster:
                msg.append("Hamster Booster - Value must be an integer greater than or equal to 0")

            if (power_type != "hamster" and aux_power_type != "hamster") and int(hamster_booster) > 0:
                msg.append("Hamster Booster - Can only be set if power type is hamster")
                valid_hamster = False

            if aux_power_type == "none" and int(aux_power_units) > 0:
                msg.append("Auxiliary power - Cannot be greater than 0 if no auxiliary power is chosen")
                valid_aux_power = False

            flag_color = request.form['flag_color']
            flag_pattern = request.form['flag_pattern'].lower()
            flag_color_secondary = request.form['flag_color_secondary']
            tyres = request.form['tyres'].lower()

            qty_tyres = request.form['qty_tyres'].strip()
            if validate_integer(qty_wheels, 4):
                if validate_integer(int(qty_tyres), 4) and (int(qty_tyres) >= int(qty_wheels)):
                    valid_tyres = True
                else:
                    valid_tyres = False
                    msg.append("Tyres - Number of Tyres must be an integer greater than or equal to number of wheels")

            armour = request.form['armour'].lower()
            attack = request.form['attack'].lower()
            qty_attacks = request.form['qty_attacks'].strip()
            valid_attacks = validate_integer(qty_attacks, 0)
            if not valid_attacks:
                msg.append("Attacks - Value must be an integer greater than or equal to 0")

            if attack == "none" and int(qty_attacks) > 0:
                msg.append("Attack quantity - Cannot be greater than zero when no attack is chosen")
                valid_attacks = False

            if attack != "none" and int(qty_attacks) == 0:
                msg.append("Attack quantity - Cannot be zero when attack is chosen")
                valid_attacks = False

            fireproof = 'fireproof' in request.form
            insulated = 'insulated' in request.form
            antibiotic = 'antibiotic' in request.form
            banging = 'banging' in request.form

            algo = request.form['algo'].lower()

            if valid_attacks and valid_aux_power and valid_hamster and valid_power and valid_tyres and valid_wheels and \
                    valid_power_type(power_type, power_units) and valid_power_type(aux_power_type, aux_power_units):
                all_valid = True

                action = request.form['action'].strip()

                    # add/update record
                if action == "create":
                    buggy_id = get_last_buggy_id() + 1
                    # insert record
                    with sql.connect(DATABASE_FILE) as con:
                        cur = con.cursor()
                        cur.execute(''' INSERT INTO Buggy (qty_wheels, power_type, power_units, aux_power_type, 
                            aux_power_units, hamster_booster, flag_color, flag_pattern, flag_color_secondary, tyres,
                            qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo) 
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''',
                                    (int(qty_wheels), power_type, int(power_units), aux_power_type,
                                     int(aux_power_units), int(hamster_booster), flag_color, flag_pattern,
                                     flag_color_secondary, tyres, int(qty_tyres), armour, attack, int(qty_attacks),
                                     fireproof, insulated, antibiotic, banging, algo))
                        cur.execute(''' INSERT INTO Ownership (buggy_id, username) VALUES (?, ?)''',
                                    (buggy_id, username))
                        con.commit()
                        calc_cost()
                        msg.clear()
                        msg.append("New record added to database")
                else:   # update table
                    buggy_id = request.form['bid'].strip()     # get the selected buggy_id
                    # buggy_id = 2
                    with sql.connect(DATABASE_FILE) as con:
                        cur = con.cursor()
                        cur.execute("UPDATE Buggy set qty_wheels=? WHERE id=?", (int(qty_wheels), buggy_id))
                        cur.execute("UPDATE Buggy set power_type=? WHERE id=?", (power_type, buggy_id))
                        cur.execute("UPDATE Buggy set power_units=? WHERE id=?", (int(power_units), buggy_id))
                        cur.execute("UPDATE Buggy set aux_power_type=? WHERE id=?", (aux_power_type, buggy_id))
                        cur.execute("UPDATE Buggy set aux_power_units=? WHERE id=?", (int(aux_power_units), buggy_id))
                        cur.execute("UPDATE Buggy set hamster_booster=? WHERE id=?", (int(hamster_booster), buggy_id))
                        cur.execute("UPDATE Buggy set flag_color=? WHERE id=?", (flag_color, buggy_id))
                        cur.execute("UPDATE Buggy set flag_pattern=? WHERE id=?", (flag_pattern, buggy_id))
                        cur.execute("UPDATE Buggy set flag_color_secondary=? WHERE id=?", (flag_color_secondary, buggy_id))
                        cur.execute("UPDATE Buggy set tyres=? WHERE id=?", (tyres, buggy_id))
                        cur.execute("UPDATE Buggy set qty_tyres=? WHERE id=?", (int(qty_tyres), buggy_id))
                        cur.execute("UPDATE Buggy set armour=? WHERE id=?", (armour, buggy_id))
                        cur.execute("UPDATE Buggy set attack=? WHERE id=?", (attack, buggy_id))
                        cur.execute("UPDATE Buggy set qty_attacks=? WHERE id=?", (int(qty_attacks), buggy_id))
                        cur.execute("UPDATE Buggy set fireproof=? WHERE id=?", (fireproof, buggy_id))
                        cur.execute("UPDATE Buggy set insulated=? WHERE id=?", (insulated, buggy_id))
                        cur.execute("UPDATE Buggy set antibiotic=? WHERE id=?", (antibiotic, buggy_id))
                        cur.execute("UPDATE Buggy set banging=? WHERE id=?", (banging, buggy_id))
                        cur.execute("UPDATE Buggy set algo=? WHERE id=?", (algo, buggy_id))
                        con.commit()
                        msg.clear()
                        msg.append("Record successfully saved")
        except:
            con.rollback()
            msg.append("update_buggy: error in update operation")
        finally:
            if all_valid:
                calc_cost()
                con.close()
                flag_sel = {'pc': flag_color, 'sc': flag_color_secondary, 'pattern': flag_pattern}
            else:
                flag_sel = {'pc': "#ffffff", 'sc': "#ffffff", 'pattern': flag_pattern}

            return render_template("updated.html", msg=msg, flag_selection=flag_sel)


# ------------------------------------------------------------
# edit record selected by user
# ------------------------------------------------------------
@app.route('/edit-record', methods=['POST', 'GET'])
def edit_record():
    if request.method == 'POST':
        try:
            print("post received in edit record")
        except:
            print("exception in edit_record")
        finally:
            print("leaving edit_record")


# ------------------------------------------------------------
# receive selected buggy from user
# ------------------------------------------------------------
@app.route('/list', methods=['POST', 'GET'])
def list_buggies():
    global selected_buggy
    if request.method == 'POST':
        try:
            selection = []
            buggy_id = request.form['selected_id']

            selection = {
                    'sel_primary_power': (request.form['sel_primary_power']).strip(),
                    'sel_aux_power': (request.form['sel_aux_power']).strip(),
                    'sel_flag_pattern': (request.form['sel_flag_pattern']).strip(),
                    'sel_tyre_type': (request.form['sel_tyre_type']).strip(),
                    'sel_armour': (request.form['sel_armour']).strip(),
                    'sel_attack': (request.form['sel_attack']).strip(),
                    'sel_fireproof': (request.form['sel_fireproof']).strip(),
                    'sel_insulated': (request.form['sel_insulated']).strip(),
                    'sel_antibiotic': (request.form['sel_antibiotic']).strip(),
                    'sel_banging': (request.form['sel_banging']).strip(),
                    'sel_algo': (request.form['sel_algo']).strip(),
                    'sel_cost': get_buggy_cost(buggy_id),
                    }

            action = request.form['action'].strip()
            if action == "delete":
                delete_buggy(buggy_id)
            if action == "json":
                selected_buggy = int(buggy_id)
                return redirect("./json", code=302)

            print(selection)
        except:
            print("list_buggies: error in update operation")
        finally:
            record = get_buggy_record(str(buggy_id))
            if action == "edit":
                return render_template("edit-record.html", title="Edit buggy", bid=buggy_id, sel=selection, buggy=record)
    else:
        all_records = get_records()
    all_records = get_user_buggies()
    return render_template("list.html", buggies=all_records)


# ------------------------------------------------------------
# a page for listing all buggies in a database
# ------------------------------------------------------------
@app.route('/list')
def display_buggies():
    records = get_records()
    return render_template("list.html", title="Make buggy", buggy=records)


# ------------------------------------------------------------
# fetch all records from the database
# ------------------------------------------------------------
def get_records():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Buggy")
    records = cur.fetchall()
    return records


# ------------------------------------------------------------
# a page for displaying the buggy
# ------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    mimetypes.add_type("text/css", ".css", True)
    record = get_buggy_record(DEFAULT_BUGGY_ID)
    return render_template("buggy.html", buggy=record)


# ------------------------------------------------------------
# a page for displaying the buggy
# SAME ROUTE AS create_buggy IS THIS NECESSARY???
# ------------------------------------------------------------
@app.route('/new')
def make_buggy():
    mimetypes.add_type("text/css", ".css", True)
    return render_template("buggy-form.html", title="Make buggy")


# ------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping directly into the
#   database
# ------------------------------------------------------------
@app.route('/json')
def summary():
    global selected_buggy

    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT id, qty_wheels, power_type, power_units, aux_power_type, aux_power_units, hamster_booster,"
                " flag_color, flag_pattern, flag_color_secondary, tyres, qty_tyres, armour, attack, qty_attacks, "
                "fireproof, insulated, antibiotic, banging, algo FROM Buggy WHERE id=?", (selected_buggy,))
    return jsonify(
        {k: v for k, v in dict(zip(
            [column[0] for column in cur.description], cur.fetchone())).items()
         if (v != "" and v is not None)
         }
    )


# ------------------------------------------------------------
# loads login page after logging out
# ------------------------------------------------------------
@app.route('/logout')
def logout():
    mimetypes.add_type("text/css", ".css", True)
    return render_template("login.html")


# ------------------------------------------------------------
# delete the buggy - deletes a selected record
# ------------------------------------------------------------
def delete_buggy(buggy_id):
    try:
        msg = "deleting buggy"
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Buggy WHERE id = ?", (buggy_id,))
            cur.execute("DELETE FROM Ownership WHERE buggy_id = ?", (buggy_id,))
            con.commit()
            msg = "Buggy deleted"
    except:
        con.rollback()
        msg = "error in delete operation"
        return msg
    finally:
        con.close()
        return msg


if __name__ == '__main__':
    mimetypes.add_type("text/css", ".css", True)
    app.run(debug=True, host="0.0.0.0")
