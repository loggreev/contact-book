# asks the user to enter a choice from the given options
# options is a dictionary with a key representing the displayed text and a value representing a function to call
# returns the value of the user's choice
def get_choice(options):
    indexed_options = [option for option in options.keys()]
    if len(indexed_options) < 1:
        raise Exception('get_choice must contain at least 1 option!')
    # loop until a valid option is selected
    while True:
        # for every given option
        for index, option in enumerate(indexed_options):
            print(f'{index+1}: {option}')
        try:
            # user enters a number corresponding to the displayed option
            choice = int(input()) - 1
            if choice not in range(len(indexed_options)):
                raise ValueError
        except ValueError:
            print('Invalid choice.\n')
            continue
        choice = indexed_options[choice]
        return options[choice]