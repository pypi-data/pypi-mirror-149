from pandas.tseries.offsets import BusinessDay
from src.volatility_underlying import UnderlyingVolatility
import pandas as pd
import math


class TimeSpreadVolatility(UnderlyingVolatility):

    def get_historical_fwd_ts_vol(self, index, forwardness, nb_days, maturities,
                                  date_value: None, delta_t=1, tenor=1):

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
                _hist_vol = self._api.realized_ts_vol_forward(index, line, nb_days, date_from=date_value,
                                                              date_to=date_value, delta_t=delta_t, tenor=tenor)

                df_out.loc[line, :] = _hist_vol.loc[date_value, :]

            except Exception as e:
                msg = 'Could not compute line ' + str(line) + '.'
                msg += ' Error: ' + str(e)
                print(msg)

        _shift = 0.0
        df_out = df_out.iloc[:len(maturities)]
        df_out.index = [maturities[i - _shift] + '/' + maturities[i - _shift + tenor] for i in df_out.index]

        return df_out

    def ts_implied_daily_move(self, index, nb_forwards, tenor, my_vol, date_value=None, maturities=None):

        def _daily_move(month_fwd):
            delta_t1 = math.exp(-alpha * month_fwd / 12)
            delta_t2 = math.exp(-alpha * (tenor + month_fwd) / 12)

            term1 = sig1 / alpha * (delta_t1 - delta_t2)
            term2 = sig2 * (tenor / 12 - (delta_t1 - delta_t2) / alpha)
            dm = math.sqrt(term1 * term1 + term2 * term2 + 2.0 * rho * term1 * term2) / math.sqrt(259.0)

            return dm

        sig1 = my_vol['sigma1']
        sig2 = my_vol['sigma2']
        rho = my_vol['rho']
        alpha = my_vol['alpha']

        daily_moves = {}
        if not maturities:
            for i in range(nb_forwards):
                daily_moves[i] = _daily_move(i)

        else:
            mat_list = list(maturities.values)
            for m1, d in maturities:
                m2 = mat_list[mat_list.index(m1) + tenor]
                nb_days = (d - date_value.date()).days
                daily_moves[m1 + '/' + m2] = _daily_move(nb_days / 21.0)

        return daily_moves
