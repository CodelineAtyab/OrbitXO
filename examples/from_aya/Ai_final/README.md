# 📦 AI OPS - Package Measurement Conversion API

This project provides an API that converts encoded measurement input strings into a list of numbers, based on defined rules.

---

## 🚀 Features
- Conversion endpoint: `/convert-measurements`
- History endpoint: `/history` (stored in MySQL)
- Logging (console + `logs/app.log`)
- Containerized with Docker and docker-compose
- Built with FastAPI

---

## ⚙️ Requirements
- Python 3.10+
- Docker & docker-compose

---

## 📥 Run Locally
```bash
pip install -r requirements.txt
uvicorn main_app:app --reload --port 8080
```

---

## 🐳 Run with Docker
```bash
docker-compose up --build
```

API will be available at:
- Swagger docs: [http://localhost:8080/docs](http://localhost:8080/docs)
- Convert example: [http://localhost:8080/convert-measurements?input=abbcc](http://localhost:8080/convert-measurements?input=abbcc)
- History: [http://localhost:8080/history](http://localhost:8080/history)

---

## 📝 Example Inputs → Outputs
- "aa" → [1]
- "abbcc" → [2,6]
- "dz_a_aazzaaa" → [28,53,1]
- "a_" → [0]
- "abcdabcdab" → [2,7,7]
- "abcdabcdab_" → [2,7,7,0]
- "zdaaaaaaaabaaaaaaaabaaaaaaaabbaa" → [34]
- "zza_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_" → [26]
- "za_a_a_a_a_a_a_a_a_a_a_a_a_azaaa" → [40,1]

---

## 📂 Project Structure
```
ai_ops/
│── converter.py          # Conversion logic
│── main_app.py           # FastAPI app with endpoints + SQLAlchemy + logs
│── requirements.txt      # Dependencies
│── Dockerfile            # Container setup
│── docker-compose.yml    # API + MySQL
│── logs/                 # Logs directory
│── README.md             # Project documentation
```
