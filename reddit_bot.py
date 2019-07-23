from praw import Reddit

def get_hot_wdyt():
    #starts instance of reddit using bot
    r = Reddit('INSPONIZER_bot')

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

                id = post.id

                if id not in open("reddit_parsing/_scrapped_posts").read(): #if post has not already been scraped

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

                        #add file to _scrapped_posts
                        f = open("reddit_parsing/_scrapped_posts", "a")
                        f.write(id + " ")
                        f.close()

                        #generate info dictionary
                        info = {}
                        info['id'] = id
                        info["author"] = "https://www.reddit.com/user/" + author.name
                        info["url"] = "https://www.reddit.com/" + post.permalink
                        info["photoURL"] = post.url

                        #make new file
                        f_name = "reddit_parsing/" + id
                        f = open(f_name, "x")
                        f = open(f_name, "w")
                        f.write(str(info)) #write info dict onto new file

                        #prints all possible clothes comments on post
                        for comment in comments:
                            f.write("\n")
                            f.write(comment)

                        f.close()

get_hot_wdyt()