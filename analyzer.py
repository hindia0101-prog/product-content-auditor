CATEGORY_ATTRIBUTES = {
    "Electronics": [
        "brand", "model", "product type", "size", "capacity",
        "connectivity", "compatibility", "power", "color",
    ],
    "Furniture": [
        "brand", "product type", "dimensions", "material", "color",
        "capacity", "assembly", "weight",
    ],
    "Fashion": [
        "brand", "product type", "size", "color", "material",
        "fit", "occasion", "care",
    ],
    "Beauty": [
        "brand", "product type", "skin type", "key ingredients",
        "size", "benefits", "how to use",
    ],
    "Perfume": [
        "brand", "fragrance name", "fragrance type", "volume",
        "concentration", "gender", "fragrance notes", "longevity",
    ],
    "Sports": [
        "brand", "product type", "size", "material", "weight",
        "sport", "compatibility", "usage",
    ],
    "Automotive": [
        "brand", "part name", "part number", "vehicle compatibility",
        "model", "year", "material", "dimensions",
    ],
    "Grocery": [
        "brand", "product type", "weight", "size", "ingredients",
        "origin", "expiry", "storage",
    ],
    "Other": [
        "brand", "product type", "size", "color",
        "material", "features", "benefits",
    ],
}


ATTRIBUTE_KEYWORDS = {
    "brand": [
        "samsung", "apple", "sony", "lg", "nike", "adidas",
        "xiaomi", "maybelline", "philips", "bosch", "dyson", "hp", "dell",
    ],
    "model": ["model", "series"],
    "product type": [
        "tv", "laptop", "phone", "chair", "table", "shoe", "dress",
        "perfume", "cream", "headphones", "watch",
    ],
    "size": ["size", "inch", "cm", "mm", "small", "medium", "large"],
    "dimensions": [
        "dimensions", "cm", "mm", "height", "width", "depth", "length",
    ],
    "material": [
        "wood", "metal", "steel", "leather", "cotton", "plastic", "glass",
    ],
    "color": [
        "black", "white", "blue", "red", "green", "pink", "brown",
        "grey", "gray",
    ],
    "capacity": [
        "gb", "tb", "mah", "liter", "litre", "ml", "kg", "capacity",
    ],
    "connectivity": [
        "bluetooth", "wifi", "wi-fi", "usb", "hdmi", "wireless",
    ],
    "compatibility": [
        "compatible", "compatibility", "iphone", "android", "windows",
    ],
    "power": ["w", "watt", "voltage", "volt", "battery"],
    "ingredients": ["ingredients", "contains"],
    "benefits": [
        "benefit", "helps", "designed", "ideal", "perfect", "supports",
        "comfortable", "durable",
    ],
    "how to use": ["how to use", "usage", "directions", "apply", "use"],
    "skin type": [
        "dry skin", "oily skin", "sensitive skin", "combination skin",
    ],
    "key ingredients": [
        "ingredients", "niacinamide", "retinol", "vitamin c",
    ],
    "fragrance type": [
        "eau de parfum", "eau de toilette", "parfum", "cologne",
    ],
    "volume": ["ml", "oz", "ounce"],
    "concentration": ["eau de parfum", "eau de toilette", "parfum"],
    "gender": ["men", "women", "unisex", "male", "female"],
    "fragrance notes": [
        "notes", "top notes", "heart notes", "base notes",
    ],
    "longevity": ["long lasting", "longevity", "hours"],
    "sport": ["running", "football", "gym", "cycling", "tennis"],
    "usage": ["usage", "use", "designed for"],
    "part name": ["brake", "filter", "mirror", "bumper", "belt", "lamp"],
    "part number": ["part number", "oem", "sku"],
    "vehicle compatibility": [
        "toyota", "lexus", "nissan", "hyundai", "kia", "bmw", "mercedes",
    ],
    "year": [
        "2020", "2021", "2022", "2023", "2024", "2025", "2026",
    ],
    "origin": ["made in", "origin", "country"],
    "expiry": ["expiry", "expiration", "best before"],
    "storage": ["store in", "storage", "keep refrigerated"],
    "care": ["care instructions", "machine wash", "dry clean"],
    "fit": ["regular fit", "slim fit", "oversized", "relaxed fit"],
    "occasion": ["casual", "formal", "party", "wedding"],
    "weight": ["weight", "kg", "g"],
    "assembly": ["assembly", "assemble"],
    "features": ["feature", "includes", "function"],
}


def attribute_present(attribute, text):
    normalized_text = text.lower()
    return any(
        keyword in normalized_text
        for keyword in ATTRIBUTE_KEYWORDS.get(attribute, [])
    )


def analyze_title(title, category):
    score = 100
    issues = []
    word_count = len(title.split())

    if word_count < 3:
        score -= 20
        issues.append("Title is too short.")
    elif word_count < 5:
        score -= 10
        issues.append("Title could contain more useful information.")
    if word_count > 15:
        score -= 10
        issues.append("Title may be unnecessarily long.")

    required_attributes = CATEGORY_ATTRIBUTES.get(
        category, CATEGORY_ATTRIBUTES["Other"]
    )
    missing_attributes = [
        attribute for attribute in required_attributes
        if not attribute_present(attribute, title)
    ]

    if missing_attributes:
        score -= min(len(missing_attributes) * 5, 40)
        issues.append("Potentially missing: " + ", ".join(missing_attributes))

    return {
        "score": max(score, 0),
        "issues": issues,
        "missing_attributes": missing_attributes,
    }


def analyze_description(description, category):
    score = 100
    issues = []
    word_count = len(description.split())

    if word_count < 30:
        score -= 30
        issues.append("Description is too short.")
    elif word_count < 80:
        score -= 15
        issues.append("Description could provide more detail.")

    required_attributes = CATEGORY_ATTRIBUTES.get(
        category, CATEGORY_ATTRIBUTES["Other"]
    )
    missing_attributes = [
        attribute for attribute in required_attributes
        if not attribute_present(attribute, description)
    ]

    if missing_attributes:
        score -= min(len(missing_attributes) * 4, 35)
        issues.append(
            "Potentially missing information: "
            + ", ".join(missing_attributes)
        )

    if "\n" not in description:
        score -= 10
        issues.append(
            "Description should be structured using sections or bullet points."
        )

    return {
        "score": max(score, 0),
        "issues": issues,
        "missing_attributes": missing_attributes,
    }
