from libxmp import XMPFiles

'''
docs:
https://www.spacetelescope.org/static/projects/python-xmp-toolkit/docs/reference.html

#turn file xmp into a dictonary
xmp = file_to_dict("image.jpg")

#extract only the dublin core properties
dc = xmp[consts.XMP_NS_DC]

#check if property exists
xmp.get_property("http://ns.adobe.com/tiff/1.0/", "ResolutionUnit")
'''

#read file
xmpfile = XMPFiles(file_path="image.jpg", open_forupdate=True)

#set INSPONIZER URI
inspoURI = "https://www.claytondunavant.com/inspo"

#get xmp from file
xmp = xmpfile.get_xmp()

#register or update INSPO namespace URI
xmp.register_namespace(inspoURI, "INSPO")

#set shirt property to UNIQLO
xmp.set_property(inspoURI, u"shirt", u"UNIQLO")

#if you can write new xmp, write it
if xmpfile.can_put_xmp(xmp) == True:
    xmpfile.put_xmp(xmp)

xmpfile.close_file()

#print the value of the Inspo property shirt
print(xmp.get_property(inspoURI, "shirt"))


