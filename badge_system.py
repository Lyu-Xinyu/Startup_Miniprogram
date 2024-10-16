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
            print("\n每日激励:")
            print(f"\"{quote_data['content']}\" - {quote_data['author']}")
        except:
            quote, author = random.choice(offline_quotes)
            print("\n每日激励:")
            print(f"\"{quote}\" - {author}")