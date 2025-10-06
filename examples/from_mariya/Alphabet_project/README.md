# 🔮 Alphabet Alchemist API - Setup & Usage Guide

This guide explains **everything you need**: project logic, structure, docker setup,
how to run, test with Postman, and verify results.  
You can follow the commands step by step directly from VS Code terminal.

---

## 🧠 Project Logic (How It Works)

1. Each letter `a-z` represents a number (`a=1 ... z=26`)
2. `_` represents `0`
3. The first letter in a package = **COUNT** (how many values to sum)
4. The next letters are the values to sum
5. `z` **cannot stand alone** → must take next letter as one token  
   (if double `zz`, still must take the next letter)
6. If COUNT = `_` append `0` to result
7. If string ends with `_` as COUNT append `0` to result list
8. If string ends with `_` as VALUE include it in sum

### Example

Input: abbcc

Step-by-step:
- `a` → count = 1 → take `b=2` → first result = `2`
- next count = `b=2` → take next two values `cc=3+3=6` → second result = `6`

Output:
```json
[2, 6]
```

## Build & Run MySQL + API Containers 
```
docker-compose up --build
```
wait until you see this: 
Uvicorn running on http://0.0.0.0:8080

### To stop container:
```
docker-compose down
```

### Run Again Without Rebuild:
```
docker-compose up
```

### Reset Database & Volumes Completely:
```
docker-compose down -v
docker-compose up --build
```

## 🧪 Testing with Postman
Using GET endpoint:
```
GET http://localhost:8080/convert-measurements?input=abbcc
```

### Test History Endpoint:
```
GET http://localhost:8080/history
```
Expected responce:
```
[
  {
    "id": 1,
    "input": "abbcc",
    "result": "[2, 6]",
    "created_at": "2025-09-28T12:35:00"
  }
]
```

## 📜 View API Logs
```
docker logs alphabet_api
```

## ✅ Summary

With these steps you can:

1. Decode measurement strings automatically 🔑

2. Store & retrieve results from MySQL

3. Run everything with one command via Docker 🐳

4. Test easily with Postman (GET + POST) 🧪

5. Verify database contents directly 🔎