#!/usr/bin/env python
"""A script that tries to use the inventory module to see whether the PIL replacement
with Pillow module works.
- Whenever I have a script that ends with 'raise Exception('dummy exception')',
    I use it with the command "ipython --pdb script_name.py" """

import logging
import os
import json

from neolib.user.User import User
from neolib.user.Pet import Pet, get_pets
from neolib.item.Item import Item


def main():
    """Set up logging in main, not global scope."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO) # - this is the line I needed to get logging to work!

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

    darling_eunice = Pet(o_k)
    print darling_eunice.name
    mypets = get_pets(o_k)
    raise Exception('dummy exception for ipdb shell')


if __name__ == '__main__':
    main()
