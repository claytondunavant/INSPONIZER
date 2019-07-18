import praw

#starts instance of reddit using bot
r = praw.Reddit('INSPONIZER_bot')

#opens up streetwear subreddit
streetwear = r.subreddit("streetwear")

#for each post in hot
for post in streetwear.hot():

    #record the posts' author
    author = post.author

    if author != "AutoModerator":

        #records the posts title
        title = post.title

        #if post is a wdywt post
        if "[wdywt]" in title.lower():

            #removes "more comments"
            post.comments.replace_more(limit=None)

            #for all shown comments
            for comment in post.comments.list():

                #if the comment is also by op
                if comment.author == author:

                    #if the comment is longer than 30 characters
                    if len(comment.body) > 30:
                        print(comment.body)
                        print("length: " + str(len(comment.body)))
                        print("----------\n")

            print("Post URL: https://www.reddit.com/" + post.permalink)
            print("Photo URL: " + post.url)

            print("------------------------------------------\n")


