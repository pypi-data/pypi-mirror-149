from pandas.tseries.offsets import BusinessDay
from volatility.volatility_underlying import UnderlyingVolatility
import pandas as pd
import math


class FlatPriceVolatility(UnderlyingVolatility):

    def get_historical_fp_fwd_vol(self, index, forwardness, nb_days, maturities,
                                  date_value=None, delta_t=1):

        """
        computes the forward historical volatility for the given index
        """

        if isinstance(nb_days, int):
            nb_days = [nb_days]
        if date_value is None:
            date_value = [(pd.Timestamp.today() - BusinessDay(1)).strftime('%Y-%m-%d')]
        if isinstance(date_value, str):
            date_value = pd.to_datetime(date_value, format='%Y-%m-%d')

        line_range = range(1, forwardness + 1)
        df_out = pd.DataFrame(index=line_range, columns=nb_days)

        for line in line_range:
            try:
                _hist_vol = self._api.realized_fp_vol_forward(index, line, nb_days, date_from=date_value,
                                                              date_to=date_value, delta_t=delta_t)

                df_out.loc[line, :] = _hist_vol.loc[date_value, :]

            except Exception as e:
                msg = 'Could not compute line ' + str(line) + '.'
                msg += ' Error: ' + str(e)
                print(msg)

        _shift = 0.0
        df_out = df_out.iloc[:len(maturities)]
        df_out.index = [maturities[i - _shift] for i in df_out.index]

        return df_out

    def fp_implied_daily_move(self, index, nb_forwards, my_vol, date_value=None, maturities=None):

        mat_list = []
        prices = {}
        volatilities = {}

        daily_moves = {}
        for i in range(nb_forwards):
            m = mat_list[i]
            if not maturities:
                daily_moves[i] = prices[m] * volatilities[m] / 100.0 / math.sqrt(259.0)
            else:
                daily_moves[m] = prices[m] * volatilities[m] / 100.0 / math.sqrt(259.0)

        return daily_moves
