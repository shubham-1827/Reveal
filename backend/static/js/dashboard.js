// dashboard.js
import {
  fetchFunction,
  explainFunction,
  generateSummary,
  polishCode,
} from "./api.js";

const rawCode = document.getElementById("rawCode");

const filteredCode = document.getElementById("filteredCode");

const filteredTab = document.getElementById("filteredTab");

const polishedTab = document.getElementById("polishedTab");

let codeTabsInitialized = false;

const codePanelTitle = document.getElementById("codePanelTitle");

const polishButton = document.getElementById("polishButton");

const functionList = document.getElementById("functionList");

const functionExplanation = document.getElementById("functionExplanation");

const summaryContent = document.getElementById("summaryContent");

// initial state
let selectedFunctionElement = null;
let currentFilteredCode = "";
let currentPolishedCode = null;
let activeCodeTab = "filtered";

export async function renderDashboard(data) {
  if (!codeTabsInitialized) {
    initializeCodeTabs();

    codeTabsInitialized = true;
  }

  renderRawCode(data);

  renderFilteredCode(data);

  renderFunctionList(data);

  await renderSummary(data);
}

export function resetDashboard() {
  currentFilteredCode = "";
  currentPolishedCode = null;
  activeCodeTab = "filtered";

  filteredTab.classList.add("active");
  polishedTab.classList.remove("active");

  codePanelTitle.textContent = "Filtered Code";
  rawCode.textContent = "No decompiled output available.";
  filteredCode.textContent = "No filtered code available.";

  polishButton.style.display = "inline-block";
  polishButton.disabled = false;
  polishButton.textContent = "Polish Using AI";

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

function initializeCodeTabs() {
  filteredTab.addEventListener("click", () => switchCodeTab("filtered"));

  polishedTab.addEventListener("click", () => {
    if (!currentPolishedCode) {
      return;
    }

    switchCodeTab("polished");
  });

  polishButton.addEventListener("click", handlePolishRequest);
}

function switchCodeTab(tab) {
  activeCodeTab = tab;

  filteredTab.classList.remove("active");
  polishedTab.classList.remove("active");

  if (tab === "filtered") {
    polishButton.style.display = "inline-block";

    filteredTab.classList.add("active");

    codePanelTitle.textContent = "Filtered Code";

    filteredCode.textContent =
      currentFilteredCode || "No filtered code available.";
  } else {
    polishButton.style.display = "none";

    polishedTab.classList.add("active");

    codePanelTitle.textContent = "Polished Code";

    filteredCode.textContent =
      currentPolishedCode || "No polished code available.";
  }

  Prism.highlightElement(filteredCode);
}

function renderRawCode(data) {
  rawCode.textContent = data.raw_code || "No raw decompiled output.";

  // for syntax highlighting
  Prism.highlightElement(rawCode);
}

function renderFilteredCode(data) {
  currentFilteredCode = data.filtered_code || "";

  switchCodeTab("filtered");
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

  item.addEventListener("click", async () => {
    await handleFunctionClick(func.name, item);
  });

  return item;
}

function escapeHtml(text) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

async function handleFunctionClick(functionName, element) {
  try {
    updateSelectedFunction(element);

    functionExplanation.innerHTML = "";

    functionExplanation.innerHTML = `
      <div class="loading-state">
        Generating explanation...
      </div>
    `;

    const response = await fetchFunction(functionName);

    if (!response.ok) {
      throw new Error("Failed to load function");
    }

    const functionData = await response.json();

    const explainResponse = await explainFunction(
      functionData.name,
      functionData.code,
    );

    if (!explainResponse.ok) {
      throw new Error("Failed to generate explanation");
    }

    const explanationData = await explainResponse.json();

    renderFunctionExplanation(functionData, explanationData.explanation);
  } catch (error) {
    console.error(error);

    functionExplanation.innerHTML = `
      <div class="empty-state">
        Failed to generate explanation.
      </div>
    `;
  }
}

function updateSelectedFunction(element) {
  if (selectedFunctionElement) {
    selectedFunctionElement.classList.remove("active");
  }

  element.classList.add("active");

  selectedFunctionElement = element;
}

function renderFunctionExplanation(functionData, explanation) {
  functionExplanation.replaceChildren();
  functionExplanation.innerHTML = `
    <div class="function-details">

      <div class="function-title">
        ${functionData.name}
      </div>

      <div class="function-meta">
        0x${functionData.address}
      </div>

      <div class="ai-explanation-section">

        <div class="section-label">
          AI Explanation
        </div>

      <div class="ai-explanation-text">
        ${marked.parse(explanation)}
      </div>

      </div>

      <div class="function-code-section">

        <div class="section-label">
          Decompiled Function
        </div>

        <pre class="code-viewer small-code-viewer">
          <code
            class="language-c"
            id="selectedFunctionCode"
          >
${escapeHtml(functionData.code)}
          </code>
        </pre>

      </div>

    </div>
  `;

  const selectedCode = document.getElementById("selectedFunctionCode");

  Prism.highlightElement(selectedCode);
}

async function renderSummary(data) {
  const functions = data.functions;

  if (!functions || functions.length === 0) {
    summaryContent.innerHTML = `
      <div class="empty-state">
        No executable summary available.
      </div>
    `;

    return;
  }

  summaryContent.innerHTML = `
    <div class="loading-state">
      Generating executable summary...
    </div>
  `;

  try {
    const response = await generateSummary(functions);

    if (!response.ok) {
      throw new Error("Failed to generate summary");
    }

    const summaryData = await response.json();

    summaryContent.innerHTML = `
      <div class="summary-inner">
        ${marked.parse(summaryData.summary)}
      </div>
    `;
  } catch (error) {
    console.error(error);

    summaryContent.innerHTML = `
      <div class="empty-state">
        Failed to generate summary.
      </div>
    `;
  }
}

async function handlePolishRequest() {
  if (currentPolishedCode) {
    switchCodeTab("polished");
    return;
  }

  try {
    polishButton.disabled = true;

    polishButton.textContent = "Polishing...";

    const response = await polishCode(currentFilteredCode);

    if (!response.ok) {
      throw new Error("Failed to polish code");
    }

    const data = await response.json();

    setCurrentPolishedCode(data.polished_code);

    switchCodeTab("polished");
  } catch (error) {
    console.error(error);

    alert("Failed to polish code.");
  } finally {
    polishButton.disabled = false;

    polishButton.textContent = "Polish Using AI";
  }
}

// helper functions for the polish section
function getCurrentFilteredCode() {
  return currentFilteredCode;
}

function getCurrentPolishedCode() {
  return currentPolishedCode;
}

function setCurrentPolishedCode(code) {
  currentPolishedCode = code;
}
