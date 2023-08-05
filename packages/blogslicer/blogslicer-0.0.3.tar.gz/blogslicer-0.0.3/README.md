# Blog Slicer
> Slices & Dice single-file journal.md into separate Jekyll blog posts for publishing on Github Pages.


Keep a single file for all your journaling and blog posts, and with a single command, slice & dice them into individual files formatted for a Jekyll blog easily hosted on Github.

## Install

`pip install blogslicer`

## How to use

```bash
blogslicer -a "Author" -p "Folder" -t "Blog Name" -s "blog"
```

Warning: this is in alpha and I'm still figuring out how to make a pip installable package into a standalone command-line tool without cloning the repo and running it like:

```bash
python blogslicer/core.py -a "Author" -p "Folder" -t "Blog Name" -s "blog"
```
