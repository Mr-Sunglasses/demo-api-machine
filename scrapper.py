from bs4 import BeautifulSoup
html = '''<html><head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
<body>
  <h1>ESP32 Local Server Using MicroPython</h1>
  <div class="dtt">
    <p>tempreture</p><p>21.4&deg;C<p>
    <p>humidity</p><p>43.2%</p>
    <h4>acceleration</h4>
     <p>x_acc</p><p>-0.4785155</p>
     <p>y_acc</p><p>-1.257324</p>
     <p>z_acc</p><p>-0.1151898</p>
</div>
</body></html>'''

soup = BeautifulSoup(html, 'html.parser')

temperature = soup.find_all('p')[1].text
humidity = soup.find_all('p')[3].text
x_acc = soup.find_all('p')[6].text
y_acc = soup.find_all('p')[8].text
z_acc = soup.find_all('p')[10].text

print(temperature, humidity, x_acc, y_acc, z_acc)