from bs4 import BeautifulSoup
import requests
import json
import time

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

number_of_pages = 3
best_deal = {}
best_deal["discount"] = 0
def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
#make request getting html body, pass into beautiful soup

products = []
#iterate through every product in a page
def scrape():
    for i in range(0, number_of_pages):
        nao = i * 30
        category_url = f"{BASE_URL}/{category}?Nao={nao}"
        print(category_url)
        html_text = get_html_content(category_url)
        soup = BeautifulSoup(html_text)

        #get list of products
        product_card_list = soup.find_all('div', {"class", 'product-card'})

        for element in product_card_list:
            #grab product card
            card = (element.select(".product-card-content"))[0]

            #get text from link
            link = (card.select(".ui-link"))[0]
            product_name = link.get_text().replace("\n", "")
            
            price_list = card.select('.sale-price')
            price = 0
            discount = 0
            #if no savings, or multiple prices, price is set to the only price
            if len(price_list) == 1:
                price = price_list[0].get_text()
                price = price.split("$")[1]
                price = price.replace(",", "")
            else:
                #if multiple prices, discount found
                p = []
                for tag in price_list:
                    dollar_price = tag.get_text().split('$', 1)[1]
                    dollar_price = dollar_price.split("\n")[0]
                    dollar_price = dollar_price.replace(",", "")
                    p.append(dollar_price)
                p = list(map(float, p))
                if len(p) != 0: 
                    price = round(min(p), 2)
                    discount = round(max(p) - min(p), 2)
                    if discount >= best_deal["discount"]:
                        best_deal["page"] = i
                        best_deal["name"] = product_name
                        best_deal["price"] = price
                        best_deal["discount"] = discount
                        
                
                product_dict = {
                    "page": i,
                    "name": product_name,
                    "price": price, 
                    "discount": discount, 
                }
            
                products.append(product_dict)

            print("*******************************")
            print(f"Page: {i}")
            print(f"Name:{product_name}")
            print(f"Price: \n${price}")
            print(f"Discount:\n${discount}")
        with open("data.json", "w") as file:
            json.dump(products, file, indent=4)
        print("*******************************")

    print(best_deal)

    url = "https://api.pushover.net/1/messages.json"
    if best_deal["discount"] != 0:
        data = {
            "token": "akcbutkgdd49tab1kwzjtww3rxispq",
            "user": "uqmfguy4jn59b2vauxjwkqru152jv1",
            "message": f'Scraping all done! We found a great deal for you. Save ${best_deal["discount"]:.2f} on a "{best_deal["name"]}"!'
        }
        response = requests.post(url, data=data)

        # Optional: print the response status and body
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    else:
        data = {
            "token": "akcbutkgdd49tab1kwzjtww3rxispq",
            "user": "uqmfguy4jn59b2vauxjwkqru152jv1",
            "message": f'Scraping all done! We found some great deals for you!'
        }
        response = requests.post(url, data=data)

        # Optional: print the response status and body
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")




def main():
    while True:
        scrape()
        time.sleep(60)  # Wait 60 seconds before the next scrape

main()