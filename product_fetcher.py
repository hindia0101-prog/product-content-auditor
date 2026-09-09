import json
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def fetch_product_page(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise ValueError("Enter a valid product URL starting with http:// or https://.")

    response = requests.get(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (compatible; ProductContentAuditor/1.0)"
            )
        },
        timeout=20,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    title = _first_content(
        soup,
        [
            ("meta", {"property": "og:title"}),
            ("meta", {"name": "twitter:title"}),
            ("h1", {}),
            ("title", {}),
        ],
    )
    description = _first_content(
        soup,
        [
            ("meta", {"property": "og:description"}),
            ("meta", {"name": "description"}),
            ("meta", {"name": "twitter:description"}),
        ],
    )

    structured_data = _extract_product_json_ld(soup)
    if not title:
        title = structured_data.get("name", "")
    if not description:
        description = structured_data.get("description", "")

    if not description:
        description = _extract_description_text(soup)

    if not title:
        raise ValueError("Could not find a product title on this page.")
    if not description:
        raise ValueError("Could not find a product description on this page.")

    return {
        "title": title,
        "description": description,
        "details": structured_data,
    }


def _first_content(soup, selectors):
    for tag_name, attributes in selectors:
        element = soup.find(tag_name, attributes)
        if element:
            content = element.get("content") or element.get_text(" ", strip=True)
            if content:
                return content.strip()
    return ""


def _extract_description_text(soup):
    selectors = [
        "[itemprop='description']",
        "[class*='description']",
        "[id*='description']",
    ]
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            text = element.get_text(" ", strip=True)
            if text:
                return text
    return ""


def _extract_product_json_ld(soup):
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or script.get_text())
        except (TypeError, json.JSONDecodeError):
            continue

        candidates = data if isinstance(data, list) else [data]
        for candidate in candidates:
            if not isinstance(candidate, dict):
                continue
            item_type = candidate.get("@type", "")
            if item_type == "Product" or (
                isinstance(item_type, list) and "Product" in item_type
            ):
                return {
                    key: value
                    for key, value in candidate.items()
                    if key in {
                        "name", "description", "brand", "model",
                        "color", "material", "size", "sku", "offers",
                    }
                }
    return {}
