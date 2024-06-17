from collections import deque, defaultdict


n = int(input())
commands = [list(map(int, input().split())) for _ in range(n)]
sys.stdin = open("output.txt", "r")


class Node:
    def __init__(
        self, 
        m_id: int,
        p_id: int,
        color: int = 1,
        max_depth: int = 1,
    ) -> None:
        """."""
        self.m_id = m_id
        self.p_id = p_id
        self.color = color
        self.max_depth = max_depth

        self.p_node = None
        self.depth = 1
        self.children = []

        self.last_update = 0
        self.color_set = {self.color}

    @property
    def value(self) -> int:
        return len(self.color_set) ** 2

def do100(c: list, d_nodes: dict[int, Node]):
    """."""
    _, m_id, p_id, color, max_depth = c
    
    node = Node(m_id, p_id, color, max_depth)
    if node.p_id == -1:
        d_nodes[node.m_id] = node
        return

    def check_can_make(n: Node, need_depth) -> bool:
        if n.p_id == -1 and n.max_depth >= need_depth:
            return True
        elif n.max_depth < need_depth:
            return False
        return check_can_make(d_nodes[n.p_id], need_depth + 1)

    if check_can_make(d_nodes[node.p_id], 2):
        d_nodes[node.m_id] = node
        d_nodes[node.p_id].children.append(node)

        node.p_node = d_nodes[node.p_id]
        node.depth = d_nodes[node.p_id].depth + 1


def do200(c: list, d_nodes: dict[int, Node]):
    _, m_id, color = c
    q = deque([d_nodes[m_id]])
    while q:
        n = q.popleft()
        n.color = color
        for c in n.children:
            q.append(c)


def do400(d_nodes: dict[int, Node]) -> int:
    d_level_nodes = defaultdict(list)
    for n in d_nodes.values():
        d_level_nodes[n.depth].append(n)
    
    max_depth = max(n.depth for n in d_nodes.values())
    while max_depth > 0:
        nodes = d_level_nodes[max_depth]
        for n in nodes:
            n.color_set = {n.color}
            for c in n.children:
                n.color_set.update(c.color_set)
        max_depth -= 1
    
    return sum(n.value for n in d_nodes.values())


def print_nodeinfo(n: Node):
    print(
        f"Node: {n.m_id}, "
        f"Parent: {n.p_id}, "
        f"Depth: {n.depth}, "
        f"Color: {n.color}, "
        f"LastUpdate: {n.last_update}, "
        f"Value: {n.value}, "
        f"ColorSet: {n.color_set}, "
    )

def print_info(d_nodes: dict[int, Node]):
    print(f"\n# Current Node Info. ({len(d_nodes)})")
    for n in d_nodes.values():
        print_nodeinfo(n)
    print()


d_nodes: dict[int, Node] = {}
for idx, c in enumerate(commands):
    if c[0] == 100:
        do100(c, d_nodes)
    elif c[0] == 200:
        do200(c, d_nodes)
    elif c[0] == 300:
        msg = str(d_nodes[c[1]].color)
        print(msg)
        ans = input()
        assert msg == ans, f"Command 300, msg: {msg}, answer: {ans}"
    elif c[0] == 400:
        total_value = do400(d_nodes)
        msg = str(total_value)
        print(msg)
        ans = input()
        assert msg == ans, f"Command 400, msg: {msg}, answer: {ans}"