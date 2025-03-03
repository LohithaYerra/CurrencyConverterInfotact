// Handle form submission for currency conversion
document.getElementById("currency-form").addEventListener("submit", function(e) {
    e.preventDefault();  // Prevent form submission to avoid page reload

    // Get values from form
    var amount = document.getElementById("amount").value;
    var from_currency = document.getElementById("from-currency").value;
    var to_currency = document.getElementById("to-currency").value;

    // Create request data
    var data = {
        amount: amount,
        from_currency: from_currency,
        to_currency: to_currency
    };

    // Make AJAX request to backend
    fetch("/convert", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.converted_amount !== undefined) {
            // Update the converted amount input field
            document.getElementById("converted-amount").value = data.converted_amount;
        } else {
            alert(data.error);  // Show error message if conversion fails
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

// "Clear All" Button functionality
document.getElementById("clear-all-btn").addEventListener("click", function() {
    // Clear the amount input field
    document.getElementById("amount").value = '';

    // Reset currency select values to defaults
    document.getElementById("from-currency").value = 'USD';  // Reset to default currency
    document.getElementById("to-currency").value = 'INR';    // Reset to default currency

    // Clear the converted amount field
    document.getElementById("converted-amount").value = '';
});
