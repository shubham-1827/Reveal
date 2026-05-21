// dashboard.js

const rawCode = document.getElementById("rawCode");

const filteredCode = document.getElementById("filteredCode");

const functionList = document.getElementById("functionList");

const functionExplanation = document.getElementById("functionExplanation");

const summaryContent = document.getElementById("summaryContent");

export function renderDashboard(data) {
  renderRawCode(data);

  renderFilteredCode(data);

  renderFunctionList(data);

  renderSummary(data);
}

export function resetDashboard() {
  rawCode.textContent = "No decompiled output available.";

  filteredCode.textContent = "No filtered code available.";

  functionList.innerHTML = `
    <div class="empty-state">
      No functions detected.
    </div>
  `;

  functionExplanation.innerHTML = `
    <div class="empty-state">
      Select a function to generate explanation.
    </div>
  `;

  summaryContent.innerHTML = `
    <div class="empty-state">
      No executable summary available.
    </div>
  `;
}

function renderRawCode(data) {
  rawCode.textContent = data.raw_code || "No raw decompiled output.";

  // for syntax highlighting
  Prism.highlightElement(rawCode);
}

function renderFilteredCode(data) {
  filteredCode.textContent =
    data.filtered_code || "No filtered code available.";

  // for syntax highlighting
  Prism.highlightElement(filteredCode);
}

function renderFunctionList(data) {
  functionList.innerHTML = "";

  if (!data.functions || data.functions.length === 0) {
    functionList.innerHTML = `
      <div class="empty-state">
        No functions detected.
      </div>
    `;

    return;
  }

  data.functions.forEach((func) => {
    const item = createFunctionItem(func);

    functionList.appendChild(item);
  });
}

function createFunctionItem(func) {
  const item = document.createElement("div");

  item.className = "function-item";

  item.innerHTML = `
    <!-- <div class="function-name"> -->
    <!--   ${func.name} -->
    <!-- </div> -->
    <div class="function-name">
      ${func.name}
    </div>

    <div class="function-address">
      0x${func.address}
    </div>
  `;

  item.addEventListener("click", () => handleFunctionClick(func, item));

  return item;
}

function escapeHtml(text) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function handleFunctionClick(func, selectedItem) {
  clearActiveFunctions();

  selectedItem.classList.add("active");

  functionExplanation.innerHTML = `
    <p class="loading-text">
      AI explanation generation
      will appear here.
    </p>

    <br>

    <pre class="code-viewer">
      <code
        class="language-c"
        id="selectedFunctionCode"
      >
  ${escapeHtml(func.code)}
      </code>
    </pre>
  `;

  // for syntax highlighting in the code viewer
  const selectedCode = document.getElementById("selectedFunctionCode");

  Prism.highlightElement(selectedCode);
}

function clearActiveFunctions() {
  const items = document.querySelectorAll(".function-item");

  items.forEach((item) => {
    item.classList.remove("active");
  });
}

function renderSummary(data) {
  summaryContent.innerHTML = `
    <p>
      Executable summary generation
      will appear here.
    </p>
  `;
}
