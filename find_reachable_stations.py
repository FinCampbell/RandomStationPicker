# pyright: reportUndefinedVariable=false, reportGeneralTypeIssues=false

import random

import api_client


def simplify_station_name(station_name):
    """Simplify station name to extract city name."""
    # Heuristic approach: Split by spaces, take first part
    # Customize this based on actual naming conventions
    return station_name.split()[0]


def find_reachable_stations(station_name, total_duration):
    """Finds stations by name, lets the user choose one, and returns a random reachable station within the specified duration."""
    stations = api_client.get_stations_by_query(station_name)
    if stations:
        selection = stations[0]  # Choose the first station
        station_id = selection['id']
        reachable_stations = api_client.get_reachable_stations_dict(station_id)
        if "reachable_stations" in reachable_stations:
            filtered_stations = [
                station for station in reachable_stations['reachable_stations']
                if station['duration'] <= total_duration
            ]
            if filtered_stations:
                next_station = random.choice(filtered_stations)
                return next_station
            else:
                print(
                    f"No reachable stations within {total_duration} hours found for {selection['name']}"
                )
                return None
        else:
            print(f"No reachable stations found for {selection['name']}")
            return None
    else:
        print(f"Station '{station_name}' not found.")
        return None


def find_reachable_stations_with_connections(station_name, total_duration):
    """Finds stations by name and returns a random reachable station within a specified time with possible connections while avoiding revisiting cities."""
    stations = api_client.get_stations_by_query(station_name)
    if stations:
        selection = stations[0]  # Choose the first station
        station_id = selection['id']
        start_city = simplify_station_name(selection['name'])
        max_connections = random.randint(2, 4)
        print(f"Planning a journey with up to {max_connections} connections.")
        current_duration = 0
        current_station_id = station_id
        journey = []
        visited_cities = set()
        visited_cities.add(start_city)
        connection_count = 0
        last_possible_connections = []
        last_station_id = '0000000'
        while current_duration < total_duration and connection_count < max_connections:
            remaining_time = total_duration - current_duration
            avg_duration_per_connection = remaining_time / (max_connections -
                                                            connection_count)

            reachable_stations = api_client.get_reachable_stations_dict(
                current_station_id)
            if "reachable_stations" in reachable_stations:
                filtered_stations = [
                    station
                    for station in reachable_stations['reachable_stations']
                    if (avg_duration_per_connection / 2 <= station['duration']
                        <= avg_duration_per_connection * 1.5) and (
                            simplify_station_name(
                                station['name']) not in visited_cities)
                ]

                if not filtered_stations:
                    print(
                        f"No more reachable stations within the remaining time. Current duration: {current_duration} hours."
                    )
                    break

                filtered_stations = [
                    station for station in filtered_stations
                    if station["name"] not in last_possible_connections
                ]

                if not filtered_stations:
                    print(
                        f"No more reachable stations within the remaining time. Current duration: {current_duration} hours."
                    )
                    break

                next_station = random.choice(filtered_stations)
                print(next_station)
                journey.append(next_station)
                current_duration += next_station['duration']
                visited_cities.add(simplify_station_name(next_station['name']))

                for station in reachable_stations["reachable_stations"]:
                    last_possible_connections.append(station["name"])

                current_station_id = next_station['id']
                connection_count += 1
            else:
                print(
                    f"No reachable stations found for station ID {current_station_id}"
                )
                break
        if journey:
            print("Journey details:")
            for stop in journey:
                print(
                    f" - {stop['name']} (ID: {stop['id']}), Duration: {stop['duration']} hours"
                )
            return journey
        else:
            print(
                f"Could not complete the journey within {total_duration} hours."
            )
            return None
    else:
        print(f"Station '{station_name}' not found.")
        return None


def find_international_reachable_station_uk():
    """Finds one international reachable station from London St Pancras."""
    starting_station_name = "London St Pancras"
    starting_station_id = "7001424"  # Replace this with the real station ID of London St Pancras if different
    # Query the starting station
    stations = api_client.get_stations_by_query(starting_station_name)
    if not stations:
        print(f"Station '{starting_station_name}' not found.")
        return None

    # Ensure we have the correct starting station
    starting_station = next(
        (station
         for station in stations if station['id'] == starting_station_id),
        None)
    if not starting_station:
        print(f"No matching station ID for '{starting_station_name}'.")
        return None
    # Get reachable stations for the starting station
    reachable_stations = api_client.get_reachable_stations_dict(
        starting_station_id)
    if not reachable_stations or "reachable_stations" not in reachable_stations:
        print(
            f"No reachable stations found for station ID {starting_station_id}."
        )
        return None
    # Filter out domestic stations (IDs starting with '7')
    international_stations = [
        station for station in reachable_stations['reachable_stations']
        if not station['id'].startswith('7')
    ]
    if not international_stations:
        print(
            f"No international reachable stations found from {starting_station_name}."
        )
        return None
    # Select a random international station
    next_station = random.choice(international_stations)
    # Print and return the journey details
    print("Journey details:")
    print(
        f" - {next_station['name']} (ID: {next_station['id']}), Duration: {next_station['duration']} hours"
    )
    return next_station
