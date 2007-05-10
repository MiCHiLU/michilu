#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path

def get_filelist(target_path):
    target_dir = os.path.abspath(target_path)
    target_files = [os.path.join(target_dir, f) for f in os.listdir(target_dir)]
    return target_files

def trans_doc(file_path=None, source=None):
    from docutils.core import publish_parts
    if not source:
        try:
            source = open(file_path).read()
        except IOError:
            return None
    trans_doc = publish_parts(source=source, writer_name="html4css1")
    return trans_doc["html_body"]

def find_links(doc):
    from BeautifulSoup import BeautifulSoup
    result = {
        "own": set(),
        "other": set(),
        "outer": set(),
        "break": set(),
        "id": [],
    }
    
    def startswith(link):
        if link.startswith("#"):
            return "own"
        elif link.startswith("../"):
            return "other"
        elif link.startswith("http://") or link.startswith("ftp://") or link.startswith("mailto:") or link.startswith("irc://"):
            return "outer"
        else:
            return "break"
        
    links = [link["href"] for link in BeautifulSoup(doc).findAll("a", href=True)]
    [result[startswith(link)].add(link) for link in links]
    
    ids = [tag["id"] for tag in BeautifulSoup(doc).findAll(id=True)]
    result["id"].extend(ids)
    names = [tag["name"] for tag in BeautifulSoup(doc).findAll("a", attrs={"name":True})]
    result["id"].extend(names)
    
    return result

def get_own_url(file_path):
    file_name = os.path.basename(file_path)[:-4]
    return "../%s/" % file_name

def get_filepath(file_name):
    return os.path.abspath("%s.txt" % file_name.split("/")[1])

def link_check(arg):
    pass

def main(arg):
    import commands
    #link_index = ("own", "other", "outer")
    urls_dict = {}
    other_dict = {}
    outer_dict = {}
    break_dict = {}
    
    print "-"*8, "reST rendaring check by docutils."
    
    for file_path in get_filelist(arg):
        print file_path
        doc = trans_doc(file_path=file_path)
        
        if not doc:
            print "... skipped."
            continue
        
        links = find_links(doc)
        url = get_own_url(file_path)
        urls_dict[url] = links["id"]
        
        for link in links["own"]:
            try:
                assert link[1:] in urls_dict[url]
            except AssertionError:
                print "* not find own-link: %s" % link
                print commands.getoutput("grep -n '%s' %s" % (link, file_path))
        
        other_dict[url] = links["other"]
        outer_dict[url] = links["outer"]
        break_dict[url] = links["break"]
    
    print "-"*8, "not found pages and links."
    
    for own_url, links in other_dict.items():
        for link in links:
            if "#" in link:
                base, id_name = link.split("#")
            else:
                base, id_name = link, None
            
            try:
                assert base in urls_dict.keys()
            except AssertionError:
                file_path = get_filepath(own_url)
                print "\n%s" % file_path
                print "* not find page: %s at %s" % (link, own_url)
                print commands.getoutput("grep -n '%s' %s" % (link, file_path))
                continue
            try:
                if id_name:
                    assert id_name in urls_dict[base]
            except AssertionError:
                file_path = get_filepath(own_url)
                print "\n%s" % file_path
                print "* not find link: %s in %s" % (link, base)
                print commands.getoutput("grep -n '%s' %s" % (link, file_path))

    print "-"*8, "break links."

    for own_url, links in break_dict.items():
        if not links:
            continue
        file_path = get_filepath(own_url)
        print file_path
        for link in links:
            print "* break link: %s at %s" % (link, own_url)
            print commands.getoutput("grep -n '%s' %s" % (link, file_path))

    if not "--outerlink" in sys.argv:
        return
    print "-"*8, "outer links."

    for own_url, links in outer_dict.items():
        if not links:
            continue
        print get_filepath(own_url)
        for link in links:
            print " %s" % link


helpdoc = "Usage: command <target-dir> [--outerlink]"


_test_data = r"""
test_string
===========

`link <#test_string>`_
"""

def test():
    """
>>> helpdoc
'Usage: command <target-dir> [--outerlink]'
>>> _test_data
'\\ntest_string\\n===========\\n\\n`link <#test_string>`_\\n'
>>> doc = trans_doc(source=_test_data)
>>> doc
u'<div class="document" id="test-string">\\n<h1 class="title">test_string</h1>\\n<p><a class="reference" href="#test_string">link</a></p>\\n</div>\\n'
>>> trans_doc(file_path="//noting//") == None
True
>>> find_links('<a href="#own">link1</a><a href="#own">link2</a><a href="../other/#other">link</a><a href="http://outer/#outer">link</a><span id="id"><a name="name">link</a></span><a href="break">link</a>')
{'break': set([u'break']), 'own': set([u'#own']), 'outer': set([u'http://outer/#outer']), 'other': set([u'../other/#other']), 'id': [u'id', u'name']}
>>> get_own_url("/path-to/rest_file.txt")
'../rest_file/'
>>> get_filepath("../rest_file/").split("/")[-1]
'rest_file.txt'
    """

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        _test()
    elif "-h" in sys.argv or "--help" in sys.argv:
        print helpdoc
    elif len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        print helpdoc
