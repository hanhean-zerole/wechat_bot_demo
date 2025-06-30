import time
import re
import regex
import random
from wxauto import WeChat
from wxauto.msgs import FriendMessage,TickleMessage
#GROUP_NAME="青鸟市第七人民医院"
BOT_NAME="院内自助设施"
GROUP_NAME="机器人测试"
# BOT_NAME="韩和安"

def get_at(text):
    pattern = re.compile(rf'@{BOT_NAME} *')
    obj=pattern.match(text)
    if obj is None:
        return None
    to_remove = str("@"+BOT_NAME)
    if text.startswith(to_remove):
        command=text[len(to_remove):].lstrip()
    print(command)
    return command

def command_process(text):
    text=str(text)
    argcs=text.split()
    print(text)
    print(argcs)
    if argcs[0]=="抽签":
        ans=chouqian(argcs)
    elif argcs[0] == "帮助":
        ans = help()
    elif argcs[0] == "大狗叫":
        ans = bark(argcs)
    else:
        ans = f"病友你坏，如果你不知道怎么使用我，可以发送“@{BOT_NAME} 帮助”"
    return ans


def help():
    return f"病友你坏，我是院内的自动机器人，ID为{BOT_NAME}，可以代理院长完成一些自动化工作，如果我没有按照预期运行，请联系院长或213号模范病人。\n" \
           f"我目前支持的功能有：\n" \
           f"1.抽签，发送“@{BOT_NAME} 抽签 A选项 B选项 C选项”试一试\n" \
           f"2.大狗叫，发送“@{BOT_NAME} 大狗叫 任意一句话”，我会把这句话变成汪汪汪\n" \
           f"拍一拍我的芯片可能有惊喜哦（）"


def chouqian(options):
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
    return ans

def IQ(msg):
    upIQ=random.randint(1,6)
    match = re.search(r'"([^"]*)" 拍了拍我的芯片，智慧\+1d6', msg.content)
    print(match)
    # match = re.search(r'"([^"]*)" 拍了拍我.*', msg.content)
    user = match.group(1)
    flag = random.randint(1, 10)
    if flag == 1:
        return {"text": f"在拍芯片时用力过猛，被电到了，智慧-{upIQ}", "user": user, "flag": True}
    return {"text": f"1d6={upIQ},智慧＋{upIQ}", "user": user, "flag": False}

def test_group_message(msg, chat):
    attr_list =["friend","tickle","system"]
    if msg.attr not in attr_list:
        return
    if isinstance(msg,TickleMessage):#拍一拍加智慧
        ret = IQ(msg)
        time.sleep(0.7)
        print(ret['text'])
        chat.SendMsg(msg=ret['text'], who=GROUP_NAME, at=ret['user'])
        if ret['flag']:
            sleeptime = random.randint(1, 3)
            chat.SendMsg(msg=f"芯片损坏，需要检修{sleeptime}分钟", who=GROUP_NAME)
            time.sleep(sleeptime*60)
############################################################################
    if isinstance(msg, FriendMessage):
        ans = get_at(msg.content)
        if ans is None:
            return
        print(ans)
        ret=command_process(ans)
        time.sleep(0.7)
        msg.quote(ret, msg.sender)

if __name__ == '__main__':
    wx = WeChat()
    wx.AddListenChat(nickname=GROUP_NAME, callback=test_group_message)
    wx.KeepRunning()

