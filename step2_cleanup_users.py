#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import json
import logging

from turkey_cities import cities

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
hdlr = logging.FileHandler('cleaned_up.log')
fmt = logging.Formatter('%(message)s')
hdlr.setFormatter(fmt)
logger.addHandler(hdlr)

UNKNOWN = u"Unknown"
DEBUG = False

all_users = json.load(open('step1.json'))
bads = []


def guess_location(user):
    user.update({'country_code': 'TR',
                 'country_name': "Turkey",
                 'city_name': user.get('city').get('name'),
                 'has_city': True,
                 'latitude': user.get('city').get('lat'),
                 'longitude': user.get('city').get('lon'),
                 'id_int': int(user.get('id').split('-', 1)[1])})
    del(user['city'])
    return user

# DEBUG = True

if DEBUG:
    from pprint import pprint as pp ; pp(country_city_by_location(u"San Juan de los Lagos"))
    exit(0)


failed = []
valid_users = []
existing = []
unique_users = []

for user in all_users:
    new_user = guess_location(user)
    if new_user is None:
        continue
    userdesc = (u"%(country)s/%(city)s: @%(user)s: %(location)s"
                % {'country': new_user.get('country_name'),
                   'city': new_user.get('city_name'),
                   'user': new_user.get('username'),
                   'location': new_user.get('location')})
    if new_user.get('country_name') == UNKNOWN:
        failed.append(userdesc)
    else:
        valid_users.append(new_user)
        logger.info(userdesc)

for fail in failed:
    logger.info(fail)
logger.info("%d failed users" % len(failed))
logger.info("%d success users" % len(all_users))

for bad in bads:
    while True:
        try:
            all_users.remove(bad)
        except ValueError:
            break

for user in valid_users:
    if user['username'] in existing:
        continue
    unique_users.append(user)
    existing.append(user['username'])

json.dump(unique_users, open('step2.json', 'w'), indent=4)
