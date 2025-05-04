window.addEventListener("load", () => {
  const text = localStorage.getItem("highlight_text");

  if (text) {
    try {
      const json = JSON.parse(text);

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

    } catch (e) {
      console.error("Failed to parse highlight text JSON", e);
    }
  }
});

function highlightText(text) {
  if (!text) return;

  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);

  while (walker.nextNode()) {
    const node = walker.currentNode;
    const idx = node.nodeValue.indexOf(text);

    if (idx !== -1) {
      const range = document.createRange();
      range.setStart(node, idx);
      range.setEnd(node, idx + text.length);

      const highlightSpan = document.createElement("span");
      highlightSpan.style.backgroundColor = "yellow";
      highlightSpan.style.fontWeight = "bold";
      highlightSpan.textContent = text;

      range.deleteContents();
      range.insertNode(highlightSpan);
    }
  }
}
