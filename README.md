# REVEAL — Reverse Engineering Visual Explanation and Assistance Layer

REVEAL is a lightweight reverse engineering assistant built using FastAPI, Ghidra Headless, and local Mistral AI.

The project allows users to upload Windows executables, decompile them automatically, inspect raw and filtered code, explore extracted functions, and generate beginner-friendly AI explanations completely through local processing.

---

# Features

- Automated Windows executable analysis
- Ghidra Headless decompilation pipeline
- Raw decompiled C code viewer
- Filtered code output for cleaner analysis
- Runtime and library noise filtering
- Interactive function exploration
- AI-generated function explanations
- Executable behavior summarization
- Dark-themed responsive UI
- Local AI inference using Ollama + Mistral
- Modular and beginner-friendly architecture

---

# Architecture Overview

```text
                +----------------------+
                |   Vercel Frontend    |
                |  HTML / CSS / JS     |
                +----------+-----------+
                           |
                           |
                 Cloudflare Quick Tunnel
                           |
                           v
                +----------------------+
                |    FastAPI Backend   |
                +----------+-----------+
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
+----------------------+       +----------------------+
|   Ghidra Headless    |       |   Ollama + Mistral  |
| Binary Decompilation |       |   AI Explanations   |
+----------------------+       +----------------------+
```

---

# Analysis Workflow

```text
Upload Executable
        ↓
Store Uploaded File
        ↓
Ghidra Headless Decompilation
        ↓
Combined Decompiled C Output
        ↓
Function Extraction & Parsing
        ↓
Runtime / Library Noise Filtering
        ↓
Frontend Visualization
        ↓
AI Function Explanation
        ↓
Executable Summary Generation
```

---

# Tech Stack

| Category   | Technology                    |
| ---------- | ----------------------------- |
| Backend    | Python, FastAPI               |
| Frontend   | HTML, CSS, Vanilla JavaScript |
| Decompiler | Ghidra Headless Analyzer      |
| AI         | Ollama + Mistral              |
| Deployment | Vercel                        |
| Tunnel     | Cloudflare Quick Tunnel       |

---

# Project Structure

```text
.
├── backend
│   ├── ghidra_scripts
│   │   └── export_decomp.py
│   ├── main.py
│   ├── models
│   │   └── function_model.py
│   ├── routes
│   │   ├── ai_routes.py
│   │   ├── function_routes.py
│   │   └── upload_routes.py
│   ├── services
│   │   ├── ai_service.py
│   │   ├── filter_service.py
│   │   ├── ghidra_service.py
│   │   ├── parser_service.py
│   │   ├── session_service.py
│   │   ├── summary_service.py
│   │   └── upload_service.py
│   ├── static
│   │   ├── css
│   │   └── js
│   └── templates
│       └── index.html
│
├── frontend
│   ├── css
│   │   └── style.css
│   ├── index.html
│   └── js
│       ├── api.js
│       ├── app.js
│       ├── config.js
│       ├── dashboard.js
│       └── upload.js
│
├── outputs
├── uploads
├── temp
├── requirements.txt
├── test_parser.py
├── LICENSE
└── README.md
```

---

# UI Sections

## A — Raw Decompiled Code

Displays original Ghidra decompiled C output without modifications.

## B — Filtered Code

Displays cleaner code after removing runtime and library functions.

## C — Function List

Interactive list of extracted user-created functions.

## D — AI Function Explanation

Generates beginner-friendly explanations using local Mistral AI.

## E — Executable Summary

Provides a high-level overview of executable behavior.

---

# Local Setup

## 1. Clone Repository

```bash
git clone https://github.com/your-username/reveal.git

cd reveal
```

---

## 2. Create Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Ghidra

Set the Ghidra installation path inside the backend configuration.

Example:

```python
GHIDRA_HOME = "/path/to/ghidra"
```

---

## 5. Start Ollama

Start Ollama locally:

```bash
ollama serve
```

Pull the Mistral model:

```bash
ollama pull mistral
```

---

## 6. Start FastAPI Backend

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Backend will run on:

```text
http://localhost:8000
```

---

## 7. Create Cloudflare Quick Tunnel

Expose the local backend:

```bash
cloudflared tunnel --protocol http2 --url http://localhost:8000
```

Copy the generated public URL and update the frontend API configuration.

---

# Frontend Deployment

The frontend is deployed separately using Vercel.

The backend, Ghidra, and Ollama continue running locally.

```text
User Browser
      ↓
Vercel Frontend
      ↓
Cloudflare Quick Tunnel
      ↓
Local FastAPI Backend
      ↓
Local Ghidra + Ollama
```

For quick frontend updates during development, deployment is handled using:

```bash
vercel --prod
```

This avoids unnecessary Git commits and keeps the repository history cleaner while testing Cloudflare tunnel integrations.

---

# API Endpoints

| Method | Endpoint           | Description                            |
| ------ | ------------------ | -------------------------------------- |
| POST   | `/upload`          | Upload executable and trigger analysis |
| GET    | `/functions`       | Retrieve extracted functions           |
| GET    | `/function/{name}` | Retrieve selected function code        |
| POST   | `/explain`         | Generate AI explanation                |
| POST   | `/summary`         | Generate executable summary            |

---

# Future Improvements

- Docker-based deployment
- Function call graph visualization
- Support for additional executable formats
- Improved filtering heuristics
- Session persistence
- Multi-file binary analysis
- Exportable PDF analysis reports
- Enhanced frontend visualization

---

# License

This project was developed for educational and academic purposes.

REVEAL may be modified and used for learning, research, and non-commercial experimentation.
