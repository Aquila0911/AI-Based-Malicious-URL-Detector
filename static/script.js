async function makePrediction() {
  const url = document.getElementById("urlInput").value;
  const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: url }),
  });
  const result = await response.json();
  const resultElement = document.getElementById("result");
  
  // Apply different colors based on the prediction
  if (result.prediction === "safe") {
    resultElement.innerHTML = `Prediction: <span style="color: green;">${result.prediction}</span>`;
  } else {
    resultElement.innerHTML = `Prediction: <span style="color: red;">${result.prediction}</span>`;
  }
}

function clearPrediction() {
  const resultElement = document.getElementById("result");
  resultElement.innerHTML = "";
}
