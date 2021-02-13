import re
from copy import copy
import yaml
import argparse
from slugify import slugify
import os

urlre = re.compile(r'^<a class=".*?" href="(.*?)">$')

parser = argparse.ArgumentParser()
parser.add_argument('input_dir')
parser.add_argument('output_dir')

args = parser.parse_args()


def extract(input_file):
    tags = []
    data = {}
    with open(input_file) as f:
        found = False
        for i in f:
            i = i.strip()
            if found:
                data['name'] = i
                tags.append(copy(data))
                data = {}
                found = False
                continue
            m = urlre.match(i)
            if m:
                href = m.groups()[0]
                found = True
                data['permalink'] = href
   
    return tags

def capitalize(s):
    return s[0].upper() + s[1:]

def write(output_dir, tags, type_, layout):
    for tag in tags:
        slug = slugify(tag['name'])
        path = os.path.join(output_dir, '%s-%s.md' % (type_, slug))
        with open(path, 'w') as of:
            lines = []
            lines.append('---')
            lines.append('layout: %s' % layout)
            lines.append('%s-name: %s' % (type_, tag['name']))
            lines.append('title: %s - %s' % (capitalize(type_),
                capitalize(tag['name'])))
            lines.append('permalink: "%s"' % tag['permalink'])
            lines.append('---')
            of.write('\n'.join(lines))
        print('Written %s' % path)

# categories
cats = extract(os.path.join(args.input_dir, 'categories.html'))
write(args.output_dir, cats, 'category', 'categories')
tags = extract(os.path.join(args.input_dir, 'tags.html'))
write(args.output_dir, tags, 'tag', 'tags')
