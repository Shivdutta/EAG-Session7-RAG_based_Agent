// ====== Blocked domains ======
const blockedDomains = [
  "web.whatsapp.com",
  "gmail.com",
  "mail.google.com",
  "drive.google.com",
  "docs.google.com",    
  "http://localhost:8000",
  "http://www.google.com/",
  "https://www.google.com/",
  "http://chatgpt.com/",
  "https://chatgpt.com/"
];

// ====== Check if a URL is blocked ======
function isBlocked(url) {
  try {
    const hostname = new URL(url).hostname;
    return blockedDomains.some(domain => hostname.includes(domain));
  } catch (e) {
    return true;
  }
}

// ====== Validate URL ======
function isValidUrl(url) {
  return !url.startsWith("chrome://") && !url.startsWith("about://");
}

// ====== Function to clean the HTML content ======
function cleanHtmlContent(html) {
  const doc = new DOMParser().parseFromString(html, 'text/html');
  
  // Remove script and style tags, and get just the text content
  const scripts = doc.querySelectorAll('script, style');
  scripts.forEach(script => script.remove());

  // Get the clean text content
  const textContent = doc.body.innerText;

  // Optional: Remove extra whitespace
  return textContent.replace(/\s+/g, ' ').trim();
}

// ====== Main logic: handle tab updates ======
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (
    changeInfo.status === "complete" &&
    tab.url &&
    tab.title &&
    !isBlocked(tab.url) &&
    isValidUrl(tab.url)
  ) {
    // Inject content script to get the HTML content of the page
    chrome.tabs.executeScript(tabId, { file: 'content.js' }, () => {
      // After injecting, get HTML content from content.js (it will be injected in the page)
      chrome.tabs.sendMessage(tabId, { action: "getHtmlContent" }, (response) => {
        if (response && response.htmlContent) {
          // Clean the HTML content before saving
          // const cleanedText = cleanHtmlContent(response.htmlContent);
          const cleanedText = response.htmlContent;

          const payload = {
            url: tab.url,
            text: cleanedText,
            title : tab.title
          };

          console.log("Cleaned Data to be sent:", payload);

          fetch('http://localhost:8001/add_to_index', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
          })
          .then(response => response.json())
          .then(responseData => {
            console.log("API Response:", responseData);
          })
          .catch(error => {
            console.error("Error sending data to API:", error);
          });

          // Save visit in local storage
          chrome.storage.local.get({ visits: [] }, (storageResult) => {
            const visits = storageResult.visits;
            visits.push(payload);
            chrome.storage.local.set({ visits });
          });
        }
      });
    });
  }
});
