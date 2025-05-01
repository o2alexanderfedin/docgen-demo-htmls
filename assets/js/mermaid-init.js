document.addEventListener("DOMContentLoaded", function() {
  mermaid.initialize({
    startOnLoad: true,
    theme: "default",
    securityLevel: "loose",
    flowchart: { 
      curve: 'basis',
      useMaxWidth: false
    }
  });
  
  // Find all pre.language-mermaid elements and process them
  document.querySelectorAll('pre.language-mermaid, div.language-mermaid').forEach(function(element) {
    // Create a div with class mermaid
    var mermaidDiv = document.createElement('div');
    mermaidDiv.classList.add('mermaid');
    // Set the inner text to be the same as the pre element
    mermaidDiv.innerText = element.innerText;
    // Replace the pre element with the mermaid div
    element.parentNode.replaceChild(mermaidDiv, element);
  });
  
  // Initialize mermaid after modifying the DOM
  mermaid.init(undefined, document.querySelectorAll('.mermaid'));
});