
import re
import requests

urls = ['instagram.com/drmercola', 'facebook.com/doctor.health', 'twitter.com/mercola',
        'instagram.com/RobertFKennedyJr', 'facebook.com/rfkjr', 'twitter.com/RobertKennedyJr',
        'instagram.com/thetruthaboutvaccinesttav', 'facebook.com/tycharlene.bollinger', 'twitter.com/truthaboutbigc',
        'instagram.com/drtenpenny', 'facebook.com/VaccineInfo', 'twitter.com/BusyDrT',
        'instagram.com/_rizzaislam', 'facebook.com/rizza.infinity', 'twitter.com/IslamRizza',
        'instagram.com/drbuttar', 'facebook.com/DrRashidAButtar', 'twitter.com/DrButtar',
        'instagram.com/healthnutnews', 'facebook.com/HealthNutNews', 'twitter.com/unhealthytruth',
        'instagram.com/greenmedinfo', 'facebook.com/greenmedinfo', 'twitter.com/GreenMedInfo',
        'instagram.com/kellybroganmd', 'facebook.com/KellyBroganMD', 'twitter.com/kellybroganmd',
        'instagram.com/drchristianenorthrup', 'facebook.com/DrChristianeNorthrup', 'twitter.com/DrChrisNorthrup',
        'instagram.com/dr.bentapper', 'facebook.com/DrBenTapper', 'twitter.com/DrBenTapper1'
        ]

all_accounts = []
count = 0
person_list = []

for url in urls:

    status_codes = {}

    with open(url.replace("/", "_") + '.txt', 'r') as file:
        lines = file.readlines()[2:-4]

    for line in lines:
        line = line.strip()
        match = re.search("<(.+)>", line)
        uri_m = match.group(1)

        try:
            r = requests.head(uri_m)

            if r.status_code != 200 and r.status_code != 302:
                print(uri_m + " has the following status code: " + str(r.status_code))

            if r.status_code not in status_codes:
                status_codes.update({r.status_code: 1})
            else:
                status_codes[r.status_code] += 1

        except requests.ConnectionError as e:
            print("failed to connect" + e.args[0].reason)


    print(url)
    print(status_codes)


for url in urls:

    archive_dict = {"web.archive.org": 0, "wayback.archive-it.org": 0, 'archive.md': 0, 'webarchive.loc.gov': 0,
                    'www.webarchive.org.uk': 0, 'web.archive.org.au': 0, 'arquivo.pt': 0 }

    with open(url.replace("/", "_") + '.txt', 'r') as file:
        lines = file.readlines()[2:-4]

    for line in lines:
        line = line.strip()
        print(line)
        match = re.search("//([^/]+)", line)
        host = match.group(1)
        if host not in archive_dict:
            archive_dict.update({host: 1})
        else:
            archive_dict[host] += 1

    person_list.append(archive_dict)
    count += 1
    if count == 3:
        all_accounts.append(person_list)
        count = 0
        person_list = []

print(all_accounts)

latex_input = ""

for person in all_accounts:

    person_table = "\\begin{table}[]\n\\begin{tabular}{|c|c|c|c|}\n\hline\n& Instagram & Facebook & Twitter \\\\\n\hline\n" \
               f"Internet Archive & {person[0]['web.archive.org']} & {person[1]['web.archive.org']} & {person[2]['web.archive.org']} \\\\\n" \
               f"Archive-It & {person[0]['wayback.archive-it.org']} & {person[1]['wayback.archive-it.org']} & {person[2]['wayback.archive-it.org']} \\\\\n" \
               f"archive.today & {person[0]['archive.md']} & {person[1]['archive.md']} & {person[2]['archive.md']} \\\\\n" \
               f"Library of Congress & {person[0]['webarchive.loc.gov']} & {person[1]['webarchive.loc.gov']} & {person[2]['webarchive.loc.gov']} \\\\\n" \
               f"UK Web Archive & {person[0]['www.webarchive.org.uk']} & {person[1]['www.webarchive.org.uk']} & {person[2]['www.webarchive.org.uk']}  \\\\\n" \
               f"Australian Web Archive & {person[0]['web.archive.org.au']} & {person[1]['web.archive.org.au']} & {person[2]['web.archive.org.au']} \\\\\n" \
               f"Portuguese Web Archive & {person[0]['arquivo.pt']} & {person[1]['arquivo.pt']} & {person[2]['arquivo.pt']} \\\\\n" \
               f"\hline\nTotal & {sum(person[0].values())} & {sum(person[1].values())} & {sum(person[2].values())} \\\\\n\hline\n" \
               "\end{tabular}\n" \
               "\end{table}\n"

    latex_input += person_table + "\n"

print(latex_input)