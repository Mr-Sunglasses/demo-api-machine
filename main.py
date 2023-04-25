from flask import Flask, jsonify
import sqlite3
import time
from files_download import save_out
app = Flask(__name__)

# Create a database and a table
conn = sqlite3.connect('sensor_data.db')
print("Opened database successfully")
conn.execute('''CREATE TABLE IF NOT EXISTS sensor_data
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             TEMPERATURE REAL NOT NULL,
             HUMIDITY REAL NOT NULL,
             X_ACC REAL NOT NULL,
             Y_ACC REAL NOT NULL,
             Z_ACC REAL NOT NULL);''')
print("Table created successfully")
conn.close()

#Download Content
save_out(url = "Your URL")

# Define a function to parse the HTML file and insert data into the database
def insert_sensor_data():
    with open('sensor_data.html', 'r') as f:
        content = f.read()

    # Parse the temperature, humidity, x_acc, y_acc, and z_acc from the HTML file
    temperature = float(content.split('tempreture</p><p>')[1].split('&#xB0;C</p>')[0])
    humidity = float(content.split('humidity</p><p>')[1].split('%</p>')[0])
    x_acc = float(content.split('<p>x_acc</p><p>')[1].split('</p>')[0])
    y_acc = float(content.split('<p>y_acc</p><p>')[1].split('</p>')[0])
    z_acc = float(content.split('<p>z_acc</p><p>')[1].split('</p>')[0])

    # Insert the data into the database
    conn = sqlite3.connect('sensor_data.db')
    print("Opened database successfully")
    conn.execute(f"INSERT INTO sensor_data (TEMPERATURE, HUMIDITY, X_ACC, Y_ACC, Z_ACC) \
                 VALUES ({temperature}, {humidity}, {x_acc}, {y_acc}, {z_acc})")
    conn.commit()
    print("Records created successfully")
    conn.close()

# Define a route to retrieve the data from the database
@app.route('/sensor-data')
def get_sensor_data():
    # Connect to the database
    conn = sqlite3.connect('sensor_data.db')

    # Retrieve the data from the table
    cursor = conn.execute("SELECT * from sensor_data")
    data = cursor.fetchall()

    # Close the connection
    conn.close()

    # Convert the data into a list of dictionaries
    sensor_data = []
    for row in data:
        sensor_data.append({'id': row[0], 'temperature': row[1], 'humidity': row[2],
                            'x_acc': row[3], 'y_acc': row[4], 'z_acc': row[5]})

    # Return the data as a JSON response
    return jsonify(sensor_data)

if __name__ == '__main__':
    while True:
        insert_sensor_data()
        # REALOAD PAGE AT EVERY 100MS
        time.sleep(0.1)
        app.run(debug=True)
