from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func
from database import Base, engine, get_db
from models import Movies, Actors
from pydantic import BaseModel, SecretStr
from typing import List
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# =============================
# 📦 Pydantic Schemas
# =============================

class ActorBase(BaseModel):
    actor_name: str

class ActorPublic(ActorBase):
    id: int

    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    title: str
    year: int
    director: str
    actors: List[ActorBase]

class MoviePublic(BaseModel):
    id: int
    title: str
    year: int
    director: str
    actors: List[ActorPublic]

    class Config:
        orm_mode = True

class SummaryRequest(BaseModel):
    movie_id: int

class SummaryResponse(BaseModel):
    summary_text: str

# =============================
# 🎬 Movie Endpoints
# =============================

@app.post("/movies/", response_model=MoviePublic)
def create_movie(movie: MovieBase, db: Session = Depends(get_db)):
    db_movie = Movies(
        title=movie.title,
        year=movie.year,
        director=movie.director
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    for actor in movie.actors:
        db_actor = Actors(actor_name=actor.actor_name, movie_id=db_movie.id)
        db.add(db_actor)
    db.commit()

    # Reload movie with actors
    db.refresh(db_movie)
    return db_movie

@app.get("/movies/random/", response_model=MoviePublic)
def get_random_movie(db: Session = Depends(get_db)):
    movie = db.query(Movies).options(joinedload(Movies.actors)).order_by(func.random()).first()
    if not movie:
        raise HTTPException(status_code=404, detail="No movies found.")
    return movie

# =============================
# 🤖 LLM Summary Endpoint
# =============================

@app.post("/generate_summary/", response_model=SummaryResponse)
def generate_summary(request: SummaryRequest, db: Session = Depends(get_db)):
    movie = db.query(Movies).options(joinedload(Movies.actors)).filter(Movies.id == request.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")

    actor_list = ", ".join([actor.actor_name for actor in movie.actors])

    prompt = PromptTemplate(
        input_variables=["title", "year", "director", "actor_list"],
        template="Generate a short, engaging summary for the movie '{title}' ({year}), directed by {director} and starring {actor_list}."
    )

    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY is not set in the environment variables.")

    llm = ChatGroq(api_key=SecretStr(groq_api_key), model="llama3-70b-8192")
    chain = LLMChain(prompt=prompt, llm=llm)

    summary = chain.run({
        "title": movie.title,
        "year": movie.year,
        "director": movie.director,
        "actor_list": actor_list
    })

    return {"summary_text": summary}
