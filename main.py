from flask import Flask, render_template, url_for
import utils


BOND_PAGE_URL = 'https://bvb.ro/FinancialInstruments/Details/FinancialInstrumentsDetails.aspx?s='
INSTRUMENT_LIST = ['R2208A', 'R2408A', 'R2112A', 'R2312A', 'R2203A', 'R2403A', 'R2207A', 'R2307A',
                   'R2210A', 'R2410A', 'R2212A', 'R2412A', 'R2304A', 'R2504A', 'R2306A', 'R2506A',
                   'R2508AE', 'R2512AE', 'R2603AE', 'R2307AE', 'R2610AE', 'R2612AE', 'R2304AE',
                   'R2404AE', 'R2306AE', 'R2406AE']

# INSTRUMENT_LIST = ['R2408A']

sorted_bonds_list = utils.build_sorted_by_irr_bonds_list(instrument_list=INSTRUMENT_LIST, bond_page_url=BOND_PAGE_URL)

app = Flask(__name__)


@app.route("/")
def index():

    return render_template('index.html', sorted_bonds_list=sorted_bonds_list, bond_page_url=BOND_PAGE_URL)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
