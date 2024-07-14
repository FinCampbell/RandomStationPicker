import os

from flask import Flask, jsonify, render_template, request

import api_client
import find_reachable_stations

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_health')
def check_health():
    try:
        healthy = api_client.check_health()
        return jsonify({'healthy': healthy})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stations_by_query', methods=['POST'])
def stations_by_query():
    try:
        query = request.form['query']
        stations = api_client.get_stations_by_query(query)
        return jsonify(stations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/station_by_id', methods=['POST'])
def station_by_id():
    try:
        station_id = request.form['station_id']
        station = api_client.get_station_by_id(station_id)
        return jsonify(station)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reachable_stations', methods=['POST'])
def reachable_stations():
    try:
        station_id = request.form['station_id']
        local_trains_only = request.form['local_trains_only'].lower() == 'yes'
        stations = api_client.get_reachable_stations_dict(station_id, local_trains_only)
        return jsonify(stations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reachable_stations_by_name', methods=['POST'])
def reachable_stations_by_name():
    try:
        station_name = request.form['station_name']
        total_duration = 24
        reachable_stations = find_reachable_stations.find_reachable_stations(station_name, total_duration)
        return jsonify(reachable_stations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reachable_stations_with_connections', methods=['POST'])
def reachable_stations_with_connections():
    try:
        station_name = request.form['station_name']
        total_duration = int(request.form['total_duration'])
        journey = find_reachable_stations.find_reachable_stations_with_connections(station_name, total_duration)
        return jsonify(journey)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/international_station')
def international_station():
    try:
        journey = find_reachable_stations.find_international_reachable_station_uk()
        return jsonify(journey)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)