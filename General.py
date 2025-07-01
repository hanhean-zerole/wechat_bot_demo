import random

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
