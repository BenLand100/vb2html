import os

from .bbcode import BBCodeVB4

try:
    from IPython.display import display, HTML
    def test_render(html, *css_fragments):
        css = "\n".join(css_fragments)
        wrapper = f"<div><style>{css}</style>{html}</div>"
        display(HTML(wrapper))
except:
    pass
        
class HTMLGen:
    '''Contains all the HTML fragments'''

    def __init__(self, sitename='SRL Archive', bbcode=None, old_domain='villavu.com', prefix='/srl/', exclude_set={}):
        if bbcode is None:
            self.bbcode = BBCodeVB4(prefix=prefix, old_domain=old_domain)
        else:    
            self.bbcode = bbcode
        self.sitename = sitename
        self.exclude_set = exclude_set
        self.prefix = prefix
         
    def href(self, asset):
        return f'href="{os.path.join(self.prefix, asset)}"'
        
    def title(self, f):
        if f.forumid == -1:
            return f'<h1>{f.title}</h1>'
        else:
            return f"<h1><a {self.href('')}>{self.sitename}</a> - {f.title}</h1>"
        
    ### Thread Page

    def post_fragment(self, f, t, p): 
        return f'''
<div class="post">
<div class="who">
<h3>{p.username}</h3>
<p>{p.timestamp}</p>
</div>
<div class="postbody">
{self.bbcode.render(p.text)}
</div>
</div>
'''

    def thread_view(self, f, t):
        forum_link  = self.href("")
        thread_link = self.href(f"f/{f.forumid}/")

        sep        = "\n<hr>\n"
        posts_html = sep.join(
            self.post_fragment(f, t, p)
            for p in t.posts
        )

        return f"""
            <h1>
            <a {forum_link}>{self.sitename}</a>
            -
            <a {thread_link}>{f.title}</a>
            </h1>
            <h2>{t.title}</h2>
            <hr>
            {posts_html}
        """

### Forum Page

    def thread_fragment(self, f, t): 
        return f'''
<div class="thread">
<div class="threadhead">
<h3><a {self.href(f't/{t.threadid}/')}>{t.title}</a></h3>
<p>{t.postusername} - {t.firstpost}</p>
</div>
<div class="threadmeta">
<p>Last Post: {t.lastpostusername}<br>{t.lastpost}<br>Posts: {len(t.posts)} Views: {t.views}</p>
</div>
</div>
'''

    def child_fragment(self, f, c, h='2'): 
        return f'''
<div class="subform">
<h{h}><a {self.href(f'f/{c.forumid}/')}>{c.title}</a></h{h}>
<p class="subdescr">{c.description}</p>
</div>
'''

    def reg_forum_view(self, f):
        title_html = self.title(f)
    
        sub_sep  = "\n<hr>\n"
        sub_html = sub_sep.join(
            self.child_fragment(f, c)
            for c in f.children
        )
    
        thr_sep  = "\n<hr>"
        thr_html = thr_sep.join(
            self.thread_fragment(f, t)
            for t in f.threads
            if t.posts  # same as len(t.posts) > 0
        )
    
        return f"""
            {title_html}
            <div class="subforums">
            {sub_html}
            </div>
            <hr><hr>
            <div class="threads">
            {thr_html}
            </div>
        """


    def group_forum_view(self, f):
        title_html = self.title(f)

        group_sep   = "\n<br><br>\n"
        child_sep   = "<hr>\n"

        groups = []
        for subf in f.children:
            if not (subf.children or subf.threads):
                continue
            if subf.forumid in self.exclude_set:
                continue

            if not subf.threads:
                header = f'<div class="forumgroup">\n<h2>{subf.title}</h2>'
            else:
                link = self.href(f"f/{subf.forumid}/")
                header = f'<div class="forumgroup">\n<h2><a {link}>{subf.title}</a></h2>'

            desc = f'<p>{subf.description}</p><hr>'

            children_html = child_sep.join(
                self.child_fragment(subf, c, h=3)
                for c in subf.children
            )

            # close the div
            footer = "</div>"

            groups.append(header + desc + children_html + footer)

        groups_html = group_sep.join(groups)

        return f"""
    {title_html}
    <div class="forums">
    {groups_html}
    </div>
    """


    def forum_view(self, f):
        if len(f.threads) == 0:
            if len(f.children) == 0:
                return ''
            return self.group_forum_view(f)
        return self.reg_forum_view(f)
        
    def html_page(self, body, title='SRL Forums | Archive', description=''): 
        return f'''<!DOCTYPE html>
<html lang="en-us">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" {self.href('style.css')}/>
</head>
<body>
<main>
{body}
</main>
</body>
</html>
'''
