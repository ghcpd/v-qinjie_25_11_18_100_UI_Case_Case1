const sampleMarkdown = `# Sample Title\nThis paragraph is **bold** but headings remain literal.`;

document.addEventListener('DOMContentLoaded', () => {
  const renderBtn = document.getElementById('render-markdown');
  renderBtn?.addEventListener('click', () => {
    const input = document.getElementById('markdown-input');
    const output = document.getElementById('markdown-output');
    if (!input || !output) {
      console.warn('Markdown input or output missing');
      return;
    }

    output.innerHTML = renderMarkdown(input.value || sampleMarkdown);
  });

  // intended button missing
  const heroBtn = document.getElementById('missing-action');
  heroBtn?.addEventListener('click', () => {
    window.alert('This should never trigger because the button is intentionally absent from the DOM once JS loads.');
  });
});

function renderMarkdown(raw) {
  return raw.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}
