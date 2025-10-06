# Package Measurement Conversion API

A Python Flask API that converts encoded measurement strings into a list of integer values. The application persists conversion history in MySQL, logs activity to both console and files, and is containerized using Docker.

## Features
- Convert measurement strings to numeric lists
- Configurable port via environment or CLI
- History persistence in MySQL database
- History retrieval endpoint
- Logging with file rotation (7 days)
- Dockerized deployment with health checks

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

```bash
# Clone and run
git clone <repository_url>
cd <repository_name>
docker-compose up --build

# Test the API
curl "http://localhost:8080/convert-measurements?input=abbcc"
```

## API Endpoints

### Convert Measurements
```http
GET http://localhost:8080/convert-measurements?input=zz
```
Example: `http://localhost:8080/convert-measurements?input=abbcc`
Response: `[2, 6]`

### Retrieve History
```http
GET http://localhost:8080/history
```
Example response:
```json
{
  "history": [
    {
      "id": 1,
      "input_string": "abbcc",
      "output_result": "[2, 6]",
      "timestamp": "2023-10-05T14:48:00Z"
    }
  ],
  "count": 1
}
```

## Database Setup & Storage
 
### MySQL Database Server <useing DBserver>
The application uses a MySQL 8.0 database to persist conversion history. This database is set up using Docker Compose alongside the Flask API.

#### Database Management
```bash
# Start database only
docker-compose up -d db

# Check container status
docker ps

# Connect to MySQL (for debugging)
docker exec -it aiops_2025_solution_db_1 mysql -uuser -ppassword aiops_db
```

### Data Storage
Each conversion request is stored in two places:
1. JSON file in `outputs/` directory
2. MySQL database `history` table

#### Database Schema
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Auto-increment primary key |
| input_string | String(255) | Original input string |
| output_result | Text | Conversion result as JSON |
| timestamp | DateTime | Conversion timestamp |

Example record:
```sql
INSERT INTO history (input_string, output_result, timestamp)
VALUES ('abbcc', '[2, 6]', '2025-09-29 10:12:45');
```

#### Connection String
The database connection URL format:
```
mysql+pymysql://user:password@db:3306/aiops_db
```
Configure via `DATABASE_URL` environment variable.

## Database Visualization

### Using DB Server
1. Connect to MySQL database:
```bash
docker exec -it aiops_2025_solution_db_1 mysql -uuser -ppassword aiops_db
```

2. View tables and data:
```sql
-- Show all tables
SHOW TABLES;

-- View conversion history
SELECT * FROM history;

-- View latest 5 conversions
SELECT * FROM history ORDER BY timestamp DESC LIMIT 5;
```

3. Monitor real-time updates:
```sql
-- Keep this query running in terminal
WATCH "SELECT * FROM history ORDER BY timestamp DESC LIMIT 5;"
```

### Database Schema Details
```sql
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    input_string VARCHAR(255) NOT NULL,
    output_result TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Encoding Logic

### Character Mapping
- Letters 'a' to 'z' → integers 1 to 26
- Underscore '_' → 0

### Rules
1. First character = count (package size)
2. Package values:
   - 'z' sequences combine with next character
   - Each 'z' adds 26
   - First non-'z' character completes package
3. Special cases:
   - Count of 0 → append 0
   - '_' as count → append 0
   - '_' as value → add 0 to sum

### Example
Input: `zdaaaaaaaabaaaaaaaabaaaaaaaabbaa`
- Count: z(26) + d(4) = 30
- Values: a×8 + b + a×8 + b + a×8 + b×2 + a×2
- Output: [34]

## Testing

### Example Requests
```bash
# Basic conversion
curl "http://localhost:8080/convert-measurements?input=abbcc"

# Complex z-sequence
curl "http://localhost:8080/convert-measurements?input=zdaaaaaaaabaaaaaaaabaaaaaaaabbaa"

# View history
curl "http://localhost:8080/history"
```

### Verification Steps
1. Make API request
2. Check JSON response
3. Verify in database:
```sql
SELECT * FROM history WHERE input_string = 'abbcc';
```
4. Check logs:
```bash
docker-compose logs app | grep "Converting"
```

## Project Structure
```
/project-root
├── app.py                # Flask application
├── converter.py          # Conversion logic
├── docker-compose.yml    # Service configuration
├── Dockerfile           # Container definition
├── requirements.txt     # Dependencies
├── version.txt         # Version info
└── logs/               # Application logs
```
