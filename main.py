import matplotlib.pyplot as plt


def compute_code(x, y, x_min, x_max, y_min, y_max):
    code = 0
    if x < x_min:
        code |= 1  # Лівий край
    elif x > x_max:
        code |= 2  # Правий край
    if y < y_min:
        code |= 4  # Нижній край
    elif y > y_max:
        code |= 8  # Верхній край
    return code


def cohen_sutherland_clip(x1, y1, x2, y2, x_min, x_max, y_min, y_max):
    code1 = compute_code(x1, y1, x_min, x_max, y_min, y_max)
    code2 = compute_code(x2, y2, x_min, x_max, y_min, y_max)
    accept = False
    original_segment = ((x1, y1), (x2, y2))  # Початковий відрізок для відображення обрізаної частини

    while True:
        if (code1 | code2) == 0:
            accept = True
            break
        elif (code1 & code2) != 0:
            break
        else:
            x = y = 0
            code_out = code1 if code1 != 0 else code2

            if code_out & 8:  # Верхній край
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif code_out & 4:  # Нижній край
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif code_out & 2:  # Правий край
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif code_out & 1:  # Лівий край
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min

            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1, x_min, x_max, y_min, y_max)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2, x_min, x_max, y_min, y_max)

    if accept:
        return (x1, y1, x2, y2), original_segment
    else:
        return None, original_segment


x_min, x_max = 1, 7
y_min, y_max = 1, 7

segments = [((2, 5, 8, 9), 'red'),  # Відрізок частково виходить за межі
            ((0, 3, 6, 3), 'blue'),  # Відрізок повністю виходить за межі
            ((3, 0, 4, 4), 'green')]  # Відрізок частково виходить за межі

fig, ax = plt.subplots()

plt.plot([x_min, x_max], [y_min, y_min], 'k-')  # Нижній край
plt.plot([x_min, x_max], [y_max, y_max], 'k-')  # Верхній край
plt.plot([x_min, x_min], [y_min, y_max], 'k-')  # Лівий край
plt.plot([x_max, x_max], [y_min, y_max], 'k-')  # Правий край

for (x1, y1, x2, y2), color in segments:
    clipped_segment, original_segment = cohen_sutherland_clip(x1, y1, x2, y2, x_min, x_max, y_min, y_max)

    if clipped_segment:
        (cx1, cy1, cx2, cy2) = clipped_segment
        ax.plot([cx1, cx2], [cy1, cy2], color=color, marker='o')  # Залишена частина
        # Обрізана частина чорним кольором
        if (x1, y1) != (cx1, cy1):
            ax.plot([x1, cx1], [y1, cy1], color='black', linestyle='--')
        if (x2, y2) != (cx2, cy2):
            ax.plot([x2, cx2], [y2, cy2], color='black', linestyle='--')
    else:
        ax.plot([x1, x2], [y1, y2], color='black', linestyle='--', marker='x')

plt.xlim(0, 10)
plt.ylim(0, 10)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.title('Відсічені відрізки (чорним кольором — обрізані частини)')
plt.show()
