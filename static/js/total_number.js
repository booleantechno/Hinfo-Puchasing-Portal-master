function fetchData() {
    fetch('/get_data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('numPurchasers').textContent = data.num_purchasers;
            document.getElementById('totalQuantity').textContent = data.total_quantity;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

// Fetch data when the page loads
window.onload = fetchData;
