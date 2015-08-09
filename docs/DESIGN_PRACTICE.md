# Project Design

## Table of Contents

1. [App Division](#app-division)

## App Division

### Referenced or Referencing

> Apps of the project should category into at least 2 types -- **referenced** or **referencing**

- **Referenced** service provider
- **Referencing** service consumer

In order to avoid infinited import loops between apps. Only *referencing* could import *referenced*

###### [project folder structure](#project-folder-structure):

``` script
/project
  |-account (profile)
  |-auth (authenication and authority)
  |-post (article/blog etc.)
  |-tag (tag anything)
  |_comment (add comment to anything)
```
Take app `tag` and `comment` as *referenced* app by `account` and `post` as *referencing* app

Take app `account` as *referenced* app by `auth` as *referencing* app


### Communication via protocol/interface/contract

Just like `Object-Oritented` design principle, only invoke the defined **protocol/interface/contract**. Many goods would come from decouple benefit if stick to this rule.

e.g.:
```python

class TagBase(object):
  def __init__(self, *args, **kwargs):
    self.name = kwargs.get('name')
  def get_name(self):
    return self.name
  
class HierarchyTag(TagBase):
  def __init__(self, *args, **kwargs):
    self.parent = kwargs.pop('parent')
    super(HierarchyTag, self).__init__(*args, **kwargs)
  
class Tag(TagBase):
  pass
  
if __name__ == '__main__':
  tag = HierarachyTag(parent=None, name='foo')
  tag.get_name()  # via protocol/interface/contract
  tag = Tag(name='foo')
  tag.get_name()  # via protocol/interface/contract
```

### Communication via pk(id) only