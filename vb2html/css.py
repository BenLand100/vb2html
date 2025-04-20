main_css = '''
:root {
  --bg: #f0f2f5;
  --card-bg: #ffffff;
  --border: #dddddd;
  --primary: #0077cc;
  --secondary: #555555;
  --text: #333333;
  --code-bg: #f2f2f2;
  --shadow: rgba(0, 0, 0, 0.1);
}
html {
  font-family: 'Trebuchet MS', 'Arial', sans-serif; font-weight: 400;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
}
body {
  max-width: 1000px;
  margin: auto;
  padding: 1rem;
}
a {
  color: var(--primary);
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
h1, h2, h3 {
  color: var(--secondary);
  margin: 0.5rem 0;
}
img {
  max-width: 100%;
  border-radius: 4px;
}
code, pre {
  background: var(--code-bg);
  font-family: 'Courier New', monospace;
}
pre {
  padding: 1rem;
  border-radius: 4px;
  overflow: auto;
  max-height: 600px;
}
'''  

forum_css = '''
.forumgroup,
.thread,
.post {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  box-shadow: 0 2px 4px var(--shadow);
  margin-bottom: 1rem;
  padding: 1rem;
}
.forumgroup {
  display: flex;
  flex-direction: column;
}
.forumgroup h2 {
  margin: 0 0.5rem;
}
.forums {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.subform {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}
.subdescr {
  max-width: 60%;
  text-align: right;
}
'''  

thread_css = '''
.threadhead h3 {
  margin: 0;
}
.threadmeta {
  font-size: 0.9rem;
  color: var(--secondary);
}
.who {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.5rem;
  margin-bottom: 0.5rem;
}
.postbody {
  padding: 0.5rem 0;
}
'''
