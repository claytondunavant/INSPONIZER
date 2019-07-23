from libxmp import XMPFiles

'''
 ____ _____  _  _____ ___ ____ ____  
/ ___|_   _|/ \|_   _|_ _/ ___/ ___| 
\___ \ | | / _ \ | |  | | |   \___ \ 
 ___) || |/ ___ \| |  | | |___ ___) |
|____/ |_/_/   \_\_| |___\____|____/ 
'''

#static variables
INSPO_URI = "https://www.claytondunavant.com/inspo" #insponizer URI
#all possible articles of clothing
ARTICLES = ["hat","glasses","jacket","top","bag","watch","belt","bottom","socks","shoes"]



'''
 ____  _____    _    ____
|  _ \| ____|  / \  |  _ \
| |_) |  _|   / _ \ | | | |
|  _ <| |___ / ___ \| |_| |
|_| \_\_____/_/   \_\____/
'''

#check to see if inspo xmp data exists
def check_inspo_xmp(file):

    #get xmp from file
    xmpfile = XMPFiles(file_path=file)
    xmp = xmpfile.get_xmp()

    #check to see
    try:
        xmp.get_prefix_for_namespace(INSPO_URI)
        xmpfile.close_file()
        return True
    except:
        xmpfile.close_file()
        return False



'''
__        ______  ___ _____ _____ 
\ \      / /  _ \|_ _|_   _| ____|
 \ \ /\ / /| |_) || |  | | |  _|  
  \ V  V / |  _ < | |  | | | |___ 
   \_/\_/  |_| \_\___| |_| |_____|

'''

#check to see if xmp can be written
def check_xmp_writable(file):
    # get xmp from file
    xmpfile = XMPFiles(file_path=file, open_forupdate=True)
    xmp = xmpfile.get_xmp()

    #if you can write new xmp
    if xmpfile.can_put_xmp(xmp) == True:
        xmpfile.close_file()
        return True
    else:
        xmpfile.close_file()
        return False

#write INSPO data from dictonary
def dictonary_write(file, dict):
    # get xmp from file
    xmpfile = XMPFiles(file_path=file, open_forupdate=True)
    xmp = xmpfile.get_xmp()

    if check_xmp_writable(file) == True: #if xmp can be written to file

        if check_inspo_xmp(file) == False: #if INSPO xmp does not exist

            # register or update INSPO namespace URI
            xmp.register_namespace(INSPO_URI, "INSPO")

            # for each possible article
            for article in ARTICLES:
                print("trying for " + article)
                try:
                    value = dict[article]
                    xmp.set_property(INSPO_URI, article, value)
                except:
                    pass

            xmpfile.put_xmp(xmp)
            xmpfile.close_file()

        else:
            xmpfile.close_file()
            print("INSPO DATA ALREADY EXISTS")
            return

    else:
        xmpfile.close_file()
        print("XMP NOT WRITEABLE")
        return

#manually write INSPO data in terminal
def terminal_write(file):
    # get xmp from file
    xmpfile = XMPFiles(file_path=file, open_forupdate=True)
    xmp = xmpfile.get_xmp()

    if check_xmp_writable(file) == True: #if xmp can be written to file

        if check_inspo_xmp(file) == False: #if INSPO xmp does not exist

            # register or update INSPO namespace URI
            xmp.register_namespace(INSPO_URI, "INSPO")

            # for each possible article
            for article in ARTICLES:

                value = input("What " + article + " are they wearing?: ")  # ask if they are wearing a certain article of clothing

                if value == "":  # if the value is empty then pass
                    pass
                else:  # else set that article of clothing
                    xmp.set_property(INSPO_URI, article, value)

            xmpfile.put_xmp(xmp)
            xmpfile.close_file()

        else:
            xmpfile.close_file()
            print("INSPO DATA ALREADY EXISTS")
            return

    else:
        xmpfile.close_file()
        print("XMP NOT WRITEABLE")
        return


'''
  ____ _____ _   _ _____ ____      _    _     
 / ___| ____| \ | | ____|  _ \    / \  | |    
| |  _|  _| |  \| |  _| | |_) |  / _ \ | |    
| |_| | |___| |\  | |___|  _ <  / ___ \| |___ 
 \____|_____|_| \_|_____|_| \_\/_/   \_\_____|

'''

def get_ARTICLES():
    return ARTICLES
