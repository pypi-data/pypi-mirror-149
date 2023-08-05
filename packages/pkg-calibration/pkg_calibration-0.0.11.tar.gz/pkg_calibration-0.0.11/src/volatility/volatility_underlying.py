from pandas.tseries.offsets import BusinessDay
from volatility.time_series import TimeSeries
import pandas as pd


class UnderlyingVolatility:
    _api = TimeSeries()

    def get_historical_daily_move(self, index, forwardness, nb_days, maturities,
                                  date_value=None, delta_t=1):

        """
        Computes the forward historical daily move for the given index
        """

        if isinstance(nb_days, int):
            nb_days = [nb_days]
        if date_value is None:
            date_value = (pd.Timestamp.today() - BusinessDay(1)).strftime('%Y-%m-%d')
        if isinstance(date_value, str):
            date_value = pd.to_datetime(date_value, format='%Y-%m-%d')

        line_range = range(1, forwardness + 1)
        df_out = pd.DataFrame(index=line_range, columns=nb_days)

        for line in line_range:
            try:
                _hist_vol = self._api.realized_daily_move(index, line, nb_days, date_from=date_value,
                                                          date_to=date_value, delta_t=delta_t)

                df_out.loc[line, :] = _hist_vol.loc[date_value, :]

            except Exception as e:
                msg = 'Could not compute line ' + str(line) + '.'
                msg += ' Error: ' + str(e)
                print(msg)

        _shift = 0
        df_out = df_out.iloc[:len(maturities)]
        df_out.index = [maturities[i - _shift] for i in df_out.index]

        return df_out
