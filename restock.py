import variables        # Stores my Google Email & Password
import requests                           # Web Scraping
from bs4 import BeautifulSoup             # Web Scraping
import smtplib                            # Send Email
from email.message import EmailMessage    # Send Email
from twilio.rest import Client            # Twilio
from datetime import datetime             # Display Time
import time                               # Go To Sleep

def sendEmail(subject, recepient, message):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = variables.EMAIL_USER
    msg['To'] = recepient
    msg.set_content(message)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(variables.EMAIL_USER, variables.EMAIL_PASS)
        smtp.send_message(msg)

def send_sms(recepient, message):
    client = Client(variables.TWILIO_ACCOUNT_SID, variables.TWILIO_AUTH_TOKEN)

    client.messages.create(
        body=message,
        from_=variables.number_twilio,
        to=recepient
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
    new_sum = 0
    old_sum = 0
    while (True):
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
                    new_sum = new_sum + len(listings)

            if (old_sum != new_sum):
                message = datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + ": There's been a change in the number of items up for sale." \
                            "Records show the number of items up for sale has changed from " + str(old_sum) + " to " + str(new_sum)
                sendEmail('Gardino Nursery Notification Bot', variables.EMAIL_TO_SISTER, message)
                send_sms(variables.number_sister, message)
                send_sms(variables.number_ediel, message)
            else:
                message = datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + ": There's been no change in the number of items up for sale."

            # Print message to the console.
            print(message)
            old_sum = new_sum
            new_sum = 0

            time.sleep(30)
            # =======================================================================
        except Exception as e:

            # Print to the console.
            errorMessage = "AN ERROR OCCURRED AT " + datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + "!\nHere is the specific error:\n\n" + e.__str__()
            print(errorMessage)

            # Create message and send the email.
            sendEmail('Problem: Gardino Nursery Notification Bot', errorMessage)
            send_sms(variables.number_ediel, message)
            break
