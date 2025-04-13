from bs4 import BeautifulSoup
import requests
BASE_URL = "https://www.musiciansfriend.com"
# category = input()
number_of_pages = 3

SALE_PARAMETERS = "#N=100202+100203+500257+100202+100203&pageName=department-page"
SALE = input("Sale? Enter Y or N.")

def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
#make request getting html body, pass into beautiful soup

#iterate through every product in a page
for i in range(0, number_of_pages):
    nao = i * 30
    if SALE.lower() == "y":
        category_url = f"{BASE_URL}/bass?Nao={nao}&{SALE_PARAMETERS}"
    else:
        category_url = f"{BASE_URL}/bass?Nao={nao}"
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
        product_name = link.get_text()
        
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
                price = min(p)
                discount = max(p) - min(p) 

        print("*******************************")
        print(f"Page: {i}")
        print(f"Name:{product_name}")
        print(f"Price: \n{price}")
        print(f"Discount:\n{discount}")
        print("*******************************")

            
        