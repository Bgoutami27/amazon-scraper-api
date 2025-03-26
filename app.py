from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_amazon_tv(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    product_data = {
        "name": soup.find("span", id="productTitle").text.strip() if soup.find("span", id="productTitle") else "N/A",
        "rating": soup.find("span", class_="a-icon-alt").text.split()[0] if soup.find("span", class_="a-icon-alt") else "N/A",
        "num_ratings": soup.find("span", id="acrCustomerReviewText").text.split()[0] if soup.find("span", id="acrCustomerReviewText") else "N/A",
        "price": soup.find("span", class_="a-price-whole").text if soup.find("span", class_="a-price-whole") else "N/A",
        "discount": soup.find("span", class_="a-color-price").text.strip() if soup.find("span", class_="a-color-price") else "N/A",
        "bank_offers": [offer.text.strip() for offer in soup.select("#dealsFeatureBullets_feature_div span")],
        "about_this_item": [item.text.strip() for item in soup.select("#feature-bullets li span")],
        "product_info": [info.text.strip() for info in soup.select("#productDetails_techSpec_section_1 td")],
        "images": [img["src"] for img in soup.select("#altImages img")],
        "manufacturer_images": [img["src"] for img in soup.select("#imageBlock img")],
    }
    
    return product_data

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    product_url = data.get("url")
    
    if not product_url:
        return jsonify({"error": "URL is required"}), 400
    
    product_data = scrape_amazon_tv(product_url)
    return jsonify(product_data)

if __name__ == '__main__':
    app.run(debug=True)
