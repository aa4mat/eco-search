import webbrowser
import random
from typing import TextIO, Tuple, Optional
import os

browser = "https://google.com/"


def user_input(url: str):
    """Takes input and performs search."""
    print("Launching...\n")
    print("Find something sustainable today!\nEnter a search term, as you normally would on Google. We'll find you sustainable alternatives.\n")
    keyword = input("Search for something.")
    syntax = get_syntax(url)
    path = '/Users/aeolianblue/Downloads/keywords - Sheet1.csv'
    launch_search(syntax, path, keyword, url)


def get_syntax(url: str) -> str:
    """Turns out, every search engine uses unique syntaxes, so here we go."""
    if any(x in url for x in ["google", "bing", "aol"]):
        # if url contains any of ^
        return "search?q="
    elif "duckduckgo" in url:
        return "?q="
    elif "yahoo" in url:
        return "search?p="
    elif "ask" in url:
        return "web?q="
    elif "wolframalpha" in url:
        return "input/?i="
    # if it isn't one of these, it's google by default


def launch_search(syntax: str, path: str, keyword: str, url: str) -> None:
    with open(path) as file:
        sustainable_list = file.readlines()
        if syntax is None:
            syntax = ''

    sust = sustainable_list[random.randrange(0, len(sustainable_list))].strip('\n')

    webbrowser.open_new(url + syntax + '+'.join(sust.split(" ")) + '+' + '+'.join(keyword.split(" ")))

# For privileged DuckDuckGo users:


def get_browser(default: str = browser) -> str:  # Sorry about that.
    """Set a default browser"""
    # TODO: Different browsers have different search syntaxes.
    # google uses "search?q="
    # duckduckgo uses "
    url = default.lower()
    if url is None or url =='':
        return browser
    if "https://" not in url:
        url = "https://" + url
    if "aol" in url:
        if "search." not in url:
            url = url.split("//")[1]  # remove everything below and re-add
            url = "https://search." + url  # because it makes my life simpler
    if "wolframalpha" in url:
        if "www." not in url:
            url = url.split("//")
            url = url[0] + "//www." + url[1]
    if ".com" not in url:
        url = url + ".com/"

        return url


def set_browser() -> Tuple[bool, str]:
    ch = input("Would you like to set up a default search engine?\n We support Google, Yahoo, Ask, Bing, Aol, WolframAlpha and DuckDuckGo!\n(Y/N)")

    if ch in "YyYesyesYES":
        url = get_browser(input("\nEnter your browser of choice."))
        return True, url.lower()
        # configure global browser
    else:
        return False, browser


def new_browser(cachefile: TextIO):
    """If browser doesn't already exist.
    This is an upcoming feature still under construction!"""
    # TODO!
    flag, chosen_browser = set_browser()
    if flag:
        cachefile.write(str(flag) + "," + chosen_browser)
        ind = [flag, chosen_browser]
        if ind[1] != '':
            url = ind[1]
        return url  # if user just hit Enter, use default


def try_browser(cachefile: TextIO):
    """If browser exists.
    This is an upcoming feature still under construction!"""

    cachefile.seek(0)  # just making sure
    ind = cachefile.readline().split(',')

    if ind[0] and (ind[1] != ''):  # True that they set up a default browser
        # Also True that they didn't just hit Enter
        url = ind[1]
        return url


def reset_browser(cachefile: TextIO) -> str:
    """Reset existing browser.
    This is an upcoming feature still under construction!"""
    warn = input("Are you sure you want to reset your browser?\n"
                 "Any present configurations will be lost.\n")
    if warn in "YesyesYESYyyeahokayfinenevermindnvmdoit": # yes, I'm considerate
        cachefile.truncate(0)
        return new_browser(cachefile)


def intro_greet():
    import time
    print("\n\nHello, welcome to the sustainable browser!\n"
          "We help you make sustainable choices. Let's get you started.\n"
          "There's a bunch of cool stuff you can do from here.\n")


def hidden_cool_function() -> None:
    """Programmers may be rumoured to never sleep, but Python dozes off
    sometimes. Who knew?
    """
    import time
    time.sleep(6)
    print("... wait,zz— wh- what? I'm awake!")


def main_menu() -> bool:
    """This code's main menu. Handy for navigation!"""

    print("Choose what you want to do.\n"
          "Search: Use our cool search feature! \t\t(Press S)\n"
          "Thinking of trying a different browser? Reset browser\t(Press R)\n"
          "Just wanted a quick wow today? Press W\n"
          "Looking for your way out? Press X to exit\n")
    ip = input()
    if ip in 'Ss':  # search time!
        url = set_up()
        user_input(url)
    elif ip in "Rr": # reset browser
        # need the cachefile here somehow!
        # TODO!
        with open("cache_file.txt", 'w') as cachefile:
            url = reset_browser(cachefile)
        pass
    elif ip in "Ww":
        hidden_cool_function()
    elif ip in "Xx":
        return False
    return True

def set_up() -> str:
    """Browser configuration only. Configures url."""
    url = browser
    # SET UP A BROWSER ONLY ONCE
    try:
        with open("cache_file.txt", 'r+') as cachefile:
            url = try_browser(cachefile)

    except IOError:
        with open("cache_file.txt", 'w') as cachefile:
            url = new_browser(cachefile)
    finally:
        return url

# main functions that drive everything (call all others) are set_up() and
# user_input(). Special functions: reset_browser() and feature function hidden()


if __name__ == '__main__':
    intro_greet()
    url = browser

    run = True
    while run:
        run = main_menu()

    # reach here only if run is False and user wants out
    print("Sad to see you go. Until next time!")
    exit(0)

