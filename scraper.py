from bs4 import BeautifulSoup
import requests
import os
import databaseLayer as db

class Student:
    #Constructor for student
    #Has firstName, secondName (if applicable), lastName, classYear, and email
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

    while(studentCount < 10):
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
            names = assignNames(name)

            db.insertStudent(conn, names[0], names[1], names[2], int(classYear[-4:]), email)

        studentCount += 10
        print(studentCount)

    return students

#Returns list of [firstName, secondName, lastName]
def assignNames(name):
    names = name.split(' ')
    while(len(names) != 3):
        names.insert(1, '')
    return names

def main():
    conn = db.create_connection('directory.db')
    db.createProject(conn)
    scrape(conn)
    db.selectAll(conn)
    conn.close()

if __name__ == '__main__':
    main()