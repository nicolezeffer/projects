__author__ = 'Nicole Zeffer'
# SI 330 Project #3 - Nicole Zeffer -  nzeffer
# -*- coding: utf-8 -*-
#!/usr/bin/python -tt

import re
from bs4 import BeautifulSoup
import json, urllib2
import time
import sys
import graphviz, pydot
import itertools
reload(sys)
sys.setdefaultencoding("utf-8")





################# Step 1. #################
# Fetch the IMDB top 100 movies (by number of votes) page using this URL: http://www.imdb.com/search/title?at=0&sort=num_votes&count=100 (Links to an external site.)
# and save it in a HTML file named step1.html. The saved HTML file should look similar to (but does not have to be character-for-character identical to) step1_desired_output.html.  Note that a few movies have titles or actors with, e.g. accented characters. Make sure you use the utf8 encoding to write out the HTML to use Unicode and preserve any non-English characters.
def grab100(url):
    response = urllib2.urlopen(url)
    html_doc = response.read()
    html_doc.encode('utf8')
    with open('step1.html', 'w') as fid:
        fid.write(html_doc)






################# Step 2. #################

# Parse the HTML page above with BeautifulSoup, extract movie information as described below, and save the result in a tab-delimited file named step2.txt.
# Your step2.txt file should have 3 columns and 100 rows. The 3 columns should be:
# IMDB_ID
# Rank
# Title

# The IMDB_ID is the part that sits between last two slashes in the movie URL in the table.
# For example, if the URL is http://www.imdb.com/title/tt0111161/, the IMDB ID is tt0111161
# Your tab-delimited step2.txt file should look a lot like step2_desired_output.txt.
# However, we have noticed a bug in BeautifulSoup 4 that sometimes seems to truncate this top-100 table after the first 50 rows.
# So it's OK if your output (and mine) only have the top 50 movies.

# Here's a sample of the first four lines:
# tt0111161   1     The Shawshank Redemption (1994)
# tt0468569   2     The Dark Knight (2008)
# tt1375666   3     Inception (2010)
# tt0110912   4     Pulp Fiction (1994)

def parse100(url):
    response = urllib2.urlopen(url)
    html_doc = response.read()
    html_doc.encode('utf8')
    soup = BeautifulSoup(html_doc, 'html.parser')

    idresults = []
    rankresults = []
    titleresults = []

    for ids in soup.find_all('span'):                              #finding IDs
        id = ids.get('data-tconst')
        if id != None:
            id = id.encode('utf8')
            idresults.append(id)

    for ranks in soup.find_all('td', {"class" : "number"}):        #finding ranks
        for rank in ranks:
            newrank = rank.string
            if newrank != None:
                newrank = newrank.encode('utf8')
                newrank = newrank.strip(" ")
                newrank = newrank.strip(".")
                rankresults.append(newrank)

    for titles in soup.find_all('a'):                              #finding titles
        if titles.parent.name == 'td':
            title = titles.get('title')
            if title != None:
                title = title.encode('utf8')
                titleresults.append(title)

    zipped = zip(idresults, rankresults, titleresults)

    f = open('step2.txt', 'w')
    for movie in zipped:
        f.write(movie[0] + '\t' + movie[1] + '\t' + movie[2] + '\n')
    f.close()

    return idresults






################# Step 3. #################
# Use the Web service http://omdbapi.com/ to get movie metadata for each of the top 100 movies using the IMDB ID you collected in Step 2.
# The API with sample requests is documented on the homepage. For example, this URL fetches JSON for the movie "The Social Network",
# which has IMDB ID tt1285016: http://www.omdbapi.com/?i=tt1285016 (Links to an external site.)

# You should see something like this JSON response:
# {"Title":"The Social Network","Year":"2010","Rated":"PG-13","Released":"01 Oct 2010","Runtime":"120 min","Genre":"Biography, Drama",
# "Director":"David Fincher","Writer":"Aaron Sorkin (screenplay), Ben Mezrich (book)","Actors":"Jesse Eisenberg, Rooney Mara, Bryan Barter,
# Dustin Fitzsimons","Plot":"Harvard student Mark Zuckerberg creates the social networking site that would become known as Facebook, but is
# later sued by two brothers who claimed he stole their idea, and the cofounder who was later squeezed out of the business.",
# "Language":"English, French","Country":"USA","Awards":"Won 3 Oscars. Another 102 wins & 86 nominations.",
# "Poster":"http://ia.media-imdb.com/images/M/MV5BMTM2ODk0NDAwMF5BMl5BanBnXkFtZTcwNTM1MDc2Mw@@._V1_SX300.jpg","Metascore":"95",
# "imdbRating":"7.8","imdbVotes":"326,376","imdbID":"tt1285016","Type":"movie","Response":"True"}

# IMPORTANT!  You MUST pause 5 seconds between EVERY HTTP request to omdbapi.com. If you don't do this, and send requests omdbapi.com
# continuously in a loop with no delay, the server may reject your requests AND MAY EVEN SHUT DOWN.  (Yes, this has happened before.)
# Make sure you call the time module function sleep(5) after each HTTP request call to urlopen to pause for 5 seconds.

# Save your results in a text file named step3.txt that contains a JSON string for each movie on each line. The file
# should look like step3_desired_output.txt.

def getmetadata(idresults):
    url = 'http://www.omdbapi.com/'
    f = open('step3.txt', 'w')
    for id in idresults:
        newurl = url + '?i=' + id
        response = urllib2.urlopen(newurl)
        jsondict = response.read()
        time.sleep(5)
        f.write(jsondict + '\n')
    f.close()






################# Step 4. #################

# After you verify that your step 3 output is correct, you can comment out your URL fetching code for step 3 to avoid running that
# time-consuming step from now on. Now open the file you saved in step 3, load the JSON string on each line into a variable,
# extract just the movie title and actors list, and save the results in a tab-delimited file named step4.txt.

# There should be two columns in your tab-delimited step4.txt file:
# ---
# Movie name
# A JSON string containing the first 4 actors in the actors list.

# The first ten entries in your file should look like this (with a tab character between the movie name and actor list)
# ---
# The Shawshank Redemption   ["Tim Robbins", "Morgan Freeman", "Bob Gunton", "William Sadler"]
# The Dark Knight   ["Christian Bale", "Heath Ledger", "Aaron Eckhart", "Michael Caine"]
# Inception     ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page", "Tom Hardy"]
# Fight Club    ["Edward Norton", "Brad Pitt", "Helena Bonham Carter", "Meat Loaf"]
# Pulp Fiction   ["Tim Roth", "Amanda Plummer", "Laura Lovelace", "John Travolta"]
# The Lord of the Rings: The Fellowship of the Ring    ["Alan Howard", "Noel Appleby", "Sean Astin", "Sala Baker"]
# Forrest Gump   ["Tom Hanks", "Rebecca Williams", "Sally Field", "Michael Conner Humphreys"]
# The Matrix     ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss", "Hugo Weaving"]
# The Lord of the Rings: The Return of the King     ["Noel Appleby", "Ali Astin", "Sean Astin", "David Aston"]
# The Godfather    ["Marlon Brando", "Al Pacino", "James Caan", "Richard S. Castellano"]

def titleandactors():
    f = open('step3.txt', 'r')
    titles = []
    actors = []
    for line in f:
        line = json.loads(line)
        title = (line['Title']).encode('utf8')
        titles.append(title)
        actor = (line['Actors']).encode('utf8')
        actor = actor.split(', ')
        if len(actor) > 4:
            actors.append(actor[:4])
        else:
            actors.append(actor)
    f.close()
    zipped = zip(titles, actors)
    f = open('step4.txt', 'w')
    for item in zipped:
        f.write(item[0] + '\t' + str(item[1]) + '\n')
    f.close()







################# Step 5. #################

# In this step you'll generate the DOT file containing the actor graph, using the pydot module as described in class.
# After downloading and install GraphViz from http://www.graphviz.org/ (Links to an external site.), you should install
# the pydot package in your usual way, e.g. pip install pydot or sudo pip install pydot. Read and try out the examples
# at http://pythonhaven.wordpress.com/tag/pydot/ (Links to an external site.)

# Now load the file you saved in step 4 and generate a graph using the actor lists. Each actor will be a graph node,
# and if two actors are in the actors list (of the first four actors, that is) for the same movie, then there will be
# an edge between them in the graph. Save the resulting graph in a .dot file, which is a plain text file in the DOT
# language.  Note that we don't want to save a PNG file: we want the DOT file instead. The pydot manual at
# http://code.google.com/p/pydot/downloads/list (Links to an external site.) explains how to do this.

# Save your .dot file to a file called actors_graph_output.dot.  It should look like the file actors_graph_desired_output.dot
# supplied in the homework ZIP file.

# HINT:  Suppose A, B, C, D, E is the actors list for a movie. You'll need to add edges for every possible pairs
# of actors in this list, e.g. (A, B)  (A, C) etc. This is where the optional itertools module will come in useful,
# if you choose to use it.  The combinations method will generate every possible pair of elements, given a list.

def generategraph():
    f = open('step4.txt', 'r')
    graph = pydot.Dot(graph_type = 'graph')
    for line in f:                                                 # for title & actors...
        newitems = line.split('\t')
        actors = newitems[1].strip('\n')
        actors = actors.replace('[', '')
        actors = actors.replace(']', '')
        actors = actors.replace("'", "")
        actors = actors.split(', ')

        for actorpair in itertools.combinations(actors, 2):
            edge = pydot.Edge(actorpair[0], actorpair[1])
            graph.add_edge(edge)
    graph.write('actors_graph_output.dot')
    graph.write_png('actors_graph.png')
    f.close()



def generategraph():
    f = open('step4.txt', 'r')
    graph = pydot.Dot(graph_type = 'graph')
    for line in f:
        newitems = line.split('\t')
        actors = newitems[1].strip('\n')
        actors = actors.replace('[', '')
        actors = actors.replace(']', '')
        actors = actors.replace("'", "")
        actors = actors.split(', ')

        for actorpair in itertools.combinations(actors, 2):
            edge = pydot.Edge(actorpair[0], actorpair[1])
            graph.add_edge(edge)
    graph.write('actors_graph_output.dot')
    graph.write_png('actors_graph.png')
    f.close()



################# Step 6. #################

# Open the saved actors_graph_output.dot file you created in step 5 using the gvedit application that comes with GraphViz.
# Using the Graph/Settings dialog, save the graph visualization in a PNG image file named actors_graph.png.
# You can compare the left-most main graph in your result with the corresponding left-most graphs in the partial result
# file actors_graph_desired_output_sample.png provided in the homework ZIP file. (Note: Your PNG image file will be wider
# and have a bunch more little graphlets to the right, compared to the sample.)






################# MAIN CODE #################
imdburl = 'http://www.imdb.com/search/title?at=0&sort=num_votes&count=100'
grab100(imdburl)
globalidresults = parse100(imdburl)
titleandactors()
generategraph()