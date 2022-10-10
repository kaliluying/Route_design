from PIL import Image, ImageOps

# 行进方向
direction_image = "img/direction.png"
# 单横木
one_path = 'img/one.png'
# 组合障碍
com_image = "img/com.png"


# 检测字符串中是否是数字，支持正负整数，小数，中文数字如：一
def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        unicodedata.numeric(s)  # 把一个表示数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
    return False


# 合并图片
def merge(m, m1=0):
    img_obj = Image.open(one_path)
    img_obj2 = Image.open(one_path)
    result = Image.new(img_obj.mode, (m + m1 + 10, 40))
    result.paste(img_obj, box=(0, 0))
    result.paste(img_obj2, box=(m + m1, 0))
    if m1:
        image3 = Image.open(one_path)
        result.paste(image3, box=(m, 0))
        result.save("img/com2.png")
        com_image = "img/com2.png"
        return com_image
    com_image = "img/com.png"
    result.save(com_image)
    return com_image


# 图片扩展
def expand(path):
    img = Image.open(path)
    w, h = img.size
    l = r = t = b = 0
    if w < h:
        var_ex = h - w
        l = var_ex // 2
        r = var_ex - l
    elif w > h:
        var_ex = w - h
        t = var_ex // 2
        b = var_ex - t

    left_pad = l
    top_pad = t
    right_pad = r
    bottom_pad = b

    padding = (left_pad, top_pad, right_pad, bottom_pad)
    img2 = ImageOps.expand(img, padding, fill=(236, 236, 236, 0))
    image_path = path.replace('.', '-exp.')
    img2.save(image_path)
    return image_path


# 添加行进方向
def start_direction(image_path):
    img1 = Image.open(image_path)
    w, h = img1.size
    img2 = Image.open(direction_image)
    w1, h1 = img2.size
    img2 = img2.resize((w, h1))
    r, g, b, alpha = img2.split()
    img1.paste(img2, (0, h // 2 - 5), alpha)
    image_path = image_path.replace('.', '-dir.')
    img1.save(image_path)
    return image_path
