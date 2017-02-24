
# coding: utf-8

# In[114]:

import numpy as np
"""
This section of code is for getting the contents of the text files into LISTS of STRINGS
fileIndex = dictionary of index through the different files
fileLength = dictionary of lengths for each file
dataList = one main list containing each file's list of strings
"""
classifiedFile = 'classified_tweets.txt'
corpusFile = 'corpus.txt'
stopFile = 'stop_words.txt'
unclassifiedFile = 'unclassified_tweets.txt'
fileList = [classifiedFile, corpusFile, stopFile, unclassifiedFile]

fileIndex = {classifiedFile:0,
              corpusFile:1,
              stopFile:2,
              unclassifiedFile:3}

fileLength = {classifiedFile:0,
              corpusFile:0,
              stopFile:0,
              unclassifiedFile:0}

for fileName in fileList: ##get file lengths
    with open(fileName) as inputfile:
        count = 0
        for line in inputfile:
            count = count + 1
        fileLength[fileName] = count
        
##make a data file with the number of files (4)
classifiedData = []
corpusData = []
stopData = []
unclassifiedData = []
dataList = [classifiedData, corpusData, stopData, unclassifiedData]

## Put all the text files data into 1 list consisting of 4 lists
i=0
for fileName in fileList: ##get file lengths
    with open(fileName) as inputfile:
        for line in inputfile:
            dataList[i].append(line)
        i = i + 1
        
#print("classified", fileLength[classifiedFile])
#print("corpusFile", fileLength[corpusFile])
#print("stopFile", fileLength[stopFile])
#print("unclassifiedFile", fileLength[unclassifiedFile])


# # Generate Function List. To be called after the end of each function, to change all the data in that file.

# In[2]:

def generateFunctionList(func, fileType, inputList, exampleNumber):
    """
    This function helps take the output of the function and convert it to a LIST for all the lines in the text file.
    Ultimately inputList needs a LIST and is somewhat dependent on func because it works as y = func(inputList)
    This is because all of the data pulled from the text documents are strings in a list

    Each function (clean_data, tokenize_unigram, etc.) can call generateFunctionList with the appropriate inputs   
        #func = clean_data, tokenize_unigram
        #fileType = classifiedFile, unclassifiedFile
        #inputList = dataList[0], cleanedDataList, tokenizedList
        #exampleNumber = 0, 1, 2....N text lines

    This works in a cascaded fashion, such that the ouput of one function became the input to the next, as seen 
    the assignment.
    """
    generatedList = []
    for i in range(0, fileLength[fileType]):
        y = func(inputList[i])
        generatedList.append(y)
    #print "Complete"
    return generatedList


# # Clean Data

# In[3]:

def clean_data(tw):
    """
    Initailly change every symbol to its lowercase representative.
    Cleans the data, removing the symbols seen in "symbolList"
    All of those symbols are common unicode symbols, as seen in the keyboard, and are typical in tweets

    """
    #remove these symbols from the tweet tw'
    symbolList = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', 
                  '-', '_', '+', '=', '{', '}', '[', ']', '|', ':',
                  ';', '"', '<', '>', ',', '.', '?', '/', ',', "'",
                  '~', '`', '*']
    goodList = []
    tw_lower = tw.lower() #set all tweets to lower case
    for i in range(0, len(tw)):
        if tw_lower[i] not in symbolList:
            goodList.append(tw_lower[i])
    cleanString = ''.join(goodList)
    return cleanString #output type string


# # Tokenize Unigram ( Used by remove_stop_words )

# In[115]:

def tokenize_unigram(tw):
    """
    Initially not used for remove_stop_words, but it was found to be much more efficient to perform this way, instead
    of by comparing each stop word and each character in the tweet, which could have complexity of O(n^2)
    There is a tendancy for certain words at the output to have a unicode-utf8 encoding problem as seen with text like
    \aoe\ac3\xe4 etc.
    """    
    
    partWord = [] #create a list containing the partial word in a tweet
    tokenList = []
    currentWord = [] #create a list containing the fully spelled word in a tweet
    for t in range(0, len(tw)):
        if tw[t] == " ": #indicate when at a blank space in the tweet
            if len(partWord) != 0:
                currentWord = ''.join(partWord)
                partWord = [] #clear the partWord
                tokenList.append(currentWord.replace('\xc2\xa0', ' '))
        else:
            partWord.append(tw[t])

    if partWord.count('\n') >= 1: #check if unigram has \n as an element
        partWord.remove('\n')
    if partWord.count('\r') >= 1: #check if unigram has \r as an element
        partWord.remove('\r')
    
    tokenList.append(''.join((partWord)))
    
    return tokenList #output type list


# # Remove Stop Words

# In[116]:

def remove_stop_words(tw):
    """
    Stop words are written in lowercase. Hence sentences like "where am I" or "Everyone is.." have capitals in them.
    This is why it was important in clean_words to turn the sentences to lowercase.
    """
    stop_dict = {}
    removeStop = []
    for i in range(0, fileLength[stopFile]):
        x = dataList[2][i].strip('\n')
        current_dict = {x: x}
        stop_dict.update(current_dict)  
    token = tokenize_unigram(tw)
    for i in range(0, len(token)):
        if stop_dict.has_key(token[i]):
            token[i] = ""
    removeStop.append(' '.join((token)))

    return removeStop[0] #output type string


# # Bag of Words

# In[117]:

def bag_of_words(tw): #input is a string
    """
    The works off using the tokenized words from previous sections. 
    Data comes in as a normal string but is immediately tokenized.
    When taking text from a text file, it comes in as a list of tokens
    """
    bag_dict = {}
    if type(tw) == str:
        tokenTweet = tokenize_unigram(tw) #input is a string. Convert to list
    else:
        tokenTweet = tw #input is a list. Use as list.
    for i in range(0, len(tokenTweet)):
        amount = tokenTweet.count(tokenTweet[i])
        current_dict = {tokenTweet[i] : amount}
        bag_dict.update(current_dict)
       
    return bag_dict #output type dictionary


# # Party

# In[118]:

def party(tw): #input is a string
    """
    The party words chosen are based on a few criteria in order to catch as many variations
    Some examples include: 
    1) liberal and liberals, which is both plural and possessive ('s with the apostrophe removed)
    2) party leader first name
    3) party leader last name, which is both plural and possessive, simialr to point 1
    4) party leader firstlast name, as seen with some hashtags like #justintrudeau
    5) liberalparty and conservativeparty are common hashtags, but ndpparty is not. Just try saying it you'll know.
    5) omitted words like "party" because it is often used with liberal or conservative, which is already used
    
    This was scored based on the number of token keywords used for each party.
    The one with the most keywords used was the assigned party
    To handle the edge case of a tie, the current highest number was compared to other party's numbers.
    If there was a tie, or if there was zero use of any political keywords in the tweet, the output was "other"
    
    """
    
    
    if dict == type(tw):
        current_dict = tw
    else:
        current_dict = bag_of_words(tw) #takes in string and converts to bag of words

    liberal_words = ['liberal', 'liberals', 'liberalparty', 'justin', 'trudeau', 'trudeaus', 'justintrudeau']
    conservative_words = ['conservative', 'conservatives', 'conservativeparty', 'stephen', 'harper', 'harpers', 'stephenharper']
    ndp_words = ['ndp', 'ndps', 'tom', 'thomas' 'mulcair', 'mulcairs', 'tommulcair', 'thomasmulcair']
    party_words = [liberal_words, conservative_words, ndp_words]
    
    liberal_count = 0
    conservative_count = 0
    ndp_count = 0
    party_count = [liberal_count, conservative_count, ndp_count]
    
    political_parties = ['Liberals', 'Conservatives', 'NDP']
    
    for p in range(0, len(party_count)):
        for w in range(0, len(party_words[p])):
            y = party_words[p][w]
            x = current_dict.get(y)
            if x == None:
                x = 0
            party_count[p] = party_count[p] + x
    
    currentMax = -1 #Used for retaining the count of the party with most counts
    maxName = "" # Used for assigning the name of the current highest count party
    
    #Thi
    for i in range(0, len(political_parties)):
        #print party_count[i], currentMax
        if party_count[i] == currentMax: #created a 4th option. Should be political, if TIED use of party words
            maxName = "Others"
        elif party_count[i] > currentMax:
            currentMax = party_count[i]
            maxName = political_parties[i]   
            
    return maxName #output is a string


# # Get Sentiment Dictionary

# In[119]:

def getSentimentDictionary(sentimentFile):
    """
    Custom function to get the sentimentFile into a dictionary
    """
    sent_dict = {}
    for i in range(0, fileLength[sentimentFile]):
        sentiment_word, sentiment_score = dataList[fileIndex[sentimentFile]][i].split("\t")
        sentiment_score = sentiment_score.strip('\n')
        current_dict = {sentiment_word: sentiment_score}
        sent_dict.update(current_dict)

    return sent_dict



sentimentDictionary = getSentimentDictionary(corpusFile)

# In[121]:

      
def tweet_score(tw):
    #print type(tw)
    token_tweet = tokenize_unigram(tw) #tw is a string or a list and x is a dictionary
    #sentimentDictionary = getSentimentDictionary(corpusFile)
    current_score = float(0)
    for i in range(0, len(token_tweet)):
        word_score = sentimentDictionary.get(token_tweet[i])
        if word_score == None:
            word_score = 0.0    
        word_score = float(word_score)
        current_score = current_score + (word_score/5) # divide by 5 to normalize values -5 to 5 to be between -1 and 1
    score = current_score/len(token_tweet) #divided by the number of words in the whole tweet
    if score == 0: #cannot classify tweet, therefore assign value of -1
        score = -1
    sentiment = round(score, 2)
    
    return sentiment #float


# In[122]:

def tweet_classifier(tw):
    #print type(tw)
    score = tweet_score(tw)
    if score == -1:
        classifier = -1
    elif score >= 0.5:
        classifier = 1
    else:
        classifier = 0
    return classifier


example = 8
clean_data_list = generateFunctionList(clean_data, unclassifiedFile, dataList[3], example)
remove_stop_words_list = generateFunctionList(remove_stop_words, unclassifiedFile, clean_data_list, example)
tokenized_unigram_list = generateFunctionList(tokenize_unigram, unclassifiedFile, remove_stop_words_list, example)
bag_of_words_list = generateFunctionList(bag_of_words, unclassifiedFile, tokenized_unigram_list, example)
party_list = generateFunctionList(party, unclassifiedFile, bag_of_words_list, example)
tweet_classifier = generateFunctionList(tweet_classifier, unclassifiedFile, clean_data_list, example)
tweet_score = generateFunctionList(tweet_score, unclassifiedFile, clean_data_list, example)

#print clean_data_list[example]
#print remove_stop_words_list[example]
#print tokenized_unigram_list[example]
#print bag_of_words_list[example]
#print party_list[example]
#print tweet_classifier[example]
#print tweet_score[example]




