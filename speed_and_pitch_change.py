from pydub import AudioSegment


class PaceGiver:
    def speed_change(sound, speed=1.0):
        # This is a copy-paste of a solution posted by a stackoverflow user here:
        # https://stackoverflow.com/questions/43408833/how-to-increase-decrease-playback-speed-on-wav-file
        # This method alters the pitch as well as the speed.
        # Ideally, it would be replaced with an algorithm which preserves the original pitch.
        sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * speed)
        })
        return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

    def pace_giver(self, distance, time):
        test_sound = AudioSegment.from_wav("musicfile.wav")
        # As I add more songs to the library, I should consider using a tempo detection algorithm.
        # For now, the song I am using for testing purposes was recorded with a tempo of 136 bpm.
        song_bpm = 136
        # The default step length is defined as one meter here. A future version could allow users
        # to customize this.
        runner_step = 1
        running_distance = distance * 1000
        running_steps_min = (running_distance / runner_step) / time
        speed_change_factor = running_steps_min / song_bpm
        sound = PaceGiver.speed_change(test_sound, float(speed_change_factor))
        return sound


def main():
    pg = PaceGiver()
    test_run_song = pg.pace_giver(5, 25)
    test_run_song.export("song.wav", format="wav")


if __name__ == "__main__":
    main()