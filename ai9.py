# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 15:17
# @Author  : Breeze
# @Email   : 578450426@qq.com
# -*- coding: utf-8 -*-
# @Time    : 2020/10/9 16:48
# @Author  : Breeze
# @Email   : 578450426@qq.com
# 初始状态
import numpy as np
from queue import PriorityQueue

"""
 由于 0 是空格，因此我们在考虑状态的逆序对问题的时候，就不需要考虑 0 对逆序对数量的影响。
 也就是说我们只需要考虑：把整个3*3矩阵去掉 0 之后写成一个序列，这个序列逆序对的数量，以及两个状态的逆序对奇偶性是否相同。
 如果两个状态的奇偶性相同，则这两个状态的奇偶性相互可达；否则相互不可达。

 其次，我们再考虑移动数字对逆序对奇偶性的影响。由于 0 并不参与逆序对的统计，因此将 0 左右移动，写成的序列并不变，并不影响逆序对的数量。
 而将 0 上下移动的时候，相当于有一个数字被后移或前移了 2 位。如abcdefg八个数中，将c后移 2 位，得到序列abdecfg.
 显然，逆序对可能发生改变的部分只有cde三个数字。
 根据线性代数的知识，我们可以知道，两个相邻数字进行一次交换，逆序对的奇偶性改变；
 而上述操作可以视为c分别于d e对调一次，逆序对的奇偶性改变了两次，和原来相比相当于没有改变。

 因此，用归纳法我们可以证明：只要两个状态的序列逆序对奇偶性相同，他们就一定互相可达；否则一定互相不可达，因为交换 0 并不影响逆序对的奇偶性。
"""
goal_dic = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 0: (2, 2)
}


def GetDistance(src, dest):
    dic, d = goal_dic, 0
    for i in range(len(src)):
        for j in range(len(src[i])):
            pos = dic[src[i][j]]
            y, x = pos[0], pos[1]
            d += abs(y - i) + abs(x - j)
    return d


def calDistance(node, w):
    dis = 0
    for i in range(len(node)):
        if node[i] == 0:
            continue
        dis += abs(i // w - (node[i] - 1) // w) + abs(i % w - (node[i] - 1) % w)
    return 0


# A*算法寻找初始状态到目标状态的路径
def AStar(init, goal):
    # 边缘队列初始已有源状态节点
    size = int(9 ** 0.5)
    start = tuple(init)
    process = list([])
    target = tuple(goal)

    # 优先队列，值越小，优先级越高
    pQueue = PriorityQueue()
    pQueue.put([0 + calDistance(start, size), start, start.index(0), 0, process])

    seen = {start}  # 已遍历过的结点

    while not pQueue.empty():
        _pri, board, pos0, depth, process = pQueue.get()

        if board == target:
            return depth, process
        for d in (-1, 1, -size, size):  # 对应的是左右上下的相邻结点
            nei = pos0 + d
            if abs(nei // size - pos0 // size) + abs(nei % size - pos0 % size) != 1:
                continue
            if 0 <= nei < size ** 2:  # 符合边界条件的相邻结点
                newboard = list(board)
                newboard[pos0], newboard[nei] = newboard[nei], newboard[pos0]
                newt = tuple(newboard)
                if newt not in seen:  # 没有被遍历过的状态
                    seen.add(newt)
                    # pQueue.put([depth + 1 + 2 * self.calDistance(newt), newt, nei, depth + 1, process + [d]])
                    pQueue.put(
                        [depth + 1 + 0.9 * calDistance(newt, size), newt, nei, depth + 1,
                         process + [d]])  # 调整启发函数的权重可以缩短时间但增加步数


def InversionNum(lst):
    # 改写归并排序,在归并排序中，每当R部分元素先于L部分元素插入原列表时，逆序对数要加L剩余元素数
    if len(lst) == 1:
        return lst, 0
    else:
        n = len(lst) // 2
        lst1, count1 = InversionNum(lst[0:n])
        lst2, count2 = InversionNum(lst[n:len(lst)])
        lst, count = Count(lst1, lst2, 0)
        return lst, count1 + count2 + count


def Count(lst1, lst2, count):
    i = 0
    j = 0
    res = []
    while i < len(lst1) and j < len(lst2):
        if lst1[i] <= lst2[j]:
            res.append(lst1[i])
            i += 1
        else:
            res.append(lst2[j])
            count += len(lst1) - i  # 当右半部分的元素先于左半部分元素进入有序列表时，逆序对数量增加左半部分剩余的元素数
            j += 1
    res += lst1[i:]
    res += lst2[j:]
    return res, count


def swapit(process, state, toswap):
    zero = state.index(0)
    for i in process:
        temp = state[zero + i]
        state[zero + i] = 0
        state[zero] = temp
        zero += i
    t = state[toswap[0]]
    state[toswap[0]] = state[toswap[1]]
    state[toswap[1]] = t
    res = [i for i in state]
    return res


def mapped(sequel):
    se = [str(i) for i in sequel]
    mmap = dict(zip(["-3", "-1", "3", "1"], ['MoveUp', 'MoveLeft', 'MoveDown', 'MoveRight']))
    res = [mmap[i] for i in se]
    return res


def ai(initState, goalState, swap, step):
    global goal_state
    global init_state
    seq = ""
    init_state = list(np.array(initState).reshape(9).tolist())
    goal_state = list(np.array(goalState).reshape(9).tolist())
    print(init_state, goal_state)
    init_ = list(np.array(init_state).reshape(9).tolist())
    goal_ = list(np.array(goal_state).reshape(9).tolist())
    init_.remove(0)
    goal_.remove(0)
    _, init_IN = InversionNum(init_)
    _, goal_IN = InversionNum(goal_)
    if init_IN % 2 != goal_IN % 2:
        print("初始序列无解")
        zero = init_state.index(0)
        if step % 2 == 0:
            if (zero % 3) != 0:
                for i in range(int(step / 2)):
                    seq = seq + "ad"
            else:
                for i in range(int(step / 2)):
                    seq = seq + "da"
        else:
            if (zero % 3) != 0:
                t = init_state[zero - 1]
                init_state[zero - 1] = init_state[zero]
                init_state[zero] = t
                for i in range(int(step / 2)):
                    seq = seq + "ad"
                seq = seq + "a"
            else:
                t = init_state[zero + 1]
                init_state[zero + 1] = init_state[zero]
                init_state[zero] = t
                for i in range(int(step / 2)):
                    seq = seq + "da"
                seq = seq + "d"
        print("提前进入强制交换")
        temp = list(np.array(init_state).reshape(9).tolist())
        t = temp[swap[0]]
        temp[swap[0]] = temp[swap[1]]
        temp[swap[1]] = t
        print("After being swapped:", temp)
        ti = [i for i in temp]
        ti.remove(0)
        _, temp_IN = InversionNum(ti)
        print("(ai)temp_IN:", temp_IN)
        if temp_IN % 2 != goal_IN % 2:
            print("强制交换后无解，进入手动交换")
            print("ATTENTION")
            init_state = temp
            swappededState, swappedPos = finestSwap(init_state)
            swappededState = list(np.array(swappededState).reshape(9).tolist())
            print(swappededState, swappedPos)
            _, process = AStar(swappededState, goal_state)
            # swappedPos[0] += 1
            # swappedPos[1] += 1
            return mapped(process), swappedPos, seq
        print("强制交换后有解，搜索中：")
        init_state = temp
        _, process = AStar(init_state, goal_state)
        swap = [-1, -1]
        return mapped(process), swap, seq

    else:
        print("初始序列有解：")
        _, process = AStar(init_state, goal_state)
        if len(process) >= step:
            print("步数到了，强制交换")
            process = process[:step]
            swappedState = swapit(process, init_state, swap)
            print(swappedState)

            # _, reprocess = AStar(swappedState, goal_state)
            # process = process + reprocess
            # swappedState = swapit(process, init_state, swap)
            print("swapped:", swappedState)
            swapped_t = [i for i in swappedState]
            swapped_t.remove(0)
            _, _t = InversionNum(swapped_t)
            print(_t)
            if _t % 2 != 0:
                print("强制交换后无解")
                print("进入手动交换：")

                swappededState, swappedPos = finestSwap(swappedState)
                swappededState = list(np.array(swappededState).reshape(9).tolist())

                _, reprocess = AStar(swappededState, goal_state)
                process = process + reprocess
                # swappedPos[0] += 1
                # swappedPos[1] += 1
                return mapped(process), swappedPos, seq
            else:
                print("强制交换后有解")
                _, reprocess = AStar(swappedState, goal_state)
                process = process + reprocess
                swap = [-1, -1]
                return mapped(process), swap, seq


def finestSwap(state):
    """

    :param state:3*3 无解状态数组
    :return: 3*3 根据启发值选取最优
    """
    init_ = list(np.array(state).reshape(9).tolist())
    toswap = []
    cur = 0
    while cur < 8:
        if init_[cur] != 0 and init_[cur + 1] != 0:
            toswap.append([cur, cur + 1])
        cur += 1
    # print(toswap)
    swappedState = []
    for item in toswap:
        temp = [i for i in init_]
        t = temp[item[0]]
        temp[item[0]] = temp[item[1]]
        temp[item[1]] = t
        swappedState.append(list(np.array(temp).reshape(3, 3).tolist()))
    # print(swappedState)
    dele = [[2, 3], [3, 2], [5, 6], [6, 5], []]
    for i in swappedState:
        if i == [2, 3] or i == [3, 2] or i == [5, 6] or i == [6, 5]:
            swappedState.remove(i)
    distances = []
    for swapped in swappedState:
        distances.append(GetDistance(swapped, goal_state))
    res = swappedState[distances.index(min(distances))]
    return res, toswap[distances.index(min(distances))]


if __name__ == '__main__':
    # mmap = dict(zip(['MoveUp', 'MoveLeft', 'MoveDown', 'MoveRight'], ['w', 'a', 's', 'd']))
    # res = [mmap[i] for i in _main()]
    # print(res)
    process, _ = ai([0, 7, 4, 1, 8, 6, 2, 5, 3], [1, 2, 3, 4, 0, 5, 6, 7, 8], [0, 1], 19)
    mmap = dict(zip(['MoveUp', 'MoveLeft', 'MoveDown', 'MoveRight'], ['w', 'a', 's', 'd']))
    res = [mmap[i] for i in process]
    print(res)
    print(_)
