import re


def invited_person(text):
    """
    从邀请相关的文本中提取"被邀请人"的ID

    参数:
        text (str): 包含邀请信息的文本，可能是以下两种格式之一:
            1. ""邀请人"邀请"被邀请人"加入了群聊"
            2. ""被邀请人"通过扫描"邀请人"分享的二维码加入群聊"

    返回:
        str: "被邀请人"对应的ID
    """
    # 定义匹配被邀请人的正则表达式模式
    # 匹配被引导的引号内的内容（"被邀请人"）
    # 确保不会匹配到"邀请人"的部分
    pattern = r'"(.*?)".*?"(.*?)"'

    matches = re.findall(pattern, text)

    if not matches:
        raise ValueError("无法从文本中提取邀请信息")

    # 第一种情况："邀请人"在前，"被邀请人"在后
    if "邀请" in text and "加入" in text:
        return matches[0][1]
    # 第二种情况："被邀请人"在前
    elif "通过扫描" in text:
        return matches[0][0]
    else:
        raise ValueError("未知的邀请信息格式")


# 测试用例
test_case1 = '"张三"邀请"李四"加入了群聊'
test_case2 = '"王五"通过扫描"赵六"分享的二维码加入群聊'

print(extract_invitee_id(test_case1))  # 输出: 李四
print(extract_invitee_id(test_case2))  # 输出: 王五