from calibrate import averages
from parse import events
import ROOT
from array import array

x = [0, 15, 405, 785, 1085, 1385]
x = x[2:]

# y = a + bx
coeff_a = []
coeff_b = []

for event in events:
    y = []

    hit_planes = 0
    for i in range(1, 5):
        plane = 'P{0}'.format(i)
        if len(event[plane]) != 0:
            hit_planes += 1

    if hit_planes < 4:
        continue

    for i in range(1, 5):
        plane = 'P{0}'.format(i)
        y_current = sum([int(n) for n in event[plane]]) / float(len(event[plane]))
        y.append(y_current - averages[plane])

    graph = ROOT.TGraphErrors(
        len(x),
        array('d', x),
        array('d', y),
        array('d', [0 for i in range(len(x))]),
        array('d', [1. / 12 for i in range(len(y))]))

    func = ROOT.TF1('func', 'pol1')
    graph.Fit(func)

    if func.GetChisquare() < 5:
        coeff_a.append(func.GetParameter(0))
        coeff_b.append(func.GetParameter(1))

hist_angle = ROOT.TH1D('angle', 'angle', 100, -10, 10)
hist_pos = ROOT.TH1D('position', 'position', 100, -100, 100)
for pos, angle in zip(coeff_a, coeff_b):
    hist_pos.Fill(pos)
    hist_angle.Fill(ROOT.TMath.ATan(angle) * 180 / ROOT.TMath.Pi())
