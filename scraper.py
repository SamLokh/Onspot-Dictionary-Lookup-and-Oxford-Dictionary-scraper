from bs4 import BeautifulSoup
import requests
import _thread
import os

#Improvements that can be made: The 2 print functions and their corresponding 2 printValues functions can be converted into a single print function with 1 printValues function... similar thing about the 2 store functions

class meaning:


    def __init__(self, word):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}
        self.word = word
        self.totalNoOfDefinitions = 0
        #self.url = 'https://www.oxfordlearnersdictionaries.com/definition/english/'+str(word)+'?q='+(word)
        self.url = 'https://www.oxfordlearnersdictionaries.com/definition/english/'+word#+'_1' 
        self.req = requests.get(self.url, headers=headers)
        self.soup = BeautifulSoup(self.req.content, 'html.parser')
        self.grammarTextList = []
        self.labelTextList = []
        self.definitionTextList = []
        self.synonymTextList = []
        self.listOfListOfExamples = []
        self.oppositeTextList = []
        self.seeAlsoTextList = []
        self.topicsTextList = []
        self.allInfoAsAString = ''
        self.allInfoAsALongString = ''

        self.wordNotAvailableFlag = 0
        self.possibleCorrectWords = []
        if self.soup.find('div', attrs = {'id':'didyoumean'}) != None:
            element = self.soup.find('ul', attrs = {'class':'result-list'})
            if element != None:
                liElements = element.findAll('li')
                if liElements != None:
                    self.wordNotAvailableFlag = 1
                    for liElement in liElements:
                        self.possibleCorrectWords.append(liElement.get_text())
                
        
        

    def getCommonValues(self, soupElement, attributeValue):
        if attributeValue == 'syn' or attributeValue == 'opp' or attributeValue == 'see':
            element = soupElement.find('span', attrs = {'xt':attributeValue})
            if element != None:
                temp = element.a
                if temp != None:
                    temp = temp.span
                    if temp != None:
                        temp = temp.span
                        if temp != None:
                            print('HELLOOOOO'+temp.get_text())
                            return temp.get_text()
                #return element.a.span.span.get_text()
            else:
                return ''
        elif attributeValue == 'topic-g':
            element = soupElement.find('span', attrs = {'class':'topic_name'})
            if element != None:
                return element.get_text()
            else:
                return ''
        else:
            element = soupElement.find('span', attrs = {'class':attributeValue})
            if element != None:
                return element.get_text()
            else:
                return ''

        '''
        if element != None:
            print('How tf is the program control reaching here?')
            return element.get_text()
        else:
            return ''
        '''
    def getExamples(self, soupElement):
        ulElement = soupElement.find('ul')
        listOfExampes = []
        if ulElement != None:
            listOfExampeElements = ulElement.findAll('li')
            for element in listOfExampeElements:
                listOfExampes.append(element.span.get_text())
        return listOfExampes
    
    def buildMeanings(self):
        self.totalNoOfDefinitions = len(self.soup.findAll('span', attrs = {'class':'def'}))
        #self.totalNoOfDefinitions = len(self.soup.findAll('li', attrs = {'class':'sense'}))
        for i in range(1, self.totalNoOfDefinitions+1):
            allElementsOfCurrentDefinition = self.soup.find('li', attrs = {'sensenum':i})
            if allElementsOfCurrentDefinition != None:

                self.grammarTextList.append(self.getCommonValues(allElementsOfCurrentDefinition, 'grammar'))
                self.labelTextList.append(self.getCommonValues(allElementsOfCurrentDefinition, 'labels'))
                self.definitionTextList.append(self.getCommonValues(allElementsOfCurrentDefinition, 'def'))

                self.synonymTextList.append(self.getCommonValues(allElementsOfCurrentDefinition, 'syn'))

                self.listOfListOfExamples.append(self.getExamples(allElementsOfCurrentDefinition))

                self.oppositeTextList.append(self.getCommonValues(allElementsOfCurrentDefinition, 'opp'))
                self.seeAlsoTextList.append(self.getCommonValues(allElementsOfCurrentDefinition, 'see'))
                self.topicsTextList.append(self.getCommonValues(allElementsOfCurrentDefinition, 'topic-g'))

            else:
                self.totalNoOfDefinitions -= 1

    def storeShortString(self, dummy):
        fileShort = open("shortMeanings.txt", "a+")
        if os.stat("shortMeanings.txt").st_size != 0:
            alreadyStoredShortMeanings = fileShort.readlines()
            if len(alreadyStoredShortMeanings) > 0:
                if self.allInfoAsAString not in alreadyStoredShortMeanings:
                    print('Hello')
                    fileShort.write(self.allInfoAsAString)
        else:
            fileShort.write(self.allInfoAsAString)
        fileShort.close()
        
    def storeLongString(self, dummy):
        fileLong = open("longMeanings.txt", "a+")
        if os.stat("longMeanings.txt").st_size != 0:
            alreadyStoredLongMeanings = fileLong.readlines()
            if len(alreadyStoredLongMeanings) > 0:
                if self.allInfoAsALongString not in alreadyStoredLongMeanings:
                    print('Hello2')
                    fileLong.write(self.allInfoAsALongString)
        else:
            fileLong.write(self.allInfoAsALongString)
        fileLong.close()

    def printValues2(self, value, text):     #for long(complete, actual) string from the website
        print('VALUEEEEE TYPE '+str(type(value)))
        if text != '':
            #print(' '+text+': ', end = '')
            self.allInfoAsALongString = self.allInfoAsALongString+' '
            self.allInfoAsALongString = self.allInfoAsALongString+text
            self.allInfoAsALongString = self.allInfoAsALongString+': '
        if str(type(value)) == "<class 'NoneType'>":
            return
        if value != '':            
            self.allInfoAsALongString = self.allInfoAsALongString+value+'\n'


    def printValues(self, value, text):     #for short string
        if text != '':
            #print(' '+text+': ', end = '')
            self.allInfoAsAString = self.allInfoAsAString+' '
            self.allInfoAsAString = self.allInfoAsAString+text
            self.allInfoAsAString = self.allInfoAsAString+': '
        if value != '':
            #print(value)
            self.allInfoAsAString = self.allInfoAsAString+value+'\n'

    def printMeanings(self):
        #print(self.totalNoOfDefinitions)
        for i in range(self.totalNoOfDefinitions):
            #print(str(i+1)+'.', end = ' ')
            self.allInfoAsALongString = self.allInfoAsALongString+str(i+1)
            self.allInfoAsALongString = self.allInfoAsALongString+'. '
            '''
            print(self.grammarTextList[i], end = ' ')
            print(self.labelTextList[i])
            print(self.definitionTextList[i]+'\n')
            print(self.synonymTextList[i])
            '''
            self.printValues2(self.grammarTextList[i], '')
            self.printValues2(self.labelTextList[i], '')
            self.printValues2(self.definitionTextList[i], '')
            #print()
            self.allInfoAsALongString = self.allInfoAsALongString+'\n'
            #print(' Synonmy: ', end = ' ')
            self.printValues2(self.synonymTextList[i], 'Synonym')
            self.allInfoAsALongString = self.allInfoAsALongString+' Examples: \n'
            #print(' Examples: ')
            for j in self.listOfListOfExamples[i]:
                #print(' * '+j)
                self.allInfoAsALongString = self.allInfoAsALongString+' * '+j+'\n'
            #print(' Opposite: ', end = ' ')
            self.printValues2(self.oppositeTextList[i], 'Opposite')
            #print(' See Also: ', end = ' ')
            self.printValues2(self.seeAlsoTextList[i], 'See Also')
            #print(' Topics: ', end = ' ')
            self.printValues2(self.topicsTextList[i], 'Topics')
            '''
            print(self.oppositeTextList[i])
            print(self.seeAlsoTextList[i])
            print(self.topicsTextList[i])
            '''
            #print()
            #print()
            self.allInfoAsALongString = self.allInfoAsALongString+'\n'
            self.allInfoAsALongString = self.allInfoAsALongString+'\n'
            #_thread.start_new_thread(self.storeLongString, ('dummy',))
            #self.storeLongString('dummy')

    def printMeaningsWithLessInfo(self):
        if self.totalNoOfDefinitions >= 2:      #Displaying atmost 2 meanings per word
            noOfMeaningsToBeDisplayed = 2
        else:
            noOfMeaningsToBeDisplayed = self.totalNoOfDefinitions
        for i in range(noOfMeaningsToBeDisplayed):
            #print(str(i+1)+'.', end = ' ')
            self.allInfoAsAString = self.allInfoAsAString+str(i+1)
            self.allInfoAsAString = self.allInfoAsAString+'. '
            
            self.printValues(self.grammarTextList[i], '')
            self.printValues(self.labelTextList[i], '')
            self.printValues(self.definitionTextList[i], '')
            self.allInfoAsAString = self.allInfoAsAString+'\n'
            self.allInfoAsAString = self.allInfoAsAString+' Examples: \n'
            #print(' Examples: ')
            count = 0
            for j in self.listOfListOfExamples[i]:
                if count < 2:               #for print only 2 examples per meaning
                    #print(' * '+j)
                    self.allInfoAsAString = self.allInfoAsAString+' * '+j+'\n'
                count += 1
            self.allInfoAsAString = self.allInfoAsAString+'\n'
            self.allInfoAsAString = self.allInfoAsAString+'\n'
            #_thread.start_new_thread(self.storeShortString, ('dummy',))
            #self.storeShortString('dummy')


if __name__=="__main__":
    word = 'alloy'
    obj1 = meaning(word)
    print(word)
    print()
    obj1.buildMeanings()
    obj1.printMeanings()
    obj1.printMeaningsWithLessInfo()
    
    print(obj1.allInfoAsAString)
    print()
    print()
    print(obj1.allInfoAsALongString)
    

'''
word = 'pious'

url = 'https://www.oxfordlearnersdictionaries.com/definition/english/'+str(word)+'?q='+(word)
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html5lib')
'''

'''
soupElement = soup.find('li', attrs = {'sensenum':2})
ulElement = soupElement.find('ul')
listOfExampeElements = ulElement.findAll('li')
listOfExampes = []
for element in listOfExampeElements:
    listOfExampes.append(element.span.get_text())
#print(listOfExampes[1])

count = 1
for i in listOfExampes:
    print()
    print(str(count)+' '+i)
    count += 1
print()

'''

'''
elements = []

grammars = []
totalNoOfGrammars = 0
definitions = []
totalNoOfDefinitions = 0


def getMultiple(classType):
    tempList = []
    elements = soup.findAll('span', attrs = {'class':classType})
    if elements != None:
        for element in elements:
            tempList.append(element.get_text())
    return tempList


grammars = getMultiple('grammar')
definitions = getMultiple('def')
'''

'''
print('1. '+definitions[0])
print('2. '+definitions[1])
print('3. '+definitions[2])
'''

'''
elements = soup.findAll('span', attrs = {'class':'grammar'})
if elements != None:
    totalNoOfGrammars = len(elements)
    grammarText = element.get_text()
print(grammarText)


elements = soup.findAll('span', attrs = {'class':'def'})
if elements != None:
    totalNoOfDefinitions = len(elements)
    for definition in elements:
        definitions.append(definition.get_text())
    #definitionText = elements.get_text()
print(definitions)
'''


