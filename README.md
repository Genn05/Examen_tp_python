# LLM-Powered Movie & Actor Explorer Application

## Overview
This application consists of:
1. **FastAPI Backend**: Manages movies and actors, provides endpoints for random movie retrieval and LLM-powered summaries.
2. **Streamlit Frontend**: Allows users to explore random movies and request summaries.

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL
- `.env` file with `DATABASE_URL` and `GROQ_API_KEY`

### Backend Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up the database:
   ```bash
   createdb moviedb
   ```
3. Run the FastAPI server:
   ```bash
   uvicorn main_fastapi:app --reload
   ```

### Frontend Setup
1. Run the Streamlit app:
   ```bash
   streamlit run main_streamlit.py
   ```

### Testing
1. Use the FastAPI Swagger UI (`http://localhost:8000/docs`) to add movie data via POST `/movies/`.
2. Explore movies and summaries via the Streamlit app.
