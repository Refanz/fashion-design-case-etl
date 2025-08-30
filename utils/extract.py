import time

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def fetching_content(url):
    """Get HTML content from a URL."""
    session = requests.Session()
    response = session.get(url, headers=HEADERS)

    try:
        response.raise_for_status()
        return response.content
    except requests.exceptions.ConnectionError as e:
        print(f"Error fetching {url}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_fashion_info(product_card: BeautifulSoup):
    """Get product details namely title, price, rating, colors, size and gender."""

    product_details = product_card.find("div", class_="product-details")

    title = product_details.find("h3", class_="product-title").text
    price_tag = product_details.find("span", class_="price")
    price = price_tag.text if price_tag else product_details.find("p", class_="price").text

    product_desc = product_details.find_all("p")
    rating = product_desc[0].text
    colors = product_desc[1].text
    size = product_desc[2].text
    gender = product_desc[3].text

    fashion_products = {
        "title": title,
        "price": price,
        "rating": rating,
        "colors": colors,
        "size": size,
        "gender": gender
    }

    return fashion_products


def scrape_fashion(base_url, start_page=1, delay=2):
    """Function to scrape fashion products from a website."""
    all_fashion_products = []
    page_number = start_page

    while True:
        url = base_url.format(f"page{page_number}") if page_number > 1 else base_url.format("")
        print(f"Scraping page: {url}")

        content = fetching_content(url)
        if content:
            soup = BeautifulSoup(content, "html.parser")
            product_cards = soup.find_all("div", class_="collection-card")

            for card in product_cards:
                product = extract_fashion_info(card)
                print(product)
                all_fashion_products.append(product)

            next_page_button = soup.find("li", class_="next")
            if next_page_button:
                page_number += 1
                time.sleep(delay)
            else:
                break
        else:
            break

    return all_fashion_products
