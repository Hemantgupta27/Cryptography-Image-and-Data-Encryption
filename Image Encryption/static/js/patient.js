// Function to show a specific form section and hide others
function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.form-section');
    sections.forEach(section => {
        section.classList.add('hidden');
    });

    // Show the desired section
    const sectionToShow = document.getElementById(sectionId);
    if (sectionToShow) {
        sectionToShow.classList.remove('hidden');
    }
}




// Function to check if the visit-id is unique (AJAX)
function checkVisitIdUniqueness(visitId, errorMessage) {
    fetch('/check_visit_id', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ visit_id: visitId })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.unique) {
            errorMessage.textContent = "Visit ID already exists. Please choose a different one.";
        } else {
            errorMessage.textContent = "";  // Clear the error message if unique
        }
    })
    .catch(error => {
        console.error('Error:', error);
        errorMessage.textContent = "An error occurred while checking the Visit ID.";
    });
}




// Function to handle form submission confirmation
function returnToForm() {
    
}

// Initialize the form to show the first section
document.addEventListener('DOMContentLoaded', function() {
    showSection('personal-info');  // Show the first section by default
});
