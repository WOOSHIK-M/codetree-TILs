import copy
import heapq
from collections import deque


class PriorityCoord:

    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def __lt__(self, other: "PriorityCoord"):
        if self.y == other.y:
            return self.x > other.x
        return self.y < other.y
        

class Solution:

    def __init__(self, arr, i, j, reward, degree, coords):
        self.arr = arr
        self.i, self.j = i, j
        self.reward = reward
        self.degree = degree

        self.coords = coords
    
    def __lt__(self, other: "Solution"):
        if self.reward == other.reward:
            if self.degree == other.degree:
                if self.j == other.j:
                    return self.i > other.i
                return self.j > other.j
            return self.degree > other.degree
        return self.reward < other.reward


class TreasureMap:
    """Treasure map."""

    def __init__(self) -> None:
        """Initialize."""
        self.K, self.M = map(int, input().split())
        self.arr = [list(map(int, input().split())) for _ in range(5)]
        # print(self.arr)
        
        # re-fill values
        self.board = list(map(int, input().split()))

        # exploration
        self.dx, self.dy = [1, -1, 0, 0], [0, 0, 1, -1]

    def run(self) -> None:
        """Run."""
        rewards = []
        board_idx = 0
        for _ in range(self.K):
            # print(self.arr)
    
            opt_sol = self.explore()
            arr, coords, reward = opt_sol.arr, opt_sol.coords, opt_sol.reward
            if reward == 0:
                break

            total_reward = 0
            while reward > 0:
                total_reward += reward

                p_coords = [PriorityCoord(x, y) for x, y in coords]
                heapq.heapify(p_coords)

                # print(self.board[board_idx:])
                while p_coords:
                    coord = heapq.heappop(p_coords)
                    arr[coord.x][coord.y] = self.board[board_idx]
                    board_idx += 1

                reward, coords = self._do_bfs(arr)

            self.arr = arr
            rewards.append(total_reward)
            # print(arr, opt_sol.i, opt_sol.j, opt_sol.degree)
            # print()
        print(" ".join(map(str, rewards)))

    def explore(self) -> None:
        """."""
        solutions = []
        for i in [1, 2, 3]:
            for j in [1, 2, 3]:        
                for d in [0, 90, 180, 270]:
                    arr = self._rotate_by_degree(i, j, d)
                    tmp_r, coords = self._do_bfs(arr)
                    solutions.append(Solution(arr, i, j, tmp_r, d, coords))

        # for s in solutions:
        #     print(s.i, s.j, s.degree, s.reward, s.arr)
        return max(solutions)

    def _rotate_by_degree(self, i: int, j: int, degree: int):
        arr = copy.deepcopy(self.arr)
        if degree == 0:
            return arr

        patch = [self.arr[i + tmp_i][j - 1: j + 2] for tmp_i in [-1, 0, 1]]
        if degree == 90:
            patch = [list(row)[::-1] for row in zip(*patch)]
        elif degree == 180:
            patch = [row[::-1] for row in patch[::-1]]
        elif degree == 270:
            patch = [list(row) for row in zip(*patch)][::-1]

        for idx, row in enumerate(patch, start=-1):
            arr[i + idx][j - 1: j + 2] = row
        return arr

    def _do_bfs(self, arr) -> None:
        """."""
        visited = [[0] * 5 for _ in range(5)]

        total_reward, total_coords= 0, []
        for i in range(5):
            for j in range(5):
                if visited[i][j]:
                    continue

                q = deque([(i, j, arr[i][j], {(i, j)})])
                visited[i][j] = 1

                while q:
                    x, y, value, coords = q.popleft()

                    found_coords = set()
                    for di in range(4):
                        nx, ny = x + self.dx[di], y + self.dy[di]
                        if nx < 0 or nx > 4 or ny < 0 or ny > 4 or visited[nx][ny] or arr[nx][ny] != arr[x][y]:
                            continue

                        found_coords.add((nx, ny))
                        visited[nx][ny] = 1
                    
                    for nx, ny in found_coords:
                        coords.update(found_coords)
                        q.append((nx, ny, value, coords))

                    if not q and len(coords) > 2:
                        total_reward += len(coords)
                        total_coords += coords        
        return total_reward, total_coords


TreasureMap().run()