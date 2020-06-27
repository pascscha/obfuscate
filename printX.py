import time


def printX(width, height, weight):
    for h in range(height):
        progression = h / height
        pos1_1 = (0+progression) * (width - weight) + 0
        pos1_2 = (0+progression) * (width - weight) + weight
        pos2_1 = (1-progression) * (width - weight) + 0
        pos2_2 = (1-progression) * (width - weight) + weight
        for w in range(width):
            if pos1_1 < w < pos1_2 or pos2_1 < w < pos2_2:
                print("X", end="", flush=True)
            else:
                print(" ", end="", flush=True)
            time.sleep(.1)
        print()


if __name__ == "__main__":
    printX(10, 10, 3)
