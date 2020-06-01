from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
import os
import mimetypes

app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"


# ------------------------------------------------------------
# validate integer: num=number, lower=lower bound check
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
# the index page
# ------------------------------------------------------------
@app.route('/')
def home():
    mimetypes.add_type("text/css", ".css", True)
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)


# ------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
# ------------------------------------------------------------
@app.route('/new', methods=['POST', 'GET'])
def create_buggy():
    mimetypes.add_type("text/css", ".css", True)
    msg = []
    valid_wheels = False
    valid_power = False
    valid_aux_power = False
    valid_hamster = False
    valid_tyres = False
    valid_attacks = False
    all_valid = False

    msg.append("Invalid data input, record not written to database")

    if request.method == 'GET':
        return render_template("buggy-form.html")
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

            aux_power_type = request.form['aux_power_type'].lower()

            aux_power_units = request.form['aux_power_units'].strip()
            valid_aux_power = validate_integer(aux_power_units, 0)
            if not valid_aux_power:
                msg.append("Aux Power - Value must be an integer greater than or equal to 0")

            hamster_booster = request.form['hamster_booster'].strip()
            valid_hamster = validate_integer(hamster_booster, 0)
            if not valid_hamster:
                msg.append("Hamster Booster - Value must be an integer greater than or equal to 0")

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

            fireproof = 'fireproof' in request.form
            insulated = 'insulated' in request.form
            antibiotic = 'antibiotic' in request.form
            banging = 'banging' in request.form

            algo = request.form['algo'].lower()

            if valid_attacks and valid_aux_power and valid_hamster and valid_power and valid_tyres and valid_wheels:
                all_valid = True
                with sql.connect(DATABASE_FILE) as con:
                    cur = con.cursor()
                    cur.execute("UPDATE Buggy set qty_wheels=? WHERE id=?", (int(qty_wheels), DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set power_type=? WHERE id=?", (power_type, DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set power_units=? WHERE id=?", (int(power_units), DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set aux_power_type=? WHERE id=?", (aux_power_type, DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set aux_power_units=? WHERE id=?", (int(aux_power_units), DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set hamster_booster=? WHERE id=?", (int(hamster_booster), DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set flag_color=? WHERE id=?", (flag_color, DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set flag_pattern=? WHERE id=?", (flag_pattern, DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set flag_color_secondary=? WHERE id=?", (flag_color_secondary, DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set tyres=? WHERE id=?", (tyres, DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set qty_tyres=? WHERE id=?", (int(qty_tyres), DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set armour=? WHERE id=?", (armour, DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set attack=? WHERE id=?", (attack, DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set qty_attacks=? WHERE id=?", (int(qty_attacks), DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set fireproof=? WHERE id=?", (fireproof, DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set insulated=? WHERE id=?", (insulated, DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set antibiotic=? WHERE id=?", (antibiotic, DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set banging=? WHERE id=?", (banging, DEFAULT_BUGGY_ID))
                    cur.execute("UPDATE Buggy set algo=? WHERE id=?", (algo, DEFAULT_BUGGY_ID))
                    con.commit()
                    msg.clear()
                    msg.append("Record successfully saved")
        except:
            con.rollback()
            msg.append("error in update operation")
        finally:
            if all_valid:
                con.close()
            return render_template("updated.html", msg=msg)


# ------------------------------------------------------------
# a page for displaying the buggy
# ------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    mimetypes.add_type("text/css", ".css", True)

    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Buggy")
    record = cur.fetchone();
    return render_template("buggy.html", buggy=record)


# ------------------------------------------------------------
# a page for displaying the buggy
# ------------------------------------------------------------
@app.route('/new')
def edit_buggy():
    mimetypes.add_type("text/css", ".css", True)
    return render_template("buggy-form.html")


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
# delete the buggy
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
# ------------------------------------------------------------
@app.route('/delete', methods=['POST'])
def delete_buggy():
    try:
        msg = "deleting buggy"
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Buggy")
            con.commit()
            msg = "Buggy deleted"
    except:
        con.rollback()
        msg = "error in delete operation"
    finally:
        con.close()
        return render_template("updated.html", msg=msg)


if __name__ == '__main__':
    mimetypes.add_type("text/css", ".css", True)
    app.run(debug=True, host="0.0.0.0")
