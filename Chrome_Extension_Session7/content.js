// Listen for the background script to request the page's HTML content
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getHtmlContent") {
    // Send the page's HTML content back to the background script
    sendResponse({ htmlContent: document.documentElement.outerHTML });
  }
});
