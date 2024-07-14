function updateResult(result) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = ''; // Clear previous results
    
    if (typeof result === 'string') {
        resultDiv.innerHTML = `<p>${result}</p>`;
    } else if (Array.isArray(result)) {
        result.forEach(item => {
            const div = document.createElement('div');
            div.className = 'result-item';
            div.innerHTML = JSON.stringify(item, null, 2);
            resultDiv.appendChild(div);
        });
    } else {
        const div = document.createElement('div');
        div.className = 'result-item';
        div.innerHTML = JSON.stringify(result, null, 2);
        resultDiv.appendChild(div);
    }
}

function handleFormSubmit(event, endpoint) {
    event.preventDefault();
    const formData = new FormData(event.target);
    
    fetch(endpoint, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => updateResult(data))
    .catch(error => {
        console.error('Error:', error);
        updateResult('An error occurred');
    });
}

function showQueryForm() {
    document.getElementById('form-container').innerHTML = `
        <div class="container">
            <form onsubmit="handleFormSubmit(event, '/stations_by_query')">
                <label for="query">Enter your query:</label>
                <input type="text" name="query" placeholder="Enter your query">
                <button type="submit">Submit</button>
            </form>
        </div>
    `;
}

function showIdForm() {
    document.getElementById('form-container').innerHTML = `
        <div class="container">
            <form onsubmit="handleFormSubmit(event, '/station_by_id')">
                <label for="station_id">Enter station ID:</label>
                <input type="text" name="station_id" placeholder="Enter station ID">
                <button type="submit">Submit</button>
            </form>
        </div>
    `;
}

function showReachableStationsForm() {
    document.getElementById('form-container').innerHTML = `
        <div class="container">
            <form onsubmit="handleFormSubmit(event, '/reachable_stations')">
                <label for="station_id">Enter station ID:</label>
                <input type="text" name="station_id" placeholder="Enter station ID">
                <label for="local_trains_only">Include only local trains?</label>
                <select name="local_trains_only">
                    <option value="no">No</option>
                    <option value="yes">Yes</option>
                </select>
                <button type="submit">Submit</button>
            </form>
        </div>
    `;
}

function showNameForm() {
    document.getElementById('form-container').innerHTML = `
        <div class="container">
            <form onsubmit="handleFormSubmit(event, '/reachable_stations_by_name')">
                <label for="station_name">Enter station name:</label>
                <input type="text" name="station_name" placeholder="Enter station name">
                <button type="submit">Submit</button>
            </form>
        </div>
    `;
}

function showConnectionsForm() {
    document.getElementById('form-container').innerHTML = `
        <div class="container">
            <form onsubmit="handleFormSubmit(event, '/reachable_stations_with_connections')">
                <label for="station_name">Enter station name:</label>
                <input type="text" name="station_name" placeholder="Enter station name">
                <label for="total_duration">Enter total duration in hours:</label>
                <input type="number" name="total_duration" placeholder="Enter total duration in hours">
                <button type="submit">Submit</button>
            </form>
        </div>
    `;
}