# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 12:23:50 2017

@author: Malhotra
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 12:19:59 2017

@author: Malhotra
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 12:18:19 2017

@author: Malhotra
"""
from xml.dom import minidom

doc = minidom.parse("meineVerortung2.xml")

# doc.getElementsByTagName returns NodeList
name = doc.getElementsByTagName("node")
print(name)

# Print detail of each movie.
#for movie in movies:
#   print "*****Movie*****"
 #  if movie.hasAttribute("title"):
 #     print "Title: %s" % movie.getAttribute("title")