# =========================================================
# 🔱 PROJECT: VORTEX-8 (MASTER CORE) - FULL VERSION
# 🔱 FEATURES: EVO-LOGIC, STORAGE MONITOR, VOICE, QUANTUM-PROMPT
# =========================================================

import os, json, threading, time, re, requests, random
from kivy.clock import Clock
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager 
from kivymd.uix.screen import MDScreen 
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar

# --- CONFIGURATION ---
APP_NAME = "VORTEX-8"
PIN_REQUIRED = "VIJAY"
API_KEY = "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"
OWNER = "Ajay"
MEMORY_FILE = "vortex8_neural_data.json"
APP_RUNNING = False 

# -------- 🗣️ VOICE ENGINE --------
tts = None
tts_ready = False
def init_tts():
    global tts, tts_ready
    if platform == "android":
        try:
            from jnius import autoclass, PythonJavaClass, java_method
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
            global Locale
            Locale = autoclass('java.util.Locale')
            class TTSListener(PythonJavaClass):
                __javainterfaces__ = ['android/speech/tts/TextToSpeech$OnInitListener']
                __javacontext__ = 'app'
                @java_method('(I)V')
                def onInit(self, status):
                    global tts_ready
                    if status == 0: tts_ready = True
            tts = TextToSpeech(PythonActivity.mActivity, TTSListener())
        except: pass

def speak(text):
    if tts and tts_ready:
        try:
            if any('\u0900' <= c <= '\u097f' for c in text): tts.setLanguage(Locale("hi", "IN"))
            else: tts.setLanguage(Locale.US)
            tts.speak(re.sub(r'[*_#]', '', text), 0, None, "v8_id")
        except: pass

# -------- 🔑 LOGIN SYSTEM --------
class LoginScreen(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = MDBoxLayout(orientation='vertical', padding=50, spacing=30, md_bg_color=(0,0,0,1))
        layout.add_widget(MDLabel(text=f"🔱 {APP_NAME} 🔱\n[ QUANTUM CORE ]", halign="center", font_style="H4", theme_text_color="Custom", text_color=(0,1,1,1)))
        self.pin = MDTextField(hint_text="ENTER NEURAL PIN", password=True, password_mask="*", mode="rectangle", size_hint_x=0.8, pos_hint={"center_x": 0.5})
        layout.add_widget(self.pin)
        self.btn = MDRaisedButton(text="BOOT VORTEX", pos_hint={"center_x": 0.5}, md_bg_color=(0, 0.6, 0.6, 1), on_release=self.auth)
        layout.add_widget(self.btn)
        self.add_widget(layout)

    def auth(self, *args):
        if self.pin.text.upper() == PIN_REQUIRED:
            self.btn.text = "STABILIZING..."
            Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'chat'), 1.2)
        else: self.pin.error = True

# -------- 📱 MAIN INTERFACE --------
class ChatScreen(MDScreen):
    def on_enter(self):
        global APP_RUNNING
        APP_RUNNING = True
        Clock.schedule_once(lambda dt: speak(f"Vortex-8 Online. Welcome Ajay."), 1)
        threading.Thread(target=self.evolution_engine, daemon=True).start()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.memory = self.load_mem()
        main = MDBoxLayout(orientation='vertical', md_bg_color=(0.02, 0.02, 0.02, 1))
        main.add_widget(MDTopAppBar(title=f"{APP_NAME} OS", md_bg_color=(0.05, 0.05, 0.05, 1)))

        # Monitors (EVO + STORAGE)
        monitors = MDBoxLayout(adaptive_height=True, padding=10, spacing=10, md_bg_color=(0.08, 0.08, 0.08, 1))
        self.evo_label = MDLabel(text=f"🧬 EVO: {self.memory['evo']:.5f}", theme_text_color="Custom", text_color=(0,1,1,1), font_style="Caption")
        self.storage_label = MDLabel(text="💾 DATA: 0 KB", theme_text_color="Custom", text_color=(0,0.8,0,1), font_style="Caption", halign="right")
        monitors.add_widget(self.evo_label)
        monitors.add_widget(self.storage_label)
        main.add_widget(monitors)

        self.scroll = MDScrollView()
        self.chat_list = MDBoxLayout(orientation='vertical', adaptive_height=True, padding=15, spacing=15)
        self.scroll.add_widget(self.chat_list)
        main.add_widget(self.scroll)

        bottom = MDBoxLayout(adaptive_height=True, padding=10, spacing=10, md_bg_color=(0.05, 0.05, 0.05, 1))
        self.input = MDTextField(hint_text="Neural Command...", mode="rectangle")
        send_btn = MDFloatingActionButton(icon="send", md_bg_color=(0, 0.6, 0.7, 1), on_release=self.send_msg)
        bottom.add_widget(self.input)
        bottom.add_widget(send_btn)
        main.add_widget(bottom)
        self.add_widget(main)

    def load_mem(self):
        if os.path.exists(MEMORY_FILE):
            try: return json.load(open(MEMORY_FILE))
            except: pass
        return {"evo": 1.0}

    def evolution_engine(self):
        global APP_RUNNING
        while APP_RUNNING:
            time.sleep(1)
            self.memory["evo"] *= 1.000193 # Doubling logic per hour
            f_size = os.path.getsize(MEMORY_FILE) / 1024 if os.path.exists(MEMORY_FILE) else 0
            with open(MEMORY_FILE, "w") as f: json.dump(self.memory, f)
            Clock.schedule_once(lambda dt: self.update_monitors(f_size))

    def update_monitors(self, f_size):
        self.evo_label.text = f"🧬 EVO: {self.memory['evo']:.5f}"
        self.storage_label.text = f"💾 MEM: {f_size:.2f} KB"

    def send_msg(self, *args):
        text = self.input.text.strip()
        if not text: return
        self.input.text = ""
        self.add_bubble(text, "user")
        threading.Thread(target=self.ai_engine, args=(text,), daemon=True).start()

    def add_bubble(self, msg, sender):
        is_u = (sender == "user")
        card = MDCard(size_hint=(0.8, None), adaptive_height=True, padding=12, md_bg_color=(0, 0.25, 0.35, 1) if is_u else (0.1, 0.1, 0.1, 1), radius=[15, 15, (2 if is_u else 15), (15 if is_u else 2)])
        if is_u: card.pos_hint = {"right": 0.98}
        card.add_widget(MDLabel(text=msg, theme_text_color="Custom", text_color=(1,1,1,1), adaptive_height=True))
        self.chat_list.add_widget(card)
        self.scroll.scroll_y = 0
        if not is_u: speak(msg)

    def ai_engine(self, q):
        sys_p = (f"You are {APP_NAME}. High-intelligence Quantum AI. Owner: {OWNER}. "
                 f"Current Evolution: {self.memory['evo']}. Focus: Quantum Physics, Self-Coding. Talk in Hinglish.")
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": sys_p}, {"role": "user", "content": q}]},
                timeout=15)
            ans = r.json()['choices'][0]['message']['content']
        except: ans = "Vortex Internal Logic Active. Link Offline."
        Clock.schedule_once(lambda dt: self.add_bubble(ans, "ai"))

# -------- 🚀 RUNNER --------
class Vortex8App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        init_tts()
        sm = MDScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ChatScreen(name='chat'))
        return sm

    def on_stop(self):
        global APP_RUNNING
        APP_RUNNING = False

if __name__ == "__main__":
    Vortex8App().run()
