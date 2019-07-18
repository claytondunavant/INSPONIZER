from libxmp import XMPFiles

#read file
xmpfile = XMPFiles(file_path="image.jpg", open_forupdate=True)

#set INSPONIZER URI
inspoURI = "https://www.claytondunavant.com/inspo"

#get xmp from file
xmp = xmpfile.get_xmp()

#register or update INSPO namespace URI
xmp.register_namespace(inspoURI, "INSPO")

#all possible articles of clothing
articles = ["hat","glasses","jacket","top","bag","belt","bottom","socks","shoes"]

#for each possible article
for article in articles:
    value = input("What " + article + " are they wearing?: ") #ask if they are wearing a certain article of clothing

    if value == "": #if the value is empty then pass
         pass
    else: #else set that article of clothing
        xmp.set_property(inspoURI, article, value)


#if you can write new xmp, write it
if xmpfile.can_put_xmp(xmp) == True:
    xmpfile.put_xmp(xmp)

#closes file
xmpfile.close_file()



