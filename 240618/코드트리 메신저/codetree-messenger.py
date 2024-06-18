from collections import deque


N, Q = map(int, input().split())
queries = [input().split() for _ in range(Q)]
chats = []


class Chat:
    def __init__(self, i):
        self.i = i

        self.parent = None
        self.children = dict()
        self.authority = 1

        self.to_parent = 1  # ON-1 / OFF--1

    def __repr__(self):
        return (
            f"ID: {self.i}, "
            f"Parent: {self.parent.i if self.parent else -1}, "
            f"Children: {[c.i for c in self.children.values()]},"
            f"Authority: {self.authority}, "
            f"ToParent: {self.to_parent}, "
        )


def create_chats(query):
    global chats

    info = list(map(int, query[1:]))
    parents = info[:N]
    authorities = info[N:]

    chats = {i: Chat(i) for i in range(N + 1)}
    for child, (parent, authority) in enumerate(zip(parents, authorities), start=1):
        chats[child].parent = chats[parent]
        chats[child].authority = authority
        chats[parent].children[chats[child].i] = chats[child]


def change_authority(query):
    c, power = map(int, query[1:])
    chats[c].authority = power


def switch_status(query):
    chats[int(query[1])].to_parent *= -1


def switch_parent(query):
    a, b = map(int, query[1:])
    ca, cb = chats[a], chats[b]
    pca, pcb = ca.parent, cb.parent

    del pca.children[ca.i]
    pca.children.update({cb.i: cb})
    del pcb.children[cb.i]
    pcb.children.update({ca.i: ca})
    ca.parent, cb.parent = cb.parent, ca.parent


def count_child_nodes(query):
    answer = 0

    q = deque([(chats[int(query[1])], 0)])
    while q:
        c, depth = q.popleft()
        if depth <= c.authority:
            answer += 1

        for child in c.children.values():
            if child.to_parent == 1:
                q.append((child, depth + 1))
    print(answer - 1)


for query in queries:
    if query[0] == "100":
        create_chats(query)
    elif query[0] == "200":
        switch_status(query)
    elif query[0] == "300":
        change_authority(query)
    elif query[0] == "400":
        switch_parent(query)
    elif query[0] == "500":
        count_child_nodes(query)