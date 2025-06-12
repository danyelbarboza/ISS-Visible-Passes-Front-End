
# ISS Visible Passes Web Application

Track upcoming visible passes of the International Space Station (ISS) for any location with this web application. This tool combines orbital data from N2YO with weather forecasts from Open-Meteo to provide the best viewing opportunities. Simply enter a city, and the system will return upcoming ISS passes, detailing the specific weather conditions and a custom visibility score for each event.

The application features a user-friendly interface built with Flask and a responsive design based on the Fractal template by HTML5 UP. It also provides a JSON API for programmatic access to the data.

-----

## How It Works

The application operates in two main ways: through a web interface or a JSON API.

**1. Web Interface:**

1.  A user enters a city name into the search form on the homepage.
2.  The Flask backend (`app.py`) receives the request via the `/buscar` route and passes the city name to the controller.
3.  The `controller.py` module orchestrates the data retrieval and processing:
      * It uses the **Nominatim API** to convert the city name into geographic coordinates (latitude and longitude).
      * It then uses the **N2YO API** to fetch upcoming ISS visual passes for those coordinates. Pass times are converted from UTC to the local timezone (GMT-3).
      * For each pass, the **Open-Meteo API** is queried to get a detailed weather forecast for the precise start time of the pass. This includes temperature, cloud cover, visibility, and humidity.
      * Finally, it calculates a custom **visibility score** (from 0 to 10) for each pass based on weather parameters and pass duration, helping the user quickly identify the best viewing times.
4.  The processed data is rendered on the `result.html` page, displaying a list of passes with their corresponding weather conditions and visibility scores.

**2. JSON API:**

1.  A request is made to the `/api/passes` endpoint with a city name as a query parameter (e.g., `/api/passes?cidade=New+York`).
2.  The Flask backend receives the request, and the process follows the same data retrieval and processing steps as the web interface.
3.  Instead of rendering an HTML page, the final data, including the visibility scores, is structured into a JSON object and returned as the response.

-----

## Features

  - **City to Coordinates Conversion**: Automatically converts city names into geographical coordinates using the Nominatim API.
  - **ISS Pass Times**: Fetches upcoming ISS pass times for the specified location from the N2YO API.
  - **Specific Weather Conditions**: Retrieves weather forecasts (temperature, cloud cover, visibility, humidity) for the exact time of each pass using the Open-Meteo API.
  - **Visibility Score**: Each pass is assigned a unique visibility score based on cloud cover, humidity, pass duration, and weather visibility to help you choose the optimal viewing times.
  - **Timezone Conversion**: Converts UTC pass times from the N2YO API to a local timezone (GMT-3).
  - **JSON API Endpoint**: Provides programmatic access to ISS pass data through a simple RESTful endpoint.
  - **API Response Caching**: Implements caching for Open-Meteo API responses to improve performance and reduce redundant calls.
  - **User-Friendly Web Interface**: Provides an intuitive interface for inputting a location and viewing results, built on a responsive HTML5 UP template.

-----

## Tech Stack

**Backend:**

  - Python 3
  - Flask (Web Framework)
  - Gunicorn (for production)

**Frontend:**

  - HTML5
  - CSS3 & SASS
  - JavaScript

**APIs Used:**

  - [N2YO](https://www.n2yo.com/api/) (ISS orbital data)
  - [Nominatim](https://nominatim.org/release-docs/develop/api/Search/) (Geocoding)
  - [Open-Meteo](https://open-meteo.com/en/docs) (Weather Forecasts)

**Key Python Libraries:**

  - `Flask`
  - `requests` & `requests_cache`
  - `pandas`
  - `python-dotenv`
  - `openmeteo_requests`
  - `gunicorn`
    (See `requirements.txt` for a full list).

-----

## Project Structure

  - `app.py`: The main Flask application file that handles routing for the web interface and the JSON API, rendering HTML templates or returning JSON data.
  - `src/controller/controller.py`: Contains the core logic for fetching and processing data from all external APIs. It coordinates the client modules and calculates the visibility score.
  - `src/config/config.py`: Manages configuration variables, such as API keys and observation parameters.
  - `src/clients/n2yo_client.py`: A client module to interact with the N2YO API for ISS pass data.
  - `src/clients/nominatim_client.py`: A client module for the Nominatim API to perform geocoding.
  - `src/clients/openmeteo_client.py`: A client module for the Open-Meteo API to fetch weather forecasts.
  - `templates/`: Contains the Jinja2 HTML templates (`index.html` and `result.html`).
  - `static/`: Contains static assets like CSS, JavaScript, and images.

-----

## API Usage

To get ISS pass data programmatically, use the `/api/passes` endpoint.

**Endpoint:** `GET /api/passes`

**Query Parameter:**

  - `cidade` (string, required): The name of the city for which you want to retrieve ISS passes.

**Example Request:**

```bash
curl "http://127.0.0.1:5000/api/passes?cidade=Vitoria"
```

**Example JSON Response:**

```json
{
  "passes": [
    {
      "cloudcover": 85,
      "duration": 435,
      "humidity": 82,
      "id": 1,
      "is_day": "Night",
      "start": "2025-06-12T18:02",
      "temperature": 23.4,
      "visibility": 24140.0,
      "visibility_score": 3.7
    },
    {
      "cloudcover": 98,
      "duration": 605,
      "humidity": 82,
      "id": 2,
      "is_day": "Night",
      "start": "2025-06-14T17:58",
      "temperature": 23.5,
      "visibility": 24140.0,
      "visibility_score": 2.6
    }
  ],
  "query_city": "Vitoria",
  "resolved_location": "Vitória, Região Geográfica Imediata de Vitória, Região Geográfica Intermediária de Vitória, Espírito Santo, Região Sudeste, Brasil"
}
```

-----

## Quick Start

### 1\. Prerequisites

  - Python 3.x
  - pip (Python package installer)

### 2\. Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/danyelbarboza/ISS-Visible-Passes-Front-End.git
    cd ISS-Visible-Passes-Front-End
    ```

2.  **Create and activate a virtual environment (recommended):**

    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### 3\. Configuration

The application requires an N2YO API key to function.

1.  **Add Your N2YO API Key:**

      - Open the file `src/config/config.py`.
      - Replace the placeholder string for the `api_key` variable with your actual key from [N2YO.com](https://www.n2yo.com/api/).

    <!-- end list -->

    ```python
    # In src/config/config.py
    class Config:
        def __init__(self, latitude, longitude):
            load_dotenv()
            # ... other configs
            self.api_key = "YOUR_N2YO_API_KEY" # <-- REPLACE THIS VALUE
            # ...
    ```

### 4\. Running the Application

  - **Development Server:**
    To run the application using Flask's built-in development server:

    ```bash
    python app.py
    ```

    Open your web browser and navigate to `http://127.0.0.1:5000/`.

  - **Production Server:**
    For a production environment, use a WSGI server like Gunicorn (included in `requirements.txt`):

    ```bash
    gunicorn --bind 0.0.0.0:8000 app:app
    ```

-----

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.