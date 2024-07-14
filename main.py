import api_client
import find_reachable_stations


def main():
  """Main function for user interaction."""
  while True:
    print("\nChoose an action:")
    print("1. Check server health")
    print("2. Get stations by query")
    print("3. Get station by ID")
    print("4. Get reachable stations")
    print("5. Get reachable stations (by name)")
    print(
        "6. Find reachable station with connections (by name and total time)")
    print(
        "7. Find one international reachable station from London St Pancras (UK)"
    )
    print("8. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
      if api_client.check_health():
        print("Server is healthy.")
      else:
        print("Server is not healthy.")
    elif choice == '2':
      query = input("Enter your query: ")
      stations = api_client.get_stations_by_query(query)
      if stations:
        print(stations)
    elif choice == '3':
      station_id = input("Enter station ID: ")
      station = api_client.get_station_by_id(station_id)
      if station:
        print(station)
    elif choice == '4':
      station_id = input("Enter station ID: ")
      local_trains_only = input("Include only local trains? (yes/no): ")
      local_trains_only = local_trains_only.lower() == "yes"
      stations = api_client.get_reachable_stations_formatted(
          station_id, local_trains_only)
      if stations:
        print(stations)
    elif choice == '5':
      station_name = input("Enter station name: ")
      reachable_stations = find_reachable_stations.find_reachable_stations(
          station_name)
      if reachable_stations:
        print(reachable_stations)
    elif choice == '6':
      station_name = input("Enter station name: ")
      journey = find_reachable_stations.find_reachable_stations_with_connections(
          station_name)
      if journey:
        print("Journey completed successfully.")
    elif choice == '7':
      journey = find_reachable_stations.find_international_reachable_station_uk(
      )
      if journey:
        print("Journey completed successfully.")
    elif choice == '8':
      print("Exiting...")
      break
    else:
      print("Invalid choice. Please try again.")


if __name__ == "__main__":
  main()
