#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom.minidom import Document

if __name__ == "__main__":
    doc = Document()
    people = doc.createElement("people")
    doc.appendChild(people)
    aperson = doc.createElement("person")
    people.appendChild(aperson)
    name = doc.createElement("name")
    aperson.appendChild(name)
    personname = doc.createTextNode("Annie")
    name.appendChild(personname)
    filename = "people.xml"
    f = open(filename, "w")
    f.write(doc.toprettyxml(indent="  "))
    f.close()

