import re

pattern = re.compile(r'@院内自主设施 *')                    # 用于匹配至少一个数字
m = pattern.match('@院内自主设施 测试')        # 查找头部，没有匹配
print(m)