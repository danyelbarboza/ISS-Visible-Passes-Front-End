
# ISS Visible Passes Web Application

Track upcoming visible passes of the International Space Station (ISS) from anywhere in the world with this web application. ISS Visible Passes combines orbital data from N2YO with weather forecasts from Open-Meteo to provide you with the best viewing opportunities. Simply enter a city, and the system will return upcoming ISS passes, detailing weather conditions and a visibility score for each.

The application features a user-friendly interface built with Flask and a responsive design based on the Fractal template by HTML5 UP.

---

## Features

-   **City to Coordinates Conversion**: Automatically converts city names into geographical coordinates using the Nominatim API.
-   **ISS Pass Times**: Fetches upcoming ISS pass times for the specified location via the N2YO API.
-   **Weather Conditions**: Retrieves weather forecasts (temperature, cloud cover, visibility, humidity) for the exact time of each pass using the Open-Meteo API.
-   **Visibility Evaluation**: Each pass is assigned a visibility score based on factors like cloud cover, humidity, pass duration, temperature, and weather visibility to help you choose the optimal viewing times.
-   **Dynamic Timezone Conversion**: Converts UTC pass times to the user's local time (defaulting to GMT-3, configurable).
-   **API Response Caching**: Implements caching for Open-Meteo API responses to improve performance and reduce redundant calls.
-   **User-Friendly Web Interface**: Provides an intuitive web page for inputting location and viewing results.

---

## Tech Stack

**Frontend:**
-   HTML5
-   CSS3 (including assets from Fractal by HTML5 UP)
-   JavaScript

**Backend:**
-   Python 3
-   Flask (Web Framework)

**APIs Utilized:**
-   [N2YO](https://www.n2yo.com/api/) (ISS orbital data)
-   [Nominatim](https://nominatim.org/release-docs/develop/api/Search/) (Geocoding)
-   [Open-Meteo](https://open-meteo.com/en/docs) (Weather Forecasts)

**Key Python Libraries:**
-   `Flask`
-   `requests` + `requests_cache` (for API communication and caching)
-   `pandas` (for weather data processing)
-   `python-dotenv` (for environment variable management)
-   `openmeteo_requests` (Open-Meteo API client library)
-   `gunicorn` (WSGI HTTP Server for production)

---

## Project Structure

The project is organized into several Python modules:

-   `app.py`: The main Flask application file that handles routing and serves web pages.
-   `controler.py`: Contains the core logic for fetching and processing data from various services. It uses the client modules to get coordinates, ISS passes, and weather, then evaluates pass visibility.
-   `config.py`: Manages configuration variables such as API endpoints, default observer altitude, and N2YO API parameters. It intends to load sensitive data like API keys from an environment file.
-   `n2yo_client.py`: A client module to interact with the N2YO API for ISS pass data.
-   `nominatim_client.py`: A client module for the Nominatim API to perform geocoding.
-   `openmeteo_client.py`: A client module for the Open-Meteo API to fetch weather forecasts.
-   `templates/`: Contains HTML templates (`index.html` for the main page, `result.html` for displaying pass information).
-   `static/`: Contains static assets like CSS, JavaScript, and images.

---

## Quick Start

### 1. Prerequisites
-   Python 3.x
-   pip (Python package installer)

### 2. Setup
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/danyelbarboza/ISS-Visible-Passes-Front-End.git](https://github.com/danyelbarboza/ISS-Visible-Passes-Front-End.git)
    cd ISS-Visible-Passes-Front-End
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This will install all necessary packages including Flask, Requests, Pandas, etc.

### 3. Configuration
Create a `.env` file in the root directory of the project. This file will store your API key and other configurations.
   ```ini
   # .env
   API_KEY=YOUR_N2YO_API_KEY
   OBSERVER_ALT=0
   DAYS=10
   MIN_VISIBILITY_N2YO=60
   GMT_OFFSET=-3
````

  - `API_KEY`: Your personal API key from [N2YO.com](https://www.n2yo.com/api/). The application calls `load_dotenv()`, but ensure the `N2yoClient` (or `Config` class) correctly uses `os.getenv("API_KEY")` to fetch this value.
  - `OBSERVER_ALT`: Observer's altitude in meters (default is `0`).
  - `DAYS`: Number of days to fetch ISS passes for (default is `10`).
  - `MIN_VISIBILITY_N2YO`: Minimum duration in seconds for an ISS pass to be considered visible by the N2YO API (default is `60`).
  - `GMT_OFFSET`: Your local GMT offset (e.g., `-3` for GMT-3). This is used for converting UTC times from N2YO to local time.

### 4\. Running the Application

  - **Development Server:**
    To run the application using Flask's built-in development server:

    ```bash
    python app.py
    ```

    Open your web browser and go to `http://127.0.0.1:5000/`.

  - **Production (Optional):**
    For a production environment, it's recommended to use a WSGI server like Gunicorn (which is included in `requirements.txt`):

    ```bash
    gunicorn app:app
    ```

-----

## How It Works

1.  The user visits the homepage, which presents a brief introduction and a search form.
2.  The user enters a city name (e.g., "New York, NY") into the search field and submits the form.
3.  The Flask backend (`app.py`) receives the city name.
4.  The `controler.py` module:
      * Uses `NominatimClient` to convert the city name to latitude and longitude.
      * If coordinates are found, it uses `N2yoClient` to fetch upcoming ISS visual passes for those coordinates, considering the configured number of days and minimum visibility duration.
      * For each pass, it uses `OpenMeteoClient` to get the weather forecast (temperature, cloud cover, visibility, humidity, and whether it's day or night) for the precise start time of the pass.
      * It then calculates a custom "visibility score" for each pass based on these weather parameters and pass duration.
5.  The collected and processed data (pass details, weather, and scores) are sent to the `result.html` template.
6.  The results page displays the list of ISS passes for the chosen city, along with their respective weather conditions and visibility scores, allowing the user to identify the best viewing opportunities.

-----

## License

**MIT License** - This project is open source and available for use and modification. See the `LICENSE` file for more details.