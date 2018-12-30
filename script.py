#!/usr/bin/env python
from operator import attrgetter
import logging
import os
import json

DEFAULT_LOGDIR = '/home/kelly/github/neolib-parent/Orange_Kangaskhan/'


from neolib.user.User import User
from neolib.stock.Portfolio import Portfolio
from neolib.stock.BargainStocks import BargainStocks


UPPER_LIMIT = 15 # inclusive
SELL_THRESHOLD = 0.8
SELL_AMOUNT = 1000


def sort_and_filter(stock_list):
    return sorted(filter(lambda s:s.curr_price <= UPPER_LIMIT, stock_list),
            key=lambda s: s.curr_price)


def main():
    with open('user.json') as f:
        user_config = json.load(f)
    LOGDIR = user_config.get("logdir", DEFAULT_LOGDIR)

    # Set up logging in main, not global scope.
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO) # - this is the line I needed to get logging to work!

    fh = logging.FileHandler(os.path.join(LOGDIR, 'anacron_output.log'))
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # So we also see logging to stderr so we can see it...
    stderr = logging.StreamHandler()
    stderr.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())


    ok = User(user_config['username'],user_config['password'])
    ok.login()

    # Start off your day by collecting interest at the bank
    ok.bank.load()
    ok.bank.collectInterest()
    logger.info('NP before transactions: {}'.format(ok.nps))

    p = Portfolio(ok)
    bs = BargainStocks(ok)

    # Thought: this way is like fine whatever, but what if I just made a thing
    # "default dict" where the value is 0 if it's not in the portfolio
    # and take the one with minimum curr_price and lowest portfolio qty
    diverse = [
            s for s in sort_and_filter(bs.purchasable_stocks)
            if s.ticker not in p.tickers()
            and s.curr_price <= UPPER_LIMIT
            ]
    already = [
            s for s in sort_and_filter(bs.purchasable_stocks)
            if s.ticker in p.tickers()
            and s.curr_price <= UPPER_LIMIT
            ]

    min_diverse_stock = min(diverse, key=attrgetter('curr_price')) if diverse else None
    min_already_stock = min(already, key=attrgetter('curr_price')) if already else None
    choice = min_diverse_stock if min_diverse_stock else min_already_stock

    if choice is not None:
        logger.info('Buying 1000 of {} at {}'.format(choice.ticker, choice.curr_price))
        # We buy 1000 a day (unless it's a bad day)
        p.buy(choice.ticker, 1000)
    else:
        logger.info("Not buying anything")

    # And we sell SELL_AMOUNT of anything over SELL_THRESHOLD
    sellable = [s for s in p.stocks if s.percent_change >= SELL_THRESHOLD]
    for s in sellable:
        logger.info('Selling {}, {}'.format(s.ticker, s.percent_change))
        p.sell(s.ticker, SELL_AMOUNT)
    if len(sellable) == 0:
        logger.info("Nothing worth selling")

    ok.bank.load()
    logger.info('NP after transations: {}'.format(ok.nps))

if __name__ == '__main__':
    main()
