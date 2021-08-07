import os, subprocess, time
from pymediainfo import MediaInfo

""" 
A module that'll enables us navigate to our TV Shows' directory.
We can then choose a TV Show to watch in various modes; 
1. Watch in series, episode after episode using the preceding episode's time duration as automatic cue
2. For those shows with multiple seasons, we can choose a season & watch
3. For those with single seasons, we can choose an episode or entire season

NB: Assumption that your library is well arranged & VLC is installed
"""

# first, we navigate to the TV Series directory
# we can also choose to see our tv series list if preferred.
def navigate_to_directory(dir_url, show_list=False):
    os.chdir(dir_url)
    if show_list:
        x = os.path.split(dir_url)
        print(f"You're now in the {x[1].capitalize()} directory.")
        print(" ")
        print('Available TV Series are:')
        print('*' * 24)
        # we shall only print out entries that are directories
        for series in os.listdir():
            series_path = os.path.join(os.getcwd(), series)
            if os.path.isdir(series_path):
                print(series)

# once in the target directory, we check that all entries are directories
# we then add the same to a list
series_list = []
def create_tv_list():
    for series in os.listdir():
        series_path = os.path.join(os.getcwd(), series)
        if os.path.isdir(series_path):
            series_list.append(series)

# It would be helpful to index our TV shows, hence we create a dictionary 
# We can use these indices as keys later
# If preferred, we can list the series and their respective indices
series_dict = {}

def tv_series_index(show_tv_index=False):
    for number, series in enumerate(series_list, start=1):
        series_dict[number] = series
        continue
    if show_tv_index:
        print('Index'.ljust(15), 'TV Series')
        print('*'* 5,' '* 5, '*' * 20)
        for k, v in series_dict.items():
            print(str(k).ljust(10), v)

# we then choose a TV show to watch by passing its respective index
# we however first create lists that we'll populate with either seasons or episodes
# if the show only has a single season
season_list = []
episode_list = []

def tv_series_choice(series_index):
    # change current directory to Tv show chosen
    series_dir = os.path.join(os.getcwd(), series_dict[series_index])
    os.chdir(series_dir)


    # we check if entries in the directory are episodes or seasons 
    # we add the same to respective lists
    for entry in os.listdir():
        
        entry_path = os.path.join(os.getcwd(), entry)

        if os.path.isdir(entry_path):
            season_list.append(entry)
            continue

        # checks if entry is a file & is not a text or other file but a media one
        # we therefore add a file size check, lower limit 15MB
        if os.path.isfile(entry_path) and os.stat(entry_path).st_size > 15728640:
            episode_list.append(entry)
            continue
    
    # choose which mode you'd like to watch the single season in
    def episode_play_mode(episode_list):
        
        play_mode = input("Would you like to play in series(Y), choose episode(C) or all(A): ").upper()
        
        if play_mode == 'Y':
            for entry in os.listdir():
                if os.stat(entry_path).st_size > 15728640:
                    os.startfile(entry_path)

                    # getting TV episode time duration
                    media_info = MediaInfo.parse(entry_path)
                    duration_ms = media_info.tracks[0].duration
                    duration_secs = duration_ms / 1000
                    print(f"Now Playing {entry}")

                    # starts next episode after previous episode's time duration
                    # NB: sleep function is dependent on your system & may not be accurate
                    time.sleep(duration_secs)

        elif play_mode == 'C':
            try:
                ep_num = int(input(f"Please enter episode number from the list below:\n {episode_list}: "))
            
                episode_path = os.path.join(os.getcwd(), episode_list[ep_num - 1])

                if os.path.lexists(episode_path):
                    print('*' * 50)
                    print(f"Now playing {os.path.split(episode_path)[1]}")
                    subprocess.run(["start", "vlc.exe", episode_path], shell=True)
            except ValueError as err:
                print("")
                print("Oops! Your entry doesn't seem to be a number:", err)
            except (IndexError, UnboundLocalError):
                print("")
                print("Error: Please recheck your entry, ensure it matches with the list given.")

        elif play_mode == 'A':
            subprocess.run(["start", "vlc.exe", series_dir], shell=True)

        else:
            print("Oops! There seems to be an error with your entry.")

    # choose a season to watch if a TV show has several seasons    
    def choose_season(season_list):
        try:
            season_num = int(input(f"Please enter the season number you'd like to watch from the list \n    {season_list}: "))

            season_path = os.path.join(os.getcwd(), season_list[season_num - 1])

            if os.path.lexists(season_path):
                print('*' * 50)
                print(f"Now playing {os.path.split(season_path)[1]}")
                subprocess.run(["start", "vlc.exe", season_path], shell=True)

        except ValueError as err:
            print("")
            print("Oops! Your entry doesn't seem to be a number:", err)
        except (IndexError, UnboundLocalError):
            print("")
            print("Error: Please recheck your entry, ensure it matches with the list given.")

    # call respective functions if we've got a single or multiple season TV show    
    if len(season_list) > 0:
        choose_season(season_list)
    elif len(episode_list) > 0:
        episode_play_mode(episode_list)

def main():
    # enter your media library's path
    dir_url = 'e:\\tv series'

    # choose show_list to True if you want to see your TV show list
    navigate_to_directory(dir_url, show_list=False)

    create_tv_list()

    # choose show_tv_index to True if you want to see TV shows & their indices
    tv_series_index(show_tv_index=True)

    # Index 110: You Sn 1
    # Index 26: Everybody Hates Chris
    print("")
    try:
        series_index = int(input("Please enter TV Series Index: "))
        print("*" * 50)
        print(f"Cool! You have chosen {series_dict[series_index]}")

        tv_series_choice(series_index)
    except ValueError as err:
        print("Oops! Please check entry, not a number")

if __name__ == "__main__":
    main()
