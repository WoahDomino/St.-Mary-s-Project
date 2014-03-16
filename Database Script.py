#Database Script.  Works with turning my XML Database (FoodBlogDatabase.xml)
#into a data structure that is usable by my finder program
#That data structure is pickled and the .p file referenced by the finder


#Import statements... made because of how important they are
#...in other news..I may be a terrible person
import xml.etree.cElementTree as ET
import cPickle as pickle

#Blogs are stored and handled as objects composed of two fields
#values is a dictionary where strings are mapped to integers 
    #The Strings used are the different categories (outside of name) given to each blog in FoodBlogDatabase.xml
    #I haven't completely given up the idea of making 17 variables and getting rid of the dictionary entirely...Just a matter of getting around to it 
    #Name is the only field where it is easier to call by name than iterating through things at the moment.  
class Blog:
    def __init__(self):
        self.data=[]
        self.name=""
        self.values={}
    #Gets and Sets for string Name
    def setName (self, n):
        self.name = n
    def getName(self):
        return self.name
    #Methods to add and remove values from the dictionary... remove isn't really ever used, but might be useful one day
    def AddValue (self, key, value):
        self.values[key]=value
    def RemoveValue(self, key):
        del self.values[key]
        
#database acts as a list of Blogs.  It is this that is eventually pickled
#the finder application examines this datastructure when looking for new blogs to suggest
database = []

#Finds the root node in the XML document
def FindRoot ():
    tree = ET.parse('FoodBlogDatabase.xml')
    root = tree.getroot()
    return root

#Creates a new object blog and fills in all valuable information
def CreateBlog(blog):
    newBlog = Blog()
    newBlog.setName(blog.attrib['Name'])
    for quality in blog:
            #URL is not added to the dictionary values 
            if quality.tag == "URL":
                continue
            #All other qualities are
            else:
                newBlog.AddValue(quality.tag, int(quality.text))
    return newBlog

#main method, calls methods to iterate through xml nodes and create a Blog for each

def main():
    global ET
    global database
    root = FindRoot()
    for blog in root:
        newBlog=CreateBlog(blog)
        #Once a new blog has been created, it's added to the list database
        database.append(newBlog)
    #Once there are no more nodes to turn into Blogs, we pickle database 
    pickle.dump(database, open ("save.p", "wb"))


            


