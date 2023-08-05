from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from station.app.api import dependencies
from station.app.schemas.users import User

router = APIRouter()


@router.get("/config")
def get_station_config(db: Session = Depends(dependencies.get_db)):
    # TODO store station configuration either inside yaml/config file or in db and read it here
    pass


@router.get("/config/test")
def test_station_config(user: User = Depends(dependencies.get_current_user)):
    print(user)


@router.put("/config")
def update_station_config():
    # TODO allow for updates and storage of configuration values for a station
    pass
