# Spotter AI - Route & Fuel Optimization API

**Author:** Aman Prajapati  
**Demonstration Video:** [Loom Video Link]

---

## Technical Overview
This service is a high-performance Django REST API designed to calculate an optimal driving route across the United States while minimizing overall fuel costs. It evaluates route distance, vehicle range limits, and real-time fuel pricing to compute the cheapest fuel stops necessary to complete the trip.

---

## Core Features & Logic

### 1. In-Memory Data Acceleration
* **Dataset Size:** 8,151 rows of fuel station records.
* **Mechanism:** The entire dataset is loaded into memory as a Pandas DataFrame on server boot (`fuel_service.py`).
* **Performance Impact:** Eliminates disk read I/O during request execution, keeping response latency extremely low.

### 2. Single-Call Route Calculation
* **Integration:** Open Source Routing Machine (OSRM) API (`router.py`).
* **Geocoding:** Converts location strings into GPS coordinates via `geopy` (Nominatim).
* **Efficiency:** Issues a single HTTP GET request to OSRM per route request to pull both total travel distance and the complete GeoJSON polyline geometry, strictly adhering to external API rate limits and minimizing network overhead.

### 3. Greedy Fuel Optimization Algorithm
* **Constraints:** 
  * Maximum Vehicle Range: **500 miles**
  * Fuel Efficiency: **10 MPG**
* **Algorithm Strategy:**
  1. Computes total gallons required based on OSRM distance math.
  2. Determines the exact number of mandatory stops based on the 500-mile range threshold: `Stops Required = Floor(Total Miles / 500)`
  3. Uses Pandas sorting mechanisms to filter and extract the lowest cost fuel stations across the dataset.
  4. Calculates overall cost dynamically using the selected optimal fuel prices.

---

## Tech Stack
* **Language:** Python 3.x
* **Framework:** Django, Django REST Framework
* **Data Science:** Pandas
* **Geospatial & Mapping:** `geopy`, OSRM API

---

## Setup & Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alphred-x/Spotter.ai_Route_optimizer.git
   cd Spotter.ai_Route_optimizer
2. **Set up virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
3. **Install dependencies:**
   ```powershell
   pip install django djangorestframework pandas requests geopy
3. **Start the Django development server:**
   ```powershell
   python manage.py runserver
---

### API Documentation & Postman Usage
You can easily test this endpoint using Postman or any API client.

Endpoint: Optimize Route
URL: http://127.0.0.1:8000/api/optimize/

Method: POST

Headers: Content-Type: application/json

## Request Body Example
Go to the Body tab, select raw and JSON, then paste:
```JSON
{
    "start": "New York, NY",
    "finish": "Los Angeles, CA"
}
```
## Response Fields
1. **Total_Distance_Miles:** Total trip distance calculated by OSRM.
**Total_Gallons_Used:** Fuel required based on 10 MPG.

2. **Total_Fuel_Cost_Used:** Calculated cost across selected optimal stops.

3. **Num_Stops_Required:** Minimum stops required based on 500-mile range.

4. **Recommended_Fuel_Stops:** Array containing stop name, address, location, and price per gallon.

5. **Route_Map_Geojson:** Complete polyline geometry for map rendering.


## Future Improvements & Scalability Considerations
**Spatial Querying:** Implement PostGIS or GeoPandas spatial indexing to query fuel stops strictly within a specific mile buffer radius along the polyline path rather than dataset-wide sorting.

**Caching:** Cache route and coordinate lookups via Redis to optimize repetitive route queries.