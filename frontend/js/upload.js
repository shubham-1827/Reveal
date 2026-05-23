// upload.js

import { uploadExecutable } from "./api.js";

import { renderDashboard, resetDashboard } from "./dashboard.js";

const uploadButton = document.getElementById("uploadButton");

const fileInput = document.getElementById("fileInput");

const uploadStatus = document.getElementById("uploadStatus");

export function setupUpload() {
  uploadButton.addEventListener("click", handleUploadButtonClick);

  fileInput.addEventListener("change", handleFileSelection);
}

function handleUploadButtonClick() {
  fileInput.click();
}

async function handleFileSelection() {
  const file = fileInput.files[0];

  if (!file) {
    return;
  }

  resetDashboard();

  setLoadingState(true);

  uploadStatus.textContent = "Running Ghidra analysis...";

  const formData = new FormData();

  formData.append("file", file);

  try {
    const response = await uploadExecutable(formData);

    const data = await response.json();

    if (!response.ok) {
      uploadStatus.textContent = data.detail || "Upload failed";

      setLoadingState(false);

      return;
    }

    uploadStatus.textContent = `Loaded executable: ${data.filename}`;

    renderDashboard(data);
  } catch (error) {
    uploadStatus.textContent = "Server error during analysis";
  } finally {
    setLoadingState(false);
  }
}

function setLoadingState(isLoading) {
  uploadButton.disabled = isLoading;

  if (isLoading) {
    uploadButton.textContent = "Processing...";
  } else {
    uploadButton.textContent = "Upload Executable";
  }
}
