from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.database.session import get_db
from app.models.entities import Asset, Vulnerability, Finding

router = APIRouter(prefix="/assets", tags=["Assets"])

class AssetCreate(BaseModel):
    name: str
    asset_type: str
    ip_address: Optional[str] = None
    hostname: Optional[str] = None
    environment: str = "Production"
    is_internet_facing: bool = False
    criticality: str = "MEDIUM"
    owner: Optional[str] = None
    technologies: List[str] = []
    risk_score: float = 5.0

class VulnerabilityOut(BaseModel):
    id: str
    cve_id: Optional[str]
    title: str
    severity: str
    cvss_score: float
    remediation: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class AssetOut(BaseModel):
    id: str
    name: str
    asset_type: str
    ip_address: Optional[str]
    hostname: Optional[str]
    environment: str
    is_internet_facing: bool
    criticality: str
    owner: Optional[str]
    technologies: List[str]
    risk_score: float
    vulnerabilities: List[VulnerabilityOut] = []

    model_config = ConfigDict(from_attributes=True)

@router.get("", response_model=List[AssetOut])
def list_assets(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    return assets

@router.post("", response_model=AssetOut, status_code=status.HTTP_201_CREATED)
def create_asset(asset_in: AssetCreate, db: Session = Depends(get_db)):
    asset = Asset(**asset_in.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

@router.get("/{asset_id}", response_model=AssetOut)
def get_asset(asset_id: str, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(asset_id: str, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(asset)
    db.commit()
    return None
