import pickle

from vb2html import SiteGen

sitename = 'SRL Archive'
description = 'Archive of the SRL Forums'
prefix='/srl/'
webroot='dist'
exclude_set={30, 7, 129, 136, 6, 481, 14, 285, 91}

with open('srl-archive.pkl', 'rb') as inf:
    wf = pickle.load(inf)

gen = SiteGen(wf, webroot=webroot, exclude_set=exclude_set, prefix=prefix)
gen.build_site()