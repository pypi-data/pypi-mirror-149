""""""
from . import logger

logger.initialize_project_logger(
    name=__name__,
    path_dir_where_to_store_logs="",
    is_stdout_debug=True,
    is_to_propagate_to_root_logger=False,
)
# Standard library imports

# Third party imports

# Local imports
from .backtester import run_backtest
from .simple_execution import create_df_simple_execution_prices

# Global constants

__all__ = ["run_backtest", "create_df_simple_execution_prices"]
