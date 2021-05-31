from github import Github 


# login to github
g = Github('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')

# repo gets my w-atch repository
repo = g.get_repo('anim-e/w-atch')


# contents is a list of all my files and folders in my w-atch repository
contents = repo.get_contents('')


# loop through all files and folders
for c in contents:
    # c.path is the path of each content file
    print(c.path)
    
    # delete html file if it exist
    if c.path == 'a1.html':
        print(c.path,'will be deleted')
        
        # delete the old html file
        repo.delete_file(c.path, 'Chadley BOT deleting your file', c.sha)

class lucky():
    class guy():
        def here():
            pass

lucky.guy.here()

# create new html file
repo.create_file('test', 'commit', 'Hello Moto')
