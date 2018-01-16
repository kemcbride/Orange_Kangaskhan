#!/usr/bin/env python
"""A script that tries to use the inventory module to see whether the PIL replacement
with Pillow module works. """

import logging
import os
import json

from neolib.user.User import User
from neolib.item.Item import Item


def main():
    """Set up logging in main, not global scope."""
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

    with open('user.json') as pwd_file:
        login = json.load(pwd_file)

    o_k = User(login['username'], login['password'])
    o_k.login()

    o_k.inventory.load()
    items = o_k.inventory.items
    raise Exception('Dummy Exception to drop into pdb shell')


if __name__ == '__main__':
    main()
