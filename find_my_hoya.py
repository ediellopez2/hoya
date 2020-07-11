import variables        # Stores my Google Email & Password
import requests                           # Web Scraping
from bs4 import BeautifulSoup             # Web Scraping
from openpyxl import Workbook             # EXCEL
import smtplib                            # Send Email
from email.message import EmailMessage    # Send Email

#                       Create Excel Sheet
# ========================================================================
workbook = Workbook()
sheet = workbook.active
sheet.title = "Hoya"
sheet.column_dimensions['A'].width = 45
sheet.column_dimensions['B'].width = 30
sheet.append(("Item", "Availibility"))

#                       Do the Web Scraping
# =======================================================================

# NOTICE: There may be more than two pages.
# URL = ['https://gardinonursery.com/product-category/categories/hoyas/hoyas-full-list/',
#             'https://gardinonursery.com/product-category/categories/hoyas/hoyas-full-list/page/2/']

URL = ['https://gardinonursery.com/product-category/categories/hoyas/hoyas-full-list/',
       'https://gardinonursery.com/product-category/categories/hoyas/hoyas-full-list/page/2/',
       'https://gardinonursery.com/product-category/categories/hoyas/hoyas-full-list/page/3/',
       'https://gardinonursery.com/product-category/categories/hoyas/hoyas-full-list/page/4/']

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
        # print(title.text)
        # print(status.text)
        # print("")

        # Add the PLANT and it's current Availability to the Excel spreadsheet.
        sheet.append((title.text, status.text))

workbook.save("C:/Users/elope/Desktop/find_my_hoya/results_hoya.xlsx")


#                   Send the results through email
# =======================================================================
msg = EmailMessage()
msg['Subject'] = 'Hoya Report'
msg['From'] = variables.EMAIL_USER
msg['To'] = variables.EMAIL_USER        # Sending an email to myself
msg.set_content('See the attached file ...')

with open('C:/Users/elope/Desktop/find_my_hoya/results_hoya.xlsx','rb') as myFile:
    file_data = myFile.read()
    file_name = 'results_hoya.xlsx'

msg.add_attachment(file_data,maintype='application',subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=file_name)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(variables.EMAIL_USER, variables.EMAIL_PASS)
    smtp.send_message(msg)