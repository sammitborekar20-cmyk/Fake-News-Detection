document.getElementById("checkButton").addEventListener("click", async () => {
    // Get text from current page
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        func: () => document.body.innerText
      }, async (results) => {
        const pageText = results[0].result;
  
        // Send text to your FastAPI backend
        const response = await fetch("http://127.0.0.1:8000/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: pageText })
        });
  
        const data = await response.json();
        document.getElementById("result").innerText = `🧠 Prediction: ${data.prediction}`;
      });
    });
  });  