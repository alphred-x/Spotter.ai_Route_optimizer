from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .router import get_coordinates, get_osrm_route
from .optimizer import calculate_optimal_fuel_stops

class RouteOptimizeView(APIView):
    def post(self, request):
        # 1. Get the start and finish locations from the user's request
        start_location = request.data.get('start')
        finish_location = request.data.get('finish')
        
        if not start_location or not finish_location:
            return Response(
                {"error": "Please provide both 'start' and 'finish' locations in the JSON body."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # 2. Convert city names to GPS coordinates
            start_coords = get_coordinates(start_location)
            finish_coords = get_coordinates(finish_location)
            
            # 3. Get the route distance and map geometry from OSRM
            distance_miles, route_geometry = get_osrm_route(start_coords, finish_coords)
            
            # 4. Calculate the optimal fuel stops and total cost
            fuel_data = calculate_optimal_fuel_stops(distance_miles)
            
            # 5. Send the final compiled data back to the user
            return Response({
                "start_location": start_location,
                "finish_location": finish_location,
                "total_distance_miles": round(distance_miles, 2),
                "total_gallons_used": fuel_data["total_gallons_used"],
                "total_fuel_cost_usd": fuel_data["total_fuel_cost_usd"],
                "num_stops_required": fuel_data["num_stops_required"],
                "recommended_fuel_stops": fuel_data["recommended_fuel_stops"],
                "route_map_geojson": route_geometry
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)