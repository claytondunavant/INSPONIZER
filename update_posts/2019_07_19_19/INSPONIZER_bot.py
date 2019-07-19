#goes through all the [wdywt] posts on r/streetwears hot page and grabs the post and photo url if there seems to be a clothes comment

import praw

#starts instance of reddit using bot
r = praw.Reddit('INSPONIZER_bot')

#opens up streetwear subreddit
streetwear = r.subreddit("streetwear")

#for each post in hot
for post in streetwear.hot():

    #record the posts' author
    author = post.author

    #if the post is not the automoderator
    if author != "AutoModerator":

        #records the posts title
        title = post.title

        #if post is a wdywt post
        if "[wdywt]" in title.lower():

            #removes "more comments"
            post.comments.replace_more(limit=None)

            #scrapped comments thought to contain clothes
            comments = []

            #switch for if the most likely comment is found
            comment_found = False

            #for all shown comments
            for comment in post.comments.list():

                if comment_found == False:

                    #if the comment is also by op
                    if comment.author == author:

                        #the text of the comment
                        text = comment.body

                        #if the comment is longer than 30 characters
                        if len(text) > 30:
                            comments.append(text)

                            #if the text has a : or - in it, often used in clothes formating
                            if ":" in text or "-" in text:
                                del comments[:] #delete all other comments
                                comments.append(text) #add comment to comments
                                comment_found = True #indicate the most likely comment is found


            if len(comments) > 0:

                #prints the posts link and the posts' photos' link
                print("Post URL: https://www.reddit.com/" + post.permalink)
                print("Photo URL: " + post.url)

                #prints all possible clothes comments on post
                for comment in comments:
                    print(comment)

                print("------------------------------------------\n")