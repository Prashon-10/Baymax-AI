import logging
from livekit.agents import function_tool, RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun


@function_tool()
async def get_weather(context: RunContext, city: str) -> str:  # type: ignore
    """
    Get the current weather for a given city.
    """
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {city}: {response.text.strip()}")
            return response.text.strip()
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error getting weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}."


@function_tool()
async def search_web(context: RunContext, query: str) -> str:
    """
    Search the web using DuckDuckGo
    """
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching for '{query}': {e}")
        return f"An error occurred while searching for '{query}'."


@function_tool()
async def get_latest_news(context: RunContext, topic: str) -> str:
    """
    Get the latest news for a given topic.
    """
    try:
        response = requests.get(
            f"https://newsapi.org/v2/everything?q={topic}&apiKey=1f7ba7e6e07d43c0a5b86f384b749025"
        )
        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get("articles", [])
            if articles:
                latest_news = articles[0]["title"]
                logging.info(f"Latest news for {topic}: {latest_news}")
                return latest_news
            else:
                return f"No news found for {topic}."
        else:
            logging.error(f"Failed to get news for {topic}: {response.status_code}")
            return f"Could not retrieve news for {topic}."
    except Exception as e:
        logging.error(f"Error getting news for {topic}: {e}")
        return f"An error occurred while retrieving news for {topic}."
