async function fetchAvailableSlots(date) {
    let response = await fetch(`/appointments/available-slots/${date}/`);

    if (!response.ok) {
        console.error("Error fetching slots:", response.status, response.statusText);
        let text = await response.text();  // Read response as text
        console.error("Response Text:", text); // Log it
        return;
    }

    let data = await response.json();
    let slotSelect = document.getElementById("time_slot");
    slotSelect.innerHTML = "";

    data.available_slots.forEach(slot => {
        let option = document.createElement("option");
        option.value = slot;
        option.textContent = slot;
        slotSelect.appendChild(option);
    });
}

function getCSRFToken() {
    let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return csrfToken ? csrfToken.value : "";
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("date").addEventListener("change", function () {
        fetchAvailableSlots(this.value);
    });

    document.getElementById("bookingForm").addEventListener("submit", async function (e) {
        e.preventDefault();
        let formData = new FormData(this);

        let response = await fetch("/appointments/book/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCSRFToken(),  // Send CSRF Token
                "X-Requested-With": "XMLHttpRequest",
            },
        });

        try {
            let text = await response.text();
            console.log("Raw Response:", text);

            let result = JSON.parse(text);
            alert(result.message);
        } catch (error) {
            alert("Error processing request.");
            console.error("JSON parsing error:", error);
        }
    });
});
