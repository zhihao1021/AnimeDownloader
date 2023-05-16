from models.anime import MyselfDataBase
from utils import optional


class MyselfDataCreate(MyselfDataBase):
    pass


@optional
class MyselfDataUpdate(MyselfDataBase):
    pass
