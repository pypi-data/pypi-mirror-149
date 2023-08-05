




# def calc_execution_price_rough(
#         # df_positions_short : pd.DataFrame,
#         df_execution_prices_full : pd.DataFrame,
#         td_execution_duration : datetime.timedelta
# ) -> pd.DataFrame:
#     """Get execution price as mean price over execution duration

#     Args:
#         df_positions_short (pd.DataFrame): Positions we want to take
#         df_execution_prices_full (pd.DataFrame): Prices of assets in higher resolution
#         td_execution_duration ([datetime.timedelta]): \
#             How long should the execution take

#     Returns:
#         pd.DataFrame: Prices by which asset can be bought at any moment
#     """
#     # Reverse the df with prices because rolling mean price
#     # Should go into future not the past and then at the end reverse back
#     LOGGER.debug("------> Calculate full execution prices")

#     if td_execution_duration:
#         df_exec_price_full = df_execution_prices_full[::-1].rolling(
#             td_execution_duration, min_periods=2).mean()[::-1]
#     else:
#         df_exec_price_full = df_execution_prices_full[::-1].rolling(2).mean()[::-1]


#     return df_exec_price_full
#     # LOGGER.debug("------> Convert them into short format")
#     # # Convert Execution prices to the short format
#     # df_exec_prices_short = _convert_full_prices_df_to_short(
#     #     df_positions_short, df_exec_price_full)
#     # LOGGER.debug("---------> Done")
#     # return df_exec_prices_short




# def _convert_full_prices_df_to_short(
#         df_positions_short,
#         df_execution_prices_full
# ):
#     """Convert prices in high resolution to the resolution of short DFs"""
#     from tqdm.auto import tqdm
#     start = time.time()
#     set_index_short = set(df_positions_short.index.tolist())
#     set_index_full = set(df_execution_prices_full.index.tolist())
#     new_full_index_rev_sorted = reversed(
#         sorted(set_index_short.union(set_index_full)))

#     print(0, time.time() - start)

#     dict_df_execution_prices_short = {}

#     dict_df = df_execution_prices_full.to_dict(orient='list')
#     print(1, time.time() - start)
#     # dict_df = df_execution_prices_full.to_dict(orient='dict')
#     print(1.5, time.time() - start)

#     for ticker in tqdm(dict_df):
#         list_values_for_ticker = reversed(dict_df[ticker])
#         dict_value_by_timestamp_short = {}
#         last_value = None
#         index = 0
#         for timestamp in new_full_index_rev_sorted:
#             if timestamp in set_index_full:
#                 last_value = list_values_for_ticker[index]
#                 index += 1
#             if timestamp in set_index_short:
#                 dict_value_by_timestamp_short[timestamp] = last_value
#         dict_df_execution_prices_short[ticker] = dict_value_by_timestamp_short
#     print(2, time.time() - start)
#     df = pd.DataFrame.from_dict(dict_df_execution_prices_short)
#     print(3, time.time() - start)
#     return df


# def _convert_full_prices_df_to_short(
#         df_positions_short,
#         df_execution_prices_full
# ):
#     """
#     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     DO NOT DELETE, this is a benchmark that my realization works correctly
#     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     Convert prices in high resolution to the resolution of short DFs
#     """
#     df_positions_empty = pd.DataFrame(
#         index=df_positions_short.index, columns=df_positions_short.columns)
#     df_prices_full_size = pd.concat(
#         [df_execution_prices_full, df_positions_empty], axis=1)
#     df_prices_full_size.sort_index(inplace=True)



#     df_grouped = df_prices_full_size.groupby(by=df_prices_full_size.index.date)
#     for name, group in tqdm(df_grouped):
#         group.bfill(inplace=True)


#     # df_prices_full_size.bfill(inplace=True)
#     df_prices_short = df_prices_full_size.loc[df_positions_short.index]
#     return df_prices_short






# def _backfill_values_in_dataframe(df):
#     """"""
#     dict_df = df.to_dict(orient='list')
#     for ticker in dict_df:
#         print(ticker)
#         break

#     return pd.DataFrame.from_dict(dict_df)
