from pandas.tseries.offsets import BusinessDay, BusinessMonthEnd
import pandas as pd
import math
import datetime as dt
import numpy as np
from numbers_parser import Document


class TimeSeries:

    def __init__(self):
        doc = Document("src/brent.numbers")
        sheets = doc.sheets()
        tables = sheets[0].tables()
        rows = tables[0].rows()
        df = pd.DataFrame(rows)
        df.set_index(0, inplace=True)
        df.index = [dt.datetime(2019, 1, 1) + BusinessDay(i) for i in range(len(df.index))]
        for i in df.index:
            for j in df.columns:
                df.loc[i, j] = df.loc[i, j].value
        self.df = df

    def _fwd_match_table(self, date_list):
        _d = {}
        for date in date_list:
            _d.update({date: {i: date + BusinessMonthEnd(i) for i in range(1, 12)}})
        return {'future': _d}

    def mark_forward(self, index, line, date_from, date_to=None, volatility=False):
        """"""
        # df = pd.read_csv('historical_' + index + '.csv')
        return self.df[line]

    def realized_daily_move(self, index, line, nb_days, date_from, date_to, delta_t):
        """
        Computes the realized volatility of a forward line, taking the rolling into account
        """

        if isinstance(nb_days, int):
            _nb_days = [nb_days]
        else:
            _nb_days = nb_days

        date_from_prices = pd.Timestamp(date_from) - BusinessDay(n=max(_nb_days) + 30)

        price_series = self.mark_forward(index, line, date_from_prices, date_to)
        price_series_rolling = self.mark_forward(index, line + 1, date_from_prices, date_to)

        vol_series = price_series.diff(periods=delta_t)
        date_list = vol_series.index
        fwd_match_table = self._fwd_match_table(date_list)

        # Handle rolling
        for _i in range(delta_t, len(vol_series.index)):
            _d = vol_series.index[_i]
            _d_prev = vol_series.index[_i - delta_t]

            _m = fwd_match_table.get('future').get(_d).get(line)
            _m_prev = fwd_match_table.get('future').get(_d_prev).get(line)

            change_month = False

            if _m is None or _m_prev is None:
                if _d.month != _d_prev.month:
                    change_month = True

            if _m != _m_prev:
                change_month = True

            if change_month:
                _p = price_series[_d]
                _p_prev = price_series_rolling[_d_prev]

                vol_series[_d] = _p - _p_prev

        df_output = pd.DataFrame()
        for _d in _nb_days:
            _vol = vol_series.rolling(_d).std()
            _vol = _vol.loc[pd.Timestamp(date_from):].dropna(axis=0)

            _vol = _vol.multiply(math.sqrt(1.0 / delta_t))
            df_output[_d] = _vol

        if isinstance(nb_days, int):
            return df_output.iloc[:0]
        else:
            return df_output

    def realized_vol_forward(self, index, line, nb_days, date_from, date_to, delta_t=1):
        """
        Computes the realized volatility of a forward line, taking the rolling into account
        For spread = daily move
        """
        self.realized_daily_move(index, line, nb_days, date_from, date_to, delta_t)

    def realized_fp_vol_forward(self, index, line, nb_days, date_from, date_to, delta_t=1):
        """
        Computes the realized volatility of a forward line, taking the rolling into account
        """

        if isinstance(nb_days, int):
            _nb_days = [nb_days]
        else:
            _nb_days = nb_days

        date_from_prices = pd.Timestamp(date_from) - BusinessDay(n=_nb_days + 30)

        price_series = self.mark_forward(index, line, date_from_prices, date_to)
        price_series_rolling = self.mark_forward(index, line + 1, date_from_prices, date_to)

        vol_series = np.log(price_series).diff(periods=delta_t)

        # Handle rolling
        for _i in range(delta_t, len(vol_series.index)):
            _d = vol_series.index[_i]
            _d_prev = vol_series.index[_i - delta_t]

            _m = self._fwd_match_table().get('future').get(_d).get(line)
            _m_prev = self._fwd_match_table().get('future').get(_d_prev).get(line)

            change_month = False

            if _m is None or _m_prev is None:
                if _d.month != _d_prev.month:
                    change_month = True

            if _m != _m_prev:
                change_month = True

            if change_month:
                _p = price_series[_d]
                _p_prev = price_series_rolling[_d_prev]

                vol_series[_d] = np.log(_p) - np.log(_p_prev)

        df_output = pd.DataFrame()
        for _d in _nb_days:
            _vol = vol_series.rolling(_d).std()
            _vol = _vol.loc[pd.Timestamp(date_from):].dropna(axis=0)

            _vol = _vol.multiply(math.sqrt(259.0 / delta_t))

        if isinstance(nb_days, int):
            return df_output.iloc[:0]
        else:
            return df_output

    def realized_ts_vol_forward(self, index, line, nb_days, date_from, date_to, delta_t=1, tenor=1):
        """
        Computes the realized volatility of a forward line, taking the rolling into account
        """

        if isinstance(nb_days, int):
            _nb_days = [nb_days]
        else:
            _nb_days = nb_days

        date_from_prices = pd.Timestamp(date_from) - BusinessDay(n=_nb_days + 15)

        price_series = self.mark_forward(index, line, date_from_prices, date_to)
        price_series_rolling = self.mark_forward(index, line + 1, date_from_prices, date_to)

        price_series2 = self.mark_forward(index, line + tenor, date_from_prices, date_to)
        price_series2_rolling = self.mark_forward(index, line + tenor + 1, date_from_prices, date_to)

        ts_series = (price_series - price_series2).diff(periods=delta_t)

        # Handle rolling
        for _i in range(delta_t, len(ts_series.index)):
            _d = ts_series.index[_i]
            _d_prev = ts_series.index[_i - delta_t]

            _m = self._fwd_match_table().get('future').get(_d).get(line)
            _m_prev = self._fwd_match_table().get('future').get(_d_prev).get(line)

            if _m != _m_prev:
                term1 = price_series[_d] - price_series2[_d]
                term2 = price_series_rolling[_d_prev] - price_series2_rolling[_d_prev]

                ts_series[_d] = term1 - term2

        df_output = pd.DataFrame()
        for _d in _nb_days:
            _vol = ts_series.rolling(_d).std()
            _vol = _vol.loc[pd.Timestamp(date_from):].dropna(axis=0)
            _vol = _vol.multiply(math.sqrt(1.0 / delta_t))

        if isinstance(nb_days, int):
            return df_output.iloc[:0]
        else:
            return df_output
