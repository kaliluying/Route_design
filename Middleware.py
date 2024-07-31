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

# 弧线起始对象
arc_start_obj = None

# 弧线终止对象
arc_end_obj = None

# 弧线列表
arc_list = []

# 矩形中心
rect_center = []


def set_rect_center(center):
    """
    设置矩形中心
    :param center:
    :return:
    """
    global rect_center
    rect_center.clear()
    for i in center:
        rect_center.append(i)


def get_rect_center():
    """
    获取矩形中心
    :return:
    """
    return rect_center


def set_arc_list(arc_list_):
    """
    设置弧线列表
    :param arc_list_:
    :return:
    """
    global arc_list
    arc_list = arc_list_


def get_arc_list():
    """
    获取弧线列表
    :return:
    """
    return arc_list


def set_arc_start_obj(obj):
    """
    设置弧线的起始对象
    :param obj:
    :return:
    """
    global arc_start_obj
    arc_start_obj = obj


def get_arc_start_obj():
    """
    获取弧线的起始对象
    :return:
    """
    return arc_start_obj


def get_arc_end_obj():
    """
    获取弧线的终止对象
    :return:
    """
    return arc_end_obj


def set_arc_end_obj(obj):
    """
    设置弧线的终止对象
    :param obj:
    :return:
    """
    global arc_end_obj
    arc_end_obj = obj


def set_arc_start(start):
    """
    设置弧线的起始点
    :param start:
    :return:
    """
    global arc_start
    arc_start = start


def get_arc_start():
    """
    获取弧线的起始点
    :return:
    """
    return arc_start


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
