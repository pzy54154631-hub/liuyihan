/* Math assets are served with the site so reading does not depend on a CDN. */
document.querySelectorAll('.math.inline, .math.block').forEach((element) => {
  if (!window.katex) return;
  try {
    katex.render(element.textContent, element, {
      displayMode: element.classList.contains('block'),
      throwOnError: true,
      trust: false,
      output: 'htmlAndMathml'
    });
  } catch (error) {
    element.classList.add('math-error');
    element.setAttribute('title', '公式暂未渲染，显示原始写法');
    console.error('Math rendering failed:', error.message);
  }
});

document.querySelectorAll('.article-body pre').forEach((pre) => {
  const code = pre.querySelector('code');
  if (!code) return;
  const shell = document.createElement('div');
  shell.className = 'code-shell';
  const toolbar = document.createElement('div');
  toolbar.className = 'code-toolbar';
  const label = document.createElement('span');
  label.textContent = (code.className.match(/language-([\w-]+)/)?.[1] || '代码').toUpperCase();
  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = '复制代码';
  button.setAttribute('aria-label', '复制这段代码');
  const status = document.createElement('span');
  status.className = 'copy-status';
  status.setAttribute('aria-live', 'polite');
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(code.textContent);
      status.textContent = '已复制';
      button.textContent = '已复制 ✓';
    } catch {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(code);
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = '已选中代码，请使用系统复制';
      button.textContent = '请手动复制';
    }
  });
  toolbar.append(label, status, button);
  pre.before(shell);
  shell.append(toolbar, pre);
});
