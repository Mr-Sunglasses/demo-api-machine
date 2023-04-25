import urllib.request

def save_out(url: str):
    # Download the webpage HTML
    response = urllib.request.urlopen(url)
    html = response.read()
    
    # Save the HTML to a file
    with open("sensor_data.html", "wb") as file:
        file.write(html)
