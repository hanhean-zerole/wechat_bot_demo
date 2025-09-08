import os
import random
import re
import regex


from General import GROUP_NAME, BOT_NAME, PIXIV_IMG, be_crazy, rate_limiter, daily_limiter, TIPS


def help():
    if be_crazy(5):
        return f"你这有机体好笨( ˃ ⤙ ˂)"
    return TIPS


def chouqian(options):
    if be_crazy(10):
        return f"抽签结果：钝角"
    if len(options)>1:
        choose = random.choice(options[1:])
        return "抽签结果：" + choose
    return "抽签失败，请检查格式是否正确。正确格式实例：" + "抽签 A选项 B选项 C选项"


def bark(strs):
    nums = len(strs)-1
    if nums <= 0:
        return "狗狗沉默……"
    ans = ""
    for i in range(nums):
        pattern = regex.compile(r'[^\p{P}\s]', regex.UNICODE)
        result = pattern.sub('汪', strs[i+1])
        ans += result
        ans += ' '
    if be_crazy(10):
        return f"狗狗不是很想叫……"
    return ans


def IQ(msg):
    upIQ=random.randint(1,6)
    match = re.search(r'"([^"]*)" 拍了拍 "院内自助设施" 的芯片，智慧\+1d6', msg.content)
    user = match.group(1)
    if be_crazy(10):
        return {"text": f"在拍芯片时用力过猛，被电到了，智慧-{upIQ}", "user": user, "flag": True}
    return {"text": f"1d6={upIQ},智慧＋{upIQ}", "user": user, "flag": False}

@rate_limiter(5)
@daily_limiter(220)
def llm_chating(llmchat, content, sender):
    str_without_tail = "{用户名:"+sender+";用户发言:"+content+";"
    response = llmchat.get_llm_response(str_without_tail)
    return response

def invited_person(text):
    """
    从邀请相关的文本中提取"被邀请人"的ID
        str: "被邀请人"对应的ID
    """
    pattern = r'"(.*?)".*?"(.*?)"'
    matches = re.findall(pattern, text)
    if not matches:
        raise ValueError("无法从文本中提取邀请信息")
    if "邀请" in text and "加入" in text:
        return matches[0][1]
    elif "通过扫描" in text:
        return matches[0][0]
    else:
        raise ValueError("未知的邀请信息格式")


@rate_limiter(60)
def show_Pixiv(wxchat):
        files = []
        for dirpath, _, filenames in os.walk(PIXIV_IMG):
            for filename in filenames:
                files.append(os.path.join(dirpath, filename))
        # 如果没有找到文件
        if not files:
            print(f"警告: 目录 '{PIXIV_IMG}' 中没有找到任何文件")
            return "今日库存还没有补充，以后再来探索吧~"
        # 随机选择一个文件
        file = random.choice(files)
        id = re.search('([0-9]+)\.(jpg|png)', file).group(1)
        wxchat.SendFiles(filepath=file, who=GROUP_NAME)
        os.remove(file)
        return f"pid={id}"



