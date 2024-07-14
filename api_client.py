import requests


def check_health():
  """Checks the health of the server."""
  response = requests.get("https://api.direkt.bahn.guru/health")
  return response.status_code == 200


def get_stations_by_query(query):
  """Gets a list of stations based on a query."""
  response = requests.get(
      f"https://api.direkt.bahn.guru/stations?query={query}")
  if response.status_code == 200:
    return response.json()
  else:
    print("Error getting stations by query.")
    return None


def get_station_by_id(station_id):
  """Gets information about a specific station by its ID."""
  response = requests.get(
      f"https://api.direkt.bahn.guru/stations/{station_id}")
  if response.status_code == 200:
    return response.json()
  else:
    print("Error getting station by ID.")
    return None


def get_reachable_stations(station_id, local_trains_only=False):
  """Gets a list of stations reachable from a given station."""
  url = f"https://api.direkt.bahn.guru/{station_id}"
  params = {"localTrainsOnly": local_trains_only}
  response = requests.get(url, params=params)
  if response.status_code == 200:
    return response.json()
  else:
    print("Error getting reachable stations.")
    return None


def get_reachable_stations_formatted(station_id, local_trains_only=False):
  """Gets a list of stations reachable from a given station and formats the output."""
  stations = get_reachable_stations(station_id, local_trains_only)
  if stations:
    print("Reachable Stations:")
    for station in stations:
      print(f" - {station['name']} (ID: {station['id']})")
      print(f" - {station['duration']/60} hours")
  else:
    print("Error getting reachable stations.")


def get_reachable_stations_dict(station_id, local_trains_only=False):
  """Gets a list of stations reachable from a given station and formats the output
  as a Python dictionary."""
  stations = get_reachable_stations(station_id, local_trains_only)
  if stations:
    formatted_stations = []
    for station in stations:
      formatted_station = {
          "name": station['name'],
          "id": station['id'],
          "duration":
          station['duration'] / 60  # Assuming duration is in seconds
      }
      formatted_stations.append(formatted_station)
    return {"reachable_stations": formatted_stations}
  else:
    return {"error": "Error getting reachable stations."}
