import webbrowser

def browse(page):

    if page == "-h":
        webbrowser.open("https://www.jw.org/en/")
    elif page == "-a":
        webbrowser.open("https://www.jw.org/en/jehovahs-witnesses/")
    elif page == '-n':
        webbrowser.open("https://www.jw.org/en/news/jw/")
    elif page == "-bt":
        webbrowser.open("https://www.jw.org/en/bible-teachings/")
    elif page == "-l":
        webbrowser.open("https://www.jw.org/en/library/")
    else:
        print("Enter a valid input parameter.")