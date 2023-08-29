function fetchData() {
    fetch('/get_data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('numPurchasers').textContent = data.num_purchasers;
            document.getElementById('numProducts').textContent = data.num_products;
            document.getElementById('totalQuantity').textContent = data.total_quantity;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

// Fetch data when the page loads
window.onload = fetchData;
// caender for dashboard
document.addEventListener('DOMContentLoaded', function() {
    var datepickerPopup = document.getElementById('datepicker-popup');
    var input = datepickerPopup.querySelector('input');

    var calendar = new FullCalendar.Calendar(input, {
        // Configuration options for FullCalendar
        // For example, you can specify events here
        initialView: 'dayGridMonth',
        events: [
            {
                title: 'Event 1',
                start: '2023-08-29'
            },
            // Add more events as needed
        ]
    });

    calendar.render();
});
