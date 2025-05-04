document.addEventListener("DOMContentLoaded", function () {
  const searchBtn = document.getElementById("searchBtn");

  searchBtn.addEventListener("click", function () {
    const query = document.getElementById("query").value;

    if (!query) {
      alert("Please enter a query!");
      return;
    }

    chrome.runtime.sendMessage({ action: "search_query", query: query }, function (response) {
      const resultsList = document.getElementById("resultsList");
      resultsList.innerHTML = "";

      console.log("Response from backend:", response);

      if (chrome.runtime.lastError) {
        console.error('Runtime error:', chrome.runtime.lastError.message);
        resultsList.innerHTML = "<li>Failed to get response from background script.</li>";
        return;
      }

      if (response && typeof response.answer === "string") {
        const finalPrefix = "FINAL_ANSWER: ";
        if (response.answer.startsWith(finalPrefix)) {
          try {
            const jsonStr = response.answer.slice(finalPrefix.length);
            const parsed = JSON.parse(jsonStr); // parsed = [description, url]

            const description = parsed[0];
            const url = parsed[1];

            const listItem = document.createElement("li");
            listItem.innerHTML = `
              <a href="#" class="result-link" data-url="${url}">${url}</a><br>
              <strong>Description:</strong> ${description}
            `;

            resultsList.appendChild(listItem);

            const link = listItem.querySelector(".result-link");
            link.addEventListener("click", function (event) {
              event.preventDefault();

              const targetUrl = event.target.getAttribute("data-url");
              const highlightPayload = [{ description }];

              // Save highlight text to chrome.storage.local
              chrome.storage.local.set({ highlight_text: JSON.stringify(highlightPayload) }, function () {
                // Open the target URL in a new tab (to avoid chrome:// error)
                chrome.tabs.create({ url: targetUrl });
              });
            });

          } catch (e) {
            console.error("Failed to parse FINAL_ANSWER:", e);
            resultsList.innerHTML = "<li>Invalid result format.</li>";
          }
        } else {
          resultsList.innerHTML = "<li>Unexpected format: missing FINAL_ANSWER.</li>";
        }
      } else {
        resultsList.innerHTML = "<li>No results found or unexpected response format.</li>";
      }
    });
  });
});

