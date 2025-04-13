from bs4 import BeautifulSoup
import requests
import json
import time
import http.server
import socketserver
import threading

BASE_URL = "https://www.musiciansfriend.com"

print("Select a category: ")
print("Electric Guitars")
print("Bass")
print("Amplifiers Effects")
print("Drums Percussion")
print("Keyboards MIDI")
print("Live Sound")
print("Recording Gear")
print("Accessories")
print("New Arrivals")

category = input().lower().replace(" ", "-")
number_of_pages = int(input("How many pages would you like to scrape? "))

best_deal = {"discount": 0}
products = []

def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def start_web_server():
    PORT = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"✅ Serving at http://localhost:{PORT}")
        httpd.serve_forever()

# Attach an attribute to control server start
def scrape():
    for i in range(0, number_of_pages):
        nao = i * 30
        category_url = f"{BASE_URL}/{category}?Nao={nao}"
        print(category_url)
        html_text = get_html_content(category_url)
        if html_text is None:
            continue

        soup = BeautifulSoup(html_text, "html.parser")
        product_card_list = soup.find_all('div', {"class", 'product-card'})

        for element in product_card_list:
            card = element.select_one(".product-card-content")
            if not card:
                continue

            link = card.select_one(".ui-link")
            if not link or not link.get('href'):
                continue

            link_href = f"{BASE_URL}{link['href']}"
            product_name = link.get_text(strip=True)

            price_list = card.select('.sale-price')
            price = 0
            discount = 0

            if len(price_list) == 1:
                price = price_list[0].get_text().split("$")[1].replace(",", "")
                price = float(price)
            elif len(price_list) > 1:
                p = []
                for tag in price_list:
                    try:
                        dollar_price = tag.get_text().split('$', 1)[1].split("\n")[0].replace(",", "")
                        p.append(float(dollar_price))
                    except:
                        continue

                if p:
                    price = round(min(p), 2)
                    discount = round(max(p) - min(p), 2)
                    if discount >= best_deal["discount"]:
                        best_deal.update({
                            "page": i,
                            "name": product_name,
                            "link": link_href,
                            "price": price,
                            "discount": discount
                        })

            product_dict = {
                "page": i,
                "name": product_name,
                "link": link_href,
                "price": price,
                "discount": discount,
            }

            products.append(product_dict)

            print("*******************************")
            print(f"Page: {i}")
            print(f"Name: {product_name}")
            print(f"Price: ${price}")
            print(f"Discount: ${discount}")

        with open("data.json", "w") as file:
            json.dump(products, file, indent=4)

        print("*******************************")

    print("Best deal so far:")
    print(best_deal)

    url = "https://api.pushover.net/1/messages.json"
    if best_deal["discount"] != 0:
        message = f'Scraping all done! Save ${best_deal["discount"]:.2f} on "{best_deal["name"]}"!'
    else:
        message = "Scraping all done! We found some great deals for you!"

    data = {
        "token": "akcbutkgdd49tab1kwzjtww3rxispq",
        "user": "uqmfguy4jn59b2vauxjwkqru152jv1",
        "message": message
    }
    response = requests.post(url, data=data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if not scrape.has_started_server:
        scrape.has_started_server = True
        threading.Thread(target=start_web_server, daemon=True).start()

# Initialize attribute
scrape.has_started_server = False

def main():
    while True:
        scrape()
        time.sleep(60)  # Run every 60 seconds

main()
