from requests import get
from bs4 import BeautifulSoup
import csv

# kraj Olomouc, okres Olomouc

address = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102"
response = get(address)
parsed_html = BeautifulSoup(response.text, features="html.parser")

# get list of municipalities

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

with open("election_results.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data_rows)
