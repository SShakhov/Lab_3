import parse

averages = {}
for event in parse.events:
    for plane, hits in event.items():
        # only single hits
        if len(hits) == 1:
            if plane not in averages.keys():
                averages[plane] = []
            averages[plane].append(hits[0].split(':')[0])

for key, item in averages.items():
    averages[key] = sum([int(i) for i in averages[key]]) / len(averages[key])
