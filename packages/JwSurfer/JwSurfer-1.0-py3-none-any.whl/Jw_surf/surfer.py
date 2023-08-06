'''
This module is to surf to the main pages of Jw.og and to download publications from it.
'''

from browseJw import browse


class JwSurfer:
    '''
    This class contains methods to surf the main pages of Jw and to download publications from Jw.org and save to a Folder. 
    '''

    def showInfo():
        print("-------Usage-------")
        print("[-h] >> To navigate to the home page")
        print("[-n] >> To navigate to the news-room page")
        print("[-l] >> To navigate to the Library page")
        print("[-bt] >> To navigate to the Bible teachings page")
        print("[-a] >> To navigate to the about page")
        print("[quit] >> To quit the program")

    while True:
        showInfo()
        user_input = str(input())
        if user_input.lower() == "quit":
            break
        if user_input.lower() == "-h":
            browse(user_input)
        elif user_input.lower() == "-n":
            browse(user_input)
        elif user_input.lower() == "-l":
            browse(user_input)
        elif user_input.lower() == "-bt":
            browse(user_input)
        elif user_input.lower() == "-a":
            browse(user_input)
        else:
            print("input a valid Argument")
            print("Your input was ", user_input.lower())
            print("Please refer the usage for proper input")
            # showInfo()
