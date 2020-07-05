import variables                # Twilio SID & AUTH_TOKEN
import requests
from bs4 import BeautifulSoup   # Web Scraping
from twilio.rest import Client  # Twilio

def send_sms(header, inStock):
    #                   Send the results through SMS
    # =======================================================================
    client = Client(variables.TWILIO_ACCOUNT_SID, variables.TWILIO_AUTH_TOKEN)

    inStock.insert(0, header)

    client.messages.create(
        body="\n".join(inStock),
        from_=variables.number_twilio,
        to=variables.number_me
    )
    return

def web_scraping(URL):
    #                       Do the Web Scraping
    # =======================================================================
    in_stock = []
    inventory = {}  # stores all the plants and its availability.

    for page in URL:
        page = requests.get(page)
        soup = BeautifulSoup(page.text, 'html.parser')

        # The section where all the listings are located.
        find_listings = soup.find('ul', class_='products columns-3')
        # Each listing (PLANT) is stored in listings as a list.
        listings = find_listings.find_all('li')

        # Extract the NAME OF THE PLANT and its AVAILABILITY. Store it in the inventory Dictionary.
        for entry in listings:
            title = entry.find('h2', class_="woocommerce-loop-product__title")
            status = entry.find_all('a')[1]
            inventory[title.text] = status.text

    # Search the inventory Dictionary for any plants that are In Stock.
    for plant, status in inventory.items():
        if status == 'Add to cart':
            in_stock.append(plant)

    return in_stock

if __name__ == "__main__":
    header = 'Here\'s what\'s in stock:'

    URL = ['https://gardinonursery.com/product-category/categories/hoyas/hoyas-full-list/',
            'https://gardinonursery.com/product-category/categories/hoyas/hoyas-full-list/page/2/']

    # stores the names of the plants that are available.
    inStock = web_scraping(URL)

    # send the list of available plants to the twilio_me.
    send_sms(header, inStock)


