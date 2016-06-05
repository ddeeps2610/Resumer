#!/usr/bin/python
import os,sys,traceback
import pickle

stack =[]

def cdDotDot():
    """ 
    Traverses the whole stack until it has reached the end of the stack    """
    entity = resume
    try:
        for i in range (0, len(stack)):
            key = stack[i]
            if 'list' in key:
                entity = entity[int(key.split(":")[1])]
            elif 'dict' in key:
                entity = entity.get(key.split(':')[1])
            else:
                print 'Can\'t go any further'
                break
        return entity
    except:
        print 'Error occured in cdDotDot. Returning None'
        return None

def handleList(entity):
    """
    Handles the list entity as the name suggests.
    """
    # Print the entity
    print 'List:', entity
    # Provide options for operating on list entity
    operations ='-a entry - append entry in the list\n'+\
        '-r entry - remove an entry from the list\n' +\
        '-d index - dive further into the entry\n'+\
        '-b - go back to the previous entiry\n'+\
        '-e - exit'
    #Request for the user input
    feed = raw_input(operations)
    items=feed.split()

    # Handle the user input
    if '-a' in feed:
        print feed
        if len(items)>=2:
            for i in range(1, len(items)):
                entity.append(items[i])
        else:
            print 'Wrong number of parameters'
    elif '-r' in feed:
        print feed
        if len(items) >=2:
             for i in range(1, len(items)):
                 try:
                     index = entity.index(items[i])
                     if isinstance(index, int):
                         entity.pop(index)
                     else:
                         print 'Item {} not present!.'.format(items[i])
    elif '-d' in feed:
        print feed
        if len(items)==2:
            try:
                index=int(items[1])
                stack.append('list:{}'.format(str(index)))
                entity = entity[index] 
            except:
                print 'Entity {} couldn\'t be fetched'.\
                format(entity[index])  
    elif '-b' in feed:
        print feed
        stack.pop()
        preEntity = cdDotDot()
        if preEntity != None:
            entity = preEntity
    elif '-e' in feed:
        print 
        # Check if you want to save modifications
        message = 'Do you want to save modifications to the resume?(y/n)'
        feed = raw_input(message)
        if 'y' in feed.lower():
            # Store all modifications to the pickle file so far.
            pickle.dump(resume, open(pickleFile, 'wb'))
        sys.exit(0)
    else:
        print 'Wrong option'

    # Generate the next entity and continue
    return entity

def handleDict(entity):
    # Print the entity
    print 'Dictionary keys:', entity.keys()

    # Based on the entity provide options
    operations = '-u key value - update an entry\n' +\
       '-r key - remove an entry based on key\n' +\
       #'-v value - remove an entry based on value\n' + \
       '-d key - dive further into entry for key\n' +\
       '-b - go back to previous entry\n' +\
       '-e - exit'

    # Request for the user input
    feed = raw_input(operations)
    items = feed.split()
    # Handle the user input
    if '-u' in feed:
        if len(items) == 3:
            key = items[1]
            value = items[2]
            try:
                entity[key] = value
            except:
                print 'Something went wrong while updating dictionary'
            return entity
        else:
            print 'Wrong number of parameters'
            return entity
    elif '-r ' in feed:
        print feed
        if len(items) != 2:
            print 'Wrong number of parameters'
        else:
            key = items[1]
            if key in entity.keys():
                entity.pop(key)
            else:
                print 'Key: {} is not present'.format(key)
        return entity
    #elif '-v' in feed:
    #    print feed
    elif '-d' in feed:
        print feed
        if len(items) != 2:
            print 'Wrong number of parameters'
        else:
            key = items[1]
            if key in entity.keys():
                if type(entity.get(key)) in (dict, list):
                    stack.append('dict:{}'.format(key))
                    entity = entity.get(key)
                else:
                    print key, ":", entity.get(key)
            else:
                print 'Key: {} is not present'.format(key)
        return entity
    elif '-b' in feed:
        print entity
        key=stack.pop()
        prevEntity = cdDotDot()
        if prevEntity != None:
            entity = prevEntity
        return entity
    elif '-e' in feed:
        print feed
        # Check if you want to save modifications
        message = 'Do you want to save modifications to the resume?(y/n)'
        feed = raw_input(message)
        if 'y' in feed.lower():
            # Store all modifications to the pickle file so far.
            pickle.dump(resume, open(pickleFile, 'wb'))
        sys.exit(0)
    else:
        print 'Wrong option'
        
    # Generate the next entity and continue
    return entity


####### Main ###########

# import the resume from the existing resume
pickleFile='resume.pkl'

resume = pickle.load(open(pickleFile, 'rb'))


entity =resume
feed = 'None'
while(entity != None and (feed != 'e'))
    if isinstance(entity, dict):
        entity = handleDict(entity)
    elif isinstance(entity, list):
        entity = handleList(entity)
    else:
        print 'Some other type of element: {}'.format(type(entity))

