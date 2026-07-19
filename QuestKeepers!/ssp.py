from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.clock import Clock
import subprocess
import sys

from pywin.framework.editor import color

#import threading

Window.clearcolor = (0.43, 0.67, 0.89, 1)


# ---------- HOME SCREEN ----------

class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        title = Label(
            text="QuestKeeper",
            font_size=80,
            bold=True,
            color=(0, 0.3, 0, 1),
            pos_hint={"x": 0.01, "y": 0.0}
        )

        start_button = Button(
            text="Start Quest",
            font_size=24,
            background_normal="",
            background_color=(0.6, 0.9, 0.6, 1),
            color=(0, 0.3, 0, 1),
            size_hint=(0.4, None),
            height=60,
            pos_hint={"center_x": 0.5}
        )

        start_button.bind(on_press=self.open_goal_screen)

        cloud1 = Image(
            source="cloud.png",
            size_hint=(None, None),
            size=(120, 80),
            pos=(40, 500)
        )

        cloud2 = Image(
            source="cloud.png",
            size_hint=(None, None),
            size=(90, 60),
            pos=(300, 420)
        )

        cloud3 = Image(
            source="cloud.png",
            size_hint=(None, None),
            size=(140, 90),
            pos=(560, 540)
        )

        layout.add_widget(cloud1)
        layout.add_widget(cloud2)
        layout.add_widget(cloud3)

        self.clouds = [cloud1, cloud2, cloud3]

        Clock.schedule_interval(self.move_clouds, 1 / 60)

        layout.add_widget(title)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def open_goal_screen(self, button):
        self.manager.current = "goal"

    def move_clouds(self, dt):
        for cloud in self.clouds:
            cloud.x += 0.3
        if cloud.x > Window.width:
            cloud.x = -cloud.width


# ---------- GOAL SCREEN ----------

class GoalScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.goalslocked = False
        self.xp = 0

        layout = BoxLayout(
            orientation="vertical",
            spacing=20,
            padding=60
        )

        instruction = Label(
            text="**Minimum requirement to reach the peak is 2*180/6-10 QP**",
            color=(0.58, 0.29, 0.0, 1),
            font_size=30,
            bold=True
        )

        title = Label(
            text="My Quests",
            font_size=70,
            bold=True
        )

        self.xp_label = Label(
            text="QuestPoints: 0",
            font_size=20,
            size_hint=(1, None),
            height=35
        )

        goal_input = TextInput(
            hint_text="Enter a goal...",
            multiline=False,
            size_hint=(1, None),
            height=70
        )

        self.add_button = Button(
            text="+ Add Goal",
            size_hint=(0.4, None),
            height=50,
            pos_hint={"center_x": 0.5},
            background_normal="",
            background_color=(0.4, 0.8, 0.4, 1),
        )

        self.add_button.bind(on_press=lambda x: self.add_goal(goal_input))

        scroll = ScrollView()

        self.goal_list = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None
        )

        self.goal_list.bind(minimum_height=self.goal_list.setter("height"))

        scroll.add_widget(self.goal_list)

        back_button = Button(
            text="Back",
            font_size=24,
            background_normal="",
            background_color=(0.55, 0.35, 0.18, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.4, None),
            height=60,
            pos_hint={"center_x": 0.5}
        )

        limit_button = Button(
            text="Lock todays tasks",
            font_size=24,
            background_normal="",
            background_color=(255, 0, 0, 5),
            color=(1, 1, 1, 1),
            size_hint=(0.4, None),
            height=60,
            pos_hint={
                "center_x":0.5
            }

        )
        limit_button.bind(on_press=self.limit_goals)
        back_button.bind(on_press=self.go_back)

        layout.add_widget(instruction)
        layout.add_widget(title)
        layout.add_widget(self.xp_label)
        layout.add_widget(goal_input)
        layout.add_widget(self.add_button)
        layout.add_widget(scroll)
        layout.add_widget(limit_button)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def add_goal(self, goal_input):

        if self.goalslocked:
            print("Goals are locked!")
            return

        text = goal_input.text.strip()

        if text == "":
            return

        goal = Button(
            text="[   ] " + text,
            size_hint_y=None,
            height=50,
            background_normal="",
            background_color=(1, 1, 1, 1),
            color=(0, 0, 0, 1)
        )

        goal.bind(on_press=lambda x: self.complete_goal(goal))

        self.goal_list.add_widget(goal)

        goal_input.text = ""

    def complete_goal(self, goal):
        if goal.text.startswith("[Done]"):
            return

        goal.text = "[Done] " + goal.text[5:]
        goal.background_color = (0.7, 1, 0.7, 1)

        self.xp += 10
        self.xp_label.text = f"XP: {self.xp}"

        goal.unbind(on_press=goal.on_press)

    def go_back(self, button):
        self.manager.current = "home"

    def limit_goals(self, button):
        self.goals_locked = True




        # Disable the Add Goal button
        self.add_button.disabled = True

        # Disable the Lock button
        button.disabled = True
        button.text = "Goals Locked"

        subprocess.Popen(
            [sys.executable, "main.py", str(self.xp)]
        )
        #main.climbing(self.xp)
                  #print("Today's goals have been locked!")



# ---------- APP ----------

class QuestKeeper(App):

    def build(self):
        screen_manager = ScreenManager()

        screen_manager.add_widget(HomeScreen(name="home"))
        screen_manager.add_widget(GoalScreen(name="goal"))

        return screen_manager


QuestKeeper().run()