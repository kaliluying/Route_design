# 当前标签
current_tag = None
# 线段标签
line_tag = None
# 当前多选框状态
current_frame_stare = True
# 利物浦状态
live_state = 0
# 全局障碍长度
bar_len = 4

# 当前障碍对象
current_obstacle = None

# 记录弧线的起始点
arc_start = None

# 记录弧线的终止点
arc_end = None


def set_arc_start(start):
    """
    设置弧线的起始点
    :param start:
    :return:
    """
    global arc_start
    arc_start = start


def set_arc_end(end):
    """
    设置弧线的终止点
    :param end:
    :return:
    """
    global arc_end
    arc_end = end


def get_arc_center():
    """
    获取弧线的中心点
    :return:
    """
    x1, y1 = arc_start
    x2, y2 = arc_end
    x3 = (x1 + x2) / 2
    y3 = (y1 + y2) / 2
    return x3, y3


def get_arc_start():
    """
    获取弧线的起始点
    :return:
    """
    return arc_start


def get_arc_end():
    """
    获取弧线的终止点
    :return:
    """
    return arc_end


def set_obstacle(obstacle):
    """
    设置障碍对象
    :param obstacle:
    :return:
    """
    global current_obstacle
    current_obstacle = obstacle


def get_obstacle():
    """
    获取障碍对象
    :return:
    """
    return current_obstacle


def set_cur(cur):
    """
    设置障碍tag
    :param cur:
    :return:
    """
    global current_tag
    current_tag = cur


def set_line(line):
    """
    设置辅助线tag
    :param line:
    :return:
    """
    global line_tag
    line_tag = line


def get_cur():
    """
    获取障碍tag和辅助线tag
    :return:
    """
    return current_tag, line_tag


def set_frame_stare(frame_stare):
    """
    设置多选框状态
    :param frame_stare:
    :return:
    """
    global current_frame_stare
    current_frame_stare = frame_stare


def get_frame_stare():
    """
    获取多选框状态
    :return:
    """
    return current_frame_stare


def set_live(state):
    """
    设置利物浦是否为双横木
    :param state:
    :return:
    """
    global live_state
    live_state = state


def get_live():
    """
    利物浦是否为双横木
    :return:
    """
    return live_state


def set_len(len):
    """
    设置全局障碍长度
    :param len:
    :return:
    """
    global bar_len
    try:
        bar_len = float(len.get())
    except:
        bar_len = float(len)


def get_len():
    """
    获取全局障碍长度
    :return:
    """
    return bar_len
