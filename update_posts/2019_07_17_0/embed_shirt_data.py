#import files
from libxmp import XMPFiles

#set image to add data to
image = "image.jpg"

#read file
xmpfile = XMPFiles(file_path=image, open_forupdate=True)

#set INSPONIZER URI
inspoURI = "https://www.claytondunavant.com/inspo"

#get xmp from file
xmp = xmpfile.get_xmp()

#register or update INSPO namespace URI
xmp.register_namespace(inspoURI, "INSPO")

#set shirt property to UNIQLO
xmp.set_property(inspoURI, u"shirt", u"Uniqlo U T-Shirt")

#if you can write new xmp, write it
if xmpfile.can_put_xmp(xmp) == True:
    xmpfile.put_xmp(xmp)

#close the file
xmpfile.close_file()
