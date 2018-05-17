#!/usr/bin/env python
from operator import attrgetter
import logging
import os
import json

from neolib.user.User import User
from neolib.stock.Portfolio import Portfolio
from neolib.stock.BargainStocks import BargainStocks
from neolib.daily.GiantOmelette import GiantOmelette
from neolib.daily.Daily import Daily


LOGDIR = '/home/kelly/github/neolib-parent/Orange_Kangaskhan/'
DAILY_LIST = [
        'GiantOmelette',
        'GiantJelly',
        'Tombola',
        'FruitMachine',
        'ColtzanShrine',
        'ShopOfOffers',
        'MarrowGuess',
        ]

UPPER_LIMIT = 15 # inclusive
SELL_THRESHOLD = 1.2
SELL_AMOUNT = 1000


def sort_and_filter(stock_list):
    return sorted(filter(lambda s:s.curr_price <= UPPER_LIMIT, stock_list),
            key=lambda s: s.curr_price)


def try_to_do_stocks(usr, logger):
    p = Portfolio(usr)
    bs = BargainStocks(usr)

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
        # TODO: It's identifying what to sell properly but there's a bit of an iffy:
        # I wanat to know HOW MUCH i sold, and how much I made, and how much I have lft
        p.sell(s.ticker, SELL_AMOUNT)
    if len(sellable) == 0:
        logger.info("Nothing worth selling")


def main():
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

    with open('user.json') as f:
        login = json.load(f)
    ok = User(login['username'],login['password'])
    ok.login()

    # Start off your day by collecting interest at the bank
    ok.bank.load()
    ok.bank.collectInterest()
    logger.info('Stored/Bank NP before transactions: {}'.format(ok.bank.balance))
    logger.info('NP before transactions: {}'.format(ok.nps))

    # Then let's get do some dailies...
    # NOTE: doing these in this way guards from "Already did today!" exceptions
    for message in Daily.doDailies(ok, DAILY_LIST):
        logger.info(message)

    # Obviously, this script part doesn't really work anymore: but still,
    # for posterity,
    try_to_do_stocks(ok, logger)


if __name__ == '__main__':
    main()
