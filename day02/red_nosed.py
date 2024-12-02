import sys

def test_report(report):
    if report[0] < report[1]:
        return test_ascending(report)
    else:
        return test_descending(report)

def test_ascending(report):
    for i in range(len(report)-1):
        delta = report[i+1]-report[i]
        if delta < 1 or delta > 3:
            return 0
    return 1

def test_descending(report):
    for i in range(len(report)-1):
        delta = report[i+1]-report[i]
        if delta > -1 or delta < -3:
            return 0
    return 1

def main():
    # parse the input
    reports = []
    with open(sys.argv[1]) as f:
        for line in f:
            reports.append([int(x) for x in line.rstrip().split(' ')])
                   
    print('Part 1:', sum([test_report(r) for r in reports]))

main()
