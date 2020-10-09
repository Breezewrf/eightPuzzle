# -*- coding: utf-8 -*-
# @Time    : 2020/10/9 16:48
# @Author  : Breeze
# @Email   : 578450426@qq.com
# 初始状态
import numpy as np
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
init_state = [
    [7, 5, 4],
    [6, 1, 0],
    [2, 3, 8]
]
# 目标状态
goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]
# 目标状态 值-位置表
goal_dic = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 0: (2, 2)
}


# 输出状态
def PrintState(state):
    for i in state: print(i)


# 复制状态
def CopyState(state):
    s = []
    for i in state: s.append(i[:])
    return s


# 获取空格的位置
def GetSpace(state):
    for y in range(len(state)):
        for x in range(len(state[y])):
            if state[y][x] == 0: return y, x


# 获取空格上移后的状态，不改变原状态
def MoveUp(state):
    s = CopyState(state)
    y, x = GetSpace(s)
    s[y][x], s[y - 1][x] = s[y - 1][x], s[y][x]
    return s


# 获取空格下移后的状态，不改变原状态
def MoveDown(state):
    s = CopyState(state)
    y, x = GetSpace(s)
    s[y][x], s[y + 1][x] = s[y + 1][x], s[y][x]
    return s


# 获取空格左移后的状态，不改变原状态
def MoveLeft(state):
    s = CopyState(state)
    y, x = GetSpace(s)
    s[y][x], s[y][x - 1] = s[y][x - 1], s[y][x]
    return s


# 获取空格右移后的状态，不改变原状态
def MoveRight(state):
    s = CopyState(state)
    y, x = GetSpace(s)
    s[y][x], s[y][x + 1] = s[y][x + 1], s[y][x]
    return s


# 获取两个状态之间的启发距离
def GetDistance(src, dest):
    dic, d = goal_dic, 0
    for i in range(len(src)):
        for j in range(len(src[i])):
            pos = dic[src[i][j]]
            y, x = pos[0], pos[1]
            d += abs(y - i) + abs(x - j)
    return d


# 获取指定状态下的操作
def GetActions(state):
    acts = []
    y, x = GetSpace(state)
    if x > 0: acts.append(MoveLeft)
    if y > 0: acts.append(MoveUp)
    if x < len(state[0]) - 1: acts.append(MoveRight)
    if y < len(state[0]) - 1: acts.append(MoveDown)
    return acts


# 用于统一操作序列的函数
def Start(state):
    return


# 边缘队列中的节点类
class Node:
    state = None  # 状态
    value = -1  # 启发值
    step = 0  # 初始状态到当前状态的距离（步数）
    action = Start  # 到达此节点所进行的操作
    parent = None,  # 父节点

    # 用状态和步数构造节点对象
    def __init__(self, state, step, action, parent):
        self.state = state
        self.step = step
        self.action = action
        self.parent = parent
        # 计算估计距离
        self.value = GetDistance(state, goal_state) + step


# 获取拥有最小启发值的元素索引
def GetMinIndex(queue):
    index = 0
    for i in range(len(queue)):
        node = queue[i]
        if node.value < queue[index].value:
            index = i
    return index


# 将状态转换为整数
def toInt(state):
    value = 0
    for i in state:
        for j in i:
            value = value * 10 + j
    return value


# A*算法寻找初始状态到目标状态的路径
def AStar(init, goal):
    # 边缘队列初始已有源状态节点
    queue = [Node(init, 0, Start, None)]
    visit = {}  # 访问过的状态表
    count = 0  # 循环次数
    # 队列没有元素则查找失败
    while queue:
        # 获取拥有最小估计距离的节点索引
        index = GetMinIndex(queue)
        node = queue[index]
        visit[toInt(node.state)] = True
        count += 1
        if node.state == goal:
            return node, count
        del queue[index]
        # 扩展当前节点
        for act in GetActions(node.state):
            # 获取此操作下到达的状态节点并将其加入边缘队列中
            near = Node(act(node.state), node.step + 1, act, node)
            if toInt(near.state) not in visit:
                queue.append(near)
    return None, count


# 将链表倒序，返回链头和链尾
def reverse(node):
    if node.parent == None:
        return node, node
    head, rear = reverse(node.parent)
    rear.parent, node.parent = node, None
    return head, node


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


if __name__ == '__main__':
    # init_state.remove(0)
    init_ = list(np.array(init_state).reshape(9).tolist())
    goal_ = list(np.array(goal_state).reshape(9).tolist())
    # goal_ = goal_.remove(0)
    init_.remove(0)
    goal_.remove(0)
    print(init_, goal_)
    _, init_IN = InversionNum(init_)
    _, goal_IN = InversionNum(goal_)
    print(init_IN, goal_IN)
    if init_IN % 2 != goal_IN % 2:
        print("无解")
        exit()
    node, count = AStar(init_state, goal_state)
    if node is None:
        print("无法从初始状态到达目标状态！")
    else:
        print("搜索成功，循环次数：", count)
        node, rear = reverse(node)
        count = 0
        while node:
            # 启发值包括从起点到此节点的距离
            print("第", count + 1, "步：", node.action.__name__, "启发值为：", count, "+", node.value - count)
            PrintState(node.state)
            node = node.parent
            count += 1
