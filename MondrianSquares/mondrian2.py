"""This module attempts to solve the first half of the Mondrian Squares
Problem.
"""
import math
import time
import heapq
import json


# ===== UTILITY FUNCTIONS ====================================================
def area(rect):
    """Calculates the area of a rectangle."""
    return rect[0] * rect[1]


def optimal(size):
    """Returns a(n) for 3 <= n <= 57 where a(n) is the optimal tiling of the
    Mondrian Art Puzzle.
    """
    OEIS = [
        0, 0, 0, 2, 4, 4, 5, 5, 6, 6, 8, 6, 7, 8, 6, 8, 8, 8, 8, 8, 9, 9, 9,
        8, 9, 10, 9, 10, 9, 9, 11, 11, 10, 12, 12, 11, 12, 11, 10, 11, 12, 13,
        12, 12, 12, 13, 13, 12, 14, 12, 13, 14, 13, 14, 15, 14, 14, 15
    ]
    return OEIS[size]


def defect(rectlist):
    """Returns the defect of a rectlist."""
    arealist = [area(x) for x in rectlist]
    return max(arealist) - min(arealist)


def simp_time(time_in_s):
    """Returns a string of the duration given the time in seconds."""
    if time_in_s < 60:
        return f"{time_in_s:.1f}s"
    elif time_in_s < 3600:
        return f"{time_in_s/60:.1f}m"
    elif time_in_s < 86400:
        return f"{time_in_s/3600:.1f}h"
    else:
        return f"{time_in_s//86400}d {time_in_s%86400:.1f}h"


# ===== PART 1 ===============================================================
def create_rect_list(size, quiet=False, generator=True):
    """Returns a generator or an array of rect objects for the size x size
    square. Faster than sorting.
    """
    # The upper bound for rectangle objects.
    ceiling = math.ceil(size * size / 2)
    rect_list = []
    for a in range(1, size + 1):
        temp_list = []
        for b in range(a, size + 1):
            if a * b > ceiling:
                break
            temp_list.append((a, b))
        rect_list = heapq.merge(rect_list, temp_list, key=area)
    if not quiet:
        print("Rectangle list generation complete")
    if generator:
        return rect_list
    else:
        return [x for x in rect_list]


def search_sum(size, bound=0, quiet=False, index=False):
    """Returns all possible arrangements of rects with valid area"""
    if bound == 0:  # See oeis.org/A276523
        if size % 2 == 0:
            bound = math.ceil(size / math.log(size) + 3)
        else:
            bound = size
    rect_list = create_rect_list(size, quiet, generator=False)

    def subsetsum(sum, start, lower):
        """Recursive tree search for total subset size"""
        subset = []
        for i in range(len(rect_list) - start):
            a = area(rect_list[i + start])
            if a - lower > bound or a > sum:
                # Depth exceeded or value too large
                break
            elif a < sum:
                # Recursion
                rlist = subsetsum(sum - a, i + start + 1, lower)
                for r in rlist:
                    if index:
                        r.append(i + start)
                    else:
                        r.append(rect_list[i + start])
                    subset.append(r)
            elif a == sum:
                # Base case
                if index:
                    subset.append([i + start])
                else:
                    subset.append([rect_list[i + start]])
        return subset

    def prune(rlist):
        """Returns false if the rectlist is not theoretically tileable."""
        def finish_row(sum, rlist):
            for a in range(len(rlist)):
                if sum == rlist[a][0] or sum == rlist[a][1]:
                    return True
                else:
                    templist = rlist[:a] + rlist[a + 1:]
                    if sum > rlist[a][0]:
                        if finish_row(sum - rlist[a][0], templist):
                            return True
                    if sum > rlist[a][1]:
                        if finish_row(sum - rlist[a][1], templist):
                            return True
            return False

        for a in range(len(rlist)):
            # Find if there exist a subset of the other rects which can
            #   tile with this rect.
            templist = rlist[:a] + rlist[a + 1:]
            if not finish_row(size - rlist[a][0], templist):
                return False
            if not finish_row(size - rlist[a][1], templist):
                return False
        return True

    solutionlist = []
    start = time.time()
    for i in range(len(rect_list)):
        if not quiet:
            print(f"Searching tree {i + 1} of {len(rect_list)}, n = {size}")
        a = area(rect_list[i])
        rlist = subsetsum(size * size - a, i + 1, a)
        for r in rlist:
            if index:
                r.append(i)
            else:
                r.append(rect_list[i])
            if prune(r):
                solutionlist.append(r)
        if not quiet:
            avgtime = (time.time() - start) / (i + 1)
            tleft = avgtime * (len(rect_list) - i - 1)
            esttime = time.strftime(
                '%H:%M',
                time.localtime(tleft + time.time())
            )
            print(
                f"Currently {time.strftime('%H:%M', time.localtime())}" +
                f" / Time left: {simp_time(tleft)} / ETA: {esttime}"
            )

    if not quiet:
        totaltime = time.strftime('%H:%M', time.gmtime(time.time() - start))
        print(f"Found {len(solutionlist)} possible solutions")
        print(f"Size {size} took {totaltime}.")
    return solutionlist


def count_time(value, quiet=False, iterations=1):
    """Returns the running times of start through stop inclusive."""
    if not quiet:
        print("Searching size", value)
    duration = 0
    for _ in range(iterations):
        timestart = time.perf_counter()
        search_sum(value, optimal(value), quiet)
        duration += round(time.perf_counter() - timestart, 3)
    duration /= iterations
    duration = round(duration, 3)
    print(f"Size {value} takes {duration} s over {iterations} iterations.")
    return duration


def find_duplicates(size):
    """Temporary function"""
    rect_list = create_rect_list(size, quiet=True, generator=False)
    solutionlist = search_sum(size)
    indexlist = []
    for a in solutionlist:
        templist = []
        for b in a:
            templist.append(rect_list.index(b))
        templist.sort()
        indexlist.append(templist)
    print(indexlist)


def write_part_1(size, stop=0, improve=True, quiet=False):
    """Solves part 1 of the Mondrian Squares problem and saves the results to
    file.

    size: the side length of the square
    improve: whether to search only for better than current best solutions
    """
    if stop == 0:
        stop = size + 1
    for n in range(size, stop):
        bound = 0
        if improve:
            bound = optimal(n) - 1
        else:
            resp = input("Are you sure you want suboptimal values?? [Y/N]")
            if resp != "Y" and resp != "y":
                print("Aborted.")
                return None
        solutionlist = search_sum(n, bound, quiet)
        solutiondict = {}
        for a in solutionlist:
            d = defect(a)
            if str(d) not in solutiondict:
                solutiondict[str(d)] = []
            solutiondict[str(d)].append(a)
        with open(f"MondrianSquares/Part1/length{n:03}.json", "w") as f:
            f.write(json.dumps(solutiondict))
        if not quiet:
            print("Saved to file.")


# ===== PART 2 ===============================================================
def is_tiled(square):
    for a in square:
        if a != 0:
            return False
    return True


def add_tile(square, rect):
    # assert(!is_tiled(square))
    i = 0
    while square[i] == 0:
        i += 1
    sqcopy = square[:]
    for a in range(rect[0]):
        if i + a >= len(sqcopy) or sqcopy[i + a] < rect[1]:
            return False
        sqcopy[i + a] -= rect[1]
    square[:] = sqcopy[:]   # This does a proper rewrite
    return True


def search_tiling(size, rectlist, square, tilelist):
    for r in rectlist:
        if not tilelist:
            print(f"Tile {rectlist.index(r)+1} of {len(rectlist)}")
        rlcopy = rectlist[:]
        rlcopy.remove(r)
        sqcopy = square[:]
        if add_tile(sqcopy, r):
            if rlcopy and search_tiling(size, rlcopy, sqcopy, tilelist + [r]):
                return True
        sqcopy = square[:]
        if r[0] != r[1] and add_tile(sqcopy, (r[1], r[0])):
            if rlcopy and search_tiling(
                size, rlcopy, sqcopy, tilelist + [[r[1], r[0]]]
            ):
                return True
    if is_tiled(square):
        d = defect(tilelist)
        sizedict = {str(d): tilelist}
        with open(f"MondrianSquares/Part2/length{size:03}.json", 'w') as f:
            f.write(json.dumps(sizedict))
        if d < optimal(size):
            print(f"Found a new optimal for size {size}!?")
        elif d == optimal(size):
            print(f"Optimal confirmed for size {size}.")
        else:
            print(f"Found suboptimal for size {size}. Search again?")
        return True
    return False


def find_tiling(size, quiet=False, improve=False, manual=False):
    with open(f"MondrianSquares/Part1/length{size:03}.json", 'r') as f:
        solutiondict = json.load(f)
    keylist = [x for x in solutiondict]
    keylist.sort()
    if manual:
        while True:
            response = input(f"Would you like to skip d={keylist[0]}? Y/N ")
            if response == "Y":
                keylist = keylist[1:]
            elif response == "N":
                break
            else:
                print("Invalid input")

    for a in keylist:
        if improve and int(a) >= optimal(size):
            print("Finished searching superoptimal values.")
            break
        solutionlist = solutiondict[a]
        if not quiet:
            print(f"Searching defect {a}")
        for b in solutionlist:
            if not quiet:
                print(f"Depth {solutionlist.index(b)} of {len(solutionlist)}")
            if search_tiling(size, b, [size] * size, []) and not quiet:
                print(f"Eureka! Size {size}")
                return


def write_part_2(size, stop=0, improve=False, quiet=False, manual=False):
    if stop == 0:
        stop = size + 1
    for n in range(size, stop):
        if not quiet:
            print(f"Checking size {n}")
        find_tiling(n, quiet, improve, manual)


def check_optimal(size, stop=0):
    if stop == 0:
        stop = size + 1
    for n in range(size, stop):
        with open(f"MondrianSquares/Part2/length{n:03}.json", 'r') as f:
            solutiondict = json.load(f)
        for a in solutiondict:
            if int(a) != optimal(n):
                print(f"Size {n} is suboptimal.")
    print("Optimality checking complete.")


def auto(size, stop=0, improve=True, quiet=True):
    if stop == 0:
        stop = size + 1
    for n in range(size, stop):
        write_part_1(n, improve, quiet)
        write_part_2(n, improve, quiet)


write_part_2(33, manual=True)
# write_part_1(45, stop=50)

"""
Current status
Part 1: n=33, d=10 finished
Part 2: n=45 running on home machine
"""
