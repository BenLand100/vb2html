import os

import multiprocessing as mp

from functools import partial

from .html import *
from .css import *

class SiteGen:
    '''Takes a fully populated WebForum Forum object and emits the static site.'''

    def __init__(self, webforum, webroot='webroot', exclude_set={30, 7, 129, 136, 6, 481, 14, 285, 91}, prefix='/srl/', **kwargs):
        self.webforum = webforum
        self.html = HTMLGen(webforum.sitename, exclude_set=exclude_set, prefix=prefix, **kwargs)
        self.exclude_set = exclude_set
        self.prefix = prefix
        self.webroot = webroot

    def _emit_html(self, path, body):
        path = os.path.join(self.webroot,path)
        base = os.path.dirname(path)
        if not os.path.exists(base):
            os.makedirs(base)
        with open(path,'w') as out:
            out.write(self.html.html_page(body, title=self.webforum.sitename, description=self.webforum.description))
            
    def _generate_thread(self, forum, thread):
        if len(thread.posts) > 0:
            thread_base = f't/{thread.threadid}/' 
            self._emit_html(os.path.join(thread_base,'index.html'), self.html.thread_view(forum, thread))
             
    def _generate_forum(self, forum):
        if int(forum.forumid) in self.exclude_set:
            return
        
        print(forum)
        
        base = f'f/{forum.forumid}/'
        if forum.forumid == -1:
            self._emit_html('index.html', self.html.forum_view(forum))
        else:
            self._emit_html(os.path.join(base,'index.html'), self.html.forum_view(forum))
            
        [self._generate_thread(forum, t) for t in forum.threads]
                
        for child in forum.children: # instead of forum.walk, to avoid generating children of excluded forums
            self._generate_forum(child)
            
    def build_site(self, alt_css=None):
        if not os.path.exists(self.webroot):
            os.makedirs(self.webroot)

        with open(f'{self.webroot}/style.css','w') as out:
            out.write('\n'.join([main_css, forum_css, thread_css] if alt_css is None else alt_css))
            
        self._generate_forum(self.webforum.root)
        
