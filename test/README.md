# Generating a test site 

## `srl-archive.pkl`

`srl-archive.pkl` consists of a `WebForum` object stored within, containing a small subset of 
the total SRL forums archive. This is provided for testing purposes. It was generated with 
`Generate.ipynb` requiring a MySQL server hosting the VB4 database. 

## Python
`generate.py` uses our `vb2html` library to generate a static site in `dist` using `srl-archive.pkl`.

## Jupyter
You can generate a static site in `dist` using `srl-archive.pkl` and `Generate.ipynb`.
`Process.ipynb` can be used to generate a pkl file from a MySQL database dump.