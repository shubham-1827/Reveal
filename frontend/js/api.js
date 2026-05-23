// api.js

const API_BASE =
  "https://qualifications-donations-albany-italia.trycloudflare.com";

export async function uploadExecutable(formData) {
  return fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });
}

export async function fetchFunctions() {
  return fetch(`${API_BASE}/functions`);
}

export async function fetchFunction(name) {
  return fetch(`${API_BASE}/function/${name}`);
}

export async function explainFunction(functionName, functionCode) {
  return fetch(`${API_BASE}/explain`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      function_name: functionName,
      code: functionCode,
    }),
  });
}

export async function generateSummary(functions) {
  return fetch(`${API_BASE}/summary`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      functions,
    }),
  });
}
