d = {
        "1111" : {
            "order": 10
            },
        "4444" : {
            "order": 0
            },
        "2222" : {
            "order": 11
            },
        "3333" : {
            "order": 0
            },
}

import functools
def compare(k1,k2):
    return int(d.get(k2).get("order",0)) - int(d.get(k1).get("order",0))

#for w in sorted(d, key=functools.cmp_to_key(compare), reverse=True):
print(d)
for w in sorted(d, key=lambda k: d[k]["order"]):
    print(w, d[w])
