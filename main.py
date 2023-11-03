import geopandas
from geopandas import GeoDataFrame
import json
from shapely.geometry import Point

countyMap:GeoDataFrame = geopandas.read_file('usa_counties.geojson')

def GetCountyAndState(latitude:float, longitude:float, map:GeoDataFrame) -> tuple[str,str]:
    # Create a point using coords
    point = Point(longitude, latitude)

    # converts the point to a GeoDataFrame
    points = geopandas.GeoDataFrame(geometry=[point])
    points.crs = map.crs

    # Perform the join
    result = geopandas.sjoin(points, map, predicate='within')

    # Reject if no state (or territory) value matches 
    if result.get('STATEFP').empty:
        return None
    
    # Get the county and state information
    code = result.get('STATEFP').iloc[0]
    with open('state_codes.json', 'r') as state_codes_file:
        state_codes:dict = json.load(state_codes_file)
    state = state_codes.get(code)
    county = result['NAME'].iloc[0]
    return f'{county}, {state}'



print(GetCountyAndState(41.0997803, -80.6495194, countyMap))
