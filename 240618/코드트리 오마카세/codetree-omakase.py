from collections import defaultdict


L, Q = map(int, input().split())
queries = [input().split() for _ in range(Q)]

d_name_sushi_in = defaultdict(list)
d_name_sushi_out = defaultdict(list)
d_name_person_in = {}
d_name_person_out = defaultdict(int)
take_photos = []

for query in queries:
    if query[0] == "100":
        t, x, name = int(query[1]), int(query[2]), query[3]
        d_name_sushi_in[name].append((t, x))
    elif query[0] == "200":
        t, x, name, n = int(query[1]), int(query[2]), query[3], int(query[4])
        d_name_person_in[name] = (t, x, n)
    else:
        take_photos.append(int(query[1]))


def compute_sushi_x_by_time(t, x, tg_t):
    return (x + (tg_t - t)) % L

def compute_eat_time():
    for name in d_name_person_in:
        entry_t, entry_x, _ = d_name_person_in[name]

        for t, x in d_name_sushi_in[name]:
            if entry_t >= t:
                x = compute_sushi_x_by_time(t, x, entry_t)
                last_t = entry_t
            else:
                x = x
                last_t = t

            if x > entry_x:
                distance = L - (x - entry_x)
            else:
                distance = entry_x - x
            d_name_sushi_out[name].append(last_t + distance)
        d_name_person_out[name] = max(d_name_sushi_out[name])


compute_eat_time()

# print(dict(d_name_sushi_in))
# print(dict(d_name_sushi_out))
# print(dict(d_name_person_in))
# print(dict(d_name_person_out))

for t in take_photos:
    # compute the number of persons
    n_person = 0
    for name in d_name_person_in:
        if d_name_person_in[name][0] < t < d_name_person_out[name]:
            n_person += 1
    n_sushi = 0
    for name in d_name_sushi_in:
        tins = [t for t, _ in d_name_sushi_in[name]]
        for tin, tout in zip(tins, d_name_sushi_out[name]):
            if tin < t < tout:
                n_sushi += 1

    print(n_person, n_sushi)