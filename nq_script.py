#!/usr/bin/env python

from __future__ import print_function
import logging
import os

LOGDIR = '/home/kelly/github/neolib-parent/Orange_Kangaskhan/neoquest'
logging.basicConfig(filename=os.path.join(LOGDIR, 'anacron_output.log'),
        format='%(asctime)s|%(levelname)s|%(message)s',
        level=logging.INFO,
        )

from neolib.user.User import User
from neolib.neoquest.Neoquest import Neoquest, DIR

def main():
    logger = logging.getLogger()

    stderr = logging.StreamHandler()
    stderr.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    ok = User('orange_kangaskhan', '1garura1')
    if not ok.loggedIn:
        ok.login()

    nq = Neoquest(ok)

    current_state = nq.action('noop')
    print(current_state)
    current_state.map()

    raise Exception('Dummy error to drop into ipython shell')
    # do stuff


if __name__ == '__main__':
    main()
