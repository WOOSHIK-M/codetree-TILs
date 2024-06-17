from collections import defaultdict
import heapq


Q = int(input())
COMMANDS = [list(map(int, input().split())) for _ in range(Q)]


class CodeTreeLand:
    def __init__(self, n, m, info) -> None:
        """Initialize."""
        self.n = n
        self.m = m
        self.info = info

        self.start = 0

        self.cities = defaultdict(list)
        for i in self.info:
            self.cities[i[0]].append((i[1], i[2]))
            self.cities[i[1]].append((i[0], i[2]))
        self.adj_mat = [[0] * self.n for _ in range(self.n)]
        for src, dsts in self.cities.items():
            for dst, weight in dsts:
                if self.adj_mat[src][dst]:
                    weight = min(weight, self.adj_mat[src][dst])
                self.adj_mat[src][dst] = weight
                self.adj_mat[dst][src] = weight

        self.products = {}
        self.update_benefits()

    def update_benefits(self) -> None:
        """."""

        def do_dijkstra():
            """."""
            # do dijkstra
            start = self.start
            distances = {city: float("inf") for city in self.cities}
            distances[start] = 0

            q = []
            heapq.heappush(q, (distances[start], start))
            while q:
                cur_dist, cur_dest = heapq.heappop(q)

                if distances[cur_dest] < cur_dist:
                    continue

                for new_dest, new_dist in self.cities[cur_dest]:
                    distance = cur_dist + new_dist
                    if distance < distances[new_dest]:
                        distances[new_dest] = distance
                        heapq.heappush(q, (distance, new_dest))
            return distances
        
        self.distances = do_dijkstra()

    def __str__(self) -> str:
        """."""
        return (
            f"[LAND INFO]\n"
            f"CITIES: {self.cities}\n"
            f"EDGES: {self.info}\n"
            f"PRODUCTS: {self.products}\n"
        )


# 100 - 랜드 건설
def c100(c) -> CodeTreeLand:
    """."""
    n, m = c[1:3]
    info = c[3:]
    info = list(zip(info[::3], info[1::3], info[2::3]))
    return CodeTreeLand(n, m, info)


# 200 - 여행 상품 생성
def c200(c, land: CodeTreeLand):
    """."""
    tour_id, revenue, dest = c[1:]
    land.products[tour_id] = (revenue, dest)


# 300 - 여행 상품 취소
def c300(c, land: CodeTreeLand):
    """."""
    if c[1] in land.products:
        land.products.pop(c[1])


# 400 - 최적의 여행 상품 판매
def c400(land: CodeTreeLand):
    """."""
    benefits = {
        tour_id: revenue - land.distances[dst]
        for tour_id, (revenue, dst) in land.products.items()
        if revenue - land.distances[dst] >= 0
    }
    tour_id = -1
    if benefits:
        max_benefit = max(list(benefits.values()))
        tour_ids = [tour_id for tour_id, benefit in benefits.items() if benefit == max_benefit]
        tour_id = min(tour_ids)
        land.products.pop(tour_id)
    print(tour_id)


# 500 - 여행 상품의 출발지 변경
def c500(c, land: CodeTreeLand):
    land.start = c[1]
    land.update_benefits()


land = c100(COMMANDS[0])
for command in COMMANDS[1:]:
    if command[0] == 200:
        c200(command, land)
    elif command[0] == 300:
        c300(command, land)
    elif command[0] == 400:
        c400(land)
    elif command[0] == 500:
        c500(command, land)