import csv
import io
import time
import struct
from datetime import datetime, timedelta
import logging
import logging.handlers

import pkg_resources
import requests

import pandas as pd
import seaborn as sns


class TSDataLogger():
    def __init__(self, title="TSDATA"):
        self._title=title

    def create(self):
        return logging.getLogger(self._title)

    def tcp(self, level=logging.DEBUG, host='localhost'):
        logger=self.create()
        logger.setLevel(level)
        handler = logging.handlers.SocketHandler(host, logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        logger.addHandler(handler)
        return logger

    def null(self):
        logger=self.create()
        logger.setLevel(logging.ERROR)
        handler=logging.NullHandler()
        logger.addHandler(handler)
        return logger


class TSDataQuery():
    def __init__(self, tsdata, accept='*/*'):
        self._tsdata=tsdata
        self._accept=accept

    @property
    def logger(self):
        return self._tsdata.logger

    def _validate(self):
        return True

    def _build(self):
        raise NotImplementedError

    def _decode(self, response):
        return response.text

    def acceptCsv(self):
        self._accept='text/csv'

    def acceptBinary(self):
        self._accept='application/octet-stream'

    def query(self, accept=None):
        try:
            if self._tsdata:
                if self._validate():
                    request=self._build()
                    response=self._tsdata.query(request, accept=accept or self._accept)
                    tstart=time.time()
                    data=self._decode(response)
                    self.logger.debug('decoding time %.1fs' % (time.time()-tstart))
                    return data
        except:
            pass

        return None


class TSDataQueryRecords(TSDataQuery):
    def __init__(self, tsdata, key):
        super().__init__(tsdata)
        self._key=key
        self._df=None
        self.reset()

    def reset(self):
        """Reset (clear) the stored record (the query)"""
        self._df=None
        self._utc=False
        self._condition=None
        self._asc=False
        self._limit=0
        self._offset=None

    @property
    def key(self):
        """Return the key of the record"""
        return self._key

    def where(self, condition):
        """Specify the where condition of the query"""
        self.reset()
        self._condition=condition
        return self

    def timein(self, condition):
        """Specify the 'WHERE time IN' condition of the query"""
        self.reset()
        return self.where(f'time IN {condition}')

    def yp(self, n=1):
        """Year Period condition (WHERE time in ypN, N=1 by default)"""
        if n>1:
            return self.timein(f'yp{n}')
        return self.timein('yp')

    def mp(self, n=1):
        """Month Period condition (WHERE time in mpN, N=1 by default)"""
        if n>1:
            return self.timein(f'mp{n}')
        return self.timein('mp')

    def wp(self, n=1):
        """Week Period condition (WHERE time in wpN, N=1 by default)"""
        if n>1:
            return self.timein(f'wp{n}')
        return self.timein('wp')

    def dp(self, n=1):
        """Day Period condition (WHERE time in dpN, N=1 by default)"""
        if n>1:
            return self.timein(f'dp{n}')
        return self.timein('dp')

    def f(self):
        """Full Period condition (WHERE time in f)"""
        return self.timein('f')

    def time(self, condition):
        """Specify the 'WHERE time' condition of the query"""
        return self.where(f'time {condition}')

    def fromto(self, stampFrom, stampTo):
        """Specify the 'WHERE time >= stampFrom [<= stampTo]' condition of the query"""
        return self.time(f'>= {stampFrom} <= {stampTo}')

    def utc(self):
        self.reset()
        self._utc=True
        return self

    def asc(self):
        """Specify the ASCending sort condition of the query"""
        self.reset()
        self._asc=True
        return self

    def desc(self):
        """Specify the DECCending sort condition of the query"""
        self.reset()
        self._asc=False
        return self

    def limit(self, count, offset=0):
        """Specify the LIMIT count [,offset] condition of the query"""
        self.reset()
        self._limit=count
        self._offset=offset
        return self

    def _validate(self):
        return True

    def _build(self):
        request=f'GET TS {self.key}'
        if self._utc:
            request += ' UTC'
        if self._condition:
            request += f' WHERE {self._condition}'
        if self._asc:
            request += ' ASC'
        else:
            request += ' DESC'
        if self._limit:
            request += ' LIMIT'
            if self._offset:
                request += f' {self._offset},'
            request += f' {self._limit}'

        return request

    def __repr__(self):
        return f'{self.__class__.__name__}(key={self.key}, {self._build()}, {self.count()} records)'

    def df(self):
        """"Execute the query (if needed) and return the corresponding pandas dataframe (df)"""
        try:
            if self._df is None:
                self.query()
            return self._df
        except:
            self.logger.exception('xx')
            pass

    def dataframe(self):
        """"Execute the query (if needed) and return the corresponding pandas dataframe (df)"""
        return self.df()

    def s(self):
        """Execute the query (if needed) and return the corresponding numpy serie (df['value'])"""
        try:
            return self.df()['value']
        except:
            pass

    def serie(self):
        """Execute the query (if needed) and return the corresponding numpy serie (df['value'])"""
        return self.s()

    def count(self):
        try:
            return self._df.count()[0]
        except:
            return 0

    def __len__(self):
        return self.count()

    def __iter__(self):
        return self.df().iterrows()

    def _loadData(self, stamps, values, units, flags, tz=None):
        data={'value': values, 'unit': units, 'flag': flags}
        index=pd.DatetimeIndex(stamps, dtype='datetime64[ns]', tz=tz)
        self._df=pd.DataFrame(data, index=index)
        return self._df

    def min(self):
        try:
            return self.df().min()[0]
        except:
            pass

    def max(self):
        try:
            return self.df().max()[0]
        except:
            pass

    def dtmin(self):
        try:
            return self.df().index.min()
        except:
            pass

    def dtmax(self):
        try:
            return self.df().index.min()
        except:
            pass

    def window(self):
        return (self.dtmin(), self.min(), self.dtmax(), self.max())


class TSDataQueryCsvRecords(TSDataQueryRecords):
    def __init__(self, tsdata, key):
        super().__init__(tsdata, key)
        self.acceptCsv()

    def _decode(self, response):
        try:
            self.reset()
            contentType=response.headers['content-type']
            if contentType=='text/csv':
                response.encoding='UTF-8'
                fcsv=io.StringIO(response.text)
                csvreader=csv.reader(fcsv, delimiter=',')
                next(csvreader)  # skip csv headers

                stamps=[]
                values=[]
                flags=[]
                units=[]

                for row in csvreader:
                    stamps.append(datetime.fromisoformat(row[0]))
                    values.append(float(row[1]))
                    units.append(row[2])
                    flags.append(row[3])

                self.logger.debug(f'{self.key}: retrieved {len(stamps)} records')
                self._df=self._loadData(stamps, values, units, flags)
                return self._df
        except:
            self.logger.exception(f'{__class__.__name__}._decode()')


class TSDataQueryBinaryRecords(TSDataQueryRecords):
    def __init__(self, tsdata, key):
        super().__init__(tsdata, key)
        self.acceptBinary()

    def _decode(self, response):
        try:
            self.reset()
            contentType=response.headers['content-type']
            if contentType=='application/octet-stream':
                dtRef=datetime(1, 1, 1)
                rformat='<QdHBB'
                rsize=struct.calcsize(rformat)
                rcount=len(response.content)/rsize

                stamps=[]
                values=[]
                flags=[]
                units=[]

                pos=0
                n=0
                while n<rcount:
                    # Read RECORD (TTTVVVVVVVVUUF.), T=msec since reference
                    data=struct.unpack(rformat, response.content[pos:pos+rsize])
                    stamps.append(dtRef+timedelta(milliseconds=data[0]))
                    values.append(data[1])
                    units.append(data[2])
                    flags.append(data[3])
                    pos+=rsize
                    n+=1

                self.logger.debug(f'{self.key}: retrieved {len(stamps)} records')
                self._df=self._loadData(stamps, values, units, flags)
                return self._df
        except:
            self.logger.exception(f'{__class__.__name__}._decode()')


class TSData():
    def __init__(self, url=None, timeout=3.0, token=None, user=None, logger=None, debug=False):
        self._debug=debug
        if logger is None:
            logger=TSDataLogger().tcp()
        self._logger=logger

        self._url=None
        self._token=None
        self._user=None
        self.setApiUrl(url)
        self.setApiToken(token, user)
        self._timeout=timeout

        sns.set()

    def _getUrl(self, service):
        return f'{self._url}/{service}'

    def setApiUrl(self, url):
        if url:
            self.logger.debug(f'using api-key {url}')
            self._url=url

    def setApiToken(self, token, user=None):
        if token:
            self.logger.debug(f'using api-key {token} (user {user})')
            self._token=token
            self._user=user

    def debug(self, state=True):
        self._debug=state

    def nodebug(self):
        self.debug(False)

    def isDebug(self):
        if self._debug:
            return True
        return False

    def getVersion(self):
        try:
            distribution=pkg_resources.get_distribution('digimat.tsdata')
            return distribution.parsed_version
        except:
            pass

    @property
    def version(self):
        return self.getVersion()

    @property
    def logger(self):
        return self._logger

    def __getitem__(self, key):
        return self.ts(key)

    def dump(self):
        pass

    def __repr__(self):
        return f'{self.__class__.__name__}({self._url}:{self._token}:{self._user})'

    def _get(self, service, params=None, accept='*/*'):
        url=self._getUrl(service)
        if url and self._token:
            headers={'x-api-key': self._token, 'Accept': accept}
            try:
                tstart=time.time()
                r=requests.get(url, headers=headers, params=params)
                self.logger.debug('GET(%s) %.1fs %s:%dkb' % (r.request.url, time.time()-tstart, r.headers['content-type'], len(r.content)/1024))
                if r and r.status_code==requests.codes.ok:
                    return r
            except:
                self.logger.error(f'GET({url})')
        else:
            self.logger.error('api url invalid')

    def query(self, query, accept='*/*'):
        """Execute the tsdata query"""
        try:
            return self._get('ts/query', params={'query': query}, accept=accept)
        except:
            pass

    def ts(self, key):
        """Return a TS (TimeSerie) query for the given key"""
        return TSDataQueryBinaryRecords(self, key)


if __name__ == "__main__":
    pass
