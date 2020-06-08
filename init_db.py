import sqlite3

DATABASE_FILE = "database.db"


# important:
# -------------------------------------------------------------
# This script initialises your database for you using SQLite,
# just to get you started... there are better ways to express
# the data you're going to need... especially outside SQLite.
# For example... maybe flag_pattern should be an ENUM (which
# is available in most other SQL databases), or a foreign key
# to a pattern table?
#
# Also... the name of the database (here, in SQLite, it's a
# filename) appears in more than one place in the project.
# That doesn't feel right, does it?
#
# -------------------------------------------------------------


con = sqlite3.connect(DATABASE_FILE)
print("- Opened database successfully in file \"{}\"".format(DATABASE_FILE))

# using Python's triple-quote for multi-line strings:

con.execute("""
  CREATE TABLE IF NOT EXISTS Buggy (
    id                      INTEGER DEFAULT 1,
    qty_wheels              INTEGER DEFAULT 4,
    power_type	            VARCHAR ( 20 ) DEFAULT "petrol",
    power_units             INTEGER DEFAULT 1,
    aux_power_type	        VARCHAR ( 20 ) DEFAULT "none",
    aux_power_units         INTEGER DEFAULT 0,
    hamster_booster         INTEGER DEFAULT 0,
    flag_color              VARCHAR(20) DEFAULT "#ffffff",
    flag_pattern            VARCHAR(20) DEFAULT 'plain',
    flag_color_secondary    VARCHAR ( 20 ) DEFAULT "#000000",
    tyres                   VARCHAR ( 20 )  DEFAULT 'knobbly',
    qty_tyres               INTEGER DEFAULT 4,
    armour	                VARCHAR ( 20 ) DEFAULT "none",
    attack	                VARCHAR ( 20 ) DEFAULT "none",
    qty_attacks	            INTEGER DEFAULT 0,
    fireproof	            BOOLEAN DEFAULT 0,
    insulated	            BOOLEAN DEFAULT 0,
    antibiotic	            BOOLEAN DEFAULT 0,
    banging	                BOOLEAN DEFAULT 0,
    algo	                VARCHAR ( 20 ) DEFAULT "steady",
    total_cost	            INTEGER DEFAULT 64,
    PRIMARY KEY('id')
  )
""")

con.execute("""
  CREATE TABLE IF NOT EXISTS Armour (
    type	                VARCHAR ( 20 ),
    cost	                INTEGER,
    kg	                    INTEGER,
    PRIMARY KEY('type')
  )
""")

con.execute("""
  CREATE TABLE IF NOT EXISTS Extras (
    perk                  VARCHAR ( 20 ),
    cost                  INTEGER,
    PRIMARY KEY('perk')
  )
""")


con.execute("""
  CREATE TABLE IF NOT EXISTS Motive_Power (
    power_type	            VARCHAR ( 20 ),
    cost	                INTEGER,
    kg	                    INTEGER,
    consumable	            BOOLEAN,
    PRIMARY KEY('power_type')
  )
""")

con.execute("""
  CREATE TABLE IF NOT EXISTS Offensive_Capability (
    type	                VARCHAR ( 20 ),
    cost	                INTEGER,
    kg	                    INTEGER,
    PRIMARY KEY('type')
  )
""")

con.execute("""
  CREATE TABLE IF NOT EXISTS Ownership (
    buggy_id	            INTEGER,
    username	            VARCHAR ( 255 ),
    PRIMARY KEY('buggy_id')
  )
""")

con.execute("""
  CREATE TABLE IF NOT EXISTS Tyre (
    type	                VARCHAR ( 20 ),
    cost	                INTEGER,
    kg	                    INTEGER,
    PRIMARY KEY('type')
  )
""")

con.execute("""
  CREATE TABLE IF NOT EXISTS User (
    username	            VARCHAR ( 255 ),
    password	            VARCHAR ( 255 ),
    privilege_level	        VARCHAR ( 10 ),
    email	                VARCHAR ( 255 ),
    PRIMARY KEY('username')
  )
""")

print("- Table \"Buggy\" exists OK")
print("- Table \"Armour\" exists OK")
print("- Table \"Extras\" exists OK")
print("- Table \"Motive_Power\" exists OK")
print("- Table \"Offensive_Capability\" exists OK")
print("- Table \"Ownership\" exists OK")
print("- Table \"Tyre\" exists OK")
print("- Table \"User\" exists OK")

cur = con.cursor()

# Insert default record into Buggy table
cur.execute("SELECT * FROM Buggy LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
    cur.execute("INSERT INTO Buggy (qty_wheels) VALUES (4)")
    con.commit()
    print("- Added one 4-wheeled buggy")
else:
    print("- Found a buggy in the database, nice")

print("")

# Armour table
cur.execute("SELECT * FROM Armour LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
    cur.execute("INSERT INTO Armour (type, cost, kg) VALUES ('none', 0, 0)")
    cur.execute("INSERT INTO Armour (type, cost, kg) VALUES ('wood', 40, 100)")
    cur.execute("INSERT INTO Armour (type, cost, kg) VALUES ('aluminium', 200, 50)")
    cur.execute("INSERT INTO Armour (type, cost, kg) VALUES ('thinsteel', 100, 200)")
    cur.execute("INSERT INTO Armour (type, cost, kg) VALUES ('thicksteel', 200, 400)")
    cur.execute("INSERT INTO Armour (type, cost, kg) VALUES ('titanium', 290, 300)")
    con.commit()
    print("UPDATED Armour TABLE")


# Extras Table
cur.execute("SELECT * FROM Extras LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
    cur.execute("INSERT INTO Extras (perk, cost) VALUES ('hamster_booster', 5)")
    cur.execute("INSERT INTO Extras (perk, cost) VALUES ('fireproof', 70)")
    cur.execute("INSERT INTO Extras (perk, cost) VALUES ('insulated', 100)")
    cur.execute("INSERT INTO Extras (perk, cost) VALUES ('antibiotic', 90)")
    cur.execute("INSERT INTO Extras (perk, cost) VALUES ('banging', 42)")
    con.commit()
    print("UPDATED Extras TABLE")

# Motive_Power Table
cur.execute("SELECT * FROM Motive_Power LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
    cur.execute("INSERT INTO Motive_Power (power_type, cost, kg, consumable) VALUES ('petrol', 4, 2, 'true')")
    cur.execute("INSERT INTO Motive_Power (power_type, cost, kg, consumable) VALUES ('fusion', 400, 100, 'false')")
    cur.execute("INSERT INTO Motive_Power (power_type, cost, kg, consumable) VALUES ('steam', 3, 4, 'true')")
    cur.execute("INSERT INTO Motive_Power (power_type, cost, kg, consumable) VALUES ('bio', 5, 2, 'true')")
    cur.execute("INSERT INTO Motive_Power (power_type, cost, kg, consumable) VALUES ('electric', 20, 20, 'true')")
    cur.execute("INSERT INTO Motive_Power (power_type, cost, kg, consumable) VALUES ('rocket', 16, 2, 'true')")
    cur.execute("INSERT INTO Motive_Power (power_type, cost, kg, consumable) VALUES ('hamster', 3, 1, 'true')")
    cur.execute("INSERT INTO Motive_Power (power_type, cost, kg, consumable) VALUES ('thermo', 300, 100, 'false')")
    cur.execute("INSERT INTO Motive_Power (power_type, cost, kg, consumable) VALUES ('solar', 40, 30, 'false')")
    cur.execute("INSERT INTO Motive_Power (power_type, cost, kg, consumable) VALUES ('wind', 20, 30, 'false')")
    cur.execute("INSERT INTO Motive_Power (power_type, cost, kg, consumable) VALUES ('none', 0, 0, 'true')")
    con.commit()
    print("UPDATED Motive_Power TABLE")

# Offensive_Capability Table
cur.execute("SELECT * FROM Offensive_Capability LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
    cur.execute("INSERT INTO Offensive_Capability (type, cost, kg) VALUES ('none', 0, 0)")
    cur.execute("INSERT INTO Offensive_Capability (type, cost, kg) VALUES ('spike', 5, 10)")
    cur.execute("INSERT INTO Offensive_Capability (type, cost, kg) VALUES ('flame', 20, 12)")
    cur.execute("INSERT INTO Offensive_Capability (type, cost, kg) VALUES ('charge', 28, 25)")
    cur.execute("INSERT INTO Offensive_Capability (type, cost, kg) VALUES ('biohazard', 30, 10)")
    con.commit()
    print("UPDATED Offensive_Capability TABLE")

# Ownership Table
cur.execute("SELECT * FROM Ownership LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
    cur.execute("INSERT INTO Ownership (buggy_id, username) VALUES (1, 'admin')")
    con.commit()
    print("UPDATED Ownership TABLE")

# Tyre Table
cur.execute("SELECT * FROM Tyre LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
    cur.execute("INSERT INTO Tyre (type, cost, kg) VALUES ('knobbly', 15, 20)")
    cur.execute("INSERT INTO Tyre (type, cost, kg) VALUES ('slick', 10, 14)")
    cur.execute("INSERT INTO Tyre (type, cost, kg) VALUES ('steelband', 20, 28)")
    cur.execute("INSERT INTO Tyre (type, cost, kg) VALUES ('reactive', 40, 20)")
    cur.execute("INSERT INTO Tyre (type, cost, kg) VALUES ('maglev', 50, 30)")
    con.commit()
    print("UPDATED Tyre TABLE")

# User Table
cur.execute("SELECT * FROM User LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
    cur.execute("INSERT INTO user (username, password, privilege_level, email) VALUES "
                "('admin', '$2b$12$WTg9Hl7XS4GjJCPf9VK//.NQ/uOMWVovoKu/.kY6Sl3UuC0BYZOsm', 'admin', 'aisha.buggy@outlook.com')")
    cur.execute("INSERT INTO user (username, password, privilege_level, email) VALUES "
                "('aisha', '$2b$12$RuyMyppmv4cyWQFDSeLED.Du8sb3tXmck81VV777oye//mGCKdQKi', 'admin', 'aisha.buggy@outlook.com')")
    cur.execute("INSERT INTO user (username, password, privilege_level, email) VALUES "
                "('guest', '$2b$12$88C.VaazD3zyFWUuG9Goo.WLacvf4T559G5y7igZW0B3nfqfIDu6.', 'user', 'user.buggy@outlook.com')")
    con.commit()
    print("UPDATE User TABLE")


con.close()