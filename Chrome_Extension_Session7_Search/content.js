window.addEventListener("load", () => {
  chrome.storage.local.get("highlight_text", (result) => {
    if (result.highlight_text) {
      try {
        const json = JSON.parse(result.highlight_text);
        const textsToHighlight = [];

        json.forEach(obj => {
          if (obj.description) {
            textsToHighlight.push(obj.description);
          }
          if (obj.usage) {
            Object.values(obj.usage).forEach(usageExample => {
              textsToHighlight.push(usageExample);
            });
          }
          if (obj.requirements) {
            textsToHighlight.push(obj.requirements);
          }
        });

        textsToHighlight.forEach(text => {
          highlightText(text);
        });

        // Clear after use
        chrome.storage.local.remove("highlight_text");
      } catch (e) {
        console.error("Failed to parse highlight text JSON", e);
      }
    }
  });
});

