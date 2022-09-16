from datetime import date
import utils

KEYS_TO_DISPLAY = ['Instrument', 'Current coupon', 'Yield To Maturity*', 'Start trading date', 'Maturity date',
                   'Issue currency']
CURRENT_DATE = date.today()


class Bond:
    def __init__(self, instrument, bond_page_url):
        self.soup = utils.get_soup(url=f'{bond_page_url}{instrument}')
        self.extracted_bond_dict = utils.get_details_from_soup(soup=self.soup)

        self.maturity_date = utils.compute_date(date_string=self.extracted_bond_dict['Maturity date'])
        if not self.is_expired():
            self.instrument = instrument
            self.start_date = utils.compute_date(date_string=self.extracted_bond_dict['Start trading date'])
            self.ask_price = utils.extract_ask_price_from_soup(soup=self.soup)
            self.coupon = float(self.extracted_bond_dict['Current coupon'].strip('%'))
            self.dirty_price = utils.compute_dirty_price(price=self.ask_price,
                                                         coupon=self.coupon,
                                                         start_date=self.start_date)
            self.years_to_maturity = utils.compute_years_to_maturity(maturity_date=self.maturity_date,
                                                                     current_date=CURRENT_DATE)
            self.computed_irr = utils.compute_bond_irr(price=self.ask_price,
                                                       years_to_maturity=self.years_to_maturity,
                                                       coupon=self.coupon)
            self.computed_ytm = utils.compute_bond_ytm(price=self.ask_price,
                                                       years_to_maturity=self.years_to_maturity,
                                                       coupon=self.coupon)

            self._set_display_dict()

    def is_expired(self):
        if self.maturity_date > CURRENT_DATE:
            return False
        return True

    def _set_display_dict(self):
        display_dict = {}
        display_dict['Instrument'] = self.instrument
        display_dict['Computed IRR'] = self.computed_irr

        for k, v in self.extracted_bond_dict.items():
            if k in KEYS_TO_DISPLAY:
                display_dict[k] = v

        self.display_dict = display_dict

    def get_display_dict(self):
        return self.display_dict
