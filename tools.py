from datetime import datetime
import os

def get_current_date():
    """Get the current date and time."""
    current_datetime = datetime.now()
    return {
        "date": current_datetime.strftime("%Y-%m-%d"),
        "time": current_datetime.strftime("%H:%M:%S"),
        "weekday": current_datetime.strftime("%A")
    }

def get_weather(latitude: float, longitude: float):
    """Get weather information for given coordinates using open-meteo.com API."""
    import requests

    try:
        # Build API URL with parameters
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,precipitation,weathercode,windspeed_10m"
        
        # Make API request
        response = requests.get(url)
        data = response.json()
        current = data.get('current', {})
        
        # Map weather codes to conditions
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            95: "Thunderstorm"
        }
        
        return {
            "temperature": f"{current.get('temperature_2m', 'N/A')}{data.get('current_units', {}).get('temperature_2m', '°C')}",
            "condition": weather_codes.get(current.get('weathercode', 0), "Unknown"),
            "precipitation": f"{current.get('precipitation', 'N/A')}{data.get('current_units', {}).get('precipitation', 'mm')}",
            "wind_speed": f"{current.get('windspeed_10m', 'N/A')}{data.get('current_units', {}).get('windspeed_10m', 'km/h')}"
        }
    except Exception as e:
        return {
            "error": str(e)
        }

def get_ip():
    """Get both local and public IP addresses."""
    import socket
    import requests

    try:
        # Get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

        # Get public IP
        response = requests.get("https://api.ipify.org?format=json")
        public_ip = response.json()["ip"]

        return {
            "local_ip": local_ip,
            "public_ip": public_ip
        }
    except Exception as e:
        return {
            "error": str(e)
        }

def location():
    """Get location information based on IP address."""
    import requests
    
    try:
        # Get IP addresses using existing function
        ip_info = get_ip()
        if "error" in ip_info:
            return {"error": ip_info["error"]}
            
        # Use public IP to get location data
        response = requests.get(f"https://ipapi.co/{ip_info['public_ip']}/json/")
        location_data = response.json()
        
        # Return relevant location information
        return {
            "city": location_data.get("city"),
            "region": location_data.get("region"),
            "country": location_data.get("country_name"),
            "latitude": location_data.get("latitude"),
            "longitude": location_data.get("longitude"),
            "timezone": location_data.get("timezone")
        }
    except Exception as e:
        return {
            "error": str(e)
        }

def search_wikipedia(query):
    """Search Wikipedia for a given query."""
    import wikipedia

    try:
        # Set language to German
        wikipedia.set_lang("de")

        # Search Wikipedia
        results = wikipedia.search(query)
        if not results:
            return {"error": "No results found."}

        # Get summary of first result
        summary = wikipedia.summary(results[0], sentences=2)
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}

def search_duckduckgo(query):
    """Search DuckDuckGo for a given query."""
    import requests

    try:
        # Build search URL
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        
        # Make API request
        response = requests.get(url)
        data = response.json()
        
        # Extract relevant information
        abstract = data.get("AbstractText")
        source = data.get("AbstractSource")
        image = data.get("Image")
        
        return {
            "abstract": abstract,
            "source": source,
            "image": image
        }
    except Exception as e:
        return {
            "error": str(e)
        }

import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def crawl4ai(url: str):
    """Crawl a webpage and extract content using crawl4ai."""
    try:
        browser_config = BrowserConfig(
            headless=True,
            verbose=True
        )
        
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.ENABLED
        )
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url=url,
                config=run_config
            )
            return {"content": result.markdown}
            
    except Exception as e:
        return {"error": str(e)}

# Define available tools/functions for the model
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "Get the current date and time",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather conditions for coordinates",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "The latitude of the location"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "The longitude of the location"
                    }
                },
                "required": ["latitude", "longitude"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ip",
            "description": "Get local and public IP addresses",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "location",
            "description": "Get the users location",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_wikipedia",
            "description": "Search Wikipedia for a given query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_duckduckgo",
            "description": "Search DuckDuckGo for a given query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "crawl4ai",
            "description": "Crawl a webpage and extract content",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to crawl"
                    }
                },
                "required": ["url"]
            }
        }
    }
]
