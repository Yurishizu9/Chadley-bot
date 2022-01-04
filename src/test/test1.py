import sys

def nameCreator():
    try:
        fname = sys.argv[1] 
        lname = ' ' + sys.argv[2:]
        
    except:
        #print(fname)
        #print(lname)
        if not len(sys.argv) > 1:
            fname = 'stranger'
        if not len(sys.argv) > 2: 
            lname = ''

    
    print(f'Hello {fname}!')
    x = input('press a RETURN to quit')

nameCreator()