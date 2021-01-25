# asks the user to enter a choice from the given options
# if options is a dictionary, a key represents the displayed text and its value is what is returned
# if options is a list or tuple, the selected value is returned
def get_choice(options, text = ''):
    options_type = None
    if type(options) is dict:
        options_type = 'dict'
    elif type(options) is list or type(options) is tuple:
        options_type = 'list'
    else:
        raise Exception('get_choice must be used with dictionaries, lists, or tuples!')
        
    if len(options) < 1:
        raise Exception('get_choice must contain at least 1 option!')
    
    if options_type == 'dict':
        indexed_options = [option for option in options.keys()]
    
    # loop until a valid option is selected
    while True:
        print(text)
        # for every given option
        for index, option in enumerate(options):
            print(f'{index+1}: {option}')
        try:
            # user enters a number corresponding to the displayed option
            choice = int(input()) - 1
            if choice not in range(len(options)):
                raise ValueError
        except ValueError:
            print('Invalid choice.\n')
            continue
        
        if options_type == 'dict':
            choice = indexed_options[choice]
            return options[choice]
        elif options_type == 'list':
            return options[choice]