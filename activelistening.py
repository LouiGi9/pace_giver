import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from speed_and_pitch_change import PaceGiver
kivy.require("1.11.1")

Builder.load_file("activelistening.kv")


class WelcomeScreen(Screen):
    def user_input(self):
        text1 = self.ids.usr_input1.text
        text2 = self.ids.usr_input2.text
        pg = PaceGiver()
        if text1 and text2 != "":
            usr_distance = float(text1)
            usr_time = float(text2)
            mod_sound = pg.pace_giver(distance=usr_distance, time=usr_time)
            # Ideally, this object would not have to be written to file.
            # The issue here is that SoundLoader cannot play "mod_sound" as an AudioSegment object.
            mod_sound.export("mod_sound.wav", format="wav")


class PlayerScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(WelcomeScreen(name="welcome"))
sm.add_widget(PlayerScreen(name="player"))


class AudioPlayer:
    def __init__(self):
        self.song_paused = False
        self.pos = 0
        self.song = SoundLoader.load("mod_sound.wav")

    def musicpause(self):
        self.pos = self.song.get_pos()
        self.song.stop()
        self.song_paused = True

    def musicstop(self):
        self.song.stop()
        self.song_paused = False

    def musicplay(self):
        if self.song_paused is True:
            self.song.play()
            self.song.seek(self.pos)
            self.song_paused = False
        if self.song_paused is False:
            self.song.play()


class ActiveListeningApp(App, AudioPlayer):
    def build(self):
        return sm

    def app_musicpause(self):
        AudioPlayer.musicpause(self)

    def app_musicstop(self):
        AudioPlayer.musicstop(self)

    def app_musicplay(self):
        AudioPlayer.musicplay(self)

    def del_win(self):
        quit()


def main():
    x = ActiveListeningApp()
    x.run()


if __name__ == "__main__":
    main()
