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

def remove_one(report):
    for i in range(len(report)):
        yield [report[j] for j in range(len(report)) if j != i]

def main():
    # parse the input
    reports = []
    with open(sys.argv[1]) as f:
        for line in f:
            reports.append([int(x) for x in line.rstrip().split(' ')])
                   
    print('Part 1:', sum([test_report(r) for r in reports]))

    cnt2 = 0
    for report in reports:
        if test_report(report):
            cnt2 += 1
        else:
            for r in remove_one(report):
                if test_report(r):
                    cnt2 += 1
                    break

    print('Part 2:', cnt2)
        
main()
