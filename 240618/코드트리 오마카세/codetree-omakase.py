from collections import deque, defaultdict

class Sushi:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Name: {self.name}"

    def __repr__(self):
        return self.__str__()


class Table:
    def __init__(self, l):
        self.l = l
        self.sushi = deque([defaultdict(int) for _ in range(self.l)])
        self.persons = {i: defaultdict(int) for i in range(self.l)}

        self.t = 0

    def add_sushi(self, query):
        t, x, name = int(query[1]), int(query[2]), query[3]
        while self.t < t:
            self.do_a_timestep()

        self.sushi[x][name] += 1
        if name in self.persons[x]:
            if self.eat_sushi_and_leave(x, name, self.persons[x][name]):
                del self.persons[x][name]

    def get_a_guest(self, query):
        t, x, name, n = int(query[1]), int(query[2]), query[3], int(query[4])
        self.persons[x][name] = n
        while self.t < t:
            self.do_a_timestep()

    def eat_sushi_and_leave(self, x, name, n):
        sushi_on_table = self.sushi[x][name]
        if n > sushi_on_table:
            self.persons[x][name] = n - sushi_on_table
            del self.sushi[x][name]
            return False
        elif n == sushi_on_table:
            del self.sushi[x][name]
        else:
            self.sushi[x][name] = sushi_on_table - n
        return True

    def take_a_photo(self, query):
        while self.t < int(query[1]):
            self.do_a_timestep()

        n_person = sum(len(p) for p in self.persons.values())
        n_sushi = sum(sum(s.values()) for s in self.sushi)
        print(n_person, n_sushi)

    def do_a_timestep(self):
        self.sushi.appendleft(self.sushi.pop())

        persons_to_leave = []
        for x, persons in self.persons.items():
            for name, n in persons.items():
                if self.eat_sushi_and_leave(x, name, n):
                    persons_to_leave.append((x, name))

        # update guest info
        for x, name in persons_to_leave:
            del self.persons[x][name]

        self.t += 1

    def display_info(self):
        table_info = [dict(s) if s else "*" for s in self.sushi]
        person_info = [dict(p) if p else "*" for p in self.persons.values()]
        print(
            "< TABLE INFO >\n"
            f"# of SUSHI: {sum(len(s) for s in self.sushi)}\n"
            f"# of person: {sum(len(p) for p in self.persons.values())}\n"
            f"TableInfo (SUSHI): {table_info}\n"
            f"TableInfo (PERSON): {person_info}\n"
            f"TimeStamp: {self.t}\n"
        )


L, Q = map(int, input().split())
table = Table(l=L)

for t in range(Q):
    query = input().split()

    if query[0] == "100":
        table.add_sushi(query)
    elif query[0] == "200":
        table.get_a_guest(query)
    elif query[0] == "300":
        table.take_a_photo(query)

    # table.display_info()