events = []

with open('12040960.txt') as f:
    lines = f.readlines()

for line in lines:
    spline = line.strip().split(' ')
    event = {}
    for i, word in enumerate(spline):
        if word[0].isalpha():
            wires = []
            for n in range(i + 1, len(spline)):
                if spline[n][0].isalpha():
                    break
                wires.append(spline[n])

            event[word] = wires
    events.append(event)
