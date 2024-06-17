from collections import deque, defaultdict


n = int(input())
commands = [list(map(int, input().split())) for _ in range(n)]


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

        self.depth = 1
        self.p_node = None
        self.children = []

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
    
    p_node = d_nodes[node.p_id]
    depth_dist = 1
    while p_node.max_depth > depth_dist:
        if p_node.p_id == -1:
            break

        depth_dist += 1
        p_node = d_nodes[p_node.p_id]
    
    if p_node.p_id == -1:
        d_nodes[node.m_id] = node
        node.p_node = d_nodes[node.p_id]
        node.depth = d_nodes[node.p_id].depth + 1
        d_nodes[node.p_id].children.append(node)
    

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


d_nodes = {}
for c in commands:
    if c[0] == 100:
        do100(c, d_nodes)
    elif c[0] == 200:
        do200(c, d_nodes)
    elif c[0] == 300:
        print(d_nodes[c[1]].color)
    elif c[0] == 400:
        total_value = do400(d_nodes)
        print(total_value)