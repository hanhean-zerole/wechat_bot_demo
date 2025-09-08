import threading
import json
import os
import datetime
import normal_tools as nmtools

from General import GROUP_NAME, BOT_NAME, PIXIV_IMG, be_crazy, rate_limiter, get_command


VOTE_LIST = []
VOTE_JSON_PATH = "./vote_json/"


def vote_main(argcs, wxchat, sender):
    ans = ''
    if len(argcs) < 2:
        return vote_help()
    if argcs[1] == "创建投票":  # 投票名称，时间，选项A,选项B,选项C……
        ans = add_Vote(argcs=argcs, wxchat=wxchat)
    elif argcs[1] == "查看投票":  # 返回一个列表
        ans = list_vote(argcs, wxchat)
    elif argcs[1] == "进行投票":  # 不重复投票，
        ans = voting(argcs, wxchat, sender)
    else:
        ans = vote_help()
    return ans


def vote_help():
    ans = f"病友你坏,这里是投票功能！\n" \
          f"投票功能相对比较复杂，以下是详细的讲解：\n" \
          f"要让院内进行投票，首先需要“创建”投票！\n" \
          f"发送@{BOT_NAME}    投票    创建投票    投票名称    投票时长(为一个自然数，表示几小时)    选项A     选项B(以及其他选项)\n" \
          f"这样就能创建一个投票！\n" \
          f"发送“@{BOT_NAME}    投票    查看投票”可以查看正在进行中的投票!\n" \
          f"而发送“@{BOT_NAME}    投票    进行投票    投票名称    投票选项”可以为对应投票中的选项进行投票！\n" \
          f"注意：投票不可以重名，时间为1-24小时，到时投票会自然结束并返回结果。\n" \
          f"以上！"
    return ans


def remove_vote(vote_name, chat):
    result = ''
    print(vote_name)
    for vote in VOTE_LIST:
        if vote_name == vote.name:
            with open(VOTE_JSON_PATH + vote_name + ".json", 'r') as f:
                vote_dict = json.load(f)
                result = f"{vote_name}投票结束\n"
                for choice in vote_dict.keys():
                    result += f"{choice}的票数为{vote_dict[choice]}\n"
            VOTE_LIST.remove(vote)
            os.remove(VOTE_JSON_PATH + vote_name + ".json")
            chat.SendMsg(msg=result, who=GROUP_NAME)

@rate_limiter(300)
def add_Vote(argcs, wxchat):
    tempvote = Vote(argcs=argcs, wxchat=wxchat)
    if isinstance(tempvote,Vote):
        for vote in VOTE_LIST:
            if tempvote.name == vote.name:
                return "与已有投票重名，请重新命名。"
        VOTE_LIST.append(tempvote)
        with open(VOTE_JSON_PATH + tempvote.name + ".json", 'w') as f:
            json.dump(tempvote.voteDict, f)
        return f"成功创建投票：{tempvote.name}"
    else:
        return "创建投票失败"


def list_vote(argcs, wxchat):  # 无参数返回列表与时间，有参数返回投票信息
    ret = ""
    if len(argcs) == 2:
        ret += f"当前进行的投票有：\n"
        for vote in VOTE_LIST:
            ret += vote.name + "    于" + vote.starttime.strftime("%Y/%m/%d, %H:%M:%S") + "开始，持续时长为" + str(vote.ttl) + "小时\n "
        ret += f"输入“@{BOT_NAME}    投票    查看投票    投票名称”查看投票具体信息。"
    if len(argcs) > 2:
        for vote in VOTE_LIST:
            if argcs[2] == vote.name:
                ret += vote.name + "的具体投票情况如下：\n"
                for choice in vote.voteDict.keys():
                    ret += f"{choice}的票数为{vote.voteDict[choice]}\n"
                break
        else:
            ret = "没有找到指定的投票。"
    return ret


def voting(argcs, wxchat, sender):
    ret = ''
    if len(argcs) == 4:
        for vote in VOTE_LIST:
            if argcs[2] == vote.name:
                for choice in vote.voteDict.keys():
                    if argcs[3] == choice:
                        if sender in vote.voter:
                            ret = f'你已经投票了。不要重复投票。'
                            break
                        vote.voter.add(sender)
                        vote.voteDict[choice] += 1
                        ret = f"投票成功，{choice}的票数为{vote.voteDict[choice]}\n"
                        with open(VOTE_JSON_PATH + vote.name + ".json", 'w') as f:
                            json.dump(vote.voteDict, f)
                        break
                else:
                    ret = '未找到对应的选项，请确认投票选项是否正确。'
                break
        else:
            ret = "没有找到指定的投票，请确认投票名称是否正确。"
    else:
        ret = '投票参数个数错误，请浏览投票帮助查看如何投票。'
    return ret


class Vote:

    def __init__(self, argcs, chat):  # 建立一个线程，计时ttl小时，内部一个字典对应各个选项以及票数。到时间后自动停止。
        try:
            if len(argcs) < 6:
                fail_reason = "创建投票的参数过少，请查看投票帮助。"
                chat.SendMsg(msg=fail_reason, who=GROUP_NAME)
                raise "参数过少"
            if len(VOTE_LIST) > 5:
                fail_reason = "当前投票数量过多，请等待部分投票结束后重试。"
                chat.SendMsg(msg=fail_reason, who=GROUP_NAME)
                raise "当前投票数量过多"
            self.chat = chat
            self.name = argcs[2]
            self.voter= set()
            self.ttl = int(argcs[3])
            if self.ttl < 1:
                self.ttl = 1
            if self.ttl > 24:
                self.ttl = 24
            self.starttime = datetime.datetime.now()
            self._start_timer()
            self.voteDict = dict.fromkeys(argcs[4:], 0)
        except:
            pass

    def _start_timer(self):
        timer = threading.Timer(self.ttl*3600, remove_vote, kwargs={'vote_name': self.name,'chat': self.chat})
        timer.daemon = False
        timer.start()

    def _self_destruct(self):
        remove_vote(self.name)

    def __str__(self):#输出投票剩余时间等当前投票相关信息
        pass


if __name__ == '__main__':
    while(True):
        ipt = input()
        ans = vote_main(get_command(ipt), None, None)
        print(ans)