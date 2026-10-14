def encode_runs(items):
    if not items:
        return []
    runs = []
    current = items[0]
    count = 1
    for item in items[1:]:
        if item == current:
            count += 1
        else:
            runs.append((current, count))
            current = item
            count = 1
    runs.append((current, count))
    return runs


import json
checks = [{'input': [], 'expected': []}, {'input': ['a'], 'expected': [['a', 1]]}, {'input': ['a', 'a', 'b', 'a'], 'expected': [['a', 2], ['b', 1], ['a', 1]]}, {'input': ['X', 'x', ' x', '', ''], 'expected': [['X', 1], ['x', 1], [' x', 1], ['', 2]]}]
report=[]
for check in checks:
 expected=[tuple(x) for x in check["expected"]]
 actual=encode_runs(check["input"])
 report.append({"input":check["input"],"pass":actual==expected,"actual":repr(actual),"expected":repr(expected)})
print(json.dumps(report))
