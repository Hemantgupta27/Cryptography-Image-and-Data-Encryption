document.getElementById('add-patient').addEventListener('click', function(event) {
    event.preventDefault();  // Prevent default anchor behavior
    window.location.href = "/add-patient";  // Navigate to the "Add Patient" page
});

document.getElementById('search-patient').addEventListener('click', function(event) {
    event.preventDefault();  // Prevent default anchor behavior
    window.location.href = "/search-patient";  // Navigate to the "Search Patient" page
});