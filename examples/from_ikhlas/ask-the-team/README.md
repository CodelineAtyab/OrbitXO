# AskTheTeam Chat Agent

Lightweight n8n workflow that answers team-related questions using GPT and a backend service.

## For Quick Start

1. Clone repo:
   ```bash
   git clone <repo-url>
   cd ask-the-team

2. Start services:
   docker compose up -d --build

3. Open n8n: http://localhost:5678
   Import AskTheTeam.workflow.json.

4. Test via webhook:
   POST http://localhost:5678/webhook/ask
   Body: {"question":"Who are the members of Team CodeOrbit?","sessionId":"user1"}

5. Follow-up:
   Send {"question":"Repeat the list again","sessionId":"user1"} → Answer comes from memory.

6. Stop services:
   docker compose down