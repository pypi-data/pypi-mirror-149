import datetime
import math

import numpy as np
import pandas as pd

from meixmetric.calculate import calc as cc
from meixmetric.exc.mx_exc import BizException
from meixmetric.utils.date_util import calc_date


class CalcDataFrame(object):
    """
    基于pd.DataFrame的指标计算工具类
    """

    @staticmethod
    def get_fixed_return(data: pd.DataFrame, suffix: str = 'fixed_return', swanav_column: str = 'swanav'):
        """
        计算当前df周期性的收益率
        
        :param data: 一组周期性的复权累计净值数据，日期为索引，升序排列
        :param suffix: 返回列的后缀名
        :param swanav_column: 净值数据列名
        """
        ret = pd.DataFrame(data=cc.return_rate(data[swanav_column], data[swanav_column].shift()))
        ret.columns = [suffix]
        return ret

    @staticmethod
    def get_period_return(data: pd.DataFrame, period: [str, list], interval_insufficient: bool = True,
                          method: str = 'ffill', offset: int = -1,
                          start_date: datetime.datetime = datetime.datetime(year=1990, month=1, day=1),
                          end_date: datetime.datetime = datetime.datetime.today(),
                          suffix: str = '_return', swanav_column: str = 'swanav', annualized: bool = False,
                          natural: bool = True):
        """
        获取某一时间段的收益率及年化收益率<br>

        Parameters
        ----------
        data:
            一组周期性的复权累计净值数据，日期为索引，升序排列

        period :
            时间区间或时间区间数组；取值参考date_util.ALL_DATE_PERIOD

        interval_insufficient:
            时间区间数据不足是否仍计算

        method :
            计算上一区间末日期取值方式；'ffill'不存在则取前一个, 'bfill'不存在则后一个, 'nearest'取最近的

        exacting :
            是否和预期日期一致时时进行偏移 默认True，设置false时全部偏移

        start_date:
            计算数据开始日期

        end_date:
            计算数据结束日期

        offset :
            上一区间末未匹配到数据时的偏移量

        suffix:
            返回列的后缀名

        swanav_column:
            净值数据列名

        annualized:
            是否同时计算年化收益率

        natural:
            年化时指定是否使用自然日，默认True，Fasle使用工作日

        """
        result = pd.DataFrame()
        cal_data = data[start_date:end_date]
        if isinstance(period, str):
            period = [period]

        if isinstance(period, list):
            for per in period:
                temp = cal_data.apply(CalcDataFrame.get_row_return,
                                      args=(
                                          data, per, interval_insufficient, method, offset, suffix,
                                          swanav_column,
                                          annualized, natural),
                                      axis=1)
                result = temp if len(result) == 0 else pd.merge(result, temp, how='left', left_index=True,
                                                                right_index=True)
        else:
            raise BizException("period类型错误")
        return result

    @staticmethod
    def get_row_return(row, data: pd.DataFrame, period: str, interval_insufficient: bool = True, method: str = 'ffill',
                       offset: int = -1,
                       suffix: str = '_return', swanav_column: str = 'swanav', annualized: bool = False,
                       natural: bool = True):
        """
        获取某一日期（row）对应的period的收益率及年化收益率

        Parameters
        ----------
        row:
            data中的某一行

        data:
            一组周期性的复权累计净值数据，日期为索引，升序排列

        period :
            时间区间；取值参考date_util.ALL_DATE_PERIOD

        interval_insufficient:
            时间区间数据不足是否仍计算

        method :
            计算上一区间末日期取值方式；'ffill'不存在则取前一个, 'bfill'不存在则后一个, 'nearest'取最近的

        exacting :
            是否和预期日期一致时时进行偏移 默认True，设置false时全部偏移

        offset :
            上一区间末日期未取到值时的偏移量

        suffix:
            返回列的后缀名

        swanav_column:
            净值数据列名

        annualized:
            是否同时计算年化收益率

        natural:
            年化时指定是否使用自然日，默认True，Fasle使用工作日
        """
        result = pd.Series(dtype=float)
        curr_date = row.name
        curr_idx, per_date = CalcDataFrame.get_loc(data.index, curr_date, period=period, method=method, offset=offset)
        if per_date < data.index[0] and not interval_insufficient:
            result[period + suffix] = np.nan
            if annualized:
                result[period + suffix + '_a'] = np.nan
            return result

        previous_date = data.index[curr_idx]
        result[period + suffix] = np.NaN if curr_date == previous_date else cc.return_rate(row[swanav_column],
                                                                                           data.iloc[curr_idx][
                                                                                               swanav_column])
        if annualized:
            # 计算年化收益
            if natural:
                year_days = 365
                days = (curr_date - previous_date).days
            else:
                year_days = 252
                days = len(pd.bdate_range(start=previous_date, end=curr_date)) - 1
            result[period + suffix + '_a'] = cc.return_annualized(result[period + suffix], year_days, days)
        return result

    @staticmethod
    def get_loc(index: pd.DataFrame.index, curr_date: datetime.datetime, period: str, method: str = 'nearest',
                offset: int = 0):
        """
        获取某一日期curr_date 对应的period的在index中的另一日期 previous_date

        Parameters
        ----------
        index:
            一组日期索引

        curr_date:
            需计算的日期

        period :
            时间区间；取值参考date_util.ALL_DATE_PERIOD

        method :
            计算另一日期previous_date的取值方式；'ffill'不存在则取前一个, 'bfill'不存在则后一个, 'nearest'取最近的

        offset :
            上一区间末日期未取到值时的偏移量

        """
        per_date = calc_date(curr_date, period, index[0])
        loc_old = index.get_indexer([per_date], method=method)[0]
        loc = loc_old if loc_old >= 0 else 0
        if per_date < index[loc]:
            loc_temp = loc + offset
            if loc_temp > len(index):
                loc = len(index)
            elif loc_temp < 0:
                loc = 0
            else:
                loc = loc_temp
        return loc, per_date

    @staticmethod
    def get_period_stdev(data: pd.DataFrame, period: [str, list], interval_insufficient: bool = True,
                         method: str = 'bfill',
                         start_date: datetime.datetime = datetime.datetime(year=1990, month=1, day=1),
                         end_date: datetime.datetime = datetime.datetime.today(),
                         suffix: str = '_std', return_column: str = 'week_return', annualized: bool = False,
                         sections: int = 52):
        """
        计算年化标准差及其年化，年化标准差也就是年化波动率

        年化波动率=stdev(区间周收益率)*sqrt（52）；计算年化波动率一般使用周度收益率

        Parameters
        ----------
        data:
            一组时间为索引的收益率

        period:
            时间区间或时间区间数组；取值参考date_util.ALL_DATE_PERIOD

        interval_insufficient:
            时间区间数据不足是否仍计算

        method:
            计算区间开始日期的取值方式；'ffill'不存在则取前一个, 'bfill'不存在则后一个, 'nearest'取最近的

        start_date:
            计算数据开始日期

        end_date:
            计算数据结束日期

        suffix:
            标准差后缀

        return_column:
            收益率列名

        annualized:
            是否同时计算年化波动率

        sections:
            年化周期数量

        """
        cal_data = data[start_date:end_date]
        if isinstance(period, str):
            period = [period]
        if isinstance(period, list):
            result = pd.DataFrame()
            for per in period:
                temp = cal_data.apply(CalcDataFrame.get_row_stdev,
                                      args=(
                                          data, per, interval_insufficient, method, suffix, return_column,
                                          annualized, sections),
                                      axis=1)
                result = temp if len(result) == 0 else pd.merge(result, temp, how='left', left_index=True,
                                                                right_index=True)
        else:
            raise BizException("period类型错误")
        return result

    @staticmethod
    def get_row_stdev(row, data: pd.DataFrame, period: str, interval_insufficient: bool = True, method: str = 'nearest',
                      suffix: str = '_stdev',
                      return_column: str = 'week_return',
                      annualized: bool = False,
                      sections: int = 52):
        """
        获取某一日期（row）对应的period的收益率及年化收益率

        Parameters
        ----------
        row:
            data中的某一行

        data:
            一组时间为索引的收益率

        period:
            时间区间或时间区间数组；取值参考date_util.ALL_DATE_PERIOD

        interval_insufficient:
            时间区间数据不足是否仍计算

        method:
            计算区间开始日期的取值方式；'ffill'不存在则取前一个, 'bfill'不存在则后一个, 'nearest'取最近的

        suffix:
            标准差后缀

        return_column:
            收益率列名

        annualized:
            是否同时计算年化波动率

        sections:
            年化周期数量
        """
        result = pd.Series(dtype=float)
        curr_date = row.name
        curr_idx, per_date = CalcDataFrame.get_loc(data.index, curr_date, period=period, method=method)
        if per_date < data.index[0] and not interval_insufficient:
            result[period + suffix] = np.nan
            if annualized:
                result[period + suffix + '_a'] = np.nan
            return result
        previous_date = data.index[curr_idx]
        # 标准差
        result[period + suffix] = data[previous_date:curr_date].resample('w').ffill()[return_column].std()
        if annualized:
            # 年化波动率
            result[period + suffix + '_a'] = cc.return_stdev_a(result[period + suffix], sections)
        return result

    @staticmethod
    def get_period_max_retracement(data: pd.DataFrame, period: [str, list], interval_insufficient: bool = True,
                                   method: str = 'MF', offset: int = -1,
                                   start_date: datetime.datetime = datetime.datetime(year=1990, month=1, day=1),
                                   end_date: datetime.datetime = datetime.datetime.today(),
                                   suffix: str = '_max_retracement', swanav_column: str = 'swanav'):
        """
        获取某一时间段中各个日期对应的最大回撤

        Parameters
        ----------
        data:
            一组以日期为索引升序排列的净值数据

        interval_insufficient:
            时间区间数据不足是否仍计算

        method:
            MF-最高净值回落法
            MD-最大跌幅法

        offset:
            偏移量

        start_date:
            计算开始日期

        end_date:
            计算结束日期

        suffix:
            计算结果列后缀名称

        swanav_column:
            净值列名称

        """
        cal_data = data[start_date:end_date]
        result = None
        if isinstance(period, str):
            period = [period]
        if isinstance(period, list):
            result = pd.DataFrame()
            for per in period:
                temp = cal_data.apply(func=CalcDataFrame.get_row_max_retracement,
                                      args=(
                                          data, per, interval_insufficient, method, offset, suffix,
                                          swanav_column),
                                      axis=1)
                result = temp if len(result) == 0 else pd.merge(result, temp, how='left', left_index=True,
                                                                right_index=True)
        return result

    @staticmethod
    def get_row_max_retracement(row, data: pd.DataFrame, period: str, interval_insufficient: bool = True,
                                method: str = 'MF', offset: int = -1,
                                suffix: str = '_max_retracement', swanav_column: str = 'swanav'):
        """
        获取某一日期（一行数据）的最大回撤

        Parameters
        ----------
        row:
            某日期数据

        data:
            一组以日期为索引升序排列的净值数据

        interval_insufficient:
            时间区间数据不足是否仍计算

        method:
            MF-最高净值回落法
            MD-最大跌幅法

        suffix:
            计算结果列后缀名称

        swanav_column:
            净值列名称

        """
        result = pd.Series(dtype=float)
        curr_date = row.name
        curr_idx, per_date = CalcDataFrame.get_loc(data.index, curr_date, period=period, method='ffill', offset=offset)
        real_date = data.index[curr_idx]

        max_retracement = np.nan
        edate = pd.NaT
        bdate = pd.NaT
        rdate = pd.NaT
        rdays = np.nan
        if per_date >= data.index[0] or interval_insufficient:
            per_data = data[real_date:curr_date]
            if method == 'MF':
                # 从高净值跌到低净值
                per_retracement: pd.Series = 1 - per_data[swanav_column] / per_data[swanav_column].expanding(
                    min_periods=1).max()
                if len(per_retracement.dropna()) != 0:
                    edate = per_retracement.idxmax()
                    max_retracement = per_retracement[edate]
                    max_net = per_data[:edate][swanav_column].max()
                    max_net_data = per_data[per_data[swanav_column] >= max_net]
                    bdate = max_net_data[max_net_data.index < edate].index.max()
                    rdate = max_net_data[max_net_data.index > edate].index.min()
                    if rdate is not np.nan:
                        rdays = (rdate - edate).days
            elif method == 'MD':
                per_data.sort_index(ascending=False, inplace=True)
                per_retracement: pd.Series = per_data[swanav_column].expanding(min_periods=1).min() / per_data[
                    swanav_column] - 1
                per_data.sort_index(ascending=True, inplace=True)
                if len(per_retracement.dropna()) != 0:
                    bdate = per_retracement.idxmin()
                    max_retracement = per_retracement[bdate]
                    min_net = per_data[bdate:][swanav_column].min()
                    min_net_data = per_data[per_data[swanav_column] <= min_net]
                    edate = min_net_data[min_net_data.index > bdate].index.min()
                    max_net = per_data[per_data.index == bdate][swanav_column].max()
                    max_net_data = per_data[per_data[swanav_column] >= max_net]
                    rdate = max_net_data[max_net_data.index > edate].index.min()
                    if rdate is not np.nan:
                        rdays = (rdate - edate).days
            else:
                raise BizException('最大回撤method错误,MF或MD')
        result[period + suffix] = max_retracement
        result[period + suffix + '_bdate'] = bdate
        result[period + suffix + '_edate'] = edate
        result[period + suffix + '_rdate'] = rdate
        result[period + suffix + '_rdays'] = rdays
        return result

    @staticmethod
    def get_sharp(ret_a: pd.DataFrame = None, nrr: float = 0.0175, stenv_a: pd.DataFrame = None):
        """
        计算夏普比率

        Parameters
        ----------
        ret_a:
            不同期限的年化收益率

        nrr:
            无风险收益率，默认取中国银行一年定期利率0.0175

        stenv_a:
            不同期限的年化波动率（行列数和期限需与收益率期限对应上）
        """
        temp = stenv_a.applymap(
            lambda x: x if isinstance(x, int) or isinstance(x, float) else np.nan)
        return np.true_divide(ret_a - nrr, np.asarray(temp))

    @staticmethod
    def get_karma(ret_a: pd.DataFrame = None, nrr: float = 0.0175, max_retracement: pd.DataFrame = None):
        """
        计算夏普比率

        Parameters
        ----------
        ret_a:
            不同期限的年化收益率

        nrr:
            无风险收益率，默认取中国银行一年定期利率0.0175

        max_retracement:
            不同期限的最大回撤（行列数和期限需与收益率期限对应上）
        """
        temp = max_retracement.applymap(
            lambda x: x if isinstance(x, int) or isinstance(x, float) else np.nan)
        return np.true_divide(ret_a - nrr, np.asarray(temp))

    @staticmethod
    def get_period_down_stdenv(data: pd.DataFrame, period: [str, list], interval_insufficient: bool = True,
                               start_date: datetime.datetime = datetime.datetime(year=1990, month=1, day=1),
                               end_date: datetime.datetime = datetime.datetime.today(),
                               suffix: str = '_down_stdenv', return_column: str = 'week_return',
                               snrr: float = None,
                               nrr: float = 0.0175, sections: float = 52):

        """
        计算下行标准差

        Parameters
        ----------
        data:
            一组固定周期的收益率数据

        period:
            时间区间或时间区间数组；取值参考date_util.ALL_DATE_PERIOD

        interval_insufficient:
            时间区间数据不足是否仍计算

        start_date:
            计算数据开始日期

        end_date:
            计算数据结束日期

        suffix:
            返回列名称

        snrr:
            一个周期的无风险收益率，此项设置后，nrr参数失效

        nrr:
            一年期的无风险收益率，默认取中国银行一年定期利率0.0175

        sections:
            一年中包含的周期数量，如：周度52 月度12

        return_column:
            收益率列的名称
        """
        result = pd.DataFrame()
        cal_data = data[start_date:end_date]
        if isinstance(period, str):
            period = [period]

        if isinstance(period, list):
            for per in period:
                temp = cal_data.apply(CalcDataFrame.get_row_down_stdenv,
                                      args=(data, per, interval_insufficient, suffix,
                                            return_column,
                                            snrr, nrr, sections), axis=1)
                result = temp if len(result) == 0 else pd.merge(result, temp, how='left', left_index=True,
                                                                right_index=True)
        else:
            raise BizException("period类型错误")
        return result

    @staticmethod
    def get_row_down_stdenv(row, data: pd.DataFrame, period: [str, list], interval_insufficient: bool = True,
                            suffix: str = '_down_stdenv', return_column: str = 'week_return', snrr: float = None,
                            nrr: float = 0.0175, sections: float = 52):
        """
        计算下行标准差

        Parameters
        ----------
        row:
            某个时间点的数据

        data:
            一组固定周期的收益率数据

        period:
            时间区间或时间区间数组；取值参考date_util.ALL_DATE_PERIOD

        interval_insufficient:
            时间区间数据不足是否仍计算

        suffix:
            返回列名称

        snrr:
            一个周期的无风险收益率，此项设置后，nrr参数失效

        nrr:
            一年期的无风险收益率，默认取中国银行一年定期利率0.0175

        sections:
            一年中包含的周期数量，如：周度52 月度12

        return_column:
            收益率列的名称
        """
        result = pd.Series(dtype=float)
        curr_date = row.name
        real_date = calc_date(curr_date, period, data.index[0])
        if real_date < data.index[0] and not interval_insufficient:
            result[period + suffix] = pd.NA
        else:
            cal_data = data[real_date:curr_date]
            if snrr is None:
                snrr = (1 + nrr) ** (1 / sections) - 1
            result[period + suffix] = cal_data[cal_data[return_column] < snrr][return_column].std()
        return result

    @staticmethod
    def get_sortino(ret_a: pd.DataFrame = None, nrr: float = 0.0175, down_stdenv: pd.DataFrame = None):
        """
        索提诺比率=（年化收益率-无风险收益率）/(下行标准差*sqrt(52))

        Parameters
        ----------
        ret_a:
            不同期限的年化收益率

        nrr:
            无风险收益率，默认取中国银行一年定期利率0.0175

        down_stdenv:
            不同期限的下行标准差（行列数和期限需与收益率期限对应上）
        """
        temp = down_stdenv.applymap(
            lambda x: x if isinstance(x, int) or isinstance(x, float) else np.nan)
        return np.true_divide(ret_a - nrr, np.asarray(temp * math.sqrt(52)))

    @staticmethod
    def get_period_beta(fund_ret: pd.DataFrame, market_ret: pd.DataFrame, period: [str, list],
                        interval_insufficient: bool = True, offset: int = -1,
                        start_date: datetime.datetime = datetime.datetime(year=1990, month=1, day=1),
                        end_date: datetime.datetime = datetime.datetime.today(),
                        fund_colunm: str = 'fund_ret',
                        market_colunm: str = 'market_ret',
                        suffix: str = '_beta',
                        direction: str = 'backward'):
        """
        贝塔系数=产品周收益率与市场指数周收益率的协方差/市场指数周收益率的方差

        Parameters
        ----------
        fund_ret:
            产品周度收益率

        market_ret:
            市场周度收益率

        fund_colunm:
            产品周度收益率列名称

        market_colunm:
            市场周度收益率列名称

        start_date:
            计算开始日期

        end_date:
            计算结束日期

        period:
            计算的区间

        interval_insufficient:
            区间数据不足是否仍计算

        suffix:
            返回列名的后缀

        direction:
            ‘backward’ (default), ‘forward’, or ‘nearest’
            产品周度收益率和市场指数收益率对齐方式
            是否搜索先前、后续或最接近的匹配项。
        """
        result = pd.DataFrame()
        all_data = pd.merge_asof(left=fund_ret[fund_colunm], right=market_ret[market_colunm], left_index=True,
                                 right_index=True,
                                 direction=direction)
        if fund_colunm == market_colunm:
            fund_colunm = fund_colunm + '_x'
            market_colunm = market_colunm + '_y'
        cal_data = fund_ret[start_date:end_date]
        if isinstance(period, str):
            period = [period]
        if isinstance(period, list):
            for per in period:
                temp = cal_data.apply(CalcDataFrame.get_row_beta,
                                      args=(
                                          all_data, per, interval_insufficient, offset, fund_colunm, market_colunm,
                                          suffix),
                                      axis=1)
                result = temp if len(result) == 0 else pd.merge(result, temp, how='left', left_index=True,
                                                                right_index=True)
        else:
            raise BizException("period类型错误")
        return result

    @staticmethod
    def get_row_beta(row, all_data: pd.DataFrame, period, interval_insufficient, offset, fund_colunm, market_colunm,
                     suffix):
        result = pd.Series(dtype=float)
        curr_date = row.name
        curr_idx, real_date = CalcDataFrame.get_loc(all_data.index, curr_date, period=period, method='ffill',
                                                    offset=offset)
        pre_date = all_data.index[curr_idx]
        if real_date < all_data.index[0] and not interval_insufficient:
            result[period + suffix] = pd.NA
        else:
            real_data = all_data[pre_date:curr_date]
            result[period + suffix] = real_data[fund_colunm].cov(real_data[market_colunm]) / np.var(
                real_data[market_colunm])
        return result

    @staticmethod
    def get_alpha(fund_ret_a: pd.DataFrame, market_ret_a: pd.DataFrame, beta: pd.DataFrame, direction: str = 'backward',
                  nrr: float = 0.0175):

        """
        计算阿尔法系数
        阿尔法系数=（产品年化收益率-无风险收益率）-贝塔系数*（市场指数年化收益率-无风险收益率）

        Parameters
        ----------
        fund_ret_a:
            不同期限的产品年化收益率

        market_ret_a:
            不同期限的市场指数年化收益率
        beta:
            不同期限的beta系数
        nrr:
            无风险收益率，默认取中国银行一年定期利率0.0175
        """
        fund_ret_a = fund_ret_a.copy()
        fund_ret_a['temp_colunm'] = 1
        mg_data = pd.merge_asof(fund_ret_a['temp_colunm'], market_ret_a, left_index=True, right_index=True,
                                direction=direction).drop(columns=['temp_colunm'])
        return np.subtract(fund_ret_a.drop(columns=['temp_colunm']) - nrr, np.multiply(beta, mg_data - nrr))
