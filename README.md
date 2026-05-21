# REVEAL

REVEAL is a beginner-friendly reverse engineering assistant built using:

- FastAPI
- Ghidra Headless
- Ollama
- Local Mistral AI

## Project Structure

```text
reveal/
│
├── backend/
│   ├── services/
│   ├── static/
│   ├── templates/
│   └── main.py
│
├── uploads/
├── outputs/
├── temp/
├── ghidra_scripts/
└── README.md
```

## Setup

### Create virtual environment

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

---

### Install dependencies

```bash
pip install fastapi uvicorn jinja2 python-multipart
```

---

### Run server

```bash
uvicorn backend.main:app --reload
```

---

### Open browser

```text
http://127.0.0.1:8000
```
