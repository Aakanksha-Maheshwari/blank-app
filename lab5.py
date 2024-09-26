import streamlit as st
import openai
import requests

def get_current_weather(location):
    API_key = st.secrets["OpenWeather_API"]
    
    if "," in location:
        location = location.split(",")[0].strip()
    
    urlbase = "https://api.openweathermap.org/data/2.5/weather"
    url = f"{urlbase}?q={location}&appid={API_key}"
    
    response = requests.get(url)
    data = response.json()

    # Check if the city is found
    if response.status_code != 200 or data.get("cod") != 200:
        return None

    temp = data['main']['temp'] - 273.15
    feels_like = data['main']['feels_like'] - 273.15
    temp_min = data['main']['temp_min'] - 273.15
    temp_max = data['main']['temp_max'] - 273.15
    humidity = data['main']['humidity']
    weather_description = data['weather'][0]['description']
    
    return {
        "location": location,
        "temperature": round(temp, 2),
        "feels_like": round(feels_like, 2),
        "temp_min": round(temp_min, 2),
        "temp_max": round(temp_max, 2),
        "humidity": humidity,
        "weather_description": weather_description
    }

def get_clothing_suggestions(weather_data):
    openai.api_key = st.secrets["openai_key"]

    prompt = f"""
    Given the weather conditions in {weather_data['location']}, which are:
    - Temperature: {weather_data['temperature']}°C
    - Feels like: {weather_data['feels_like']}°C
    - Weather: {weather_data['weather_description']}
    
    Provide appropriate clothing suggestions and indicate if it's a good day for a picnic.
    """

    # Correctly call the OpenAI API with the model and messages
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides clothing suggestions based on weather."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the assistant's response
    suggestions = response.choices[0].message.content.strip()
    return suggestions

def weather_suggestion_bot():
    st.title("Travel Weather and Suggestion Bot")
    
    # Input city from user
    city = st.text_input("Enter a city for weather information:", "Syracuse, NY")
    
    # Add a search button
    if st.button("Search for Weather and Suggestions"):
        weather_data = get_current_weather(city)
        
        if weather_data:
            # Display the weather info
            st.write(f"### Weather in {weather_data['location']}")
            st.write(f"Temperature: {weather_data['temperature']}°C")
            st.write(f"Feels Like: {weather_data['feels_like']}°C")
            st.write(f"Weather: {weather_data['weather_description']}")
            st.write(f"Humidity: {weather_data['humidity']}%")
        
            # Get clothing suggestions from LLM
            suggestions = get_clothing_suggestions(weather_data)
        
            # Display suggestions
            st.write("### Clothing Suggestions and Picnic Advice:")
            st.write(suggestions)
        else:
            st.error("City not found. Please try another location.")

# Run the bot
if __name__ == '__main__':
    weather_suggestion_bot()
