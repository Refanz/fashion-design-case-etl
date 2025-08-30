from utils.extract import scrape_fashion

def main():
    """Main function to execute ETL process."""
    base_url = "https://fashion-studio.dicoding.dev/{}"
    all_fashion_products = scrape_fashion(base_url)




if __name__ == '__main__':
    main()
