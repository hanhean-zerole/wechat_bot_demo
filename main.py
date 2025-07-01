import threading
import time
import re
import random
import schedule
import normal_tools as nmtools
from wxauto import WeChat
from wxauto.msgs import FriendMessage, TickleMessage, SystemMessage

from General import GROUP_NAME, BOT_NAME, be_crazy
from get_pixiv import download_pixiv_recommend

###########################################################################设置定时任务
schedule.every().day.at("04:00").do(download_pixiv_recommend)


###########################################################################
def run_scheduler():
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print(f"Scheduler error: {e}", exc_info=True)
        time.sleep(1)

def get_command(text):
    pattern = re.compile(rf'@{BOT_NAME} *')
    obj=pattern.match(text)
    if obj is None:
        return None
    to_remove = str("@" + BOT_NAME)
    if text.startswith(to_remove):
        command=text[len(to_remove):].lstrip()
        return command


def command_process(text, chat):
    text=str(text)
    argcs=text.split()
    print(argcs)
    if argcs[0]=="抽签":
        ans= nmtools.chouqian(argcs)
    elif argcs[0] == "帮助":
        ans = help()
    elif argcs[0] == "大狗叫":
        ans = nmtools.bark(argcs)
    elif argcs[0] == "我的图图呢":
        ans = nmtools.show_Pixiv(chat)
    else:
        ans = f"病友你坏，如果你不知道怎么使用我，可以发送“@{BOT_NAME} 帮助”"
    return ans


def test_group_message(msg, chat):
    attr_list =["friend","tickle","system"]
    if msg.attr not in attr_list:
        return
    ##################################################################
    if isinstance(msg,TickleMessage):#拍一拍加智慧
        ret = nmtools.IQ(msg)
        time.sleep(0.7)
        if be_crazy(20):
            chat.SendMsg(msg="讨厌你，你不要碰我（▼へ▼メ）", who=GROUP_NAME, at=ret['user'])
            return
        chat.SendMsg(msg=ret['text'], who=GROUP_NAME, at=ret['user'])
        if ret['flag']:
            sleeptime = random.randint(1, 3)
            chat.SendMsg(msg=f"芯片损坏，需要检修{sleeptime}分钟", who=GROUP_NAME)
            time.sleep(sleeptime*60)
############################################################################
    if isinstance(msg, FriendMessage):
        ans = get_command(msg.content)
        if ans is None:
            return
        ret=command_process(ans,chat)
        time.sleep(0.7)
        msg.quote(ret, msg.sender)
############################################################################
    if isinstance(msg, SystemMessage):
        user = nmtools.invited_person(msg.content)
        if be_crazy(5):
            chat.SendMsg(msg=f"不给自己编号的，病号不是自然数的，跟已有病号重复的病人滚粗病院！(╯>д<)╯⁽˙³˙⁾", who=GROUP_NAME, at=user)
        chat.SendMsg(msg=f"乀(ˉεˉ乀)欢迎新病友入院，请在群昵称中备注自己的病号。\n病号必须为自然数，且不能和已有病号重复。", who=GROUP_NAME, at=user)



if __name__ == '__main__':
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    wx = WeChat()
    wx.AddListenChat(nickname=GROUP_NAME, callback=test_group_message)
    wx.KeepRunning()

