import warnings

import pandas as pd
import multiprocessing as mp

from collections import deque
from functools import partial

from .structures import Forum, Thread, Post

class WebForum:
    '''Abstracts and entire VB4 website as a collection of forums threads and posts'''
    
    def __init__(self, sitename='SRL Archive', description='Archive of the SRL Forums'):
        self.sitename = sitename
        self.description = description
        self.root = Forum(dict(forumid=-1, title=sitename, description=description))
        self.forum_map = {self.root.forumid:self.root}
        
    def populate_forums(self, conn, exclude_set=set()):
        '''
        Gathers all forum / subforum metadata from a connection to a MYSQL
        database dump of a VB4 website.
        
        `conn` should be a SQLAlchemy compliant connection object
        '''
        
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            data = pd.read_sql_query('select * from forum order by forumid', conn)
            
        self.forum_map = {self.root.forumid:self.root}
        todo = deque([row for i,row in data.iterrows()])
        skipped = 0
        while len(todo) > 0 and skipped < len(todo):
            row = todo.popleft()
            if row.forumid in exclude_set:
                continue
            if row.parentid not in self.forum_map:
                todo.append(row)
                skipped += 1
                continue
            else:
                skipped = 0
            assert row.forumid not in self.forum_map, 'duplicate forumid'

            f = Forum(row)
            self.forum_map[row.forumid] = f
            self.forum_map[row.parentid].children.append(f)
            print(f)

        def child_sort(f):
            f.children = list(sorted(f.children, key=lambda f: f.displayorder))

        self.root.walk(child_sort)

    def populate_threads(self, conn, max_threads=None):
        '''
        Gathers all thread metadata from a connection to a MYSQL database dump 
        of a VB4 website.
        
        `conn` should be a SQLAlchemy compliant connection object
        '''
        
        def populate_forum_threads(forum):
            print(forum)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                if max_threads:
                    raw = pd.read_sql_query(f'''
                        select 
                            * 
                        from thread 
                        where forumid = {forum.forumid} 
                        and visible = 1
                        order by lastpost desc
                        limit {max_threads}
                    ''', conn)
                else:
                    raw = pd.read_sql_query(f'''
                        select 
                            * 
                        from thread 
                        where forumid = {forum.forumid} 
                        and visible = 1
                        order by lastpost desc
                    ''', conn)
            if len(raw) == 0:
                forum.threads = []
            else:
                forum.threads = list(raw.apply(Thread, axis='columns'))
                
        self.root.walk(populate_forum_threads)
        
    def populate_posts(self, conn, nproc=1, max_posts=None):
        '''
        Gathers all post metadata and content from a connection to a MYSQL 
        database dump of a VB4 website.
        
        `conn` should be a SQLAlchemy compliant connection object unless nproc 
        is greater than 1, then `conn` should be a callable that will return a 
        new connection object.
        '''
        
        def populate_thread_posts(thread):
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                if max_posts:
                    raw = pd.read_sql_query(f'''
                        select 
                            * 
                        from post 
                        where threadid = {thread.threadid}
                        and visible = 1
                        order by dateline asc
                        limit {max_posts}
                    ''', conn)
                else:
                    raw = pd.read_sql_query(f'''
                        select 
                            * 
                        from post 
                        where threadid = {thread.threadid}
                        and visible = 1
                        order by dateline asc
                    ''', conn)
            if len(raw) == 0:
                thread.posts = []
            else:
                thread.posts = list(raw.apply(Post, axis='columns'))
            return thread
        
        def populate_forum_thread_posts(forum):
            print(forum)
            for thread in forum.threads:
                populate_thread_posts(thread)
                
        def mp_populate_forum_thread_posts(forum):
            print(forum)
            with mp.Pool(nproc) as p:
                forum.threads = p.map(partial(_mp_populate_thread_posts, conn, max_posts), forum.threads)
                
        if nproc > 1:
            self.root.walk(mp_populate_forum_thread_posts)
        else:
            self.root.walk(populate_forum_thread_posts)
     
     
_mp_conn = None  
def _mp_populate_thread_posts(get_conn, max_posts, thread):
    global _mp_conn
    if _mp_conn is None:
        _mp_conn = get_conn()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        if max_posts:
            raw = pd.read_sql_query(f'''
                select 
                    * 
                from post 
                where threadid = {thread.threadid}
                and visible = 1
                order by dateline asc
                limit {max_posts}
            ''', _mp_conn)
        else:
            raw = pd.read_sql_query(f'''
                select 
                    * 
                from post 
                where threadid = {thread.threadid}
                and visible = 1
                order by dateline asc
            ''', _mp_conn)
    if len(raw) == 0:
        thread.posts = []
    else:
        thread.posts = list(raw.apply(Post, axis='columns'))
    return thread
