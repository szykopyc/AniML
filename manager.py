import sqlite3 
import numpy as np
from numpy.random import choice as npchoice

#required function
def initChatML():
    conn = sqlite3.connect('chatml.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS words
             (word TEXT PRIMARY KEY NOT NULL, responses TEXT);''')
    conn.commit()
    conn.close()

#required function
def insertWord(word):
    conn = sqlite3.connect('chatml.db')
    c = conn.cursor()
    c.execute(f'''INSERT INTO words VALUES('{word}','');''')
    conn.commit()
    conn.close()

#required function
def insertResponse(word,response):
    conn = sqlite3.connect('chatml.db')
    c = conn.cursor()
    c.execute(f'''SELECT responses FROM words WHERE word='{word}';''')
    data=c.fetchall()
    data=data[0][0]
    try:
        c.execute(f'''UPDATE words SET responses='{data}'||','||'{response}' WHERE word='{word}';''')
    except Exception as e:
        print(e)
    conn.commit()
    conn.close()

#statistic function
def showData():
    conn = sqlite3.connect('chatml.db')
    c = conn.cursor()
    c.execute(f'''SELECT * FROM words;''')
    data=c.fetchall()
    print(data)
    conn.close()

#required function
def returnResponsesPercentage(word):
    conn = sqlite3.connect('chatml.db')
    c = conn.cursor()
    c.execute(f'''SELECT responses FROM words WHERE word='{word}' IS NOT NULL;''')
    data=c.fetchall()
    data=data[0]
    newd=list(data)
    data=newd[0].split(",")
    if '' in data:
      data.remove('')
    data=np.array(data)
    unique, frequency = np.unique(data, 
                              return_counts = True)
    total=frequency.sum()
    percentage=[]
    for x in frequency:
      y=x/total
      percentage.append(y)
    percentage=np.array(percentage)
    percentage=np.round(percentage,decimals=2,out=None)
    probability_dict={}
    for A,B in zip(unique, percentage):
      probability_dict[A]=B
    return probability_dict
    conn.close()

#statistic function
def showResponsesFor(word): 
    conn = sqlite3.connect('chatml.db')
    c = conn.cursor()
    c.execute(f'''SELECT responses FROM words WHERE word='{word}' IS NOT 'None';''')
    data=c.fetchall()
    data=data[0]
    newd=list(data)
    data=newd[0].split(",")
    if '' in data:
      data.remove('')
    data=np.array(data)  
    unique, frequency = np.unique(data, return_counts = True)
    print("Unique Responses:", unique)
    print("Frequency Of Responses:", frequency)

#required function
def deleteWord(word):
    conn = sqlite3.connect('chatml.db')
    c = conn.cursor()
    c.execute(f'''DELETE FROM words WHERE word='{word}';''')
    conn.commit()
    conn.close()

#required function
def chooseResponse(word):
    dictn=returnResponsesPercentage(word)
    response = list(dictn.keys())
    chance=list(dictn.values())
    chance[0]+=0.01
    chc=  npchoice(response,1,p=chance)
    return chc

#statistic function
def testChooseResponse(word):
    test=[]
    for x in range(100):
      test.append(chooseResponse(word))
    test=np.array(test)
    unique, frequency = np.unique(test, return_counts = True)
    print("Model Percentages: ",returnResponsesPercentage(word))
    newfreq=[]
    deviation=[]
    for x in frequency:
      newfreq.append(x/100)
    dictn=returnResponsesPercentage(word)
    pchance=[]
    for i in dictn.values():
      pchance.append(i)
    for x in range(len(newfreq)):
      deviation.append(abs(pchance[x]-newfreq[x]))
    deviation=np.array(deviation)
    deviation=np.round(deviation,decimals=2, out=None)
    print("Actual Frequency: ",newfreq)
    print("Deviation: ",deviation)

