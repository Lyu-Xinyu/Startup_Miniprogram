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
        print("\n欢迎回来！这是今天的激励名言：")
        print(f"\"{quote_data['content']}\" - {quote_data['author']}\n")
    except:
        quote, author = random.choice(offline_quotes)
        print("\n欢迎回来！这是今天的激励名言：")
        print(f"\"{quote}\" - {author}\n")

def main():
    user_data = load_user_data()
    badge_system = BadgeSystem(user_data)

    display_welcome_quote()

    while True:
        print("\n1. 添加新任务")
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