import time


class NexusRequest:
    uids: str
    startTs: float
    endTs: float
    dataSource: int
    resolution: int

    def __init__(self, uids, startTs, endTs, dataSource, resolution):
        """Genera la estructura a pasar al método de recuperación de variables históricas
        uids: Variables que queremos leer
        startTS: fecha de inicio en formato....
        endTS: fecha de fin en formato...
        dataSource:[ 0-->RAW, 1-->STATS_PER_HOUR, 2-->STATS_PER_DAY, 3-->STATS_PER_MONTH, 4-->TRANSIENT ]
            resolution: de 0 a 10 [ RES_30_SEC, RES_1_MIN, RES_15_MIN, RES_1_HOUR, RES_1_DAY, RES_1_MONTH, RES_1_YEAR, RES_5_MIN, RES_200_MIL, ES_500_MIL, RES_1_SEC ]
        """
        self.uids = uids
        self.startTs = time.mktime(startTs.timetuple())
        self.endTs = time.mktime(endTs.timetuple())
        self.dataSource = dataSource
        self.resolution = resolution
