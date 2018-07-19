#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:  search_and_delete.py -h

"""

import click
import requests

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# example query -- ./search_and_delete.py -u https://nanopubstore.plm.biodati.com -s 'nanopub.metadata.project:"MS Model" AND nanopub.metadata.gd\:createTS:[ 2018-07-15 TO 2018-07-18 ] AND nanopub.citation.database.id: 21833088'


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--url', '-u', help="NanopubStore API url - typically of the format https://nanopubstore.<sitename>.biodati.com")
@click.option('--search', '-s', prompt="Enter search string", help="Search string to run against NanopubStore")
@click.option('--delete', '-d', is_flag=True, help="Set delete flag to remove all nanopubs found by search string")
def main(url, search, delete):
    """Search and delete nanopubs from NanopubStore

    Will only return up to 10000 results.

    Please review https://help.biodati.com/nanopubs/nanopub-advanced-searching for tips on how to search the NanopubStore.
    """
    url = url.rstrip('/')

    # search_body = {"searchQuery": search, "searchFilter": "isDeleted: false AND nanopub.metadata.project.keyword: \"MS Model\"", "max": 10000}
    search_body = {"searchQuery": search, "searchFilter": "isDeleted: false", "max": 10000}

    r = requests.post(f'{url}/search', json=search_body)

    results = r.json()

    total_items = results['totalItems']
    print(f'Found {total_items} nanopubs')

    if r.status_code == 200:
        for np in results['items']:
            print(np['nanopub']['id'])

    if delete:
        count = 0
        for np in results['items']:
            np_id = np['nanopub']['id']
            r = requests.delete(f'{url}/nanopubs/{np_id}')
            if r.status_code == 200:
                count += 1

        print(f'Successfully deleted {count} nanopubs')


if __name__ == '__main__':
    main()

