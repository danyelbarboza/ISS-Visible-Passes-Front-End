# ISS-Visible-Passes

This Python tool checks visible ISS (International Space Station) passes for any location, combining orbital data from N2YO with weather forecasts from Open-Meteo. Users enter a city name, and the system returns upcoming passes filtered by cloud cover and visibility, with UTC-to-local time conversion. Built with Python, Requests, and Pandas, it's designed for easy expansion to web interfaces or additional satellites.

---

## Features Implemented

- ✅ Converts city names to coordinates (**Nominatim API**)
- ✅ Fetches ISS pass times (**N2YO API**)
- ✅ Checks weather conditions for each pass (**Open-Meteo API**)
- ✅ Filters passes by cloud cover and visibility
- ✅ Dynamic timezone conversion
- ✅ Caching for API responses

---

## Tech Stack

**Backend:** Python 3

### APIs Utilized
- [N2YO](https://www.n2yo.com/api/) (ISS orbital data)
- [Nominatim](https://nominatim.org/release-docs/develop/api/Search/) (Geocoding)
- [Open-Meteo](https://open-meteo.com/en/docs) (Weather)

### Key Libraries
- `requests` + `requests_cache`
- `pandas` (for weather data processing)
- `python-dotenv`

**Configuration:** Environment variables (`.env`)

---

## ⚡ Quick Start

### 1. Setup

```bash
git clone https://github.com/yourusername/ISS-Tracker-Weather.git
cd ISS-Tracker-Weather
pip install requests requests_cache pandas python-dotenv openmeteo-api retry-requests
```

### 2. Configuration

Create a `.env` file in the root directory:

```ini
API_KEY=your_n2yo_api_key
observer_alt=0
days=10
min_visibility=1
gmt=-3
```

### 3. Run

```bash
python main.py
```

---

## Sample Output

```plaintext
Passagem 1:
  Horário: 2023-10-25T19:30 (Duração: 6 minutos)
  Clima:
    Temperatura: 22.5°C
    Nuvens: 20%
    Visibilidade: 12.4 km
    Período: Day
----------------------------------
Passagem 2:
  Horário: 2023-10-25T21:15 (Duração: 4 minutos)
  Clima:
    Temperatura: 18.2°C
    Nuvens: 90%
    Visibilidade: 1.2 km
    Período: Night
```

---

## License

**MIT License** - Available for use and modification. See the LICENSE file for details.