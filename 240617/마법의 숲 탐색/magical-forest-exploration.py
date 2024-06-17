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


def move(forest, col: int, d: int):
    x, y = 0, col  # center
    
    # go down
    while (
        x < r
        and not forest[x + 2][y]
        and not forest[x + 1][y - 1]
        and not forest[x + 1][y + 1]
    ):
        x += 1

    # rotate left
    while (
        x < r
        and 1 < y
        and not forest[x][y - 2]
        and not forest[x - 1][y - 1]
        and not forest[x + 1][y - 1]
        and not forest[x + 1][y - 2]
        and not forest[x + 2][y - 1]
    ):
        x += 1
        y -= 1

        # rotate counter clockwise
        if d == 0:
            d = 3
        elif d == 1:
            d = 0
        elif d == 2:
            d = 1
        else:
            d = 2

    # rotate right
    while (
        x < r
        and y < c - 2
        and not forest[x][y + 2]
        and not forest[x - 1][y + 1]
        and not forest[x + 1][y + 1]
        and not forest[x + 1][y + 2]
        and not forest[x + 2][y + 1]
    ):
        x += 1
        y += 1

        # rotate clockwise
        if d == 0:
            d = 1
        elif d == 1:
            d = 2
        elif d == 2:
            d = 3
        else:
            d = 0
    return x, y, d


def find_escape(forest, robot_i, x, y):
    max_row, visited = x, []
    
    dx, dy = [1, -1, 0, 0], [0, 0, 1, -1]
    q = deque([(x, y)])
    while q:
        x, y = q.popleft()

        max_row = max(max_row, x - 1)
        if x == r + 1:
            break

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]

            if nx < 0 or nx > r + 1 or ny < 0 or ny > c - 1:
                continue

            if (
                (forest[x][y] == 2 and forest[nx][ny] == 1)
                or robot_i[x][y] == robot_i[nx][ny]
            ):
                if (nx, ny) not in visited:
                    visited.append((nx, ny))
                    q.append((nx, ny))
    return max_row


forest = [[0] * c for _ in range(r + 2)]
robot_i = [[0] * c for _ in range(r + 2)]
answer = 0
for i, (col, d) in enumerate(info):
    col -= 1

    x, y, d = move(forest, col, d)
    if x < 3:
        forest = [[0] * c for _ in range(r + 2)]
        robot_i = [[0] * c for _ in range(r + 2)]
    else:
        reserve_area1(forest, x, y, d)
        reserve_area2(robot_i, x, y, i + 1)

        max_row = find_escape(forest, robot_i, x, y)
        answer += max_row

print(answer)