import os
import csv

with open('redirects_katy.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["year", "status_code"])

    # urls = ['instagram.com/drmercola', 'instagram.com/RobertFKennedyJr', 'instagram.com/thetruthaboutvaccinesttav',
    #         'instagram.com/drtenpenny', 'instagram.com/_rizzaislam', 'instagram.com/drbuttar',
    #         'instagram.com/healthnutnews', 'instagram.com/greenmedinfo', 'instagram.com/kellybroganmd',
    #         'instagram.com/drchristianenorthrup', 'instagram.com/dr.bentapper']

    # urls = ['instagram.com/bbcnews', 'instagram.com/unicef', 'instagram.com/cdcgov',
    #         'instagram.com/who', 'instagram.com/thisisbillgates', 'instagram.com/ukgovofficial',
    #         'instagram.com/nhs', 'instagram.com/gatesfoundation', 'instagram.com/lshtm']
    urls = ['instagram.com/katyperry']




    for url in urls:
        status_codes = {'200': 0, '301': 0, '302': 0, '-': 0}
        unknown_redirects = 0
        unknown_successes = 0
        success_list = []

        # cmd = 'curl -L -s \"http://web.archive.org/cdx/search/cdx?url=https://www.' + url + '"' + ' > ' + url.replace("/",
        # "_") + '.cdx'

        cmd = 'curl -L -s \"http://web.archive.org/cdx/search/cdx?url=https://www.' + url + '"'

        output = os.popen(cmd)
        lines = output.readlines()

        for line in lines:
            cdx_object = line.split(" ")
            status_code = cdx_object[4]
            memento_year = int(cdx_object[1][:4])
            uri_m = "https://web.archive.org/web/" + cdx_object[1] + "/" + cdx_object[2]

            if status_code == '200':
                success_list.append(uri_m)

            if status_code == '-' and memento_year >= 2021:
                unknown_redirects += 1
                status_code = 302

            if status_code == '-' and memento_year < 2021:

                cmd = 'curl -Ls ' + uri_m + ' | grep -c "Got an HTTP 302 response at crawl time\|Login • Instagram"'
                output = os.popen(cmd)
                num = output.read()
                if int(num) == 1:
                    unknown_redirects += 1
                    status_code = 302
                if int(num) == 0:
                    unknown_successes += 1
                    status_code = 200
                    success_list.append(uri_m)

            if status_code not in status_codes:
                status_codes.update({status_code: 1})
            else:
                status_codes[status_code] += 1

            print(uri_m)
            writer.writerow([memento_year, status_code])


        known_redirects = status_codes['301'] + status_codes['302']
        total_redirects = known_redirects + unknown_redirects
        known_successes = status_codes['200']
        total_successes = status_codes['200'] + unknown_successes
        total_mementos = sum(status_codes.values())

        print(success_list)

        print(status_codes)
        print("Known Redirects: " + str(known_redirects))
        print("Unknown Redirects: " + str(unknown_redirects))
        print("Total Redirects: " + str(total_redirects))
        print("Known Successes: " + str(known_successes))
        print("Unknown Successes: " + str(unknown_successes))
        print("Total Successes: " + str(total_successes))
        print("Total mementos: " + str(total_mementos))

        url = url.replace("_", "\_")
        status_table = "\\begin{table}[]\n\\vspace*{2 cm}\n\\begin{tabular}{|c|c|c|}\n\hline\n& Number of Mementos & Percentage of Total Mementos \\\\\n\hline\n" \
                       f"Identified Redirects & {known_redirects} & {round(known_redirects/total_mementos * 100, 2)}\% \\\\\n" \
                       f"Unidentified Redirects & {unknown_redirects} & {round(unknown_redirects / total_mementos * 100, 2)}\% \\\\\n\hline\n" \
                       f"Total Redirects & {total_redirects} & {round(total_redirects/total_mementos * 100, 2)}\% \\\\\n\hline\n" \
                       f"Identified Successes & {known_successes} & {round(known_successes/total_mementos * 100, 2)}\% \\\\\n" \
                       f"Unidentified Successes & {unknown_successes} & {round(unknown_successes / total_mementos * 100, 2)}\% \\\\\n\hline\n" \
                       f"Total Successes & {total_successes} & {round(total_successes / total_mementos * 100, 2)}\% \\\\\n\hline\n" \
                       f"Total Mementos & {total_mementos} & {round(total_mementos / total_mementos * 100, 2)}\% \\\\\n\hline\n" \
                       "\end{tabular}\n" \
                       f"\caption{{Redirects vs. successes for {url}}}\n" \
                       "\end{table}\n"

        print(status_table)
