import datetime as dt

class Forum:
    '''Abstraction of a VB4 forum'''
    
    def __init__(self, data):
        if type(data) == dict:
            self.forumid = data['forumid']
            self.title = data['title']
            self.description = data['description']
            self.displayorder = -1
        else:
            self.forumid = data.forumid
            self.title = data.title
            self.description = data.description_clean
            self.displayorder = data.displayorder
        self.children = []
        self.threads = [] 
        
    def __repr__(self):
        return f'{self.forumid} {self.title}'
        
    def walk(self, fn, depth=False):
        if type(depth) == bool and depth:
            depth = 0
        if type(depth) == int:
            fn(self, depth)
            for child in self.children:
                child.walk(fn, depth+1)
        else: 
            fn(self)
            for child in self.children:
                child.walk(fn)

class Thread:
    '''Abstraction of a VB4 thread'''
    
    def __init__(self, data):
        self.threadid = data.threadid
        self.title = data.title
        self.lastpost = dt.datetime.fromtimestamp(data.lastpost)
        self.firstpost = dt.datetime.fromtimestamp(data.dateline)
        self.postusername = data.postusername
        self.postuserid = data.postuserid
        self.lastpostusername = data.lastposter
        self.lastpostuserid = data.lastposterid
        self.views = data.views
        self.posts = []
        
    def __repr__(self):
        return f'{self.threadid} {self.lastpost} {self.postusername} {self.title}'
        
class Post:
    '''Abstraction of a VB4 post'''
    
    def __init__(self, data):
        self.postid = data.postid
        self.parentid = data.parentid
        self.timestamp = dt.datetime.fromtimestamp(data.dateline)
        self.userid = data.userid
        self.username = data.username
        self.text = data.pagetext
        
    def __repr__(self):
        return f'{self.postid} {self.timestamp} {self.username} {self.text[:min(len(self.text),25)]}'
