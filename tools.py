from datetime import datetime
import requests

def get_current_date():
    """Get the current date and time."""
    current_datetime = datetime.now()
    return {
        "date": current_datetime.strftime("%Y-%m-%d"),
        "time": current_datetime.strftime("%H:%M:%S"),
        "weekday": current_datetime.strftime("%A")
    }

def get_weather(location: str):
    """Get the current weather for a location."""
    # This is a mock implementation - replace with actual weather API call
    return {
        "location": location,
        "temperature": "20°C",
        "condition": "sunny"
    }

# Define available tools/functions for the model
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "Get the current date and time. Use this when someone asks about the current date, time, or day of the week.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "get_weather",
            "description": "Get the current weather conditions for a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city or location to get weather for"
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            }
        }
    }
]
