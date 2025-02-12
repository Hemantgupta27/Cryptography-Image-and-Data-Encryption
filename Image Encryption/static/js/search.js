

// Function to fetch patient data
async function fetchPatientData() {
    const visitId = document.getElementById("visitId").value;
    if (!visitId) {
        alert("Please enter a valid Visit ID.");
        return;
    }

    try {
        // Fetch data from the Python backend
        const response = await fetch(`/fetch_patient_data/${visitId}`);
        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const data = await response.json();
        updateHTMLWithDecryptedData(data);
    } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to fetch patient data. Please check the Visit ID or try again later.");
    }
}

// Function to update HTML with decrypted data
function updateHTMLWithDecryptedData(data) {
    // Update patient image if available
    const patientImage = document.getElementById("patientImage");
    if (data.image_data) {
        patientImage.src = `data:image/jpeg;base64,${data.image_data}`;
        patientImage.alt = "Decrypted Patient Image";
    } else {
        patientImage.src = "";
        patientImage.alt = "No Image Available";
    }

    // Update form data fields
    document.getElementById("firstName").textContent = data.form_data?.["First Name"] || "N/A";
    document.getElementById("lastName").textContent = data.form_data?.["Last Name"] || "N/A";
    document.getElementById("dateOfBirth").textContent = data.form_data?.["Date of Birth"] || "N/A";
    document.getElementById("bloodGroup").textContent = data.form_data?.["Blood Group"] || "N/A";
    document.getElementById("gender").textContent = data.form_data?.["Gender"] || "N/A";
    document.getElementById("contactInfo").textContent = data.form_data?.["Contact Info"] || "N/A";
    document.getElementById("state").textContent = data.form_data?.["State"] || "N/A";

    // Update clinical information fields
    document.getElementById("visitId").textContent = data.form_data?.["Visit ID"] || "N/A";
    document.getElementById("visitDate").textContent = data.form_data?.["Visit Date"] || "N/A";
    document.getElementById("visitTime").textContent = data.form_data?.["Visit Time"] || "N/A";
    document.getElementById("doctorName").textContent = data.form_data?.["Doctor"] || "N/A";
    document.getElementById("specialty").textContent = data.form_data?.["Specialty"] || "N/A";
    document.getElementById("diagnosis").textContent = data.form_data?.["Diagnosis"] || "N/A";

    // Update medical reports
    const medicalReportContainer = document.getElementById("medicalReportContainer");
    medicalReportContainer.innerHTML = ""; // Clear previous reports
    if (data.report_data?.length) {
        data.report_data.forEach((reportBase64, index) => {
            const img = document.createElement("img");
            img.src = `data:image/jpeg;base64,${reportBase64}`;
            img.alt = `Decrypted Medical Report ${index + 1}`;
            img.style.maxWidth = "100%";
            medicalReportContainer.appendChild(img);
        });
    } else {
        medicalReportContainer.textContent = "No medical reports available.";
    }

    // Update medical history fields
    document.getElementById("medicalConditions").textContent = data.form_data?.["Past Medical Conditions"] || "N/A";
    document.getElementById("currentMedications").textContent = data.form_data?.["Current Medications"] || "N/A";
    document.getElementById("allergies").textContent = data.form_data?.["Allergies"] || "N/A";
    document.getElementById("immunizations").textContent = data.form_data?.["Immunization Records"] || "N/A";
}
