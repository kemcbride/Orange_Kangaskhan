#!/usr/bin/env python
"""A script that tries to use the inventory module to see whether the PIL replacement
with Pillow module works.
- Whenever I have a script that ends with 'raise Exception('dummy exception')',
    I use it with the command "ipython --pdb script_name.py" """

import logging
import os
import json

from neolib.user.User import User
from neolib.user.Pet import Pet, get_pet_names
from neolib.item.Item import Item


DEFAULT_LOGDIR = '/home/kelly/github/neolib-parent/Orange_Kangaskhan/'


def main():
    with open('user.json') as pwd_file:
        user_config = json.load(pwd_file)
    LOGDIR = user_config.get("logdir", DEFAULT_LOGDIR)

    """Set up logging in main, not global scope."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO) # - this is the line I needed to get logging to work!

    # So we also see logging to stderr so we can see it...
    stderr = logging.StreamHandler()
    stderr.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    o_k = User(user_config['username'], user_config['password'])
    o_k.login()

    o_k.inventory.load()
    items = o_k.inventory.items
    print(items)


if __name__ == '__main__':
    main()
