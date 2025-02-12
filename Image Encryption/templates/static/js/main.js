document.addEventListener('DOMContentLoaded', function() {
    const addPatientLink = document.querySelector('.menu-item a[href="patient.html"]');
    const searchPatientLink = document.querySelector('.menu-item a[href="s1.html"]');

    // Adding event listeners for confirmation
    addPatientLink.addEventListener('click', function(event) {
        const confirmAction = confirm("Are you sure you want to add a new patient?");
        if (!confirmAction) {
            event.preventDefault(); // Prevent navigation if user clicks 'Cancel'
        }
    });

    searchPatientLink.addEventListener('click', function(event) {
        const confirmAction = confirm("Do you want to search for a patient?");
        if (!confirmAction) {
            event.preventDefault(); // Prevent navigation if user clicks 'Cancel'
        }
    });
});
