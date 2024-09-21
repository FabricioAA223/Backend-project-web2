from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/videos/", response_model=schemas.Video)
def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    return crud.create_video(db=db, video=video)

@app.get("/videos/{video_id}", response_model=schemas.Video)
def read_video(video_id: int, db: Session = Depends(get_db)):
    db_video = crud.get_video(db=db, video_id=video_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_video

@app.get("/videos/", response_model=list[schemas.Video])
def read_videos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    videos = crud.get_videos(db=db, skip=skip, limit=limit)
    return videos

@app.post("/videos/{video_id}/comments/", response_model=schemas.Comment)
def create_comment(video_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment, video_id=video_id)

@app.post("/videos/{video_id}/favorites/")
def create_favorite(video_id: int, db: Session = Depends(get_db)):
    return crud.create_favorite_video(db=db, video_id=video_id)

@app.delete("/favorites/{item_id}")
def delete_favorite(item_id: int, db: Session = Depends(get_db)):
    item = crud.delete_item(db=db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Favorite item not found")
    return {"detail": "Favorite item deleted"}

@app.get("/videos/top/views/", response_model=list[schemas.Video])
def read_top_videos(db: Session = Depends(get_db)):
    return crud.get_top_10_videos_by_views(db=db)

@app.get("/videos/top/favorites/", response_model=list[schemas.FavoriteVideo])
def read_top_favorite_videos(db: Session = Depends(get_db)):
    return crud.get_top_10_recent_favorite_videos(db=db)

@app.get("/videos/search/")
def search_videos(query: str, db: Session = Depends(get_db)):
    return crud.search_videos(db=db, query=query)

@app.put("/videos/{video_id}/increment_views/")
def increment_views(video_id: int, db: Session = Depends(get_db)):
    return crud.increment_video_views(db=db, video_id=video_id)
