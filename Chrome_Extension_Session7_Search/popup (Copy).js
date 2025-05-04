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
              <a href="${url}" class="result-link" target="_blank">${url}</a><br>
              <strong>Description:</strong> ${description}
            `;

            resultsList.appendChild(listItem);

            const highlightPayload = [{ description }];

            const link = listItem.querySelector(".result-link");
            link.addEventListener("click", function (event) {
              chrome.tabs.create({ url }, function (tab) {
                chrome.scripting.executeScript({
                  target: { tabId: tab.id },
                  func: (highlightData) => {
                    localStorage.setItem("highlight_text", JSON.stringify(highlightData));
                  },
                  args: [highlightPayload]
                });

                chrome.scripting.executeScript({
                  target: { tabId: tab.id },
                  files: ["content.js"]
                });
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

