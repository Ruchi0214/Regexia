async function analyzeText() {
    const text = document.getElementById('inputText').value;
    const resultDiv = document.getElementById('results');
    
    if (!text) return alert("Please enter text first.");

    const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    });

    const data = await response.json();

    document.getElementById('scoreValue').innerText = data.bias_score + "%";
    document.getElementById('biasMessage').innerText = data.message;
    document.getElementById('attackWords').innerText = data.attack_terms.join(", ") || "None";
    document.getElementById('emoWords').innerText = data.emotional_terms.join(", ") || "None";

    resultDiv.classList.remove('hidden');
}