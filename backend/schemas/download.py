from models import DownloadDataBase
from utils import optional


class DownloadDataCreate(DownloadDataBase):
    pass


@optional
class DownloadDataUpdate(DownloadDataBase):
    pass
