# vb2html

This is a Python tool to generate a static site from a database dumb from a VBulletin 4 web forum.
It was nominally made for the [SRL Forums](https://villavu.com/forums/) archive.

A `srl_archive_example.pkl` has a `WebForum` object stored within, containing a small subset of 
the total SRL forums archive. This is provided for testing purposes. It was generated with 
`Generate.ipynb` requiring a MySQL server hosting the VB4 database. You can generate a static 
site in `webroot_example` using this pickle file and `Process.ipynb`.
