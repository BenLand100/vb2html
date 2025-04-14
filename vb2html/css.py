main_css ='''
html {
  font-family:
    'Trebuchet MS',
    'Arial',
    sans-serif;
  font-weight: 400;
}
body {
  max-width: 900px;
  margin: auto;
  padding: 0.75em;
}
h1 {
  text-align: center;
}
a {
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
img {
    max-width: 100%;
}
blockquote {
  background: #f9f9f9;
  border-left: 3px solid #ccc;
  margin: 0.5em 10px;
  padding: 0.5em 10px;
}
code {
  font-family:
    'Courier New',
    monospace;
  background: #f9f9f9;
}
pre {
  background: #f9f9f9;
  margin: 1.5em 10px;
  padding: 0.5em 10px;
  overflow: auto;
  max-height: 600px;
}
'''

forum_css = '''
.forumgroup {
}
.subforums {
}
.subform {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.subdescr {
  max-width: 40%;
  text-wrap: balance;
  text-align: right;
}
.threads {
}
.thread {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.thread:firstchild {
  margin: 0;
}
.threadhead {
  h3 {
    margin: 8px 0 8px 0;
  }
  p {
    margin: 8px 0 8px 0;
  }
}
.threadmeta {
  width: 20%;
  p {
    margin: 8px 0 8px 0;
  }
}
'''

thread_css = '''
.post {
  display: block;
}
.who {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.postbody {
  padding: 10px 0 10px 0
}
'''
