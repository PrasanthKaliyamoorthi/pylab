import os
import pygame


def play_music(directory, song_name):

    file_path = os.path.join(directory, song_name)

    if not os.path.exists(file_path):
        print("File not found!")
        return

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    print(f"\nNow playing: {song_name}")
    print("Commands: [P]ause, [R]esume, [S]top")

    while True:

        command = input("> ").lower()

        if command == 'p':
            pygame.mixer.music.pause()
            print("Paused.")
        elif command == 'r':
            pygame.mixer.music.unpause()
            print("Playing.")
        elif command == 's':
            pygame.mixer.music.stop()
            print("Stopped.")
            return
        else:
            print("Invalid Command!")

def main():
    try:
        pygame.mixer.init()
    except pygame.error as er:
        print(f"Error Initializing pygame : {er}")
        return

    directory = "./music"

    if not os.path.isdir(directory):
        print(f"No {directory:} not found!")
        return

    audio_files = [file for file in os.listdir(directory) if file.endswith(".mp3") or file.endswith(".wav")]

    if not audio_files:
        print(f"Empty Directory? ./{directory}")

    while True:
        print("***** Audio Player *****")
        print("My song list:")

        for index, song in enumerate(audio_files, start=1):
            print(f"{index}, {song}")

        choice_input = input("\nEnter the song # to play (or 'Q' to quit): ")

        if choice_input.lower() == "q":
            print("Bye!")
            break

        if not choice_input.isdigit():
            print("Enter a valid number")
            continue

        choice = int(choice_input) - 1

        if 0 <= choice < len(audio_files):
            play_music(directory, audio_files[choice])
        else:
            print("Invalid choice.")



if __name__ == "__main__":
    main()
