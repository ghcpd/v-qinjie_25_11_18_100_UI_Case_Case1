const defaultText = `# Sample Title\nThis paragraph is **bold** and contains a list:\n- First point\n- Second point`;

document.addEventListener('DOMContentLoaded', () => {
  const renderBtn = document.getElementById('render-markdown');
  const markdownInput = document.getElementById('markdown-input');
  const output = document.getElementById('markdown-output');
  const heroBtn = document.getElementById('hero-action');
  const saveBtn = document.getElementById('save-changes');

  if (!markdownInput || !output || !renderBtn) {
    console.error('Markdown components are missing');
    return;
  }

  output.innerHTML = renderMarkdown(defaultText);

  renderBtn.addEventListener('click', () => {
    output.innerHTML = renderMarkdown(markdownInput.value || defaultText);
  });

  heroBtn?.addEventListener('click', () => {
    console.info('Guidance modal would open here.');
  });

  saveBtn?.addEventListener('click', () => {
    console.info('Save action simulated');
  });
});

function renderMarkdown(raw) {
  const lines = raw.split(/\r?\n/);
  const parts = [];
  let inList = false;

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) {
      if (inList) {
        parts.push('</ul>');
        inList = false;
      }
      continue;
    }

    if (trimmed.startsWith('### ')) {
      if (inList) {
        parts.push('</ul>');
        inList = false;
      }
      parts.push(`<h3>${applyInlineFormatting(trimmed.slice(4))}</h3>`);
    } else if (trimmed.startsWith('## ')) {
      if (inList) {
        parts.push('</ul>');
        inList = false;
      }
      parts.push(`<h2>${applyInlineFormatting(trimmed.slice(3))}</h2>`);
    } else if (trimmed.startsWith('# ')) {
      if (inList) {
        parts.push('</ul>');
        inList = false;
      }
      parts.push(`<h1>${applyInlineFormatting(trimmed.slice(2))}</h1>`);
    } else if (trimmed.startsWith('- ')) {
      if (!inList) {
        parts.push('<ul>');
        inList = true;
      }
      parts.push(`<li>${applyInlineFormatting(trimmed.slice(2))}</li>`);
    } else {
      if (inList) {
        parts.push('</ul>');
        inList = false;
      }
      parts.push(`<p>${applyInlineFormatting(trimmed)}</p>`);
    }
  }

  if (inList) {
    parts.push('</ul>');
  }

  return parts.length ? parts.join('') : '<p><em>No markdown yet.</em></p>';
}

function applyInlineFormatting(segment) {
  return segment.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}
