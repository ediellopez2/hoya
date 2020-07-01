import requests
from bs4 import BeautifulSoup   # Web Scraping
from openpyxl import Workbook   # EXCEL

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
URL = 'https://gardinonursery.com/product-category/categories/hoyas/hoyas-full-list/'
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')


# The section where all the listings are located.
find_listings = soup.find('ul', class_='products columns-3')
# Each listing (PLANT) is stored in listings as a list.
listings = find_listings.find_all('li')

# Extract the NAME OF THE PLANT and it's AVAILIBILITY.
for entry in listings:
    title = entry.find('h2', class_="woocommerce-loop-product__title")
    status = entry.find_all('a')[1]
    # print(title.text)
    # print(status.text)
    # print("")

    # Add the PLANT and it's current Availibility to the Excel spreadsheet.
    sheet.append((title.text, status.text))

workbook.save("C:/Users/elope/Desktop/find_my_hoya/results_hoya.xlsx")


#                   Send the results through email
# =======================================================================