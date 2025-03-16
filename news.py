import streamlit as st
from openai import OpenAI
from tavily import TavilyClient
from pydantic import BaseModel
from typing import List
import json

# 0. Set Clients and Variables
oaiClient = OpenAI(api_key=st.secrets.openai.aether_api_key)
tavClient = TavilyClient(api_key=st.secrets.tavily.api_key)

def get_news():
    news = tavClient.extract(urls=["themat.com"], extract_depth="advanced",include_images=True)
    return news

@st.cache_data(ttl="1d")
def get_response():
    news = f"{get_news()}"
    response = oaiClient.responses.create(model="gpt-4o", input=[{"role": "system", "content": """You are an expert at structured data extraction. You will extract the news articles from the input. You will return a json output listing news title, the article url, and the image url for each news article. DO NOT INCLUDE JSON``` or ``` ONLY RETURN THE JSON OUTPUT. EXAMPLE OUTPUT:  [{"news_title": "", "image_url": "", "news_url": ""}]"""}, {"role": "user", "content": news}])
    #response1 = json.loads(response)
    #print(response)
    print(response.output_text)
    return response

a = get_response()

# Streamlit app implementation
st.header("Wrestling News")

# Parse the JSON data (assuming a.output_text contains the JSON string)
news_articles = json.loads(a.output_text)

# Display each article
for article in news_articles:
    # Create two columns for image and text
    col1, col2 = st.columns([1, 3])
    
    # Image column
    with col1:
        st.image(article["image_url"], width=150)
    
    # Text column
    with col2:
        st.markdown(article["news_title"])
        st.write(f"[Read more]({article['news_url']})")
    
    # Add divider between articles
    st.divider()