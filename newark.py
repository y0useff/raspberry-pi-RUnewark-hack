from bs4 import BeautifulSoup
import requests
BASE_URL = "https://www.musiciansfriend.com"


# category = input()

category_url = f"{BASE_URL}/bass"

def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

html_text = get_html_content(category_url)
soup = BeautifulSoup(html_text)

product_card_list = soup.find_all('div', {"class", 'product-card'})
print(len(product_card_list))
