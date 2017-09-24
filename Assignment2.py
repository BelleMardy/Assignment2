"""
Belle
Due: 5:00pm, 1 September 2017
Assignment 1 - Songs to Learn, a Python program that replicates supplied sample output
https://github.com/CP1404-2017-2/a1-BelleMardy
"""

from operator import itemgetter

VERSION = "1.0"
AUTHOR = "Belle"
MENU = """Menu:
L – List songs
A – Add new song
C – Complete a song
Q – Quit"""
MENU_OPTIONS = ["a", "c", "l", "q"]
LEARNED = "n"
REQUIRED = "y"
CSV_FILE = "songs.csv"
USER_INPUT = ">>> ".lower()


def main():
    """Main function that runs program and calls function."""
    print("Songs To Learn {} - by {}".format(VERSION, AUTHOR))
    songs = []  # List that store songs from CSV file and any added songs
    load_song_file(songs)
    sort_song_file(songs)
    print("{} songs loaded".format(len(songs)))
    print(MENU)
    get_menu_choice = input(USER_INPUT)
    get_menu_choice = validate_menu_choice(get_menu_choice)
    while get_menu_choice != "q":
        if get_menu_choice == "a":
            title = check_if_blank("Title: ")
            artist = check_if_blank("Artist: ")
            year = check_year_range("Year: ")
            added_songs = []
            add_new_song(songs, title, artist, year, added_songs)
            print(MENU)
            get_menu_choice = input(USER_INPUT)
            get_menu_choice = validate_menu_choice(get_menu_choice)
        elif get_menu_choice == "c":
            required_count = 0
            for song in range(len(songs)):
                if songs[song][3] == REQUIRED:
                    required_count += 1  # Counts number of songs required to be learn
            if required_count == 0:
                print("No more songs to learn!")  # Returns print statement if all songs learned
            else:
                complete_song(songs)
            print(MENU)
            get_menu_choice = input(USER_INPUT)
            get_menu_choice = validate_menu_choice(get_menu_choice)
        elif get_menu_choice == "l":
            sort_song_file(songs)
            display_song_list(songs)
            print(MENU)
            get_menu_choice = input(USER_INPUT)
            get_menu_choice = validate_menu_choice(get_menu_choice)
    sort_song_file(songs)
    save_song_to_file(songs)
    print("{} songs saved to {}".format(len(songs), CSV_FILE))
    print("Have a nice day :)")


"""Create a function to open song.csv file that is passed inot main function
    open "songs.csv" as in_file for reading
    get title from in_file
    get name from in_file
    get year from in_file
    for line in in_file is reviewed prior to turning into a list
        lines = striped of whitespaces 
        lines = split by commas
        split words = passed into songs list
    close in_file"""


def load_song_file(songs):
    """Read song.csv file and append to songs list."""
    in_file = open(CSV_FILE, "r")
    for line in in_file:
        song = line.strip().split(",")
        songs.append(song)
    in_file.close()


def sort_song_file(songs):
    """Sort songs into alpha order by artist and then title."""
    songs.sort(key=itemgetter(1, 0))


def validate_menu_choice(menu_choice):
    """Check for incorrect input entry by user based on menu choice."""
    while menu_choice.lower() not in MENU_OPTIONS:
        print("Invalid menu choice")
        print(MENU)
        menu_choice = input(USER_INPUT)
    return menu_choice.lower()


def check_if_blank(prompt):
    """Check for blank (omitted) user input."""
    valid_input = input(prompt)
    while valid_input == "":
        print("Input can not be blank")
        valid_input = input(prompt)
    return valid_input


def check_year_range(prompt):
    """A try/exception for when user enters a song year that is < 0, or a non number."""
    valid_input = False
    while not valid_input:
        try:
            year = int(input(prompt))
            if year >= 0:
                valid_input = True
            else:
                print("Number must be >= 0")
                valid_input = False
        except ValueError:
            print("Invalid input; enter a valid number")
    return year


def add_new_song(songs, title, artist, year, added_songs):
    """Append song to songs list."""
    added_songs.append(title)
    added_songs.append(artist)
    added_songs.append(str(year))
    added_songs.append(REQUIRED)
    songs.append(added_songs)
    print("{} by {} ({:>4}) added to song list".format(songs[-1][0], songs[-1][1], songs[-1][2]))


"""Create a function to change songs from [1] (required to learned) once the below conditions are meet so when the
list is again printed the song will no longer have an astrix which indicates now it is learned 
    display message "Enter the number of a song to mark as learned"
    get song number (integer) from user
    if song number is in range (length of song list) and not yet learned
    while song number != song number of an required song
        if song number < 0 
            display "Number must be >= 0"
        otherwise song number == song number already learned
            display "You have already learned song number"
        except ValueError (song number entered as a string)
            display "Invalid input; enter a valid number"
        except IndexError (song number > than number of songs)
            display "Invalid song number"
        if song number == song number of a required song
            song is changed from required to learned
            display "[0] by [1] learned"
"""


def complete_song(songs):
    """Try/exception when user attempts to record a song as learned, alerts if number < 0, or > than songs in list."""
    print("Enter the number of a song to mark as learned")
    valid_input = False
    while not valid_input:
        try:
            song_choice = int(input(USER_INPUT))
            if song_choice in range(len(songs)) and songs[song_choice][3] != LEARNED:  # Compares learned and required
                valid_input = True
            elif song_choice < 0:
                print("Number must be >= 0")
            elif songs[song_choice][3] == LEARNED:
                print("You have already learned {}".format(songs[song_choice][0]))
                return valid_input
        except ValueError:
            print("Invalid input; enter a valid number")
        except IndexError:
            print("Invalid song number")
    songs[song_choice][3] = LEARNED
    print("{} by {} learned".format(songs[song_choice][0], songs[song_choice][1]))


def display_song_list(songs):
    """Displays data stored in songs list, based on how many learned and how many are required (to be learnt)."""
    learned = 0
    required = 0
    for song in range(len(songs)):
        if songs[song][3] == REQUIRED:
            required += 1
            print("{:2}. {} {:30} - {:26} ({:>4}) ".format(song, "*", songs[song][0], songs[song][1], songs[song][2]))
        else:
            learned += 1
            print("{:2}. {} {:30} - {:26} ({:>4}) ".format(song, " ", songs[song][0], songs[song][1], songs[song][2]))
    print("{} songs learned, {} songs still to learn".format(learned, required))


def save_song_to_file(songs):
    """Overwrites existing csv file (songs) ie. title, artist, year, required/learned and saves changes/additions."""
    out_file = open(CSV_FILE, "w")
    for song in range(len(songs)):
        out_file.write("{},{},{},{}\n".format(songs[song][0], songs[song][1], songs[song][2], songs[song][3]))
    out_file.close()

main()