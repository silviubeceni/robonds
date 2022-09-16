import requests
from bs4 import BeautifulSoup
from operator import itemgetter
from datetime import date, datetime
import calendar
import numpy_financial as npf
from dateutil.relativedelta import relativedelta
from bonds import Bond


def get_soup(url):
    raw_page = requests.get(url=url)
    soup = BeautifulSoup(raw_page.text, features="html.parser")

    return soup


def get_details_from_soup(soup):
    soup_details_table = soup.select('table#dvInfo td')  # list
    soup_details_table_keys = soup_details_table[::2]
    soup_details_table_values = soup_details_table[1::2]

    soup_details_table_keys = cleanup_html_tags(soup_details_table_keys)
    soup_details_table_values = cleanup_html_tags(soup_details_table_values)

    bond_details_dict = dict(zip(soup_details_table_keys, soup_details_table_values))

    return bond_details_dict


def cleanup_html_tags(source):
    return list(map(lambda elem: elem.text, source))


def extract_ask_price_from_soup(soup):
    bid_ask_string = soup.find('span', {'id': 'ctl00_body_ctl02_PricesControl_dvCPrices_Label1'}).text
    ask_price_string = bid_ask_string.split('/')[1].strip()
    ask_price_float = float(ask_price_string)
    return ask_price_float


def compute_date(date_string):
    result_date = datetime.strptime(date_string, '%m/%d/%Y').date()
    return result_date


def compute_years_to_maturity(maturity_date, current_date):
    return relativedelta(maturity_date, current_date).years + 1  # period less than a year is rounded up


def compute_bond_irr(price, years_to_maturity, coupon):
    values = [-price]
    i = 1
    while i < years_to_maturity:
        values.append(coupon)
        i += 1
    values.append(100 + coupon)

    bond_irr = npf.irr(values)
    bond_irr_percentage = f'{round(bond_irr * 100, 2)}%'
    return bond_irr_percentage


def compute_bond_ytm(price, years_to_maturity, coupon):
    bond_ytm = (coupon + (100 - price) / years_to_maturity) / ((100 + price) / 2)

    bond_ytm_percentage = f'{round(bond_ytm * 100, 2)}%'
    return bond_ytm_percentage


def compute_dirty_price(price, coupon, start_date):
    dirty_price = price + coupon*(days_accrued(start_date)/days_in_year())
    return dirty_price


def days_accrued(start_date):
    today = date.today()
    year_today = today.year
    updated_start_date = start_date.replace(year=year_today)
    diff = date.today() - updated_start_date
    return diff.days


def days_in_year(year=datetime.now().year):
    return 365 + calendar.isleap(year)


def build_sorted_by_irr_bonds_list(instrument_list, bond_page_url):
    all_bonds_list = []
    for instrument in instrument_list:
        current_bond = Bond(instrument, bond_page_url)
        if not current_bond.is_expired():
            all_bonds_list.append(current_bond.get_display_dict())
    return sorted(all_bonds_list, key=itemgetter('Computed IRR'), reverse=True)
