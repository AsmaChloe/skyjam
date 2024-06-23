from menu.menu import MenuSubOptions


class OptionsMenu(MenuSubOptions):
    def __init__(self, game, state="Options", previous_state=(None, None)):
        MenuSubOptions.__init__(self, game, state, "Options", ["Sound", "Controls"], previous_state=previous_state)

    def validate(self, text):
        '''
        Validate the current option selected in the menu
        :return:
        '''
        if text == "Sound":
            print("Sound")
        elif text == "Controls":
            print("Controls")
