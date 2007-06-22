# -*- coding: utf-8 -*-
from django.db import models

class Tag(models.Model):
    """The Tag class."""
    value = models.CharField(maxlength=100, unique=True, blank=False)
    
    def __str__(self):
        return self.value


class Entry(models.Model):
    """The Entry class.
    #インスタンス作成のテスト
    >>> content1 = "[spam][ham]: content title#1\\r\\n========================================== \
    \\r\\n\\r\\ncontent text#1"
    >>> content2 = "content title#2\\r\\n=========================\\r\\n\\r\\ncontent text#2"
    >>> content3 = "[spam][Django]: content title#3\\r\\n======================================= \
    \\r\\n\\r\\ncontent text#3"
    >>> content4 = "content: title#4\\r\\n======================================= \
    \\r\\n\\r\\ncontent text#4"
    >>> content5 = "[Presen]: content title#5\\r\\n======================================= \
    \\r\\n\\r\\ncontent text#5"
    >>> entry1 = Entry.objects.create(content=content1)
    >>> entry2 = Entry.objects.create(content=content2)
    >>> entry3 = Entry.objects.create(content=content3)
    >>> entry4 = Entry.objects.create(content=content4)
    >>> entry5 = Entry.objects.create(content=content5)
    >>> entry1.title
    ' content title#1'
    >>> entry2.title
    'content title#2'
    >>> entry4.title
    'content: title#4'
    
    #title_to_tagsのテスト
    >>> entry1.tags
    ['spam', 'ham']
    >>> entry1.tags_list
    '[spam] [ham]'
    >>> entry2.tags
    []
    
    >>> Tag.objects.filter(value=entry1.tags[0])
    [<Tag: spam>]
    >>> t11 = Tag.objects.filter(value=entry1.tags[1])
    >>> t11
    [<Tag: ham>]
    >>> t30 = Tag.objects.filter(value=entry3.tags[0])
    >>> t30
    [<Tag: spam>]
    >>> t31 = Tag.objects.filter(value=entry3.tags[1])
    >>> t31
    [<Tag: Django>]
    
    >>> Entry.objects.filter(tag=str(t31[0]))
    []
    
    #datetimeのテスト
    >>> a1 = entry1.add_date
    >>> l1 = entry1.last_mod
    >>> a1 == entry1.add_date
    True
    >>> l1 == entry1.last_mod
    True
    >>> entry1.save()
    >>> a1 == entry1.add_date
    True
    >>> l1 == entry1.last_mod
    False
    
    >>> Tag.objects.filter(value="Django")
    [<Tag: Django>]
    >>> Tag.objects.filter(value=str(t31[0]))
    [<Tag: Django>]
    >>> Entry.objects.filter(tag=t11[0])
    [<Entry:  content title#1>]
    >>> Entry.objects.filter(tag=t30[0])
    [<Entry:  content title#1>, <Entry:  content title#3>]
    >>> Entry.objects.filter(tag=t31[0])
    [<Entry:  content title#3>]
    
    #get_absolute_url
    >>> entry1.get_absolute_url()
    '/blog/posts/1/'
    >>> entry1.get_absolute_url_text()
    '/blog/posts/1.txt'
    >>> entry1.get_absolute_url_presen()
    '/blog/posts/1/presen/'
    
    #ispresen
    >>> entry1.ispresen()
    False
    >>> entry5.ispresen()
    True
    """
    content = models.TextField(blank=True)
    tag = models.ManyToManyField(Tag, blank=True, editable=False)
    add_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_mod = models.DateTimeField(auto_now=True, editable=False)
    
    def __str__(self):
        return self.title
    
    def save(self):
        super(Entry, self).save()
        for tag in self._title_to_tags():
            obj, created = Tag.objects.get_or_create(value=tag)
            self.tag.add(obj)
    
    def _content_s(self):
        return self.content.splitlines()[3]
    content_s = property(_content_s)

    def _title_line(self):
        l = self.content.splitlines()[0].split("]:")
        if len(l) >= 2:
            l[0] += "]"
        return l

    def _title(self):
        line = self._title_line()
        if len(line) >= 2:
            return ":".join(line[1:])
        return line[0]
    title = property(_title)
            
    def _title_to_tags(self):
        line = self._title_line()
        if len(line) == 1:
            return []
        return self._title_line()[0][1:-1].split("][")
    tags = property(_title_to_tags)
    
    def _tags_list(self):
        line = self._title_line()
        if len(line) == 1:
            return []
        return self._title_line()[0].replace("][","] [")
    tags_list = property(_tags_list)
    
    def ispresen(self):
        if "Presen" in self.tags:
            return True
        else:
            return False
    
    def get_absolute_url(self):
        return "/blog/posts/%s/" % self.id
    
    def get_absolute_url_text(self):
        return "/blog/posts/%s.txt" % self.id

    def get_absolute_url_presen(self):
        return "/blog/posts/%s/presen/" % self.id

    class Admin:
        list_display = ("title", "tags_list", "add_date", "last_mod")
        list_filter = ("tag", )
