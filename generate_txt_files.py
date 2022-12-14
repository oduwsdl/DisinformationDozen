
import os

urls = ['instagram.com/drmercola', 'facebook.com/doctor.health', 'twitter.com/mercola',
        'instagram.com/RobertFKennedyJr', 'facebook.com/rfkjr', 'twitter.com/RobertKennedyJr',
        'instagram.com/thetruthaboutvaccinesttav', 'facebook.com/tycharlene.bollinger', 'twitter.com/truthaboutbigc',
        'instagram.com/drtenpenny', 'facebook.com/VaccineInfo', 'twitter.com/BusyDrT',
        'instagram.com/_rizzaislam', 'facebook.com/rizza.infinity', 'twitter.com/IslamRizza',
        'instagram.com/drbuttar', 'facebook.com/DrRashidAButtar', 'twitter.com/DrButtar',
        'instagram.com/healthnutnews', 'facebook.com/HealthNutNews', 'twitter.com/unhealthytruth',
        'instagram.com/greenmedinfo', 'facebook.com/sayerji', 'twitter.com/GreenMedInfo',
        'instagram.com/kellybroganmd', 'facebook.com/KellyBroganMD', 'twitter.com/kellybroganmd',
        'instagram.com/drchristianenorthrup', 'facebook.com/DrChristianeNorthrup', 'twitter.com/DrChrisNorthrup',
        'instagram.com/dr.bentapper', 'facebook.com/DrBenTapper', 'twitter.com/DrBenTapper1'
        ]



for url in urls:
    cmd = "curl -L -s https://memgator.cs.odu.edu/timemap/link/https://" + url
    output = os.popen(cmd)
    lines = output.readlines()
    with open(url.replace("/", "_") + '.txt', 'w') as file:
        for line in lines:
            file.write(line)