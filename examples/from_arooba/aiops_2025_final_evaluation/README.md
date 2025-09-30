# Alphabet Project – Package Measurement Conversion API

This project converts encoded alphabet strings into numerical lists according to special rules.  
It includes a REST API with endpoints to **convert strings**, **store history**, and **view logs**.

---

## 📋 Features
- Convert alphabet sequences (`a-z`, `_`) into numbers with custom rules.
- Special handling for `z` and `_`.
- API endpoints:
  - `/convert-measurements?input=abbcc` → convert and return results
  - `/history` → view past conversions
- Logs all operations into `logs/app.log`.
- Runs fully inside Docker (one container for the app).

---

## 🐳 Run with Docker

### 1. Build the image
```bash
docker build -t aiops_app .
