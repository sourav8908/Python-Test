from sqlalchemy.orm import Session
import models, schemas
from geopy.distance import geodesic
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_address(db: Session, address_id: int):
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Address).offset(skip).limit(limit).all()

def create_address(db: Session, address: schemas.AddressCreate):
    db_address = models.Address(**address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    logger.info(f"Created address: {db_address.id}")
    return db_address

def update_address(db: Session, address_id: int, address: schemas.AddressUpdate):
    db_address = get_address(db, address_id)
    if not db_address:
        return None
    
    update_data = address.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_address, key, value)
    
    db.commit()
    db.refresh(db_address)
    logger.info(f"Updated address: {address_id}")
    return db_address

def delete_address(db: Session, address_id: int):
    db_address = get_address(db, address_id)
    if not db_address:
        return None
    db.delete(db_address)
    db.commit()
    logger.info(f"Deleted address: {address_id}")
    return db_address

def search_addresses_by_distance(db: Session, search: schemas.AddressSearch):
    all_addresses = db.query(models.Address).all()
    results = []
    
    origin = (search.latitude, search.longitude)
    
    for addr in all_addresses:
        target = (addr.latitude, addr.longitude)
        distance = geodesic(origin, target).km
        if distance <= search.distance_km:
            results.append(addr)
            
    return results
