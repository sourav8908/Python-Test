from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas, database
from database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Address Book API",
    description="A simple API to manage addresses and find them by distance.",
    version="1.0.0"
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.post("/addresses/", response_model=schemas.AddressResponse, status_code=201)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    return crud.create_address(db=db, address=address)

@app.get("/addresses/", response_model=List[schemas.AddressResponse])
def read_addresses(skip: int = Query(0), limit: int = Query(100), db: Session = Depends(get_db)):
    return crud.get_addresses(db, skip=skip, limit=limit)

@app.get("/addresses/{address_id}", response_model=schemas.AddressResponse)
def read_address(address_id: int, db: Session = Depends(get_db)):
    db_address = crud.get_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.patch("/addresses/{address_id}", response_model=schemas.AddressResponse)
def update_address(address_id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)):
    db_address = crud.update_address(db=db, address_id=address_id, address=address)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.delete("/addresses/{address_id}", status_code=204)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = crud.delete_address(db=db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return None

@app.get("/search/", response_model=List[schemas.AddressResponse])
def search_addresses(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    dist: float = Query(..., gt=0, description="Distance in kilometers"),
    db: Session = Depends(get_db)
):
    search_schema = schemas.AddressSearch(latitude=lat, longitude=lon, distance_km=dist)
    return crud.search_addresses_by_distance(db, search_schema)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
