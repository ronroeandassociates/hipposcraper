#!/usr/bin/env python2
"""Module for TestFileScraper"""
from scrapers import *

class TestFileScraper:
    """TestFileScraper class

    Scrapes test files from any projects.

    Args:
        soup (obj): BeautifulSoup obj containing parsed link
    """
    def __init__(self, soup):
        self.soup = soup
        self.pre = self.find_test_files()

    def find_test_files(self):
        return self.soup.select("pre")

    def write_test_files(self):
        sys.stdout.write("  -> Creating test files... ")
        for item in self.pre:
            find_test = item.text.find("cat")
            find_c = item.text.find("main.c")
            find_py = item.text.find(".py")
            find_sql = item.text.find(".sql")
            find_js = item.text.find(".js")
            find_html = item.text.find(".html")

            # find_main checks if there are main files on project page
            if find_test != -1 and (find_c != -1 or find_py != -1 or find_sql != -1 or find_js != -1 or find_html != -1):
                try:
                    user = item.text.split("$", 1)[0]
                    name = item.text.split("cat ", 1)[1]
                    if find_c != -1:
                        name = name.split(".c", 1)[0] + ".c"
                    elif find_sql != -1:
                        name = name.split(".sql", 1)[0] + ".sql"
                    elif find_js != -1:
                        name = name.split(".js", 1)[0] + ".js"
                    else:
                        name = name.split(".py", 1)[0] + ".py"
                    # html edge case test text creation
                    if find_html != -1:
                        text = item.text.split(".html")[1]
                        text = str(text.split(user, 1)[0])
                        text = text.split("\n", 1)[1]
                        name = name.split(".html", 1)[0] + ".html"
                    else:
                        text = item.text.split(name, 1)[1]
                        text = text.split("\n", 1)[1]
                        text = text.split(user, 1)[0]
                        text = text.split("\n")
                    with open(name, "w+") as w_test_file:
                        for i in range(len(text) - 1):
                            if find_html != -1:
                                w_test_file.write(text[i])
                            else:
                                w_test_file.write(text[i].encode('utf-8') + "\n")
                except (AttributeError, IndexError):
                    newlines = 0
                    # Checks if test file's name has more than 1 newline
                    for i in name:
                        if newlines > 1:
                            name = "[Not a test file]"
                            break
                        if i == "\n":
                            newlines += 1
                    sys.stdout.write("[ERROR] Could not create ")
                    sys.stdout.write("test file %s\n" % name)
                    sys.stdout.write("                        ... ")
                    continue
                except IOError:
                    sys.stdout.write("\n     [ERROR] Could not create a specific test file.\n")
                    continue
        print("done")
