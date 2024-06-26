import heapq


N = 2000
M = 10000

A = []
D = []
S = 0

package_q = []
isMade = [False] * 30001
isCancel = [False] * 30001


class Package:
    def __init__(self, tour_id, revenue, dest, profit):
        self.tour_id = tour_id
        self.revenue = revenue
        self.dest = dest
        self.profit = profit
    
    def __lt__(self, other):
        if self.profit == other.profit:
            return self.tour_id < other.tour_id
        return self.profit > other.profit

    def __str__(self):
        return (
            f"[ID: {self.tour_id}] "
            f"DESTINATION: {self.dest}, "
            f"PROFIT: {self.profit}"
        )

    def __repr__(self) -> str:
        return self.__str__()


# def dijkstra():
#     global D, S

#     # do dijkstra
#     D = [float("inf")] * N
#     D[S] = 0

#     pq = [(0, S)]
#     heapq.heapify(pq)
#     while pq: 
#         cur_dist, cur_dest = heapq.heappop(pq)
#         if D[cur_dest] < cur_dist:
#             continue
    
#         for new_dest, new_dist in enumerate(A[cur_dest]):
#             if not new_dist:
#                 continue
#             distance = cur_dist + new_dist
#             if distance < D[new_dest]:
#                 D[new_dest] = distance
#                 heapq.heappush(pq, (distance, new_dest))
        
def dijkstra():
    global D

    INF = float("inf")

    D = [INF] * N
    visit = [False] * N
    D[S] = 0
    
    for _ in range(N):
        v = -1
        minDist = INF
        for j in range(N):
            if not visit[j] and minDist > D[j]:
                v = j
                minDist = D[j]
        if v == -1:
            break
        visit[v] = True
        for j in range(N):
            if A[v][j] != INF and D[j] > D[v] + A[v][j]:
                D[j] = D[v] + A[v][j]


def c100(query):
    global A, N, M, S

    N, M, arr = query[1], query[2], query[3:]
    A = [[float("inf")] * N for _ in range(N)]
    for i in range(N):
        A[i][i] = 0
    for i in range(M):
        u, v, w = arr[i * 3], arr[i * 3 + 1], arr[i * 3 + 2]
        A[u][v] = min(A[u][v], w)
        A[v][u] = min(A[v][u], w)
    
    dijkstra()


def c200(query):
    tour_id, revenue, dest = query[1:]
    isMade[tour_id] = True
    profit = revenue - D[dest]
    heapq.heappush(package_q, Package(tour_id, revenue, dest, profit))


def c300(query):
    tour_id = query[1]
    if isMade[tour_id]:
        isCancel[tour_id] = True


def c400():
    while package_q:
        p = package_q[0]
        if p.profit < 0:
            break

        p = heapq.heappop(package_q)
        if not isCancel[p.tour_id]:
            print(p.tour_id)
            return
    print(-1)


def c500(query):
    global S

    S = query[1]
    dijkstra()

    temp_packages = []
    while package_q:
        temp_packages.append(heapq.heappop(package_q))

    for p in temp_packages:
        profit = p.revenue - D[p.dest]
        heapq.heappush(package_q, Package(p.tour_id, p.revenue, p.dest, profit))


def main():
    Q = int(input())
    for _ in range(Q):
        query = list(map(int, input().split()))
        T = query[0]
        
        # 쿼리의 종류에 따라 필요한 함수들을 호출하여 처리합니다
        if T == 100:
            c100(query)
        elif T == 200:
            c200(query)
        elif T == 300:
            c300(query)
        elif T == 400:
            c400()
        else:
            c500(query)


if __name__ == "__main__":
    main()