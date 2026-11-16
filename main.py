import json
import os
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

ORANGE = (1.0, 0.36, 0.05, 1)
BG = (0.055, 0.06, 0.07, 1)
PANEL = (0.105, 0.11, 0.12, 1)
TEXT = (0.93, 0.93, 0.93, 1)

DEFAULTS = {
    "rage_demo": False, "rage_fov": 90, "rage_smooth": 50,
    "hit_location": "Head", "legit_demo": False, "legit_fov": 45,
    "legit_smooth": 65, "aim_key": "None", "target_bone": "Head",
    "visibility_demo": True, "esp_preview": True, "box": True,
    "name": True, "health": True, "distance": True, "skeleton": False,
    "crosshair": True, "fov_circle": True, "show_fps": True,
    "show_ping": False, "watermark": True, "menu_key": "F1",
    "theme": "Black & Orange", "language": "English"
}

def label(text, size=14, color=TEXT, **kwargs):
    return Label(text=text, font_size=dp(size), color=color, **kwargs)

class NEXIUMApp(App):
    def build(self):
        self.title = "NEXIUM External v1.1.0"
        Window.clearcolor = BG
        self.settings = DEFAULTS.copy()
        self.config_path = os.path.join(self.user_data_dir, "nexium_config.json")
        self.load_settings()

        outer = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        header = BoxLayout(size_hint_y=None, height=dp(58), spacing=dp(8))
        header.add_widget(label("NEXIUM", 26, ORANGE, bold=True))
        header.add_widget(label("EXTERNAL  •  v1.1.0", 12, TEXT))
        outer.add_widget(header)

        nav = GridLayout(cols=3, size_hint_y=None, height=dp(88), spacing=dp(5))
        for name in ["RAGE", "LEGIT", "VISUALS", "SKINS", "MISC", "CONFIGS"]:
            b = Button(text=name, background_normal="", background_color=PANEL,
                       color=ORANGE, bold=True)
            b.bind(on_release=lambda btn, n=name: self.show_section(n))
            nav.add_widget(b)
        outer.add_widget(nav)

        self.content = BoxLayout(orientation="vertical", spacing=dp(8))
        outer.add_widget(self.content)
        self.status = label("DEMO MODE • No game interaction", 11, ORANGE,
                            size_hint_y=None, height=dp(24))
        outer.add_widget(self.status)
        self.show_section("RAGE")
        return outer

    def load_settings(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            self.settings.update(loaded)
        except (OSError, ValueError):
            pass

    def save_settings(self, *_):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=2)
        self.status.text = "CONFIG SAVED"

    def reset_settings(self, *_):
        self.settings = DEFAULTS.copy()
        self.save_settings()
        self.show_section("CONFIGS")

    def section_title(self, name):
        self.content.clear_widgets()
        self.content.add_widget(label(name, 20, ORANGE, bold=True,
                                      size_hint_y=None, height=dp(34)))
        scroll = ScrollView()
        self.rows = GridLayout(cols=1, spacing=dp(7), size_hint_y=None,
                               padding=(0, 0, 0, dp(8)))
        self.rows.bind(minimum_height=self.rows.setter("height"))
        scroll.add_widget(self.rows)
        self.content.add_widget(scroll)

    def add_toggle(self, title, key):
        row = BoxLayout(size_hint_y=None, height=dp(46), padding=(dp(10), 0),
                        spacing=dp(8))
        row.add_widget(label(title))
        sw = Switch(active=bool(self.settings.get(key, False)))
        sw.bind(active=lambda _, value, k=key: self.set_value(k, value))
        row.add_widget(sw)
        self.rows.add_widget(row)

    def add_slider(self, title, key, minimum=0, maximum=100):
        row = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(72),
                        padding=(dp(10), dp(3)))
        value_label = label(f"{title}: {self.settings.get(key, minimum)}", 13, TEXT)
        slider = Slider(min=minimum, max=maximum, value=float(self.settings.get(key, minimum)))
        slider.bind(value=lambda _, value, k=key, t=title, l=value_label:
                    self.update_slider(k, t, l, value))
        row.add_widget(value_label)
        row.add_widget(slider)
        self.rows.add_widget(row)

    def add_select(self, title, key, values):
        row = BoxLayout(size_hint_y=None, height=dp(48), padding=(dp(10), 0))
        row.add_widget(label(title))
        spinner = Spinner(text=str(self.settings.get(key, values[0])),
                          values=values, size_hint_x=.48,
                          background_normal="", background_color=PANEL,
                          color=ORANGE)
        spinner.bind(text=lambda _, value, k=key: self.set_value(k, value))
        row.add_widget(spinner)
        self.rows.add_widget(row)

    def add_note(self, text):
        self.rows.add_widget(label(text, 12, ORANGE, size_hint_y=None,
                                   height=dp(52), halign="left"))

    def set_value(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def update_slider(self, key, title, lbl, value):
        value = int(value)
        self.settings[key] = value
        lbl.text = f"{title}: {value}"

    def show_section(self, name):
        self.section_title(name)
        if name == "RAGE":
            self.add_note("DEMO CONTROLS ONLY — does not aim or interact with the game.")
            self.add_toggle("AIM demo indicator", "rage_demo")
            self.add_slider("FOV preview", "rage_fov", 1, 180)
            self.add_slider("Smooth preview", "rage_smooth")
            self.add_select("Hit Location preview", "hit_location",
                            ["Head", "Neck", "Body", "Legs"])
        elif name == "LEGIT":
            self.add_note("Training-scene settings only; no game targeting.")
            self.add_toggle("Legit demo profile", "legit_demo")
            self.add_slider("FOV preview", "legit_fov", 1, 180)
            self.add_slider("Smooth preview", "legit_smooth")
            self.add_select("Aim Key label", "aim_key", ["None", "F1", "F2", "Shift"])
            self.add_select("Target Bone preview", "target_bone",
                            ["Head", "Neck", "Body"])
            self.add_toggle("Visibility demo", "visibility_demo")
        elif name == "VISUALS":
            self.add_note("Visual options apply only to this app's sample preview.")
            for title, key in [("ESP sample preview", "esp_preview"),
                               ("Box", "box"), ("Name", "name"),
                               ("Health bar", "health"), ("Distance", "distance"),
                               ("Skeleton sample", "skeleton"),
                               ("Crosshair", "crosshair"), ("FOV circle", "fov_circle")]:
                self.add_toggle(title, key)
            self.add_note("[ NEXIUM ]     SAMPLE TARGET     HP 100%     12 m")
        elif name == "SKINS":
            self.add_note("Cosmetic catalog mock-up; does not change in-game inventory.")
            self.add_select("Weapon preview", "weapon_preview",
                            ["AKR", "M4", "AWM", "USP"])
            self.add_select("Skin category", "skin_category",
                            ["Rifle", "Pistol", "Knife", "Gloves"])
            self.add_note("Preview and Favorites are placeholders for the next UI pass.")
        elif name == "MISC":
            for title, key in [("Show FPS (app)", "show_fps"),
                               ("Show Ping (sample)", "show_ping"),
                               ("NEXIUM watermark", "watermark")]:
                self.add_toggle(title, key)
            self.add_select("Menu key label", "menu_key", ["F1", "F2", "Insert"])
            self.add_select("Theme", "theme", ["Black & Orange"])
            self.add_select("Language", "language", ["English", "Русский"])
        elif name == "CONFIGS":
            self.add_note("Settings are stored locally as JSON in the app data folder.")
            save = Button(text="SAVE CONFIG", size_hint_y=None, height=dp(48),
                          background_normal="", background_color=ORANGE, color=BG)
            save.bind(on_release=self.save_settings)
            reset = Button(text="RESET SETTINGS", size_hint_y=None, height=dp(48),
                           background_normal="", background_color=PANEL, color=ORANGE)
            reset.bind(on_release=self.reset_settings)
            self.rows.add_widget(save)
            self.rows.add_widget(reset)

if __name__ == "__main__":
    NEXIUMApp().run()
