import json


def formatLocation(loc):
    return loc.split(',')[0].replace(' ', '-')


f = open("times.json", "r")
raw_response = f.read()

response = json.loads(raw_response)
origins = response['origin_addresses']
destinations = response['destination_addresses']

entries = []

print("ServicePointLocation,ClientLocation,Distance,DistanceText,Duration,DurationText")

for origin_index, row in enumerate(response['rows']):
    for dest_index, entry in enumerate(row['elements']):
        # print(f"origin: {formatLocation(origins[origin_index])} dest: {formatLocation(destinations[dest_index])} distance: {entry['distance']['value']} durationText: {entry['distance']['text']} duration: {entry['duration']['value']} durationText: {entry['duration']['text']}")
        print(f"{formatLocation(origins[origin_index])},{formatLocation(destinations[dest_index])},{entry['distance']['value']},{entry['distance']['text']},{entry['duration']['value']},{entry['duration']['text']}")
