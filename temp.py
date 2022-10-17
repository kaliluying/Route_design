def oxer_a(self, x1, x2, x3, ent_a, obj, obstacle):
    """
    选中A障碍是否为双横木
    :param x1: a障碍是否为双横木
    :param x2: b障碍是否为双横木
    :param x3: c障碍是否为双横木
    :param ent_a: 输入框
    :param obj: 组件对像
    :param obstacle: ab组合还是abc
    :return:
    """
    self.oxer(x1, ent_a)
    if obstacle == "combination_abc":
        self.judge_abc(x1, x2, x3, obj)
    if x1.get() == '1':
        try:
            if x2.get() == '1':
                if obstacle == "combination_abc":
                    if x3.get() == '1':
                        self.combination_abc(obj, m1=5, m2=10, m3=5, m4=10, m5=5)
                        return
                    elif x3.get() == '0':
                        self.combination_abc(obj, m1=5, m2=10, m3=5, m4=10, m5=0)
                        return
                else:
                    self.com(obj)
            elif x2.get() == '0':
                if obstacle == "combination_abc":
                    if x3.get() == '1':
                        self.combination_abc(obj, m1=5, m2=10, m4=10, m5=5)
                        return
                    elif x3.get() == '0':
                        self.combination_abc(obj, m1=5, m2=10, m4=10)
                        return
                else:
                    obj.img_path = merge(5, m1=20)
                    obj.img = Image.open(obj.img_path)
                    obj.pic_with_win_auto_size()
        except:
            pass

    elif x1.get() == '0':
        try:
            if x2.get() == '1':
                if obstacle == "combination_abc":
                    if x3.get() == '1':
                        self.combination_abc(obj, m2=10, m3=5, m4=10, m5=5)
                        return
                    elif x3.get() == '0':
                        self.combination_abc(obj, m2=10, m3=5, m4=10)
                        return
                else:
                    obj.img_path = merge(20, m1=5)
                    obj.img = Image.open(obj.img_path)
                    obj.pic_with_win_auto_size()
                    return
            elif x2.get() == '0':
                if obstacle == "combination_abc":
                    if x3.get() == '1':
                        self.combination_abc(obj, m2=10, m4=10, m5=5)
                        return
                    elif x3.get() == '0':
                        self.combination_abc(obj, m2=10, m4=10)
                        return
                else:
                    obj.img_path = merge(10)
                    obj.img = Image.open(obj.img_path)
                    obj.pic_with_win_auto_size()
                    return
        except:
            pass


def oxer_b(self, x1, x2, x3, ent_b, obj, obstacle):
    """
    选中B障碍是否为双横木
    :param x1:
    :param x2:
    :param x3:
    :param ent_b:
    :param obj:
    :return:
    """
    if x2.get() == '1':
        ent_b.config(state='normal')
        try:
            if x1.get() == '1':
                if x3.get() == '1':
                    pass
                elif x3.get() == '0':
                    self.com(obj)
                    return
            elif x1.get() == '0':
                if x3.get() == '1':
                    pass
                elif x3.get() == '0':
                    pass
        except:
            pass
        obj.img_path = merge(20, m1=5)
        obj.img = Image.open(obj.img_path)
        obj.pic_with_win_auto_size()
    elif x2.get() == '0':
        ent_b.config(state='disabled')
        try:
            if x1.get() == '1':
                if x3.get() == '1':
                    pass
                elif x3.get() == '0':
                    obj.img_path = merge(5, m1=20)
                    obj.img = Image.open(obj.img_path)
                    obj.pic_with_win_auto_size()
                    return
            elif x1.get() == '0':
                if x3.get() == '1':
                    pass
                elif x3.get() == '0':
                    obj.img_path = merge(10)
                    obj.img = Image.open(obj.img_path)
                    obj.pic_with_win_auto_size()
                    return
        except:
            pass


def oxer_c(self, x1, x2, x3, ent_c, obj, obstacle):
    if x3.get() == '1':
        ent_c.config(state='normal')
        try:
            if x1.get() == '1':
                if x2.get() == '1':
                    pass
                elif x2.get() == '0':
                    self.com(obj)
                    return
            elif x1.get() == '0':
                if x2.get() == '1':
                    pass
                elif x2.get() == '0':
                    pass
        except:
            pass
        obj.img_path = merge(20, m1=5)
        obj.img = Image.open(obj.img_path)
        obj.pic_with_win_auto_size()
    elif x3.get() == '0':
        ent_c.config(state='disabled')
        try:
            if x1.get() == '1':
                if x2.get() == '1':
                    pass
                elif x2.get() == '0':
                    obj.img_path = merge(5, m1=20)
                    obj.img = Image.open(obj.img_path)
                    obj.pic_with_win_auto_size()
                    return
            elif x1.get() == '0':
                if x2.get() == '1':
                    pass
                elif x2.get() == '0':
                    obj.img_path = merge(10)
                    obj.img = Image.open(obj.img_path)
                    obj.pic_with_win_auto_size()
                    return
        except:
            pass


def com(self, obj):
    """
    当两个都是双横木
    :param obj:
    :return:
    """
    obj.img_path = combination(5, 15, 5)
    obj.img = Image.open(obj.img_path)
    obj.pic_with_win_auto_size()


def combination_abc(self, obj, m1=0, m2=0, m3=0, m4=0, m5=0):
    obj.img_path = com_abc(m1, m2, m3, m4, m5)
    obj.img = Image.open(obj.img_path)
    obj.pic_with_win_auto_size()


def judge_abc(self, x1, x2, x3, obj):
    if x1.get() == '1':
        try:
            if x2.get() == '1':
                if x3.get() == '1':
                    self.combination_abc(obj, m1=5, m2=10, m3=5, m4=10, m5=5)
                    return
                elif x3.get() == '0':
                    self.combination_abc(obj, m1=5, m2=10, m3=5, m4=10, m5=0)
                    return
            elif x2.get() == '0':
                if x3.get() == '1':
                    self.combination_abc(obj, m1=5, m2=10, m4=10, m5=5)
                    return
                elif x3.get() == '0':
                    self.combination_abc(obj, m1=5, m2=10, m4=10)
                    return

        except:
            pass

    elif x1.get() == '0':
        try:
            if x2.get() == '1':
                if x3.get() == '1':
                    self.combination_abc(obj, m2=10, m3=5, m4=10, m5=5)
                    return
                elif x3.get() == '0':
                    self.combination_abc(obj, m2=10, m3=5, m4=10)
                    return
            elif x2.get() == '0':
                if x3.get() == '1':
                    self.combination_abc(obj, m2=10, m4=10, m5=5)
                    return
                elif x3.get() == '0':
                    self.combination_abc(obj, m2=10, m4=10)
                    return
        except:
            pass