import variables                   # Stores my Google Email & Password
import requests                    # Web Scraping
from bs4 import BeautifulSoup      # Web Scraping
from twilio.rest import Client     # Twilio
import time

# Documentation:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find

def send_sms():
    client = Client(variables.TWILIO_ACCOUNT_SID, variables.TWILIO_AUTH_TOKEN)

    client.messages.create(
        body="Hoya update in progress.",
        from_=variables.number_twilio,
        to=variables.number_me
    )
    return

if __name__ == "__main__":
    while (True):
        # soup = BeautifulSoup(open("C:/Users/elope/Desktop/hoya_site_restock.html"), "html.parser")

        page = requests.get("https://gardinonursery.com/product-category/categories/hoyas/hoyas-full-list/")
        soup = BeautifulSoup(page.text, 'html.parser')

        # If the website is currently down due to a restock that is in progress, then
        # <div class="information"> ... </div> will be present in the html code. If the
        # site is up an running, the find_div = None.
        find_div = soup.find('div', class_='information')

        if (find_div != None):
            # Hey, it looks like the website is currently down due to a restock. Let's
            # try to find the signature message that is displayed on the website.
            if (find_div.find(string="Hoya update in progress.") == 'Hoya update in progress.'):
                send_sms()
        else:
            print("The website is up and running.")

        find_div = None
        time.sleep(1800)    # 30 minutes
