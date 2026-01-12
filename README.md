# HokieTracker

A course tracking application for Virginia Tech students to monitor class availability and manage their course watchlist.

## Tech Stack

**Frontend:** React, TypeScript, Material UI, Vite  
**Backend:** FastAPI, Python  
**Database:** PostgreSQL  
**Infrastructure:** Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js
- Python 3.x

### Setup

1. Clone the repository
2. Create a `.env` file with database credentials
3. Start the database:
   ```
   docker compose up -d
   ```
4. Install and run the backend:
   ```
   cd server
   pip install -r requirements.txt
   uvicorn apis.main:app --reload
   ```
5. Install and run the frontend:
   ```
   cd client
   npm install
   npm run dev
   ```
