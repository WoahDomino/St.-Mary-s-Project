#Finder program.  Does the actual leg work of taking in user preferences and making suggestions based on those preference



import random
import cPickle as pickle
import math
import __main__
#import sys


#NOTE TO SELF: Josh told me about latent dirichlet allocation and autotagging
    #That'd allow me to expand my database without reading too many more blogs
    #worth looking into if I have the time...

#Datastructure Blog (seen in Database Script.py) needs to be restated here
#I'm certain there is a way to get around this, but it won't be a problem once this all gets ported to C#
class Blog:
    name=""
    def __init__(self):
        #self.data=[]
        self.name=""
        self.values={}
    def setName (self, n):
        self.name = n
    def getName(self):
        return self.name
    def AddValue (self, key, value):
        self.values[key]=value
    def RemoveValue(self, key):
        del self.values[key]


class SMP:
    global template
    global newBlog
    #Database is loaded from the picke file
    database = []
    
    def loadDatabase(self, path):
        self.database = pickle.load (open(path, "rb"))
    
    #A separate list of the blogs suggested...so we don't get repeats
    suggested = []

    def find_start(self, name):
        """Method to look up the blog selected by its name.
        Takes in a string name as a parameter
        Returns the object Blog that corresponds to whatever string the user entered
        Returns -1 if no such blog is named.. won't be a problem once the UI gets running and the user wont be able to enter a Blog that doesn't exist"""

        for item in self.database:
            #print item.getName()
            if (name == item.getName()):
                return item
        print "No such blog found!"
        return -1

    def find_blog(self):
        """Takes in nothing
        Goes through database by randomly selecting a blog and seeing if that blog has been suggested yet
        if we run out of blogs to try, we're out of blogs! and an error gets thrown.
        Returns the newly selected blog"""
        for i in xrange(len(self.database)):
            newBlog = self.database[ random.randint(0,len(self.database)-1)]
            #print newBlog.getName()
            if (newBlog not in self.suggested):
                return newBlog
        #IF we run out of blogs: 
        print "Out of Blogs!"

    def evaluate_fitness(self, template, newBlog):
        """Does the actual math behind evaluating the fitness of a given blog when compared to our template blog (returned as an int)
        takes in the template (the blog that matches the user's preferences) and a newBlog (one we might suggest)"""
        fitness = 0
        for key in sorted(template.values.keys()):
            #print str(template.values[key]) + " " + str(newBlog.values[key])
            if (template.values[key]!=newBlog.values[key]):
                #In any given category, lets say Memoir, our template blog will have a score (lets say 7)
                #This new blog will also have a score for Memoir (lets say 6).
                #the fitness is calculated by doing the summation of: |(template's score in category) - (new blog's score in category)|
                x = int(template.values[key]) - int (newBlog.values[key])
                fitness = fitness + math.fabs(x)
        return fitness
    
    def checkEval(self, template):
        """Does the actual legwork involved with finding a new blog to suggest to the user
        Pulls 10 randomly selected blogs from the database, checks how much in common it shares with the template blog, and returns the blog with the best score"""
        #global database
        self.database.remove(template)
        #Initially, the best fit is an unreasonably high number (the better a fit is according to my calculations, the closer it is to 0)
        bestFit = 10000
        bestBlog = ""
        for i in xrange (10):
            #First, a blog is randomly selected
            blog = self.find_blog()
            #The blog's fitness is evaluated 
            current = self.evaluate_fitness(template, blog)
            #if the blog's fittness is smaller (and therefore better) than the BestFit number...
            if (bestFit>current):
                #Then the current number becomes the BestFit number and this blog is slated to be suggested 
                bestFit= current
                bestBlog = blog
        self.database.append(template)
        #We add our new blog to the list of blogs that have been suggested and return
        self.suggested.append(bestBlog)
        return bestBlog

    
    def modify_template_blog_LIKE (self, template, newBlog):
        """If the user does like the blog we suggested,
        we change the values in new blog to make sure the matching qualites are increased in their level of importance
        Takes in template (the blog the user asked for) and newBlog (the blog we suggested)
        Returns the newBlog with updated values.  This becomes the new template blog. """
        
        for key in sorted(template.values.keys()):
            if (template.values[key]==newBlog.values[key]):
                newBlog.values[key]= newBlog.values[key]+1
        return newBlog

    def modify_template_blog_DISLIKE(self, template, newBlog):
        """If the user *didn't* like the blog suggested, change the values of what's important in our template blog
        Thinking about changing this a bit..
        Takes in the template blog (what the user entered) and the newBlog (what we suggested)
        changes values in template blog and returns it with its updated scores"""
        for key in sorted(template.values.keys()):
            #If the initial blog and the new blog don't match on a specific field, 
            if (template.values[key]!=self.newBlog.values[key]):
                #decrease the importance of that field in the template by 1
                template.values[key]=self.template.values[key]-1
        #Return our new updated blog
        return template

    def __init__(self, name, path):
        #Add that blog to suggested, so it doesn't get sent back to the user as a suggestion
        self.loadDatabase(path)
        self.template = self.find_start(name)
        self.suggested.append(self.template)


        
        

global S 
def Begin(name, path):
    """Method to make an object of SMP"""
    global S
    S = SMP(name, path)
    print S.find_blog().getName()
    return S

def NewItem():
    """A method so C# can cleanly and easially ask for a new blog
        Takes in nothing, but returns the next suggestion""" 
    S.newBlog=S.checkEval(S.template)
    return S.newBlog.getName()
def LIKE ():
    """A method so C# can cleanly and easially send feedback to an object
        Takes nothing in and returns nothing"""
    S.modify_template_blog_LIKE(S.template, S.newBlog)
def DISLIKE ():
    """A method so C# can cleanly and easially send feedback to an object
        Takes nothing in and returns nothing"""
    S.modify_template_blog_DISLIKE(S.template, S.newBlog)


Begin ("Nostrovia", "C:\Python27\SMP\save.p")
NewItem()
print ("Butts")

    
