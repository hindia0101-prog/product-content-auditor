import requests
import streamlit as st

from analyzer import analyze_description, analyze_title
from product_fetcher import fetch_product_page


st.set_page_config(
    page_title="Ecommerce Product Content Auditor",
    page_icon="🛍️",
)

st.title("🛍️ Ecommerce Product Content Auditor")
st.write("Paste a product URL to extract its content for auditing.")

category = st.selectbox(
    "Product Category",
    [
        "Electronics",
        "Furniture",
        "Fashion",
        "Beauty",
        "Perfume",
        "Sports",
        "Automotive",
        "Grocery",
        "Other",
    ],
)

product_url = st.text_input(
    "Product URL",
    placeholder="https://example.com/product",
)


if st.button("Analyze Product"):
    if not product_url:
        st.warning("Please enter a product URL.")
    else:
        try:
            product = fetch_product_page(product_url)
        except (requests.RequestException, ValueError) as error:
            st.error(f"Unable to fetch product details: {error}")
        else:
            product_title = product["title"]
            product_description = product["description"]

            st.subheader("Extracted Product Content")
            st.write(f"**Title:** {product_title}")
            st.write(f"**Description:** {product_description}")

            if product["details"]:
                with st.expander("Extracted product details"):
                    st.json(product["details"])

            title_result = analyze_title(product_title, category)
            description_result = analyze_description(
                product_description,
                category,
            )
            overall_score = round(
                (title_result["score"] + description_result["score"]) / 2
            )

            st.divider()
            st.subheader("Content Opportunity Score")
            st.metric("Overall Score", f"{overall_score}/100")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Product Title")
                st.metric("Title Score", f"{title_result['score']}/100")
                if title_result["issues"]:
                    for issue in title_result["issues"]:
                        st.write("⚠️", issue)
                else:
                    st.success("No major title issues detected.")

            with col2:
                st.subheader("Product Description")
                st.metric(
                    "Description Score",
                    f"{description_result['score']}/100",
                )
                if description_result["issues"]:
                    for issue in description_result["issues"]:
                        st.write("⚠️", issue)
                else:
                    st.success("No major description issues detected.")

            st.subheader("Missing Opportunities")
            missing_title = title_result["missing_attributes"]
            missing_description = description_result["missing_attributes"]

            col1, col2 = st.columns(2)
            with col1:
                st.write("### Title")
                if missing_title:
                    for item in missing_title:
                        st.write("🔴", item.title())
                else:
                    st.success("No major missing title attributes detected.")

            with col2:
                st.write("### Description")
                if missing_description:
                    for item in missing_description:
                        st.write("🔴", item.title())
                else:
                    st.success(
                        "No major missing description attributes detected."
                    )
