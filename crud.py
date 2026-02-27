from sqlalchemy.orm import Session
import models, schemas
from geopy.distance import geodesic
import logging

# Configure logging to capture application events
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def get_address(db: Session, address_id: int):
    """Retrieve a single address by its ID."""
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve a list of addresses with pagination."""
    return db.query(models.Address).offset(skip).limit(limit).all()

def create_address(db: Session, address: schemas.AddressCreate):
    """Create a new address entry in the database."""
    db_address = models.Address(**address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    logger.info(f"Successfully created address ID: {db_address.id} for '{db_address.name}'")
    return db_address

def update_address(db: Session, address_id: int, address: schemas.AddressUpdate):
    """Update an existing address entry."""
    db_address = get_address(db, address_id)
    if not db_address:
        logger.warning(f"Update failed: Address ID {address_id} not found")
        return None
    
    update_data = address.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_address, key, value)
    
    db.commit()
    db.refresh(db_address)
    logger.info(f"Successfully updated address ID: {address_id}")
    return db_address

def delete_address(db: Session, address_id: int):
    """Delete an address entry from the database."""
    db_address = get_address(db, address_id)
    if not db_address:
        logger.warning(f"Delete failed: Address ID {address_id} not found")
        return None
    db.delete(db_address)
    db.commit()
    logger.info(f"Successfully deleted address ID: {address_id}")
    return db_address

def search_addresses_by_distance(db: Session, search: schemas.AddressSearch):
    """
    Search for addresses within a given distance (km) of specified coordinates.
    Uses the geodesic distance calculation from geopy.
    """
    logger.info(f"Searching addresses within {search.distance_km}km of ({search.latitude}, {search.longitude})")
    all_addresses = db.query(models.Address).all()
    results = []
    
    origin = (search.latitude, search.longitude)
    
    for addr in all_addresses:
        target = (addr.latitude, addr.longitude)
        distance = geodesic(origin, target).km
        if distance <= search.distance_km:
            results.append(addr)
    
    logger.info(f"Found {len(results)} addresses within the specified range")
    return results
