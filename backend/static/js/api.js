// api.js

export async function uploadExecutable(formData) {
  return fetch("/upload", {
    method: "POST",
    body: formData,
  });
}

/*
Future API endpoints
for AI integration
*/

export async function explainFunction(functionName, functionCode) {
  return fetch("/explain", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      name: functionName,
      code: functionCode,
    }),
  });
}

export async function generateSummary(code) {
  return fetch("/summary", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      code,
    }),
  });
}
