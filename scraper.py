from bs4 import BeautifulSoup
import requests
import os
import databaseLayer as db

class Student:
    def __init__(self, name = '', classYear = '', email = ''):
        self.assignNames(name)
        self.classYear = classYear
        self.email = email

    def assignNames(self, name):
        self.firstName = ''
        self.secondName = ''
        self.lastName = ''
        names = name.split(' ')
        self.firstName = names[0]
        if(len(names) == 3):
            self.secondName = names[1]
            self.lastName = names[2]
        elif(len(names) == 2):
            self.lastName = names[1]

    def __str__(self):
        s = ''
        s += ('First name: ' + self.firstName + '\n')
        if(self.secondName):
            s += ('Second name: ' + self.secondName + '\n')
        s += ('Last name: ' + self.lastName + '\n')
        s += ('Year: ' + self.classYear + '\n')
        s += ('Email: ' + self.email + "\n\n")
        return s

def scrape(conn):
    studentCount = 0
    doneScraping = False
    students = []

    while(not doneScraping):
        url = 'https://search.lafayette.edu/?query=*&type=directory&start=' + str(studentCount) + "&engine=directory"
        site = requests.get(url)
        soup = BeautifulSoup(site.text, 'html.parser')
        results = soup.find_all('div', {'class': 'people_information'})

        #If a page is reached where there are no more entried, end the loop
        if(len(results) == 0):
            doneScraping = True

        for result in results:
            #Obtaining relevant fields
            name = result.find('h4', {'itemprop': 'name'}).text.strip()
            role = result.find('div', {'class': 'field_title'}).text.strip()
            
            #Ignores the entry if not a student
            if role != 'Student':
                continue
            
            classYear = result.find('div', {'class': 'field_department'}).text.strip()
            email = result.find('div', {'class': 'field_email'}).text.strip()
            names = cleanNames(name)

            db.insertStudent(conn, names[0], names[1], names[2], cleanClassYear(classYear), email)

        studentCount += 10
        print(studentCount)

    return students

def cleanClassYear(text):
    text = text[-4:]
    if(isFloat(text)):
        return text
    else:
        return "\"NULL\""

#Returns list of [firstName, secondName(s), lastName]
def cleanNames(nameString):
    namesInput = nameString.split(' ')
    namesOut = []

    #First name
    namesOut.append(namesInput[0])

    #Middle name(s).. any extra names are assumed to be middle names
    if len(namesInput) > 2:
        namesOut.append(' '.join(namesInput[1:-1]))
    else:
        namesOut.append("NULL")

    #Last name(s)
    namesOut.append(namesInput[len(namesInput) - 1])
    return namesOut

def isFloat(string):
    try:
        string = float(string)
        return True
    except ValueError:
        return False

def main():
    conn = db.create_connection('directory.db')
    db.createProject(conn)
    db.clearTable(conn)
    scrape(conn)
    conn.close()

if __name__ == '__main__':
    main()