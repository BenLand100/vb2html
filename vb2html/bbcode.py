import bbcode # the package, not this file!
import re

PATHOLOGY = '???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????'

class BBCodeVB4:
    
    def __init__(self, old_domain='villavu.com'):
        self.old_domain = old_domain
    
        self.arch_re = re.compile(self.old_domain+r'/forum/archive/index.php/t-(\d+).html')
        
        self.parser = bbcode.Parser(newline='<br>', linker=self.linker)
        self.parser.add_simple_formatter('img','<img src="%(value)s">', swallow_trailing_newline=True, replace_links=False, replace_cosmetic=False, escape_html=False)
        self.parser.add_simple_formatter('html','<pre><code>%(value)s</code></pre>', swallow_trailing_newline=True, replace_links=False, replace_cosmetic=False, escape_html=True, render_embedded=False)
        self.parser.add_simple_formatter('code','<pre><code>%(value)s</code></pre>', swallow_trailing_newline=True, replace_links=False, replace_cosmetic=False, escape_html=True, render_embedded=False)
        self.parser.add_simple_formatter('report','<pre><code>%(value)s</code></pre>', swallow_trailing_newline=True, replace_links=False, replace_cosmetic=False, escape_html=True, render_embedded=False)
        self.parser.add_simple_formatter('simba','<pre><code>%(value)s</code></pre>', swallow_trailing_newline=True, replace_links=False, replace_cosmetic=False, escape_html=True, render_embedded=False)
        self.parser.add_simple_formatter('scar','<pre><code>%(value)s</code></pre>', swallow_trailing_newline=True, replace_links=False, replace_cosmetic=False, escape_html=True, render_embedded=False)
        self.parser.add_simple_formatter('highlight','<pre><code>%(value)s</code></pre>', swallow_trailing_newline=True, replace_links=False, replace_cosmetic=False, escape_html=True, render_embedded=False)
        self.parser.add_simple_formatter('mention','<strong>@%(value)s</strong>')
        self.parser.add_formatter('url', self.url_adv, replace_links=False, replace_cosmetic=False, escape_html=False)
        self.parser.add_formatter('size', self.size_adv)
        self.parser.add_formatter('font', self.font_adv)
        self.parser.add_formatter('quote', self.quote_adv)

    def clean_href(self, href):
        if '://' not in href:
            href = 'https://' + href
        if 'http://' in href:
            href = href.replace('https://','https://')
        if self.old_domain in href:
            href = href.replace('www.'+self.old_domain,self.old_domain)
            if self.old_domain+'/forum/forumdisplay.php?f=' in href:
                href = href.replace(self.old_domain+'/forum/forumdisplay.php?f=',f'{PREFIX}f/')
                href = href.replace('https://','').replace('http://','')
            if arch_re.match(href):
                href = arch_re.replace(f'{PREFIX}t/\1',href)
                href = href.replace('https://','').replace('http://','')
            if self.old_domain+'/forum/showthread.php?t=' in href:
                href = href.replace(self.old_domain+'/forum/showthread.php?t=',f'{PREFIX}t/')
                href = href.replace('https://','').replace('http://','')
        return href

    def linker(self, url):
        href = url
        return f'<a href="{self.clean_href(href)}">{url}</a>'

    def quote_adv(self, tag_name, value, options, parent, context):
        if 'quote' in options:
            who = options['quote']
            try:
                who,whoid = who.split(';')
            except:
                whoid = None
            return f'<blockquote>\n<strong>From: {who}</strong><br>\n{value}\n</blockquote>'
        else:
            return f'<blockquote>\n{value}\n</blockquote>'

    def url_adv(self, tag_name, value, options, parent, context):
        if 'url' in options:
            href = options['url']
        else:
            href = value
        return f'<a href="{self.clean_href(href)}">{value}</a>'


    def size_adv(self, tag_name, value, options, parent, context):
        if 'size' in options:
            try:
                size = float(options['size'])
                if size == 0:
                    size = '50%'
                elif size > 0:
                    size = f'{int(round(100*size)):0d}%'
                else:
                    size = f'{int(round(-100/size)):0d}%'
            except Exception as e:
                print(e)
                size = '100%'
        else:
            size = '100%'
        return f'<span style="display: inline-block; font-size: {size};">{value}</span>'

    def font_adv(self, tag_name, value, options, parent, context):
        if 'size' in options:
            font = options['font']
        else:
            font = 'Trebuchet MS'
        return f'<span style="display: inline-block; font-family: \'{font}\';">{value}</span>'


    def render(self, vbtext):
        try:
            if PATHOLOGY in vbtext:
                vbtext = vbtext.replace(PATHOLOGY,'')
            return self.parser.format(vbtext)
        except:
            return vbtext

