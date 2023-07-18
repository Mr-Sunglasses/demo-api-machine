import uvicorn
from fastapi import FastAPI, HTTPException
import sqlite3
import time
from bs4 import BeautifulSoup
import re

app = FastAPI()

# Create a database and a table
conn = sqlite3.connect('sensor_data.db')
print("Opened database successfully")
conn.execute('''CREATE TABLE IF NOT EXISTS sensor_data
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             TEMPERATURE TEXT NOT NULL,
             HUMIDITY TEXT NOT NULL,
             X_ACC TEXT NOT NULL,
             Y_ACC TEXT NOT NULL,
             Z_ACC TEXT NOT NULL);''')
print("Table created successfully")
conn.close()

# Instead of saving the file during app initialization, you can define the function to parse HTML and insert data.
def parse_and_insert_data(content):
    soup = BeautifulSoup(content, 'html.parser')

    temperature = soup.find_all('p')[1].text
    temperature = re.sub(r'[^0-9.]', '', temperature)
    humidity = soup.find_all('p')[3].text
    x_acc = soup.find_all('p')[6].text
    y_acc = soup.find_all('p')[8].text
    z_acc = soup.find_all('p')[10].text
    # Insert the data into the database
    conn = sqlite3.connect('sensor_data.db')
    print("Opened database successfully")
    conn.execute("INSERT INTO sensor_data (TEMPERATURE, HUMIDITY, X_ACC, Y_ACC, Z_ACC) VALUES (?, ?, ?, ?, ?)",
                 (temperature, humidity, x_acc, y_acc, z_acc))
    conn.commit()
    print("Records created successfully")
    conn.close()

# Define a route to retrieve the data from the database
@app.get('/sensor-data')
async def get_sensor_data():
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
    return sensor_data

# Since FastAPI is asynchronous, we can use a background task to periodically fetch data and insert it into the database.
async def background_task():
    while True:
        with open('sensor_data.html', 'r') as f:
            content = f.read()
        parse_and_insert_data(content)
        await asyncio.sleep(0.1)

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(background_task())
    uvicorn.run(app, host='0.0.0.0', port=8000)
