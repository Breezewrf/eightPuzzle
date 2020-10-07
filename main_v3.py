import random
import simpleguitk as simplegui

# 1.设置图像,载入图像
baymax = simplegui.load_image(
    './imgsSrc/c_.jpg')

# 设置画布尺寸
w = 600
h = w + 100

# 定义图像块的边长
image_size = w / 3

# 定义图像块坐标列表
all_coordinates = [[image_size * 0.5, image_size * 0.5], [image_size * 1.5, image_size * 0.5],
                   [image_size * 2.5, image_size * 0.5], [image_size * 0.5, image_size * 1.5],
                   [image_size * 1.5, image_size * 1.5], [image_size * 2.5, image_size * 1.5],
                   [image_size * 0.5, image_size * 2.5], [image_size * 1.5, image_size * 2.5], None
                   ]

# 棋盘的行列
row = 3
col = 3

# 定义步数
steps = 0

# 保存所有图像块的列表
board = [[None, None, None], [None, None, None], [None, None, None]]


# 定义一个图像块的类
class Square:
    # 定义一个构造函数，用于初始化
    def __init__(self, coordinate):
        self.center = coordinate

    # 绘制图像的方法
    def draw(self, canvas, board_pos):
        canvas.draw_image(baymax, self.center, [image_size, image_size],
                          [(board_pos[1] + 0.5) * image_size, (board_pos[0] + 0.5) * image_size],
                          [image_size, image_size])
        # print([image_size, image_size])
        # print((board_pos[1] + 0.5) * image_size)


# 定义一个方法进行拼接
def init_board():
    random.shuffle(all_coordinates)  # 打乱图像
    # 填充并且拼接图版
    for i in range(row):
        for j in range(col):
            idx = i * row + j
            squar_center = all_coordinates[idx]
            # 如果坐标值是空的，让该框为空
            if squar_center is None:
                board[i][j] = None
            else:
                board[i][j] = Square(squar_center)


def play_game():
    global steps
    steps = 0
    init_board()


def draw(canvas):  # 画步数
    canvas.draw_image(baymax, [w / 2, h / 2], [w, h], [50, w + 50], [98, 98])
    canvas.draw_text('Steps：' + str(steps), [400, 680], 22, 'black')  # 64分钟
    # 绘制游戏界面各元素
    for i in range(row):
        for j in range(col):
            if board[i][j] is not None:
                board[i][j].draw(canvas, [i, j])


def mouseclick(pos):
    global steps
    # 将点击的位置换算成拼接板上的坐标
    r = int(pos[1] / image_size)
    c = int(pos[0] / image_size)
    if r < 3 and c < 3:
        if board[r][c] is None:  # 表示点击的是一个空白位置
            return
        else:
            # 检查上下左右是否有空位置，有则移动过去
            current_square = board[r][c]
            if r - 1 >= 0 and board[r - 1][c] is None:  # 判断上面
                board[r][c] = None
                board[r - 1][c] = current_square
                steps += 1
            elif c + 1 <= 2 and board[r][c + 1] is None:  # 判断右边
                board[r][c] = None
                board[r][c + 1] = current_square
                steps += 1
            elif r + 1 <= 2 and board[r + 1][c] is None:  # 判断下边
                board[r][c] = None
                board[r + 1][c] = current_square
                steps += 1
            elif c - 1 >= 0 and board[r][c - 1] is None:  # 判断左边
                board[r][c] = None
                board[r][c - 1] = current_square
                steps += 1


if __name__ == '__main__':
    frame = simplegui.create_frame("数字华容道pro", w, h)
    frame.set_canvas_background('White')
    frame.set_draw_handler(draw)
    frame.add_button('Replay', play_game, 60)
    frame.set_mouseclick_handler(mouseclick)
    play_game()
    frame.start()
