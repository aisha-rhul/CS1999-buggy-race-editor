from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
import os
import mimetypes

app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"

username = ""
password = ""

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
            cur.execute("SELECT * FROM Buggy WHERE id=?", buggy_id)
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
                if record[15] == "true":
                    total_cost += row[0]

            # Cost for insulated
            cur.execute("SELECT cost FROM Extras WHERE perk='insulated'")
            for row in cur.fetchall():
                if record[16] == "true":
                    total_cost += row[0]

            # Cost for antibiotic
            cur.execute("SELECT cost FROM Extras WHERE perk='antibiotic'")
            for row in cur.fetchall():
                if record[17] == "true":
                    total_cost += row[0]

            # Cost for banging
            cur.execute("SELECT cost FROM Extras WHERE perk='banging'")
            for row in cur.fetchall():
                if record[18] == "true":
                    total_cost += row[0]

            # Update cost in buggy table after calculation
            cur.execute("UPDATE Buggy set total_cost=? WHERE id=?", (total_cost, buggy_id))
            con.commit()
    except:
        print("Exception")
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
# login processing username, password are stored globally
# ------------------------------------------------------------
@app.route('/login', methods=['POST', 'GET'])
def login():
    global username
    global password

    username = str(request.form['u'])   # Gets username from user
    password = str(request.form['p'])   # Gets password from user

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
                if password == row[0]:
                    return render_template('index.html')    # successful login

        # reload login page for incorrect password
        return render_template('login.html')
    except:
        # report exception
        print("Exception - in login")
        return render_template('login.html')
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

            if aux_power_type != "None" and int(aux_power_units) == 0:
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
                if validate_integer(qty_tyres, 4) and (int(qty_tyres) >= int(qty_wheels)):
                    valid_tyres = True
                else:
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

            fireproof = str('fireproof' in request.form).lower()
            insulated = str('insulated' in request.form).lower()
            antibiotic = str('antibiotic' in request.form).lower()
            banging = str('banging' in request.form).lower()

            algo = request.form['algo'].lower()

            if valid_attacks and valid_aux_power and valid_hamster and valid_power and valid_tyres and valid_wheels and \
                    valid_power_type(power_type, power_units) and valid_power_type(aux_power_type, aux_power_units):
                all_valid = True

                action = request.form['action'].strip()
                print(action)

                # add/update record
                if action == "create":
                    print("in add record - about to add ...")

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
                        con.commit()
                        msg.clear()
                        msg.append("New record added to database")
                else:   # update table
                    print("in edit - about to update ...")
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
                        calc_cost()
                        msg.clear()
                        msg.append("Record successfully saved")
        except:
            con.rollback()
            msg.append("update_buggy: error in update operation")
        finally:
            if all_valid:
                con.close()
            flag_sel = {'pc': flag_color, 'sc': flag_color_secondary, 'pattern': flag_pattern}
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
                    }

            action = request.form['action'].strip()
            if action == "delete":
                delete_buggy(buggy_id)

            print(selection)
        except:
            print("list_buggies: error in update operation")
        finally:
            record = get_buggy_record(str(buggy_id))
            if action == "edit":
                return render_template("edit-record.html", title="Edit buggy", bid=buggy_id, sel=selection, buggy=record)
    else:
        all_records = get_records()
    all_records = get_records()
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
    record = get_buggy_record(1)
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
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Buggy WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))
    return jsonify(
        {k: v for k, v in dict(zip(
            [column[0] for column in cur.description], cur.fetchone())).items()
         if (v != "" and v is not None)
         }
    )


# ------------------------------------------------------------
# delete the buggy - deletes a selected record
# ------------------------------------------------------------
def delete_buggy(buggy_id):
    try:
        msg = "deleting buggy"
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Buggy WHERE id = ?", (buggy_id,))
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
