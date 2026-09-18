import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Initialize the geocoder (Nominatim uses OpenStreetMap data)
geolocator = Nominatim(user_agent="spotter_route_optimizer_v1")

def get_coordinates(location_str):
    """Converts a city/address string into (latitude, longitude)."""
    try:
        loc = geolocator.geocode(location_str, timeout=10)
        if not loc:
            raise ValueError(f"Could not find coordinates for location: {location_str}")
        return loc.latitude, loc.longitude
    except GeocoderTimedOut:
        raise BaseException("Geocoding service timed out. Please try again.")

def get_osrm_route(start_coords, finish_coords):
    """
    Calls the free OSRM API to get the route geometry and total distance.
    OSRM expects coordinates in longitude,latitude format.
    """
    start_lon, start_lat = start_coords[1], start_coords[0]
    finish_lon, finish_lat = finish_coords[1], finish_coords[0]
    
    url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{finish_lon},{finish_lat}?overview=full&geometries=geojson"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Failed to fetch route from OSRM API.")
        
    data = response.json()
    
    if data.get('code') != 'Ok':
        raise Exception("OSRM could not calculate a route between these points.")
        
    route = data['routes'][0]
    
    # OSRM returns distance in meters. Convert to miles.
    distance_miles = route['distance'] * 0.000621371
    geometry = route['geometry']  # This is the GeoJSON path for the map
    
    return distance_miles, geometry