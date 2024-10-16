import os

def create_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"已创建文件: {filename}")

main_py = '''
import json
import requests
import random
from badge_system import BadgeSystem

offline_quotes = [
    ("成功不是最终目标，失败也不是终点。", "温斯顿·丘吉尔"),
    ("生活中最重要的不是所处的位置，而是所朝的方向。", "奥利弗·温德尔·霍姆斯"),
    ("最困难的时刻，就是离成功不远的时候。", "爱迪生"),
    ("机会总是留给有准备的人。", "路易·巴斯德"),
    ("相信你自己，你比想象中更强大。", "未知"),
]

def load_user_data():
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"tasks": {}, "badges": {}}

def save_user_data(data):
    with open('user_data.json', 'w') as f:
        json.dump(data, f, indent=2)

def display_welcome_quote():
    try:
        response = requests.get("https://api.quotable.io/random", timeout=5)
        response.raise_for_status()
        quote_data = response.json()
        print("\\n欢迎回来！这是今天的激励名言：")
        print(f"\\"{quote_data['content']}\\" - {quote_data['author']}\\n")
    except:
        quote, author = random.choice(offline_quotes)
        print("\\n欢迎回来！这是今天的激励名言：")
        print(f"\\"{quote}\\" - {author}\\n")

def main():
    user_data = load_user_data()
    badge_system = BadgeSystem(user_data)

    display_welcome_quote()

    while True:
        print("\\n1. 添加新任务")
        print("2. 打卡任务")
        print("3. 查看成就")
        print("4. 退出")
        choice = input("请选择操作: ")

        if choice == '1':
            task_name = input("输入任务名称: ")
            badge_name = input("输入徽章名称: ")
            beginner_level = int(input("输入达成初级成就的打卡次数: "))
            intermediate_level = int(input("输入达成中级成就的打卡次数: "))
            advanced_level = int(input("输入达成高级成就的打卡次数: "))
            levels = [beginner_level, intermediate_level, advanced_level]
            high_level_style = input("输入高级徽章样式描述: ")
            badge_system.add_task(task_name, badge_name, levels, high_level_style)
        elif choice == '2':
            tasks = list(user_data['tasks'].keys())
            for i, task in enumerate(tasks):
                print(f"{i+1}. {task}")
            task_index = int(input("选择要打卡的任务编号: ")) - 1
            badge_system.check_in(tasks[task_index])
        elif choice == '3':
            badge_system.display_achievements()
        elif choice == '4':
            break
        else:
            print("无效的选择，请重试。")

    save_user_data(user_data)

if __name__ == "__main__":
    main()
'''

badge_system_py = '''
import requests
import random

offline_quotes = [
    ("成功不是最终目标，失败也不是终点。", "温斯顿·丘吉尔"),
    ("生活中最重要的不是所处的位置，而是所朝的方向。", "奥利弗·温德尔·霍姆斯"),
    ("最困难的时刻，就是离成功不远的时候。", "爱迪生"),
    ("机会总是留给有准备的人。", "路易·巴斯德"),
    ("相信你自己，你比想象中更强大。", "未知"),
]

class BadgeSystem:
    def __init__(self, user_data):
        self.user_data = user_data

    def add_task(self, task_name, badge_name, levels, high_level_style):
        self.user_data['tasks'][task_name] = {
            'badge_name': badge_name,
            'levels': levels,
            'high_level_style': high_level_style,
            'check_ins': 0
        }
        print(f"任务 '{task_name}' 已添加。")
        print(f"初级成就: {levels[0]}次打卡")
        print(f"中级成就: {levels[1]}次打卡")
        print(f"高级成就: {levels[2]}次打卡")

    def check_in(self, task_name):
        if task_name in self.user_data['tasks']:
            self.user_data['tasks'][task_name]['check_ins'] += 1
            check_ins = self.user_data['tasks'][task_name]['check_ins']
            print(f"已为任务 '{task_name}' 打卡。当前打卡次数：{check_ins}")
            self._update_badge(task_name)
            self._display_quote()
        else:
            print(f"任务 '{task_name}' 不存在。")

    def _update_badge(self, task_name):
        task = self.user_data['tasks'][task_name]
        check_ins = task['check_ins']
        levels = task['levels']
        badge_name = task['badge_name']

        for i, level_requirement in enumerate(levels):
            if check_ins >= level_requirement:
                level = ['初级', '中级', '高级'][i]
                if badge_name not in self.user_data['badges'] or self.user_data['badges'][badge_name]['level'] != level:
                    self.user_data['badges'][badge_name] = {
                        'level': level,
                        'style': self._generate_badge_style(task, i)
                    }
                    print(f"恭喜！您获得了 {level} {badge_name} 徽章！")

    def _generate_badge_style(self, task, level_index):
        if level_index == 2:  # 高级徽章
            return task['high_level_style']
        elif level_index == 1:  # 中级徽章
            return f"简化版的{task['high_level_style']}"
        else:  # 初级徽章
            return f"基础版的{task['high_level_style']}"

    def display_achievements(self):
        if not self.user_data['badges']:
            print("您还没有获得任何徽章。")
        else:
            print("您的成就：")
            for badge_name, badge_info in self.user_data['badges'].items():
                print(f"{badge_name} - {badge_info['level']}：{badge_info['style']}")

    def _display_quote(self):
        try:
            response = requests.get("https://api.quotable.io/random", timeout=5)
            response.raise_for_status()
            quote_data = response.json()
            print("\\n每日激励:")
            print(f"\\"{quote_data['content']}\\" - {quote_data['author']}")
        except:
            quote, author = random.choice(offline_quotes)
            print("\\n每日激励:")
            print(f"\\"{quote}\\" - {author}")
'''

user_data_json = '''
{
  "tasks": {},
  "badges": {}
}
'''

create_file('main.py', main_py.strip())
create_file('badge_system.py', badge_system_py.strip())
create_file('user_data.json', user_data_json.strip())

print("所有文件已成功创建。")
print("请确保已安装 requests 库。如果没有，请运行: pip install requests")
print("运行程序请使用命令: python main.py")