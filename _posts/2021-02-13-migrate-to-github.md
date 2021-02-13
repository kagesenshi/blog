---
layout: post
title: Migrated to Github Pages
date: "2021-02-13 19:39 +0800"
image: assets/images/2021/github-pages.jpg
---

This blog, originally created circa 2005, was originally hosted 
on top of [Google's Blogger](http://blogger.com). At the time, Blogger
was a decent free platform, which works fine for my needs. This blog was
originally created as a platform for me to share my thoughts, which,
is pretty much taken over by social platforms such as [Facebook](http://facebook.com)
nowadays. 

The move to social feed platforms have pretty much made me wonder what to
put on this blog, and one conclusion that I've reached was to use it
mostly to post tech tutorials and howtos. However, due to the limited
features of Blogger, I regularly faced frustrations when writing on its
editor, primarily with the lack of tools for handling code snippets. 

I've reviewed [Wordpress](http://wordpress.com) and [Medium](http://medium.com)
but Wordpress seems kinda overkill for my needs, while Medium have similar 
limitations as Blogger. Having regularly used [Sphinx](http://www.sphinx-doc.org)
and [RestructuredText](https://docutils.sourceforge.io/rst.html) for my documentation 
needs, which I found pleasant for writing, made me wish for a blog platform out there
that works with RST. When I discovered Github Pages can be used to host static sites
for free, I decided that I would want to migrate this blog to it, and use some form
of static site generator to generate things from RST. 

Years of procrastination later, I stumbled upon [Ablog](https://ablog.readthedocs.io/) 
which is basically Jekyll-like extension for Sphinx, which I finally get around 
to try it out, however, its lack of Blogger migration tool, a not-that-straightforward
way to customize how things are rendered, and also the fact that it is a project
that is now stuck in maintenance mode, made it not that attractive to use.

Finally I decided to try out [Jekyll](https://ablog.readthedocs.io/), and after a day of
of hacking and tweaking, finally, this blog is migrated to GitHub. It is still not RST,
but at least it is not as bad as the editor at Blogger, and I can customize and automate
quite a bit of things. Jekyll still have some quirks that annoys me, primarily the part
where it list down all posts from beginning of time in its category/tag pages, but with
some tweaks I managed to made it a bit bearable. 

Hopefully now that this blog is on markdown+git, I can be a bit more motivated
to write again.
