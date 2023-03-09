from newsapi import NewsApiClient
import config

# Init
newsapi = NewsApiClient(api_key=config.NEWS_API_KEY)

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(
    q="unemployment",
    # sources="bbc-news,the-verge",
    category="business",
    language="en",
    country="us",
)


print(top_headlines)
