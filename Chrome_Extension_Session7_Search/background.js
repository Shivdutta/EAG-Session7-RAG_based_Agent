chrome.runtime.onInstalled.addListener(() => {
  console.log("Web History Search Extension installed.");
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "search_query") {
    fetch("http://127.0.0.1:8000/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        query: message.query,
        top_k: 1
      })
    })
    .then(res => res.json())
    .then(data => {
      sendResponse(data);
    })
    .catch(error => {
      console.error("Fetch error:", error);
      sendResponse({ result: [], error: "Fetch failed" });
    });

    // Ensure the response is kept open
    return true;
  }

  // Return false for other messages
  return false;
});
