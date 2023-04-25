import urllib.request

def save_out(url: str):
    # Download the webpage HTML
    response = urllib.request.urlopen(url)
    html = response.read()
    
    # Save the HTML to a file
    with open("example.html", "wb") as file:
        file.write(html)
