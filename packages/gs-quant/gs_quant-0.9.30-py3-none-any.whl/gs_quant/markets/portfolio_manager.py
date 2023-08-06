"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
import datetime as dt
import logging
from time import sleep
from typing import List, Union

import pandas as pd

from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.reports import GsReportApi
from gs_quant.entities.entitlements import Entitlements
from gs_quant.entities.entity import PositionedEntity, EntityType
from gs_quant.errors import MqError
from gs_quant.errors import MqValueError
from gs_quant.markets.report import PerformanceReport
from gs_quant.markets.report import ReportJobFuture
from gs_quant.target.common import Currency
from gs_quant.target.portfolios import RiskAumSource

_logger = logging.getLogger(__name__)


class CustomAUMDataPoint:
    """

    Custom AUM Data Point represents a portfolio's AUM value for a specific date

    """

    def __init__(self,
                 date: dt.date,
                 aum: float):
        self.__date = date
        self.__aum = aum

    @property
    def date(self) -> dt.date:
        return self.__date

    @date.setter
    def date(self, value: dt.date):
        self.__date = value

    @property
    def aum(self) -> float:
        return self.__aum

    @aum.setter
    def aum(self, value: float):
        self.__aum = value


class PortfolioManager(PositionedEntity):
    """

    Portfolio Manager is used to manage Marquee portfolios (setting entitlements, running and retrieving reports, etc)

    """

    def __init__(self,
                 portfolio_id: str):
        """
        Initialize a Portfolio Manager
        :param portfolio_id: Portfolio ID
        """
        self.__portfolio_id = portfolio_id
        PositionedEntity.__init__(self, portfolio_id, EntityType.PORTFOLIO)

    @property
    def portfolio_id(self) -> str:
        return self.__portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, value: str):
        self.__portfolio_id = value

    def get_performance_report(self) -> PerformanceReport:
        reports = GsReportApi.get_reports(limit=100,
                                          position_source_type='Portfolio',
                                          position_source_id=self.id,
                                          report_type='Portfolio Performance Analytics')
        if len(reports) == 0:
            raise MqError('This portfolio has no performance report.')
        return PerformanceReport.from_target(reports[0])

    def schedule_reports(self,
                         start_date: dt.date = None,
                         end_date: dt.date = None,
                         backcast: bool = False):
        GsPortfolioApi.schedule_reports(self.__portfolio_id, start_date, end_date, backcast=backcast)

    def run_reports(self,
                    start_date: dt.date = None,
                    end_date: dt.date = None,
                    backcast: bool = False,
                    is_async: bool = True) -> List[Union[pd.DataFrame, ReportJobFuture]]:
        """
        Run all reports associated with a portfolio
        :param start_date: start date of report job
        :param end_date: end date of report job
        :param backcast: true if reports should be backcasted; defaults to false
        :param is_async: true if reports should run asynchronously; defaults to true
        :return: if is_async is true, returns a list of ReportJobFuture objects; if is_async is false, returns a list
        of dataframe objects containing report results for all portfolio results
        """
        self.schedule_reports(start_date, end_date, backcast)
        reports = self.get_reports()
        report_futures = [report.get_most_recent_job() for report in reports]
        if is_async:
            return report_futures
        counter = 100
        while counter > 0:
            is_done = [future.done() for future in report_futures]
            if False not in is_done:
                return [job_future.result() for job_future in report_futures]
            sleep(6)
        raise MqValueError(f'Your reports for Portfolio {self.__portfolio_id} are taking longer than expected '
                           f'to finish. Please contact the Marquee Analytics team at '
                           f'gs-marquee-analytics-support@gs.com')

    def set_entitlements(self,
                         entitlements: Entitlements):
        """
        Set the entitlements of a portfolio
        :param entitlements: Entitlements object
        """
        entitlements_as_target = entitlements.to_target()
        portfolio_as_target = GsPortfolioApi.get_portfolio(self.__portfolio_id)
        portfolio_as_target.entitlements = entitlements_as_target
        GsPortfolioApi.update_portfolio(portfolio_as_target)

    def get_schedule_dates(self,
                           backcast: bool = False) -> List[dt.date]:
        """
        Get recommended start and end dates for a portfolio report scheduling job
        :param backcast: true if reports should be backcasted
        :return: a list of two dates, the first is the suggested start date and the second is the suggested end date
        """
        return GsPortfolioApi.get_schedule_dates(self.id, backcast)

    def get_aum_source(self) -> RiskAumSource:
        """
        Get portfolio AUM Source
        :return: AUM Source
        """
        portfolio = GsPortfolioApi.get_portfolio(self.portfolio_id)
        return portfolio.aum_source if portfolio.aum_source is not None else RiskAumSource.Long

    def set_aum_source(self,
                       aum_source: RiskAumSource):
        """
        Set portfolio AUM Source
        :param aum_source: aum source for portfolio
        :return:
        """
        portfolio = GsPortfolioApi.get_portfolio(self.portfolio_id)
        portfolio.aum_source = aum_source
        GsPortfolioApi.update_portfolio(portfolio)

    def get_custom_aum(self,
                       start_date: dt.date = None,
                       end_date: dt.date = None) -> List[CustomAUMDataPoint]:
        """
        Get AUM data for portfolio
        :param start_date: start date
        :param end_date: end date
        :return: list of AUM data between the specified range
        """
        aum_data = GsPortfolioApi.get_custom_aum(self.portfolio_id, start_date, end_date)
        return [CustomAUMDataPoint(date=dt.datetime.strptime(data['date'], '%Y-%m-%d'),
                                   aum=data['aum']) for data in aum_data]

    def get_aum(self, start_date: dt.date, end_date: dt.date):
        """
        Get AUM data for portfolio
        :param start_date: start date
        :param end_date: end date
        :return: dictionary of dates with corresponding AUM values
         """
        aum_source = self.get_aum_source()
        if aum_source == RiskAumSource.Custom_AUM:
            aum = self.get_custom_aum(start_date=start_date, end_date=end_date)
            return {aum_point.date.strftime('%Y-%m-%d'): aum_point.aum for aum_point in aum}
        if aum_source == RiskAumSource.Long:
            aum = self.get_performance_report().get_long_exposure(start_date=start_date, end_date=end_date)
            return {row['date']: row['longExposure'] for index, row in aum.iterrows()}
        if aum_source == RiskAumSource.Short:
            aum = self.get_performance_report().get_short_exposure(start_date=start_date, end_date=end_date)
            return {row['date']: row['shortExposure'] for index, row in aum.iterrows()}
        if aum_source == RiskAumSource.Gross:
            aum = self.get_performance_report().get_gross_exposure(start_date=start_date, end_date=end_date)
            return {row['date']: row['grossExposure'] for index, row in aum.iterrows()}
        if aum_source == RiskAumSource.Net:
            aum = self.get_performance_report().get_net_exposure(start_date=start_date, end_date=end_date)
            return {row['date']: row['netExposure'] for index, row in aum.iterrows()}

    def upload_custom_aum(self,
                          aum_data: List[CustomAUMDataPoint],
                          clear_existing_data: bool = None):
        """
        Add AUM data for portfolio
        :param aum_data: list of AUM data to upload
        :param clear_existing_data: delete all previously uploaded AUM data for the portfolio
        (defaults to false)
        :return:
        """
        formatted_aum_data = [{'date': data.date.strftime('%Y-%m-%d'), 'aum': data.aum} for data in aum_data]
        GsPortfolioApi.upload_custom_aum(self.portfolio_id, formatted_aum_data, clear_existing_data)

    def get_pnl_contribution(self,
                             start_date: dt.date = None,
                             end_date: dt.date = None,
                             currency: Currency = None) -> pd.DataFrame:
        """
        Get PnL Contribution of your portfolio broken down by constituents
        :param start_date: optional start date
        :param end_date: optional end date
        :param currency: optional currency; defaults to your portfolio's currency
        :return: a Pandas DataFrame of results
        """
        return pd.DataFrame(GsPortfolioApi.get_attribution(self.portfolio_id, start_date, end_date, currency))
