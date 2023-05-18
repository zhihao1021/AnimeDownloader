from models import DataBase
from utils import optional


class DataCreate(DataBase):
    pass


@optional
class DataUpdate(DataBase):
    pass
