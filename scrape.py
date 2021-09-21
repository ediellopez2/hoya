import requests                           # Web Scraping
from bs4 import BeautifulSoup             # Web Scraping

URL = ['https://gardinonursery.com/product-category/categories/hoyas/hoyas-list-full/',
       'https://gardinonursery.com/product-category/categories/hoyas/hoyas-list-full/page/2/',
       'https://gardinonursery.com/product-category/categories/hoyas/hoyas-list-full/page/3/',
       'https://gardinonursery.com/product-category/categories/hoyas/hoyas-full-list/page/4/']

# Some websites have services that block webscrapers, so it is important to include the following line.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

if __name__ == "__main__":
    try:
        for page in URL:

            print("Starting on " + page + "\n")
            page = requests.get(page, headers=headers)

            # 2xx successful – the request was successfully received, understood, and accepted
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, 'html.parser')

                # All of the items (plants) are wrapped in <ul class="products columns-3">.
                find_listings = soup.find('ul', class_='products columns-3')

                # Find all of list items in the unordered list.
                listings = find_listings.find_all('li')

                # You currently have all of the listings (represented as a list item in HTML) stored in a Python List.
                # This is what the HTML code looks like for each list item in the HTML code.
                # <li class="sales-flash-overlay woocommerce-text-align-center woocommerce-image-align-center do-quantity-buttons product type-product post-33921 status-publish first instock product_cat-fragrantscented-hoyas product_cat-hoyas product_cat-hoyas-list-full product_cat-hoyas-for-beginners product_cat-hoyas-for-foliage-lovers has-post-thumbnail taxable shipping-taxable product-type-simple">
                # <a class="woocommerce-LoopProduct-link woocommerce-loop-product__link" href="https://gardinonursery.com/product/gardino-points/">
                #    <div class="wc-product-image">
                #       <div class="inside-wc-product-image">
                #           <img alt="" class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail" height="300" loading="lazy" sizes="(max-width: 300px) 100vw, 300px" src="https://gardinonursery.com/wp-content/uploads/coupon-300x300.jpg" srcset="https://gardinonursery.com/wp-content/uploads/coupon-300x300.jpg 300w, https://gardinonursery.com/wp-content/uploads/coupon-45x45.jpg 45w, https://gardinonursery.com/wp-content/uploads/coupon-100x100.jpg 100w" width="300"/>
                #       </div>
                #    </div>
                #    <h2 class="woocommerce-loop-product__title">GARDINO POINTS</h2>
                # </a>
                # <a class="button" data-quantity="1" href="https://gardinonursery.com/product/gardino-points/">Read more</a>
                # </li>
                for item in listings:
                    # The name of the plant is stored in the h2-tag.
                    name = item.find('h2').text

                    # There is more than 2 a-tag in the HTML code. The second a-tag determines that availability.
                    status = item.find_all('a')[1]

                    if status.text == 'Add to cart':
                        print(name + " is In Stock")
                    else:
                        print(name + " is Out of Stock")

                # The view the list, uncomment the following line.
                # print(listings)

                print("\nFinished scraping this page.\n\n")
            elif page.status_code == 404:
                # The server has not found anything matching the Request-URL.
                print("Unable to scrape this page. This page is not available at this time.")
    except Exception as exc:
        # This block will execute when an unexpected error occurs.
        print(exc.__str__())