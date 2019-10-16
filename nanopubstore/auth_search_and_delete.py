#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Usage:  auth_search_and_delete.py -h

Contributed by Natalie Catlett.a

"""
import sys
import requests
import argparse
import configparser

parser = argparse.ArgumentParser(description="search nanopubs and delete.")
parser.add_argument("-s", "--string", required=True, help="search string")
parser.add_argument(
    "-d", "--delete", required=False, action="store_true", help="delete found nanopubs"
)
args = parser.parse_args()

string = args.string
delete = args.delete

# example query -- ./search_and_delete.py  -s 'nanopub.metadata.project:"MS Model" AND nanopub.metadata.gd\:createTS:[ 2018-07-15 TO 2018-07-18 ] AND nanopub.citation.database.id: 21833088'

config = configparser.ConfigParser()
config.read("config.ini")
username = config["DEFAULT"].get("username")
password = config["DEFAULT"].get("password")
server_nickname = config["DEFAULT"].get("server_nickname")


def get_header(username, password, server_nickname):
    data = {"username": username, "password": password}
    r = requests.post(f"https://userstore.{server_nickname}.biodati.com/token", data=data)
    try:
        token_json = r.json()
        jwt_auth = token_json["id_token"]
    except:
        sys.exit("Authorization error")
    header = {"authorization": "Bearer " + jwt_auth, "content-type": "application/json"}
    return header


def main(username, password, string, delete, server_nickname):
    """Search and delete nanopubs from NanopubStore

    Will only return up to 10000 results.

    Please review https://help.biodati.com/nanopubs/nanopub-advanced-searching for tips on how to search the NanopubStore.
    """

    header = get_header(username, password, server_nickname)
    url = f"https://nanopubstore.{server_nickname}.biodati.com"

    search_body = {
        "search_query": string,
        "search_filters": [],
        "max": 10000,
        "skip": 0,
        "is_deleted": "false",
    }
    # search_body = {"searchQuery": search, "searchFilter": "isDeleted: false AND nanopub.metadata.project.keyword: \"MS Model\"", "max": 10000}
    # search_body = {"searchQuery": string, "searchFilter": "isDeleted: false", "max": 10000}

    r = requests.post(f"{url}/search", json=search_body, headers=header)

    results = r.json()
    total_items = results["totalItems"]
    print(f"Found {total_items} nanopubs")

    if r.status_code == 200:
        for np in results["items"]:
            print(np["nanopub"]["id"])

    if delete:
        count = 0
        for np in results["items"]:
            np_id = np["nanopub"]["id"]
            r = requests.delete(f"{url}/nanopubs/{np_id}", headers=header)
            if r.status_code == 200:
                count += 1

        print(f"Successfully deleted {count} nanopubs")


if __name__ == "__main__":
    main(username, password, string, delete, server_nickname)
