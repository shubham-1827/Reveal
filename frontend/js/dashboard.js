// dashboard.js
import { fetchFunction, explainFunction, generateSummary } from "./api.js";

const rawCode = document.getElementById("rawCode");

const filteredCode = document.getElementById("filteredCode");

const functionList = document.getElementById("functionList");

const functionExplanation = document.getElementById("functionExplanation");

const summaryContent = document.getElementById("summaryContent");

let selectedFunctionElement = null;

export async function renderDashboard(data) {
  renderRawCode(data);

  renderFilteredCode(data);

  renderFunctionList(data);

  await renderSummary(data);
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
