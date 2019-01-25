import os, collections

#directory for all the logs
log_dir = os.path.join(os.getcwd(), "logs")

#describes the program
print("This program displays cumulative statistics for all keylog files in the log directory.")

if not os.path.exists(log_dir):
    #makes log directory if it doesn't exist and outputs an error message
    os.makedirs(log_dir)
    print("Error: Log directory not found. Run 'Keylogger.pyw' to generate log files in the 'logs' folder.")
elif len(list(file for file in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, file)))) == 0:
    #outputs an error message if the log directory is empty
    print("Error: Log directory is empty. Run 'Keylogger.pyw' to generate log files in the 'logs' folder.")
else:
    #adds all non-reformatted logs in the logs folder to log_list
    log_list = list(log_file for log_file in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, log_file)) and os.path.splitext(log_file)[0][-2:] != "_r")

    input_list = [] #stores keystrokes from all log files in the log directory
    for log_file in log_list:
        with open(os.path.join(log_dir, log_file)) as log:
            #adds keystrokes from each log directory to input_list
            input_list += [(line[line.find("'") + 1:line.find("'", line.find("'") + 1)] if line.find("Key") == -1 else line[line.find("K"):-1]) for line in log.readlines()]

    spacebar_presses, backspace_presses, misc_presses = 0, 0, 0 #stores non-alphanumeric key-presses
    #replaces all non-alphanumeric key-presses with empty strings, then increments their corresponding counters
    for i, key in enumerate(input_list):
        if len(key) != 1:
            if key == "Key.space":
                spacebar_presses += 1
            elif key == "Key.backspace":
                backspace_presses += 1
            else:
                misc_presses += 1
            input_list[i] = ""

    #removes all empty strings in input_list created by the for-loop above and converts all key-presses into lowercase
    input_list[:] = [key.lower() for key in input_list if key != ""]

    #prints various stats for key-presses
    print("\nTotal key-presses: " + str(len(input_list) + spacebar_presses + backspace_presses + misc_presses))

    print("Alphanumeric key-presses: " + str(len(input_list)))
    print("Spacebar key-presses: " + str(spacebar_presses))
    print("Backspace key-presses: " + str(backspace_presses))
    print("Miscellaneous key-presses (ctrl/shift/etc.): " + str(misc_presses))

    #prints the top 5 most pressed alphanumeric characters, along with the number of times they were pressed and the percentage of total alphanumeric presses they make up
    print("\nThe top 5 most pressed alphanumeric characters were:")
    for i in range(5):
        print("'" + str(collections.Counter(input_list).most_common(5)[i][0]) + "': " + str(collections.Counter(input_list).most_common(5)[i][1]) + " presses (", end="")
        print("%.2f" % round(collections.Counter(input_list).most_common(5)[i][1] / len(input_list) * 100.0, 2), end="")
        print("% of all alphanumeric presses.)")

    #prints the frequency of vowel presses
    print("\nThe frequency of vowel presses was:")

    vowels = ["a", "e", "i", "o", "u"]
    for vowel in vowels:
        print("'" + str(vowel) + "': " + str(input_list.count(vowel)) + " presses (", end="")
        print("%.2f" % round(input_list.count(vowel) / len(input_list) * 100.0, 2), end="")
        print("% of all alphanumeric presses.)")

    #asks the user if they would like to see stats for all alphanumeric characters
    while(True):
        show_full_stats = input("\nWould you like to see stats for all alphanumeric characters? (y/n) ")

        if show_full_stats == "y":
            #displays stats for all alphanumeric characters
            for i in range(10):
                print("'" + str(i) + "': " + str(input_list.count(str(i))) + " presses (", end="")
                print("%.2f" % round(input_list.count(str(i)) / len(input_list) * 100.0, 2), end="")
                print("% of all alphanumeric presses.)")
            for i in range(26):
                print("'" + chr(i + 97) + "': " + str(input_list.count(chr(i + 97))) + " presses (", end="")
                print("%.2f" % round(input_list.count(chr(i + 97)) / len(input_list) * 100.0, 2), end="")
                print("% of all alphanumeric presses.)")
            break
        elif show_full_stats == "n":
            print("Exiting.")
            break
        else:
            print("Invalid response. ")

exit()
