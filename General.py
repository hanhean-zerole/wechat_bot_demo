import random
import re
import time
from functools import wraps

GROUP_NAME= "机器人测试"
BOT_NAME="韩和安"
#GROUP_NAME="青鸟市第七人民医院"
#BOT_NAME="院内自助设施"


PIXIV_IMG = './Pixiv_imgs/'


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


def get_command(text):
    pattern = re.compile(rf'@{BOT_NAME} *')
    obj=pattern.match(text)
    if obj is None:
        return None
    name_to_remove = str("@" + BOT_NAME)
    if text.startswith(name_to_remove):
        command=text[len(name_to_remove):].lstrip()
        command = str(command)
        argcs = command.split()
        return argcs
