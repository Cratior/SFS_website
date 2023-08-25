from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up Chrome options to mimic a browser
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Provide the path to your ChromeDriver executable
chromedriver_path = "/path/to/chromedriver"

# URL of the Discord chat page
url = "https://discord.com/channels/400050897700257792/993056668118163466"

# Initialize the Chrome WebDriver with options directly
driver = webdriver.Chrome(chromedriver_path, options=chrome_options)

# Open the URL
driver.get(url)

# Get the page source after waiting for a moment to load the content
html_content = driver.page_source

# Close the WebDriver
driver.quit()

# Use BeautifulSoup to parse the page source
soup = BeautifulSoup(html_content, "html.parser")

blueprints = []

for message_div in soup.find_all("div", class_="message-2CShn3"):
    user_name = message_div.find("span", class_="username-h_Y3Us").get_text()
    
    message_content = message_div.find("div", class_="markup-eYLPri")
    link = message_div.find("a", class_="anchor-1X4H4q")["href"]
    description = message_content.get_text().replace(link, "").strip()

    image_tags = message_div.find_all("img", class_="lazyImg-ewiNCh")
    image_src = image_tags[0]["src"] if image_tags else ""

    blueprint = {
        "imageSrc": image_src,
        "title": user_name,
        "description": description,
        "downloadLinks": [{"label": "Download Link", "link": link}]
    }

    blueprints.append(blueprint)

with open("blueprints.json", "w") as json_file:
    json.dump(blueprints, json_file, indent=4)

print("JSON file created successfully.")
