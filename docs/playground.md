---
title: Interactive Demo
description: "Try quotes-convert Python library in your browser. No installation required. Test quote conversion with single_quotes and double_quotes functions directly in your browser."
keywords:
  - interactive demo
  - test quote conversion
  - online quotes convert
  - try quotes-convert
  - browser demo
  - test single quotes
  - test double quotes
  - quote escaping demo
---

# Interactive Playground

Try the `quotes-convert` library directly in your browser! This page uses [Pyodide](https://pyodide.org/) to run Python in the browser.

<div id="pyodide-loading" style="text-align: center; padding: 40px 20px;">
  <div class="spinner"></div>
  <p style="margin-top: 15px; color: #666;">Loading Pyodide...</p>
</div>

<div id="playground-container" style="display: none;">
  <!-- Package Info Banner -->
  <div id="package-info" style="display: none; margin-bottom: 20px; padding: 12px 16px; background: #e3f2fd; border-left: 4px solid #1976d2; border-radius: 4px;">
    <span style="font-weight: 500;">Installed:</span> <code>quotes-convert</code> <span id="package-version" style="font-weight: 600; color: #1976d2;"></span>
  </div>

  <!-- Main Layout -->
  <div class="playground-layout">
    <!-- Input Panel -->
    <div class="input-panel">
      <div class="panel-header">
        <span class="panel-title">Input Text</span>
        <div class="example-buttons">
          <button class="example-btn active" data-example="example1">JSON String</button>
          <button class="example-btn" data-example="example2">Mixed Quotes</button>
          <button class="example-btn" data-example="example3">Shell Script</button>
          <button class="example-btn" data-example="custom">Custom</button>
        </div>
      </div>

      <div class="text-editor-container">
        <textarea
          id="input-text"
          class="text-editor"
          placeholder='Enter text with quotes, e.g., {"key": "value"}'
          spellcheck="false"
        ></textarea>
      </div>
    </div>

    <!-- Operations Panel -->
    <div class="ops-panel">
      <div class="ops-tabs">
        <button class="ops-tab active" data-op="single_quotes">single_quotes</button>
        <button class="ops-tab" data-op="double_quotes">double_quotes</button>
      </div>

      <div class="ops-content">
        <!-- single_quotes Section -->
        <div class="op-section active" data-op="single_quotes">
          <h3 class="op-title">Convert to Single Quotes</h3>
          <p class="op-description">Convert all matching double-quotes to single-quotes with proper escaping.</p>

          <button id="single-btn" class="execute-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            Execute
          </button>

          <div class="code-preview">
            <div class="code-preview-header">
              <span>Python Code</span>
              <button class="copy-btn" onclick="copyCode('single_quotes')">Copy</button>
            </div>
            <div class="code-preview-body" id="single-code-preview">
              <span class="code-fn">single_quotes</span>(text)
            </div>
          </div>

          <div id="single-result" class="result-panel"></div>
        </div>

        <!-- double_quotes Section -->
        <div class="op-section" data-op="double_quotes">
          <h3 class="op-title">Convert to Double Quotes</h3>
          <p class="op-description">Convert all matching single-quotes to double-quotes with proper escaping.</p>

          <button id="double-btn" class="execute-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            Execute
          </button>

          <div class="code-preview">
            <div class="code-preview-header">
              <span>Python Code</span>
              <button class="copy-btn" onclick="copyCode('double_quotes')">Copy</button>
            </div>
            <div class="code-preview-body" id="double-code-preview">
              <span class="code-fn">double_quotes</span>(text)
            </div>
          </div>

          <div id="double-result" class="result-panel"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- Stream Methods Note -->
  <div class="info-banner">
    <strong>Note:</strong> This playground demonstrates <code>single_quotes()</code> and <code>double_quotes()</code>. 
    For streaming large files, use <code>single_quotes_stream()</code> and <code>double_quotes_stream()</code> in your Python environment. 
    See the <a href="/quotes-convert/api-reference/">API Reference</a> for details.
  </div>
</div>

<style>
  /* Spinner */
  .spinner {
    border: 4px solid #e0e0e0;
    border-top: 4px solid #1976d2;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* Main Layout */
  .playground-layout {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  /* Input Panel */
  .input-panel {
    background: #263238;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .panel-header {
    padding: 12px 16px;
    background: #1e272c;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
  }

  .panel-title {
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #90a4ae;
  }

  .example-buttons {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }

  .example-btn {
    padding: 5px 10px;
    background: transparent;
    border: 1px solid #455a64;
    color: #b0bec5;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.75rem;
    transition: all 0.2s;
  }

  .example-btn:hover {
    background: #37474f;
    border-color: #607d8b;
  }

  .example-btn.active {
    background: #1976d2;
    color: white;
    border-color: #1976d2;
  }

  /* Text Editor */
  .text-editor-container {
    display: flex;
    flex-direction: column;
    position: relative;
    height: 200px;
  }

  .text-editor {
    flex: 1;
    width: 100%;
    padding: 16px;
    background: #263238;
    border: none;
    color: #eceff1;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.85rem;
    line-height: 1.6;
    resize: none;
    outline: none;
    overflow: auto;
  }

  .text-editor::placeholder {
    color: #546e7a;
  }

  /* Operations Panel */
  .ops-panel {
    background: white;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .ops-tabs {
    display: flex;
    background: #fafafa;
    border-bottom: 1px solid #e0e0e0;
    overflow-x: auto;
    flex-shrink: 0;
  }

  .ops-tab {
    padding: 12px 16px;
    background: transparent;
    border: none;
    color: #757575;
    cursor: pointer;
    font-size: 0.8rem;
    font-weight: 500;
    font-family: 'Monaco', 'Menlo', monospace;
    border-bottom: 2px solid transparent;
    white-space: nowrap;
    transition: all 0.2s;
  }

  .ops-tab:hover {
    color: #424242;
    background: #f5f5f5;
  }

  .ops-tab.active {
    color: #1976d2;
    border-bottom-color: #1976d2;
    background: white;
  }

  .ops-content {
    flex: 1;
    overflow: auto;
    padding: 20px;
  }

  .op-section {
    display: none;
  }

  .op-section.active {
    display: block;
  }

  .op-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0 0 6px 0;
    color: #212121;
  }

  .op-description {
    color: #757575;
    font-size: 0.9rem;
    margin: 0 0 20px 0;
  }

  /* Execute Button */
  .execute-btn {
    width: 100%;
    padding: 12px 16px;
    background: #1976d2;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s, transform 0.1s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }

  .execute-btn:hover {
    background: #1565c0;
  }

  .execute-btn:active {
    transform: scale(0.98);
  }

  /* Code Preview */
  .code-preview {
    margin-top: 16px;
    background: #263238;
    border-radius: 6px;
    overflow: hidden;
  }

  .code-preview-header {
    padding: 8px 12px;
    background: #1e272c;
    color: #90a4ae;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .copy-btn {
    padding: 3px 8px;
    background: #37474f;
    border: none;
    color: #b0bec5;
    border-radius: 3px;
    cursor: pointer;
    font-size: 0.65rem;
    text-transform: uppercase;
  }

  .copy-btn:hover {
    background: #455a64;
  }

  .code-preview-body {
    padding: 12px;
    font-family: 'Monaco', 'Menlo', monospace;
    font-size: 0.85rem;
    color: #eceff1;
    overflow-x: auto;
  }

  .code-fn {
    color: #82aaff;
  }

  .code-str {
    color: #c3e88d;
  }

  /* Result Panel */
  .result-panel {
    margin-top: 16px;
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid #e0e0e0;
    min-height: 50px;
  }

  .result-panel:empty {
    display: none;
  }

  .result-panel .result-header {
    padding: 8px 12px;
    background: #fafafa;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #757575;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .result-panel .result-body {
    padding: 12px;
    font-family: 'Monaco', 'Menlo', monospace;
    font-size: 0.85rem;
    background: white;
  }

  .result-success {
    color: #2e7d32;
  }

  .result-error {
    color: #c62828;
  }

  .result-value {
    background: #f5f5f5;
    padding: 8px 12px;
    border-radius: 4px;
    margin-top: 8px;
    display: block;
    word-break: break-word;
    white-space: pre-wrap;
  }

  .result-status {
    padding: 3px 8px;
    border-radius: 12px;
    font-size: 0.65rem;
    font-weight: 600;
  }

  .result-status.success {
    background: #e8f5e9;
    color: #2e7d32;
  }

  .result-status.error {
    background: #ffebee;
    color: #c62828;
  }

  /* Info Banner */
  .info-banner {
    margin-top: 20px;
    padding: 12px 16px;
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    border-radius: 4px;
    font-size: 0.9rem;
    color: #856404;
  }

  .info-banner strong {
    font-weight: 600;
  }

  .info-banner code {
    background: rgba(0, 0, 0, 0.1);
    padding: 2px 6px;
    border-radius: 3px;
    font-family: monospace;
  }

  .info-banner a {
    color: #0056b3;
    text-decoration: underline;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .text-editor-container {
      height: 180px;
    }

    .ops-tab {
      padding: 10px 12px;
      font-size: 0.75rem;
    }

    .panel-header {
      flex-direction: column;
      align-items: flex-start;
    }

    .example-buttons {
      width: 100%;
    }
  }
</style>

<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>

<script type="text/javascript">
  let pyodide;

  async function main() {
    // Load Pyodide
    pyodide = await loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/"
    });

    // Update loading message
    document.getElementById("pyodide-loading").innerHTML = '<div class="spinner"></div><p style="margin-top: 15px; color: #666;">Installing quotes-convert package...</p>';

    // Install quotes-convert package
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");
    await micropip.install("quotes-convert");

    // Import functions
    pyodide.runPython(`
      from quotes_convert import single_quotes, double_quotes
      
      # Try to get package version
      try:
          import importlib.metadata
          package_version = importlib.metadata.version('quotes-convert')
      except:
          try:
              import importlib_metadata
              package_version = importlib_metadata.version('quotes-convert')
          except:
              package_version = "unknown"
    `);

    const packageVersion = pyodide.globals.get("package_version");

    // Display package version
    if (packageVersion && packageVersion !== "unknown") {
      document.getElementById("package-version").textContent = `v${packageVersion}`;
      document.getElementById("package-info").style.display = "block";
    }

    // Hide loading, show interface
    document.getElementById("pyodide-loading").style.display = "none";
    document.getElementById("playground-container").style.display = "block";

    // Load default example
    loadExample("example1");

    // Setup event listeners
    setupEventListeners();
  }

  function loadExample(exampleType) {
    let text = "";

    switch(exampleType) {
      case "example1":
        text = '{"name": "Alice", "message": "He said \\"Hello\\""}'
        break;
      case "example2":
        text = '"it\'s working" and "he said \\"hi\\""';
        break;
      case "example3":
        text = 'echo "Hello $USER"; grep "pattern" file.txt';
        break;
      case "custom":
        text = "";
        break;
    }

    document.getElementById("input-text").value = text;

    // Update example buttons
    document.querySelectorAll('.example-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`.example-btn[data-example="${exampleType}"]`).classList.add('active');

    // Clear results
    clearResults();
  }

  function setupEventListeners() {
    // Example buttons
    document.querySelectorAll('.example-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        loadExample(btn.dataset.example);
      });
    });

    // Operation tabs
    document.querySelectorAll('.ops-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.ops-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.op-section').forEach(s => s.classList.remove('active'));

        tab.classList.add('active');
        document.querySelector(`.op-section[data-op="${tab.dataset.op}"]`).classList.add('active');
      });
    });

    // Convert to single quotes
    document.getElementById("single-btn").addEventListener("click", async () => {
      const text = document.getElementById("input-text").value;
      const resultDiv = document.getElementById("single-result");

      if (!text) {
        showResult(resultDiv, "error", "Please enter some text");
        return;
      }

      try {
        const code = `single_quotes(${JSON.stringify(text)})`;
        const result = pyodide.runPython(code);
        showResult(resultDiv, "success", "Converted successfully", result);
      } catch (error) {
        showResult(resultDiv, "error", error.message);
      }
    });

    // Convert to double quotes
    document.getElementById("double-btn").addEventListener("click", async () => {
      const text = document.getElementById("input-text").value;
      const resultDiv = document.getElementById("double-result");

      if (!text) {
        showResult(resultDiv, "error", "Please enter some text");
        return;
      }

      try {
        const code = `double_quotes(${JSON.stringify(text)})`;
        const result = pyodide.runPython(code);
        showResult(resultDiv, "success", "Converted successfully", result);
      } catch (error) {
        showResult(resultDiv, "error", error.message);
      }
    });

    // Enter key handler
    document.getElementById("input-text").addEventListener("keypress", (e) => {
      if (e.key === "Enter" && e.ctrlKey) {
        const activeTab = document.querySelector('.ops-tab.active');
        if (activeTab.dataset.op === "single_quotes") {
          document.getElementById("single-btn").click();
        } else {
          document.getElementById("double-btn").click();
        }
      }
    });
  }

  function showResult(div, type, message, value = null) {
    const statusClass = type === "success" ? "success" : type === "error" ? "error" : "";
    const statusText = type === "success" ? "Success" : type === "error" ? "Error" : "Info";

    let html = `
      <div class="result-header">
        <span>Result</span>
        ${statusClass ? `<span class="result-status ${statusClass}">${statusText}</span>` : ''}
      </div>
      <div class="result-body">
        <span class="result-${type}">${escapeHtml(message)}</span>
        ${value ? `<code class="result-value">${escapeHtml(value)}</code>` : ''}
      </div>
    `;
    div.innerHTML = html;
  }

  function copyCode(op) {
    const text = document.getElementById("input-text").value || "text";
    let code = '';
    
    if (op === 'single_quotes') {
      code = `single_quotes(${JSON.stringify(text)})`;
    } else {
      code = `double_quotes(${JSON.stringify(text)})`;
    }

    navigator.clipboard.writeText(code).then(() => {
      const btn = event.target;
      const original = btn.textContent;
      btn.textContent = 'Copied!';
      setTimeout(() => btn.textContent = original, 1500);
    });
  }

  function clearResults() {
    document.querySelectorAll('.result-panel').forEach(el => el.innerHTML = '');
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  // Start loading Pyodide
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      main().catch(err => {
        document.getElementById("pyodide-loading").innerHTML =
          `<p style="color: #c62828;">Error loading Pyodide: ${err.message}</p>`;
        console.error(err);
      });
    });
  } else {
    main().catch(err => {
      document.getElementById("pyodide-loading").innerHTML =
        `<p style="color: #c62828;">Error loading Pyodide: ${err.message}</p>`;
      console.error(err);
    });
  }
</script>
