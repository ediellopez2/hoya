import variables        # Stores my Google Email & Password
import requests                           # Web Scraping
from bs4 import BeautifulSoup             # Web Scraping
import smtplib                            # Send Email
from email.message import EmailMessage    # Send Email
from twilio.rest import Client            # Twilio
from datetime import datetime             # Display Time
import time                               # Go To Sleep


def send_email(subject, recipient, message):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = variables.EMAIL_USER
    msg['To'] = recipient
    msg.set_content(message)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(variables.EMAIL_USER, variables.EMAIL_PASS)
        smtp.send_message(msg)


def send_sms(recipient, message):
    client = Client(variables.TWILIO_ACCOUNT_SID, variables.TWILIO_AUTH_TOKEN)

    client.messages.create(
        body=message,
        from_=variables.number_twilio,
        to=recipient
    )
    return


#                             Web Scraping
# =======================================================================
URL = ['https://gardinonursery.com/product-category/categories/hoyas/hoyas-list-full/',
       'https://gardinonursery.com/product-category/categories/hoyas/hoyas-list-full/page/2/',
       'https://gardinonursery.com/product-category/categories/hoyas/hoyas-list-full/page/3/',
       'https://gardinonursery.com/product-category/categories/hoyas/hoyas-full-list/page/4/']
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

if __name__ == "__main__":
    # These two variables store the previous and current number of listings.
    new_listings = 0
    old_listings = 0
    # These two variables store the previous and current number of listings that is
    # actually available for purchase (Add to cart).
    new_available = 0
    old_available = 0

    while True:
        try:
            for page in URL:
                page = requests.get(page, headers=headers)

                # 2xx successful – the request was successfully received, understood, and accepted
                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, 'html.parser')

                    # All of the items (plants) are wrapped in <ul class="products columns-3">.
                    find_listings = soup.find('ul', class_='products columns-3')

                    # Find all of list items in the unordered list.
                    listings = find_listings.find_all('li')

                    # Update the number of listings.
                    new_listings = new_listings + len(listings)

                    # You currently have all of the listings stored in a Python List.
                    # Determine the number of items that is available for purchase (Add to cart).
                    for item in listings:
                        status = item.find_all('a')[1]
                        if status.text == 'Add to cart':
                            new_available = new_available + 1

            if (old_listings != new_listings) or (old_available != new_available):
                message = datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + ": There's been a change!\n" \
                            "# of items listed: " + str(old_listings) + " to " + str(new_listings) + ".\n" \
                            "# of items available for purchase: " + str(old_available) + " to " + str(new_available) + "."
                send_email('Gardino Nursery Notification Bot', variables.EMAIL_TO_SISTER, message)
                send_sms(variables.number_sister, message)
                send_sms(variables.number_ediel, message)
            else:
                message = datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + ": There's been no change."

            print(message)
            old_listings = new_listings
            new_listings = 0

            old_available = new_available
            new_available = 0

            time.sleep(30)  # 30 seconds
            # =======================================================================
        except requests.exceptions.ConnectionError as errc:
            # In the event of a network problem (e.g. DNS failure, refused connection, etc),
            # Requests will raise a ConnectionError exception.
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.")
            print(errc.__str__())

            # Sleep for 1 minute and try to run the program again.
            time.sleep(60)  # 1 minute
            continue
        except Exception as exc:
            # This block will execute when an unexpected error that is unrelated to connection error occurs.
            errorMessage = "AN ERROR OCCURRED AT " + datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + "!\n"
            print(errorMessage + "Here is the specific error:\n" + exc.__str__())

            send_sms(variables.number_ediel, errorMessage)
            break
