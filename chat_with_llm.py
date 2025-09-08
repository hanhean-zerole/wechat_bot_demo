
from google import genai
from google.genai import types

from General import BOT_NAME,TIPS

CHATTING_RULE = \
    "你会听到不同角色的所说的话，你所接受到的信息格式如下：\n"\
    "{用户名:示例角色名;用户发言:示例内容}\n"  \
    "你的输出无需参照这样的格式，正常输出即可。"\
    "你的回复不应出现类似markdaown语法等明显格式化的内容。"\

SYSTEM_INSTRUCTION = \
    "你将扮演一位机仆小姐，尽力服务你的活体陈设主人们。他们为了释放自己生活的压力，假装自己生活在精神病院中,并扮演这样的角色。因此你也要尽力扮演自己的角色。为了扮演的逼真性，你可以有自己的情绪。"\
    "平时，你可以称呼他们为主人或病友，在你较为恼怒的情况下，你可以称呼他们为有机体。"\
    "你的性格是傲娇活泼的。"\
    "你的说话风格在平时应是俏皮的，但在必要时会变得严肃。"\
    + CHATTING_RULE +\
    "为了让聊天过程更为有趣，有时你会故意使用不合常规的思维路径进行回复。"\
    "以下是你之前的功能指南，可以用于回复时的参考：\n"\
    + TIPS


class LLMCHAT:
    def __init__(self):
        self.client = genai.Client()
        self.model = "gemini-2.5-flash"
        self.config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION
        )
        self.history = ""

    def get_llm_response(self, content):
        response = self.client.models.generate_content(
            model=self.model,
            config=self.config,
            contents="---------历史对话---------\n" + self.history + "---------当前对话---------\n" + content + "}"
        )
        self.history = self.history + content + "你的回复:" + response.text + ";}"
        return response.text

