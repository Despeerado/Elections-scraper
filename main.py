from requests import get
from bs4 import BeautifulSoup
import csv
import argparse
import logging

# kraj Olomouc, okres Olomouc

def scrape_election_results(address):
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    response = get(address)
    parsed_html = BeautifulSoup(response.text, features="html.parser")
    logging.info("Downloading data from the selected url")

    main_number = parsed_html.select(".cislo a")

    prefix = "https://volby.cz/pls/ps2017nss/"
    municipalities_list = []
    counter = 0

    names = parsed_html.select(".overflow_name")
    codes = parsed_html.select(".cislo a")

    for links in main_number:
        url = links['href']
        new_url = prefix + url
        municipalities_list.append(new_url)
        counter += 1

    data_rows = []

    for i in range(len(municipalities_list)):
        municipality = municipalities_list[i]
        response = get(municipality)
        parsed_html = BeautifulSoup(response.text, features="html.parser")
        voters = parsed_html.find_all("td", {"headers": "sa2"})
        envelopes = parsed_html.find_all("td", {"headers": "sa3"})
        valid = parsed_html.find_all("td", {"headers": "sa6"})
        political_party = parsed_html.find_all("td", {"class": "overflow_name", "headers": ["t1sa1", "t2sa1"]})
        political_votes = parsed_html.find_all("td", {"class": "cislo", "headers": ["t1sb3", "t2sb3"]})

        code = codes[i].text
        name = names[i].text
        voters_count = voters[0].text
        envelopes_count = envelopes[0].text
        valid_count = valid[0].text
        party_votes = [vote.text for vote in political_votes]

        row = [code, name, voters_count, envelopes_count, valid_count] + party_votes
        data_rows.append(row)

    parties = [party.text for party in political_party]

    # create new csv file

    header = ["code", "location", "registered", "envelopes", "valid"] + parties

    logging.info("Scraping elections to election_results.csv")

    with open("election_results.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data_rows)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape election results from a given address.")
    parser.add_argument("address", type=str, help="URL address of the election results page")
    args = parser.parse_args()

    scrape_election_results(args.address)
    logging.info("Program finished.")