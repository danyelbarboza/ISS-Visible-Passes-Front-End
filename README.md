Claro\! Analisei o código do seu projeto e reescrevi o `README.md` para refletir com precisão a estrutura e a funcionalidade atuais. Também corrigi algumas pequenas inconsistências e adicionei notas importantes sobre a configuração.

Aqui está o `README.md` revisado em formato Markdown:

-----

# ISS Visible Passes Web Application

Track upcoming visible passes of the International Space Station (ISS) for any location with this web application. This tool combines orbital data from N2YO with weather forecasts from Open-Meteo to provide the best viewing opportunities. Simply enter a city, and the system will return upcoming ISS passes, detailing the specific weather conditions and a custom visibility score for each event.

The application features a user-friendly interface built with Flask and a responsive design based on the Fractal template by HTML5 UP.

-----

## How It Works

1.  A user enters a city name into the search form on the homepage.
2.  The Flask backend (`app.py`) receives the request and passes the city name to the controller.
3.  The `controller.py` module orchestrates the data retrieval and processing:
      * It uses the **Nominatim API** to convert the city name into geographic coordinates (latitude and longitude).
      * It then uses the **N2YO API** to fetch upcoming ISS visual passes for those coordinates. Pass times are converted from UTC to the local time defined in the application (currently GMT-3).
      * For each pass, the **Open-Meteo API** is queried to get a detailed weather forecast for the precise start time of the pass. This includes temperature, cloud cover, visibility, and humidity.
      * Finally, it calculates a custom **visibility score** (from 0 to 10) for each pass based on weather parameters and pass duration, helping the user quickly identify the best viewing times.
4.  The processed data is rendered on the results page, displaying a list of passes with their corresponding weather conditions and visibility scores.

-----

## Features

  - **City to Coordinates Conversion**: Automatically converts city names into geographical coordinates using the Nominatim API.
  - **ISS Pass Times**: Fetches upcoming ISS pass times for the specified location from the N2YO API.
  - **Specific Weather Conditions**: Retrieves weather forecasts (temperature, cloud cover, visibility, humidity) for the exact time of each pass using the Open-Meteo API.
  - **Visibility Score**: Each pass is assigned a unique visibility score based on cloud cover, humidity, pass duration, and weather visibility to help you choose the optimal viewing times.
  - **Timezone Conversion**: Converts UTC pass times from the N2YO API to a local timezone.
  - **API Response Caching**: Implements caching for Open-Meteo API responses to improve performance and reduce redundant calls.
  - **User-Friendly Web Interface**: Provides an intuitive interface for inputting a location and viewing results, built on a responsive HTML5 UP template.

-----

## Tech Stack

**Backend:**

  - Python 3
  - Flask (Web Framework)

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
  - `gunicorn` (for production)
    (See `requirements.txt` for a full list).

-----

## Project Structure

  - `app.py`: The main Flask application file that handles routing and renders the HTML templates.
  - `src/controller/controller.py`: Contains the core logic for fetching and processing data from all external APIs. It coordinates the client modules and calculates the visibility score.
  - `src/config/config.py`: Manages configuration variables. 
  - `src/clients/n2yo_client.py`: A client module to interact with the N2YO API for ISS pass data.
  - `src/clients/nominatim_client.py`: A client module for the Nominatim API to perform geocoding.
  - `src/clients/openmeteo_client.py`: A client module for the Open-Meteo API to fetch weather forecasts.
  - `templates/`: Contains the Jinja2 HTML templates (`index.html` and `result.html`).
  - `static/`: Contains static assets like CSS, JavaScript, and images.

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

Configuration is currently handled via hardcoded values in the source files. To run the application, you must add your N2YO API key.

1.  **Add Your N2YO API Key:**

      - Open the file `src/config/config.py`.
      - Replace the placeholder string in the line `self.api_key = "YOUR_N2YO_API_KEY"` with your actual key from [N2YO.com](https://www.n2yo.com/api/).

    <!-- end list -->

    ```python
    # In src/config/config.py
    class Config:
        def __init__(self, latitude, longitude):
            load_dotenv()
            self.norad_id = 25544
            self.latitude = float(latitude)
            self.longitude = float(longitude)
            self.observer_alt = 0
            self.days = 10
            self.min_visibility = 60
            # --- REPLACE THIS VALUE ---
            self.api_key = "YOUR_N2YO_API_KEY"
            self.gmt = -3
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