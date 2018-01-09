import time
import urllib
import urllib.request


import bs4
import requests

start_url  = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Philosophy"



def text_typing(text, speed =0.07):
    for i in range(len(text)):
        print(text[i]+"", end='', flush=True)
        time.sleep(speed)
        #text_typing('\n')

def find_first_link(url):
    #Get the html of the url and run it through BeautifulSoup
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    #find the div with id mw-content-text and class mw-parser-output
    content_div = soup.find(id="mw-content-text").find(class_ = "mw-parser-output")

    #create article_link so that it will either save the first link or none if N/A
    article_link = None

    #find all direct children of content_div that are p elements
    for element in content_div.find_all("p", recursive=False): #recursive = false so that we only get direct children
        if element.find("a", recursive=False):
            article_link = element.find("a", recursive=False).get('href')
            break
    #if article_link is still None, then nothing else needs to be done as there are no links
    if not article_link:
        return

    #if article_link is not None then we found a link and we need to create a valid url
    first_link = urllib.parse.urljoin('https://en.wikipedia.org/', article_link)
    return first_link

def continue_crawl(search_history, target_url, max_steps=25):
    """Function is used so that it will tell it to continue to search unless it meets the conditions
        we want the max number of iterations to be set to 25 but the user can change it later
    """

    if search_history[-1] ==  target_url:
        text_typing("Target Article found!")
        return False
    elif len(search_history) > max_steps:
        text_typing("Running for too long, reached max...Aborting search\n")
        return False
    elif search_history[-1] in search_history[:-1]:
        text_typing(search_history[-1] + "\n")
        text_typing('We already saw the {} article! We must have run into a cycle...\nAborting search!\n'.format(search_history[-1]))
        return False
    else:
        return True

def check_if_real_wiki_page():
    wiki_topic = input("Great! Give me topic and I'll check if its a real wiki page:\n")
    while(wiki_topic != "no"):
        wiki_link = urllib.parse.urljoin('https://en.wikipedia.org/wiki/', wiki_topic)
        try:
            status = urllib.request.urlopen(wiki_link).getcode()
            text_typing("Article found!\n")
            return wiki_link
        except:
                text_typing("Sorry I couldn't find an article on {}\n Input anothe article or type no to use default\n".format(wiki_topic))
                wiki_topic = input("")
    return None

intro = "Hello! Welcome to the wiki web crawler!\nThe wiki web crawler continues to click on the first link of a wiki page until it either finds the target wiki page \nor encounters a problem such as a cycle.\n"
question = "The wiki web crawler chooses a random wiki article as its starting point.\nWould you like to set a specific starting article? (yes or no)\n"
text_typing(intro+question)
choose_starting_article = input("")

if choose_starting_article == "yes":
    wiki_link = check_if_real_wiki_page()
    if wiki_link:
        start_url = wiki_link
elif choose_starting_article == "no":
    text_typing("Ok.\n")
else:
    text_typing("I'm not sure what you meant but I'm going to go with no...\n")

text_typing("By default the target article is Philosophy.\nWould you like to change it? (yes or no)\n")
choose_target = input("")
if choose_target == "yes":
    wiki_link = check_if_real_wiki_page()
    if wiki_link:
        target_url = wiki_link
else:
    text_typing("Ok\n")

text_typing("One last thing.\nThe default for the wiki web crawler is to check if it can find the target article in a max of 25 iterations.\nWould you like to change it?(yes or no)\n")
change_max_steps = input("")
max_steps = 25
if change_max_steps == "yes":
    try:
        text_typing("What should be the new max?\n")
        max_steps= int(input())
    except:
        text_typing("Thats not an integer! Choosing default\n")
else:
    text_typing("OK. Using default\n")

article_chain = [start_url]

text_typing("Ok lets start! I'll print the urls as I search...\n")
text_typing("Searching and clicking...\n")
#Loop through ("Click") articles until we find or abort
while continue_crawl(article_chain, target_url,max_steps):
    #text_typing each article as we visit it
    text_typing(article_chain[-1] + "\n", 0.05)
    first_link = find_first_link(article_chain[-1])

    #If we get None back then article has no links
    if not first_link:
        text_typing("Looks like this article has no links...Aborting search!\n")
        break
    article_chain.append(first_link)

    #Slow program so to not spam wikipedia's servers
    time.sleep(2)
