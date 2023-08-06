"""
Code to update certain tables in the DataBase
"""
import pandas as pd
from datetime import date
import wrds

from toolbox.db.read.db_functions import db_tables, table_info
from toolbox.db.api.sql_connection import SQLConnection
import logging

logging.basicConfig(format='%(message)s ::: %(asctime)s', datefmt='%I:%M:%S %p', level=logging.INFO)

CURRENT_SPACE_PRICING, CURRENT_SPACE_PRICING_BASE = 'pricing', 'cstat.sd'


def make_stream_pricing_table(tbl_name, tbl_base, con):
    """
    makes a table to stream pricing from cstat wrds
    """
    con = SQLConnection(read_only=False).return_other_if_open(con, read_only=False)
    db = wrds.Connection(wrds_username='adicr1')
    logging.info('Created database connection')

    cols_to_select = set(db.describe_table('comp_na_daily_all', 'sec_dprc')['name'].to_list() + ['date', 'id'])
    local_col = set(table_info(tbl_base, con)['name'])
    wanted_cols = cols_to_select.intersection(local_col)

    # cs schema is current space
    copy_sql = f"""CREATE TABLE {tbl_name} AS SELECT {', '.join(wanted_cols)} FROM {tbl_base}"""

    logging.info(f'Writing data for {tbl_name}')
    con.execute(copy_sql)
    logging.info(f'Created new table {tbl_name}!')


def _ensure_have_table(tbl_name, tbl_base, con):
    """
    ensures we have the table and if not will open up the table
    """
    if tbl_name not in db_tables()['name'].to_list():
        make_stream_pricing_table(tbl_name, tbl_base, con)


def update_cs_pricing():
    """
    Updates the Compustat Security Daily file.
    Updates only certain non-static columns
    """
    con = SQLConnection(read_only=False)
    db = wrds.Connection(wrds_username='adicr1')
    logging.info('Created database connection')

    _ensure_have_table(CURRENT_SPACE_PRICING, CURRENT_SPACE_PRICING_BASE, con)

    last_local_date = _get_local_last_day_of_data(CURRENT_SPACE_PRICING, con).date()

    last_wrds_date = db.raw_sql(f"""SELECT max(datadate) 
                                    FROM comp_na_daily_all.sec_dprc 
                                    WHERE datadate <= '{date.today()}'""")['max'][0]

    if last_wrds_date == last_local_date:
        logging.info(f"Local database is up to date! Last observation date: {last_local_date}")
        return
    if last_wrds_date < last_local_date:
        logging.info(f"Local database is messed up! Last WRDS observation date: {last_wrds_date}. "
                     f"Last local observation date: {last_local_date}")
        return

    logging.info(f"Inserting data from {last_local_date} to {last_wrds_date}")
    local_col = table_info(CURRENT_SPACE_PRICING, con)['name']

    wrds_sql = f"""SELECT *, datadate as date, CONCAT(gvkey, '_', iid) as id FROM comp_na_daily_all.sec_dprc WHERE datadate > '{last_local_date}'"""
    new_data = db.raw_sql(wrds_sql)
    new_data['date'] = pd.to_datetime(new_data['date'])
    new_data = new_data[local_col.to_list()]

    logging.info(f"Adding {new_data.shape[0]} rows to {CURRENT_SPACE_PRICING}")
    con.con.append(CURRENT_SPACE_PRICING, new_data)
    logging.info(f"Appended new data")

    con.close()


def _get_local_last_day_of_data(table: str, con: SQLConnection):
    """
    Gets the last day of data we have for a table
    """
    return con.execute(f"""SELECT max(date) from {table}""").fetchone()[0]


def update_sd():
    """
    Updates the Compustat Security Daily file.
    Updates only certain non-static columns
    """
    con = SQLConnection(read_only=False)
    db = wrds.Connection(wrds_username='adicr1')
    logging.info('Created database connection')

    last_local_date = _get_local_last_day_of_data('sd', con).date()

    last_wrds_date = db.raw_sql(f"""SELECT max(datadate) 
                                    FROM comp_na_daily_all.sec_dprc 
                                    WHERE datadate <= '{date.today()}'""")['max'][0]

    if last_wrds_date == last_local_date:
        logging.info(f"Local database is up to date! Last observation date: {last_local_date}")
        return
    if last_wrds_date < last_local_date:
        logging.info(f"Local database is messed up... Last WRDS observation date: {last_wrds_date}. "
                     f"Last local observation date: {last_local_date}")
        return

    logging.info(f"Inserting data from {last_local_date} to {last_wrds_date}")
    local_col = table_info('sd', con)['name']

    wrds_sql = f"""SELECT *, prc.datadate as date, CONCAT(prc.gvkey, '_', prc.iid) as id 
                    FROM comp_na_daily_all.secd as prc
                        LEFT JOIN comp_na_daily_all.company as comp ON prc.gvkey = comp.gvkey 
                    WHERE datadate > '{last_local_date}' AND datadate <= '{last_wrds_date}'"""

    new_data = db.raw_sql(wrds_sql)
    new_data['date'] = pd.to_datetime(new_data['date'])
    new_data = new_data[local_col.to_list()]
    new_data = new_data.loc[:, ~new_data.columns.duplicated()]

    logging.info(f"Adding {new_data.shape[0]} rows to sd")
    con.con.append('sd', new_data)
    logging.info(f"Appended new data")

    con.close()


if __name__ == '__main__':
    # make_stream_pricing_table()
    # update_cs_pricing()
    update_sd()
