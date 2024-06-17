from collections import deque

r, c, k = map(int, input().split())
info = [list(map(int, input().split())) for _ in range(k)]


def reserve_area1(forest, x, y, d):
    forest[x][y] = 1
    forest[x - 1][y] = 2 if d == 0 else 1
    forest[x + 1][y] = 2 if d == 2 else 1
    forest[x][y + 1] = 2 if d == 1 else 1
    forest[x][y - 1] = 2 if d == 3 else 1
    return forest


def reserve_area2(robot_i, x, y, value):
    robot_i[x][y] = value
    robot_i[x - 1][y] = value
    robot_i[x + 1][y] = value
    robot_i[x][y + 1] = value
    robot_i[x][y - 1] = value
    return forest


def move(forest, x: int, y: int, d: int):
    flag = False
    if (
        x < r + 1
        and not forest[x + 2][y]
        and not forest[x + 1][y - 1]
        and not forest[x + 1][y + 1]
    ):
        # print("Go Down")
        flag = True
        x += 1
    elif (
        x < r + 1
        and 1 < y
        and not forest[x][y - 2]
        and not forest[x - 1][y - 1]
        and not forest[x + 1][y - 1]
        and not forest[x + 1][y - 2]
        and not forest[x + 2][y - 1]
    ):
        # print("Go Left")
        flag = True
        x += 1
        y -= 1
        d = (d + 3) % 4
    elif (
        x < r + 1
        and y < c - 2
        and not forest[x][y + 2]
        and not forest[x - 1][y + 1]
        and not forest[x + 1][y + 1]
        and not forest[x + 1][y + 2]
        and not forest[x + 2][y + 1]
    ):
        # print("Go Right")
        flag = True
        x += 1
        y += 1
        d = (d + 1) % 4
    if flag:
        x, y, d = move(forest, x, y, d)
    return x, y, d


def find_escape(forest, robot_i, x, y):
    max_row, visited = 0, []
    
    dx, dy = [1, -1, 0, 0], [0, 0, 1, -1]
    q = deque([(x, y)])
    while q:
        x, y = q.popleft()

        max_row = max(max_row, x - 2)
        if x == r + 2:
            break

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]

            if nx < 0 or nx > r + 2 or ny < 0 or ny > c - 1:
                continue

            if (
                (forest[x][y] == 2 and forest[nx][ny] != 0)
                or robot_i[x][y] == robot_i[nx][ny]
            ):
                if (nx, ny) not in visited:
                    visited.append((nx, ny))
                    q.append((nx, ny))
    return max_row


forest = [[0] * c for _ in range(r + 3)]
robot_i = [[0] * c for _ in range(r + 3)]
answer = 0
for i, (col, d) in enumerate(info):
    col -= 1

    x, y, d = move(forest, 0, col, d)
    if x < 4:
        forest = [[0] * c for _ in range(r + 3)]
        robot_i = [[0] * c for _ in range(r + 3)]
    else:
        reserve_area1(forest, x, y, d)
        reserve_area2(robot_i, x, y, i + 1)

        max_row = find_escape(forest, robot_i, x, y)
        answer += max_row

print(answer)