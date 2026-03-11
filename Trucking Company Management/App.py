Code:
from flask import Flask, render_template, request, redirect
import sqlite3

# Create the Flask app
app = Flask(__name__)

# Home route — display truck logs
@app.route("/")
def home():
    conn = sqlite3.connect('trucks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM truck_logs")
    rows = c.fetchall()
    conn.close()

    # Calculate Net Weight in Python safely
    truck_logs = []
    for r in rows:
        try:
            empty = float(r[10]) if r[10] != '' else 0
            loaded = float(r[11]) if r[11] != '' else 0
        except ValueError:
            empty = 0
            loaded = 0
        net = loaded - empty
        truck_logs.append({
            "id": r[0],
            "date": r[1],
            "order_number": r[2],
            "ticket_number": r[3],
            "truck_id": r[4],
            "truck_type": r[5],
            "material_name": r[6],
            "party_name": r[7],
            "transporter": r[8],
            "driver": r[9],
            "empty_weight": empty,
            "loaded_weight": loaded,
            "net_weight": net
        })

    return render_template("index.html", truck_logs=truck_logs)

# Add log route — handle form submission
@app.route("/add_log", methods=["POST"])
def add_log():
    date = request.form['date']
    order_number = request.form['order_number']
    ticket_number = request.form['ticket_number']
    truck_id = request.form['truck_id']
    truck_type = request.form['truck_type']
    material_name = request.form['material_name']
    party_name = request.form['party_name']
    transporter = request.form['transporter']
    driver = request.form['driver']
    empty_weight = request.form['empty_weight']
    loaded_weight = request.form['loaded_weight']

    conn = sqlite3.connect('trucks.db')
    c = conn.cursor()
    c.execute("""INSERT INTO truck_logs 
        (date, order_number, ticket_number, truck_id, truck_type, material_name, party_name, transporter, driver, empty_weight, loaded_weight) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (date, order_number, ticket_number, truck_id, truck_type, material_name, party_name, transporter, driver, empty_weight, loaded_weight))
    conn.commit()
    conn.close()

    return redirect("/")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
