import pandas as pd

from fractions import Fraction
from typing import Iterable, Mapping, Union, Optional

from .stock import Stock

def as_stock_list(stocks: Union[Stock, Iterable[Stock], Mapping[str, Fraction]]):
        if isinstance(stocks, Mapping):
            return [ Stock(code, q) for code, q in stocks.items() ]
        elif isinstance(stocks, Iterable):
            return [ x for x in stocks ]
        return [ stocks ]

class Portfolio:
    def __init__(self,
                 seed: Stock,
                 stocks: Union[Stock, Iterable[Stock], Mapping[str, Fraction]],
                 t: Optional[pd.Timestamp]=None):
        if t is None:
            t = pd.Timestamp.now()
            
        self._seed_code = seed.code
        
        stock_list = [seed] + as_stock_list(stocks)
        
        cols = [ s.code for s in stock_list ]
        vals = [[ s.q for s in stock_list ]]
        
        self.df = pd.DataFrame(vals, index=[t], columns=cols)
    
    def append(self,
               stocks: Union[Stock, Iterable[Stock], Mapping[str, Fraction]],
               t: Optional[pd.Timestamp]=None):
        if t is None:
            t = pd.Timestamp.now()
        
        stock_list = as_stock_list(stocks)
            
        pass


