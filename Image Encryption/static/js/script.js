// // Attach event listener to the "Sign in" button
// document.querySelector("button").addEventListener("click", validateAndSignIn);

// // Function to validate input fields and send data to the backend
// async function validateAndSignIn() {
//     // Get username and password input values
//     const username = document.getElementById("username").value.trim();
//     const password = document.getElementById("password").value;

//     // Input validation
    
//     try {
//         // Send data to the Flask backend
//         const response = await fetch("/login", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({ username, password }),
//         });

//         // Parse the JSON response
//         const result = await response.json();

//         if (response.ok) {
//             alert(result.message);
//             window.location.href = "/main"; // Redirect to Flask route
//         } else {
//             alert(result.error);
//         }
//     } catch (error) {
//         // Handle network or server errors
//         alert("An error occurred while signing in. Please try again later.");
//         console.error("Error:", error);
//     }
// }

// // Show or hide the password based on the checkbox state
// document.getElementById("show-password").addEventListener("change", function () {
//     const passwordInput = document.getElementById("password");
//     passwordInput.type = this.checked ? "text" : "password";
// });



document.querySelector("button").addEventListener("click", validateAndSignIn);

async function validateAndSignIn() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    if (!username || !password) {
        alert("Please enter both username and password.");
        return;
    }

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message);
            window.location.href = "/main"; // Flask route
        } else {
            alert(result.error);
        }
    } catch (error) {
        alert("An error occurred. Please try again.");
        console.error("Error:", error);
    }
}

document.getElementById("show-password").addEventListener("change", function () {
    const passwordInput = document.getElementById("password");
    passwordInput.type = this.checked ? "text" : "password";
});
