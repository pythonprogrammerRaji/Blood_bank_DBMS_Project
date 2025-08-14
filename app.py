from flask import Flask, render_template,request,redirect,session,url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # needed for session to work

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create the users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Insert a test user (you can change this later)
c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))

conn.commit()
conn.close()

print("✅ users table created and test user added!")

# Login Route and index page to render the home page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("Recevied: ",username, password)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        print("DB result: ", user)

        if user:
            session['username'] = username  # Save username in session
            print("✅ Session set:",session['username'])
            return redirect('/home')
        else:
            print("Invalid login")
            return "Invalid Credentials. Please try again."

    return render_template('index.html')

# Home Page
@app.route('/home')
def home():
    print("Checking sesstion:", session)
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return redirect('/')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


#donor pages
def create_donor_table():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS donor (
            donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            weight REAL NOT NULL,
            last_donation TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/donor', methods=['GET', 'POST'])
def donor():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        blood_group = request.form['blood_group']
        weight = request.form['weight']
        last_donation = request.form['last_donation']
        phone = request.form['phone']
        address = request.form['address']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO donor 
            (name, age, gender, blood_group, weight, last_donation, phone, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, gender, blood_group, weight, last_donation, phone, address))
        conn.commit()
        conn.close()

        return redirect('/manage_donor')
    return render_template('Donor.html')

@app.route('/manage_donor')
def manage_donor():
    print("Manage Donor route called")
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM donor")
    donors = cur.fetchall()
    conn.close()
    print("Retreved donors: ", donors)
    return render_template('Manage_donor.html', donors=donors)

# Edit donor - display form
# Edit Donor
@app.route('/edit_donor/<int:donor_id>')
def edit_donor(donor_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM donor WHERE donor_id=?", (donor_id,))
    donor = c.fetchone()
    conn.close()
    return render_template('Edit_donor.html', donor=donor)


# Update Donor
@app.route('/update_donor/<int:donor_id>', methods=['POST'])
def update_donor(donor_id):
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    blood_group = request.form['blood_group']
    weight = request.form['weight']
    last_donation = request.form['last_donation']
    phone = request.form['phone']
    address = request.form['address']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE donor SET
            name = ?,
            age = ?,
            gender = ?,
            blood_group = ?,
            weight = ?,
            last_donation = ?,
            phone = ?,
            address = ?
        WHERE donor_id = ?
    ''', (name, age, gender, blood_group, weight, last_donation, phone, address, donor_id))
    conn.commit()
    conn.close()

    return redirect('/manage_donor')


@app.route('/delete_donor/<int:donor_id>')
def delete_donor(donor_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM donor WHERE donor_id = ?", (donor_id,))
    conn.commit()
    conn.close()
    return redirect('/manage_donor')




@app.route('/admin')
def admin():
    return render_template('Admin.html')

# Patinet data

def create_patient_table():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS patient (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            weight REAL NOT NULL,
            requested_date TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/patient', methods=['GET', 'POST'])
def patient():
    if request.method == 'POST':
        name = request.form['name']
        blood_group = request.form['blood_group']
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        requested_date = request.form['requested_date']
        phone_number = request.form['phone_number']
        address = request.form['address']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO patient 
            (name, blood_group, age, gender, weight, requested_date, phone_number, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, blood_group, age, gender, weight, requested_date, phone_number, address))
        conn.commit()
        conn.close()

        return redirect('/manage_patient')
    
    return render_template('Patient.html')

@app.route('/manage_patient')
def manage_patient():
    print("Manage patient route called")
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM patient")
    patient = cur.fetchall()
    conn.close()
    print("Retreved pateint: ", len(patient))
    return render_template('Manage_patient.html', patient=patient)

# Edit Patient
@app.route('/edit_patient/<int:id>')
def edit_patient(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM patient WHERE patient_id=?", (id,))
    patient = c.fetchone()
    print("DEBUG - Patiemt fetched: ", patient)
    conn.close()
    return render_template('Edit_patient.html', patient=patient)

#Update Patient

@app.route('/update_patient/<int:id>', methods=['POST'])
def update_patient(id):
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    blood_group = request.form['blood_group']
    weight = request.form['weight']
    requested_date = request.form['requested_date']
    phone_number = request.form['phone']
    address = request.form['address']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE patient SET
            name = ?,
            age = ?,
            gender = ?,
            blood_group = ?,
            weight = ?,
            requested_date = ?,
            phone_number = ?,
            address = ?
        WHERE patient_id = ?
    ''', (name, age, gender, blood_group, weight, requested_date, phone_number, address, id))
    conn.commit()
    conn.close()

    return redirect('/manage_patient')

#delete the patiemt data
@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM patient WHERE patient_id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/manage_patient')


#Donation data
def create_donation_table():
    conn = sqlite3.connect('database.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS donation (
        donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_id INTEGER,
        blood_group TEXT,
        quantity_ml INTEGER,
        donation_date TEXT,
        FOREIGN KEY (donor_id) REFERENCES donor(donor_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
    ''')
    conn.commit()
    conn.close()

@app.route('/donation', methods=['GET', 'POST'])
def donation():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if request.method == 'POST':
       print("Form keys received:", list(request.form.keys()))

       donor_id = request.form.get('donor_id')
       blood_group = request.form['blood_group']
       quantity_ml = request.form['quantity_ml']
       donation_date = request.form['donation_date']

       cur.execute("INSERT INTO donation (donor_id, blood_group, quantity_ml, donation_date) VALUES (?, ?, ?, ?)",
                (donor_id, blood_group, quantity_ml, donation_date))
       conn.commit()
       conn.close()
       return redirect('/manage_donation')

    cur.execute("SELECT  name, blood_group From donor")
    donors = cur.fetchall()
    conn.close()
    return render_template('Donation.html', donors=donors)

#manage donation
@app.route('/manage_donation')
def manage_donation():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        select * from donation
     ''')
    donations = cur.fetchall()
    print("Donation table:", donations)

    cur.execute('''
        select name from donor
     ''')
    donors = cur.fetchall()
    print("Donation table:", donors)

    conn.close()
    return render_template('Manage_Donation.html', donations=donations)


#edit for donation
@app.route('/edit_donation/<int:donation_id>')
def edit_donation(donation_id):
    conn = sqlite3.connect('database.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    # Fetch donation record
    cur.execute("SELECT * FROM donation WHERE donation_id = ?", (donation_id,))
    donation = cur.fetchone()

    # Fetch donor list for dropdown
    cur.execute("SELECT name FROM donor")
    donors = cur.fetchall()
    
    conn.close()
    return render_template('Edit_donation.html', donation=donation, donors=donors)


# update for donation
@app.route('/update_donation/<int:donation_id>', methods=['POST'])
def update_donation(donation_id):
    donor_id = request.form['donor_id']
    blood_group = request.form['blood_group']
    quantity_ml = request.form['quantity_ml']
    donation_date = request.form['donation_date']

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        UPDATE donation
        SET blood_group = ?, quantity_ml = ?, donation_date = ?
        WHERE donation_id = ?
     ''', ( blood_group, quantity_ml, donation_date, donation_id))
    conn.commit()
    conn.close()

    return redirect('/manage_donation')

#delete for donation
@app.route('/delete_donation/<int:donation_id>')
def delete_donation(donation_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM donation WHERE donation_id = ?", (donation_id,))
    conn.commit()
    conn.close()
    return redirect('/manage_donation')

#Blood_request
def create_request_table():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS blood_request (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            blood_group TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            request_date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patient(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/blood_request')
def blood_request():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT patient_id, name FROM patient")
    patients = c.fetchall()
    conn.close()
    return render_template('Blood_request.html', patients=patients)

@app.route('/submit_blood_request', methods=['GET','POST'])
def submit_blood_request():
        if request.method == 'POST':
            patient_id = request.form['patient_id']
            blood_group = request.form['blood_group']
            quantity = request.form['quantity']
            request_date = request.form['request_date']
            status = request.form['status']

            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO blood_request 
                (patient_id, blood_group, quantity, request_date, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (patient_id, blood_group, quantity, request_date, status))
            conn.commit()
            conn.close()

        return redirect(url_for('manage_blood_request'))
    
    

@app.route('/manage_blood_request')
def manage_blood_request():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        SELECT br.id, p.name, br.blood_group, br.quantity, br.request_date, br.status
        FROM blood_request br
        JOIN patient p ON br.patient_id = p.patient_id
    ''')
    requests = c.fetchall()
    conn.close()
    return render_template('Manage_blood_request.html', requests=requests)

@app.route('/edit_blood_request/<int:id>')
def edit_blood_request(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT patient_id, name FROM patient")
    patients = c.fetchall()

    c.execute("SELECT * FROM blood_request WHERE id=?", (id,))
    request_data = c.fetchone()
    conn.close()
    return render_template('Edit_blood_request.html', request=request_data, patients=patients)


@app.route('/update_blood_request/<int:id>', methods=['POST'])
def update_blood_request(id):
    patient_id = request.form['patient_id']
    blood_group = request.form['blood_group']
    quantity = request.form['quantity']
    request_date = request.form['request_date']
    status = request.form['status']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE blood_request
        SET patient_id=?, blood_group=?, quantity=?, request_date=?, status=?
        WHERE id=?
    ''', (patient_id, blood_group, quantity, request_date, status, id))
    conn.commit()
    conn.close()

    return redirect(url_for('manage_blood_request'))

@app.route('/delete_blood_request/<int:id>')
def delete_blood_request(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM blood_request WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('manage_blood_request'))

@app.route('/manage_bloodstack')
def manage_bloodstack():
    return render_template('Blood_stock.html')


#Blood_Stack

@app.route('/blood_stock')
def blood_stock():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Total quantity donated
    cur.execute("SELECT blood_group, SUM(quantity_ml) as total_donated FROM donation GROUP BY blood_group")
    donated = {row["blood_group"]: row["total_donated"] for row in cur.fetchall()}

    # Total quantity requested
    cur.execute("SELECT blood_group, SUM(quantity) as total_requested FROM blood_request GROUP BY blood_group")
    requested = {row["blood_group"]: row["total_requested"] for row in cur.fetchall()}

    # Final stock = donations - requests
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    stock = {}
    for bg in blood_groups:
        stock[bg] = donated.get(bg, 0) - requested.get(bg, 0)

    conn.close()
    return render_template('Blood_stock.html', stock=stock)



# import sqlite3

# conn = sqlite3.connect('database.db')
# cursor = conn.cursor()

# try:
#     cursor.execute("ALTER TABLE patient ADD COLUMN age INTEGER")
#     print("Column added successfully.")
# except Exception as e:
#     print("Column might already exist or error:", e)

# conn.commit()
# conn.close()

# import sqlite3

# conn = sqlite3.connect('database.db')
# c = conn.cursor()
# c.execute("PRAGMA table_info(donor);")
# columns = c.fetchall()
# for col in columns:
#     print(col)
# conn.close()

# import sqlite3
# conn = sqlite3.connect('database.db')
# c = conn.cursor()
# c.execute("SELECT * FROM donation")
# print(c.fetchall())
# conn.close()

if __name__ == '__main__':
    create_patient_table();
    create_donor_table();
    # create_donation_table();
    create_request_table();
    app.run(debug=True)