import random
import re
import time
import datetime
import shelve

from functools import wraps

GROUP_NAME = "机器人测试"
BOT_NAME = "韩和安"
# GROUP_NAME="青鸟市第七人民医院"
# BOT_NAME="院内自助设施"


PIXIV_IMG = './Pixiv_imgs/'
COUNTER_FILE = "call_counters.db"

TIPS = \
    f"主人你坏，我是院内的机仆，ID为{BOT_NAME}，可以代理院长完成一些自动化工作，如果我没有按照预期运行，请联系我的制造者213号模范病人。\n" \
    f"我目前支持的功能有：\n" \
    f"1.抽签，发送“@{BOT_NAME}    抽签    A选项    B选项    C选项”试一试\n" \
    f"2.大狗叫，发送“@{BOT_NAME}    大狗叫    任意一句话”，我会把这句话变成汪汪汪\n" \
    f"3.展示图图，发送“@{BOT_NAME}    我的图图呢”，会给大家来一点想看的东西\n" \
    f"4.投票，发送“@{BOT_NAME}    投票”以获取详细信息\n" \
    f"5.聊天，发送“@{BOT_NAME}    对话      对话内容”可以试试跟我聊天！\n"\
    f"拍一拍我的芯片可能有惊喜哦（）"


def be_crazy(num):
    crazy_flag = random.randint(1, num)
    if crazy_flag == 1:
        return True
    return False


####################################################################
def rate_limiter(min_interval):  # 以秒为单位，限制最短调用间隔的计时器
    def decorator(func):
        last_call = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_call
            current_time = time.time()
            elapsed = current_time - last_call
            if elapsed < min_interval:
                if be_crazy(4):
                    if be_crazy(2):
                        return f"急急急急"
                    return f"我知道你很急，但你先别急"
                return f"该功能被调用的太频繁了！\n距离上次调用仅 {elapsed:.2f} 秒 (需要等待 {min_interval} 秒"
            result = func(*args, **kwargs)
            last_call = time.time()
            return result

        return wrapper

    return decorator


def daily_limiter(max_calls):  # 一个每日调用次数限制的装饰器
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 1. 获取当前日期作为唯一的键
            today_str = datetime.date.today().isoformat()
            # 2. 使用 shelve 模块来安全地访问和修改计数器
            with shelve.open(COUNTER_FILE) as db:
                # 获取该函数今天的调用计数
                # 使用一个唯一的键来区分不同函数，如：函数名 + 日期
                func_key = f"{func.__name__}_{today_str}"

                current_calls = db.get(func_key, 0)

                # 3. 检查是否超出限制
                if current_calls >= max_calls:
                    return f"该功能今天已被调用 {current_calls} 次，已达到每日 {max_calls} 次的上限。"

                # 4. 如果未超出，则增加计数并执行函数
                db[func_key] = current_calls + 1

            # 执行原始函数
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def get_command(text):
    pattern = re.compile(rf'@{BOT_NAME} *')
    obj = pattern.match(text)
    if obj is None:
        return None
    name_to_remove = str("@" + BOT_NAME)
    if text.startswith(name_to_remove):
        command = text[len(name_to_remove):].lstrip()
        command = str(command)
        argcs = command.split()
        return argcs
