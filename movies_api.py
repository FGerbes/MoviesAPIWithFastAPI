from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

movies = {}


class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str


tags_metadata = [
    {
        "name": "movies",
        "description": "Operations related to movies",
    },
]


@app.post("/movies/", tags=["movies"])
async def create_movie(movie: Movie):
    if movie.id in movies:
        raise HTTPException(status_code=400, detail="Movie already exists")

    movies[movie.id] = movie
    return movie


@app.get("/movies/{movie_id}", response_model=Movie, tags=["movies"])
async def read_movie(movie_id: int):
    movie = movies.get(movie_id)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie


@app.put("/movies/{movie_id}", response_model=Movie, tags=["movies"])
async def update_movie(movie_id: int, movie: Movie):
    if movie_id not in movies:
        raise HTTPException(status_code=404, detail="Movie not found")

    movies[movie_id] = movie
    return movie


@app.delete("/movies/{movie_id}", tags=["movies"])
async def delete_movie(movie_id: int):
    if movie_id not in movies:
        raise HTTPException(status_code=404, detail="Movie not found")

    del movies[movie_id]
    return {"message": "Movie has been deleted."}
