"""Module with functions to create execution prices"""
# Standard library imports
import logging
from typing import Optional, Any, Union
import datetime

# Third party imports
import pandas as pd

# Local imports

# Global constants
LOGGER = logging.getLogger(__name__)


def create_df_simple_execution_prices(
        df_prices_full : pd.DataFrame,
        data_frequency="30min",  # 30min, 1h, 3h, 6h, 1d
        offset="-3min",  # "-3min"
        td_trading_delay : Optional[datetime.timedelta]=None,
        td_execution_duration : Optional[datetime.timedelta]=None,
):
    """Backtest positions to understand if they can generate PNL

    Args:
        df_positions_short (pd.DataFrame): Positions we want to take
        df_prices_full (pd.DataFrame): Prices of assets in higher resolution
        td_trading_delay (datetime.timedelta): \
            Delay needed to get into the wanted positions
        td_execution_duration ([datetime.timedelta]): \
            How long should the execution take

    Returns:
        pd.DataFrame: columns with different PNLs generated at every tick
    """
    LOGGER.info("Create simple execution prices")
    #####
    # Shift prices on asked delay
    LOGGER.info("---> Shift prices on delay in the past: %s", td_trading_delay)
    # print(df_prices_full.tail(5)["AAVEUSDT"])
    LOGGER.info(
        "------> First datetime in index BEFORE: %s",
        df_prices_full.index.to_list()[0]
    )
    df_prices_full = df_prices_full.shift(freq=-td_trading_delay)
    # print(df_prices_full.tail(5)["AAVEUSDT"])
    LOGGER.info(
        "------> First datetime in index AFTER: %s",
        df_prices_full.index.to_list()[0]
    )
    LOGGER.info("------> Done")
    #####
    # Calculate rolling mean price over the given duration
    LOGGER.info(
        "---> Calculate mean price over the execution duration: %s",
        td_execution_duration)
    ## Reverse the df with prices because rolling mean price
    ## Should go into future not the past and then at the end reverse back
    # print(df_prices_full.tail(7)["AAVEUSDT"])
    df_real_exec_price_full = df_prices_full[::-1].rolling(
        td_execution_duration, min_periods=2).mean()[::-1]
    # print(df_real_exec_price_full.tail(7)["AAVEUSDT"])
    LOGGER.info("------> Done")
    #####
    # Resample to the asked frequency
    LOGGER.info(
        "---> Resample to: frequency=%s offset=%s", data_frequency, offset)
    # print(df_real_exec_price_full.tail(33)["AAVEUSDT"])
    df_real_exec_prices_short = resample_df_to_asked_frequency(
        df_real_exec_price_full,
        data_frequency=data_frequency,
        offset=offset,
    )
    LOGGER.info("------> Done")
    return df_real_exec_prices_short


def resample_df_to_asked_frequency(
        df : pd.DataFrame,
        data_frequency="30min",  # 30min, 1h, 3h, 6h, 1d
        offset="-3min",  # "-3min"
):
    """"""
    df_resampled = df.resample(
        data_frequency,
        label="right",  # left, right
        closed="right",  # left, right
        offset=offset
    )
    return df_resampled.last()




def get_df_perfect_execution_prices(
        df_positions_short : pd.DataFrame,
        df_prices_full : pd.DataFrame,
        td_trading_delay : Optional[datetime.timedelta]=None,
):
    """TODO"""
    pass


def _convert_full_prices_df_to_short(
        df_positions_short : pd.DataFrame,
        df_prices_full : pd.DataFrame,
) -> pd.DataFrame:
    """Convert prices in high resolution to the resolution of short DFs"""
    set_index_short = set(df_positions_short.index.tolist())
    set_index_full = set(df_prices_full.index.tolist())
    set_missing_ticks_in_full = set_index_short - set_index_full
    set_common_ticks = set_index_short.intersection(set_index_full)

    if set_missing_ticks_in_full:
        LOGGER.warning("Missing ticks: %d", len(set_missing_ticks_in_full))

    if len(set_missing_ticks_in_full) > 5:
        list_missing_ticks = sorted(set_missing_ticks_in_full)
        LOGGER.warning("Missing ticks: %s", list_missing_ticks[:20])
        raise ValueError(
            f"Unable to convert full df into short format as "
            f"{len(set_missing_ticks_in_full)}/{len(set_index_short)} "
            "ticks missing"
        )
    return df_prices_full.loc[sorted(set_common_ticks)]
