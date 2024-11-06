async function checkSpelling() {
    const word = document.getElementById("wordInput").value;
    try {
        const response = await fetch("/.netlify/functions/check_spelling", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ word: word })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Clear previous results
        const resultElement = document.getElementById("result");
        resultElement.innerHTML = ""; // Clear previous suggestions
        
        // Loop through each correction and display
        if (data.corrections && Array.isArray(data.corrections)) {
            data.corrections.forEach(correction => {
                const item = document.createElement("p");
                item.innerText = `Suggested correction: ${correction.word} (Probability: ${correction.probability.toFixed(4)})`;
                resultElement.appendChild(item);
            });
        } else {
            resultElement.innerText = "No corrections found.";
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("result").innerText = "An error occurred while checking the spelling.";
    }
}
