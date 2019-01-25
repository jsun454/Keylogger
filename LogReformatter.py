import os, textwrap

#directory for all the logs
log_dir = os.path.join(os.getcwd(), "logs")

#describes the program
print("This program reformats keylog files to make them easier to read. It combines key-presses into the same line and applies all backspace and spacebar presses.")

while(True):
    #ask the user for a file to reformat
    log_name = input("Enter the name of the log file to reformat (E.g. '2018-01-01.txt'). Enter 'all' to reformat all logs or enter '0' to exit.\n")

    if log_name == "0": #exits the program if '0' is pressed
        print("\nProgram exiting.")
        break
    elif not os.path.exists(log_dir): #outputs an error if 'logs' folder doesn't exist, then creates a 'logs' folder
        os.makedirs(log_dir)
        print("\nError: Log directory not found. Run 'Keylogger.pyw' to generate log files in the 'logs' folder.\n\n")
    elif len(list(file for file in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, file)))) == 0: #outputs an error if there are no logs in the 'logs' folder
        print("\nError: Log directory is empty. Run 'Keylogger.pyw' to generate log files in the 'logs' folder.\n\n")
    elif not (log_name in list(file for file in os.listdir(log_dir) if os.path.isfile(os.path.join(os.path.join(log_dir, file)))) or log_name.lower() == "all"): #outputs an error if the user-inputed file name doesn't exist
        print("\nError: Log file name not found. Log files must be located in the 'logs' folder.\n\n")
    elif os.path.splitext(log_name)[0][-2:] == "_r": #outputs an error if the user-inputed file is itself a reformatted file
        print("\nError: The specified file has already been reformatted. Choose a file that does not end in '_r' to be reformatted.\n\n")
    else:
        #adds all logs in the logs folder to Log_list if the user requested all logs to be reformatted. otherwise, this adds only the user's selected log to log_list
        log_list = list(log_file for log_file in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, log_file)) and os.path.splitext(log_file)[0][-2:] != "_r") if log_name.lower() == "all" else [log_name]

        #loops through each log in log_list and reformats to a new file
        for log_file in log_list:
            with open(os.path.join(log_dir, log_file)) as log:
                #add the keystroke from each line of the log file into input_list
                input_list = [(line[line.find("'") + 1:line.find("'", line.find("'") + 1)] if line.find("Key") == -1 else line[line.find("K"):-1]) for line in log.readlines()]

            #deletes all non-alphanumeric characters and applies all spacebar and backspace presses
            for i, key in enumerate(input_list):
                if len(key) != 1:
                    if key == "Key.space":
                        input_list[i] = " "
                    elif key == "Key.backspace":
                        #deletes the nearest character before this one that isn't another backspace key and that also wasn't deleted by another backspace key. if no such character exists then don't do anything
                        n = 1
                        while(i >= n):
                            if(input_list[i - n] != ""):
                                input_list[i - n] = ""
                                break
                            else:
                                n += 1
                        input_list[i] = ""
                    else:
                        input_list[i] = ""

            #wraps the list of key inputs into lines with a max width of 100
            reformatted_inputs = textwrap.wrap("".join(input_list), 100)

            #creates a new file for the reformatted logs and overrides the existing file for the reformatted log if one exists
            file = open(os.path.join(log_dir, os.path.splitext(log_file)[0]) + "_r.txt", "w")

            #writes each textwrapped line to the reformatted log file
            for line in reformatted_inputs:
                file.write(line + "\n")

            file.close()

        if(log_name.lower() == "all"):
            print("\nAll logs have been reformatted. Exiting.")
            break
        else:
            print("\nThe file '" + log_name + "' has been reformatted.\n\n")

exit()
