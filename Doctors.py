"""
Patient / Doctor Scheduler -
Create a patient class and a doctor class. Have a doctor that can handle multiple patients and setup a scheduling
program where a doctor can only handle 16 patients during an 8 hr work day.

users - admin, doctor, patient
"""
import calendar
import datetime
import csv
from tabulate import tabulate


class Person(object):

    def __init__(self, username, password, user_role, first_name, surname):

        self.username = username
        self.password = password
        self.user_role = user_role
        self.first_name = first_name
        self.surname = surname

    def __str__(self):
        return '{username}, {password}, {user_role}, {first_name}, {surname}'.format(username=self.username,
                                                                                     password=self.password,
                                                                                     user_role=self.user_role,
                                                                                     first_name=self.first_name,
                                                                                     surname=self.surname)


class Doctor(Person):

    def show_menu(self):
        print 'What would you like to do? Please select a number. \n\nMenu: \n'
        while True:
            try:
                menu = '1. Book appointment \n2. Edit appointment \n3. View my appointments \n4. Edit my profile ' \
                       '\n5. Exit \n'
                print menu
                response = menu.split(raw_input() + '.')[1].split('\n')[0].strip()
                return response
            except:
                print 'Invalid input \n'
                continue


class Patient(Person):

    def show_menu(self):
        print 'What would you like to do? Please select a number. \n\nMenu: \n'
        while True:
            try:
                menu = '1. Book appointment \n2. Edit appointment \n3. View my appointments \n4. Edit my profile ' \
                       '\n5. Exit \n'
                print menu
                response = menu.split(raw_input() + '.')[1].split('\n')[0].strip()
                return response
            except:
                print 'Invalid input \n'
                continue


class Admin(Person):

    def show_menu(self):
        print 'What would you like to do? Please select a number. \n\nMenu: \n'
        while True:
            try:
                menu = '1. Book appointment \n2. Edit appointment \n3. View my appointments \n4. User list ' \
                       '\n5. Add user \n6. Remove user \n7. Edit user \n8. Edit my profile \n9. Exit \n'
                print menu
                response = menu.split(raw_input() + '.')[1].split('\n')[0].strip()
                return response
            except:
                print 'Invalid input \n'
                continue


class Appointment(object):
    def __init__(self, doctor, patient, time, descr):
        self.doctor = doctor
        self.patient = patient
        self.time = time
        self.descr = descr

    def __str__(self):
        return '{doctor}, {patient}, {time}, {descr}'.format(doctor=self.doctor, patient=self.patient, time=self.time,
                                                             descr=self.descr)


def load_users():
    """
    Reads the file storing all of the system's registered users and their details, creates all of the users as
    object instances (Admin users, Doctor users and Patient users) and returns them in a dictionary (user_store)
    """
    global user_store
    with open('Doc_users.txt', 'rb') as load_user_list:
        reader = csv.reader(load_user_list, delimiter=',')
        for row in reader:
            if row[2].strip() == 'Admin':  # Load admin users as Admin objects
                user_store[row[0]] = Admin(row[0], row[1], row[2], row[3], row[4])
            elif row[2].strip() == 'Doctor':  # Load doctor users as Doctor objects
                user_store[row[0]] = Doctor(row[0], row[1], row[2], row[3], row[4])
            else:  # Load patient users as Patient objects
                user_store[row[0]] = Patient(row[0], row[1], row[2], row[3], row[4])


def create_cal():
    """
    Used only once, function creates the calendar for appointments.
    """
    global cal
    start_date = datetime.date(2017, 9, 1)
    start_time = datetime.time(9)
    end_time = datetime.time(17, 40)
    end_date = datetime.date.today() + datetime.timedelta(weeks=8)
    date = start_date
    while date < end_date:
        slot = datetime.datetime.combine(date, start_time)
        slots = [slot]
        while slot < datetime.datetime.combine(date, end_time):
            slot = slot + datetime.timedelta(minutes=20)
            slots.append(slot)
        cal[date] = slots
        date += datetime.timedelta(days=1)


def load_appts():
    """
    Function to load appointments from file
    """
    global appts, count
    with open('Appointments.txt', 'rb') as load_appts_list:
        reader = csv.reader(load_appts_list, delimiter='\t')
        for row in reader:
            appts[count] = Appointment(row[0],
                                       row[1],
                                       datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'),
                                       row[3])
            count += 1


def login():
    """
    Function to take the user's credentials and compare them against user_store to allow them access to the system.
    After three incorrect attempts the program will exit.
    """
    global user, user_store
    found = False
    try_count = 1
    while found is False and try_count < 4:
        inp_username = raw_input('Username: ')
        inp_password = raw_input('Password: ')
        for record in user_store:
            if user_store[record].username == inp_username and user_store[record].password == inp_password:
                user = user_store[record]
                print 'Hello {name}'.format(name=user.first_name)
                found = True
                break
        try_count += 1
        continue
    if found is False:
        print 'Too many incorrect attempts. '
        raise SystemExit
    else:
        menu_response(user.show_menu())


def menu_response(response):
    """
    Takes the user's menu response and calls the appropriate function
    """
    global user_store, user
    if response == 'Book appointment':
        book_appointment()
    elif response == 'Edit appointment':
        edit_appointment()
    elif response == 'View my appointments':
        view_appts(user)
    elif response == 'User list':
        user_list()
    elif response == 'Add user':
        add_user()
    elif response == 'Remove user':
        remove_user()
    elif response == 'Edit user':
        found = False
        cont = ''
        while found is False:
            edit_user = raw_input('Whose profile would you like to edit? (enter their username) ')
            for person in user_store:
                if user_store[person].username == edit_user:
                    found = True
                    edit_profile(user_store[person])
            if found is False:
                cont = yn_input_check('User not found. Try again?')
            if cont == 'Y':
                continue
            else:
                break
    elif response == 'Edit my profile':
        edit_profile(user)
    elif response == 'Exit':
        save_and_exit()
    menu_response(user.show_menu())


def book_appointment():
    """Function for booking new appointments"""
    global appts, cal, count, user_store
    while True:
        doc = raw_input('Which doctor would you like to see? Please enter their user name. ')
        for p in user_store:
            if user_store[p].username == doc and user_store[p].user_role == 'Doctor':
                break
        print 'Doctor not found.'
    while True:
        day = select_day('Which day do you want to make your appointment?')
        if day > (datetime.date.today() + datetime.timedelta(weeks=8)):
            print 'You cannot book appointments that far in advance. Please select another date. '
            continue
        elif day < datetime.date.today():
            print 'You cannot book appointments in the past. Please select another date. '
            continue
        else:
            appt_count = 0
            for appt in appts:
                if appts[appt].time.date() == day and appts[appt].doctor == doc:
                    appt_count += 1
            if appt_count > 15:
                print 'Dr {surname} has no free appointments on {date}. Please choose another day. '\
                    .format(surname=user_store[doc].surname, date=day.strftime('%a %b %d'))
                continue
            else:
                break
    print 'Dr {surname} is free at these times on {date}: '.format(surname=user_store[doc].surname,
                                                                   date=day.strftime('%a %b %d'))
    for slot in cal[day]:
        free = 1
        for appt in appts:
            if appts[appt].time == slot and appts[appt].doctor == doc:
                free = 0
        if free == 1:
            print slot.strftime('%H:%M')
    while True:
        try:
            selection = raw_input('Which time slot would you like to take? (enter HH:MM) ').split(':')
            hr = int(selection[0])
            mins = int(selection[1])
            appt_time = datetime.time(hr, mins)
            break
        except:
            print 'Invalid input. '
    description = raw_input('Please enter a brief description of what you would like to discuss with the doctor.\n')
    appts[count] = Appointment(doc, user.username, datetime.datetime.combine(day, appt_time), description)
    count += 1


def select_day(question):
    today = datetime.date.today()
    m = today.month
    y = today.year
    while True:
        print calendar.month(y, m)
        try:
            d = int(raw_input('{text}\nEnter the number or enter 0 to choose a different month. '
                              .format(text=question)))
            if d > calendar.monthrange(y, m)[1]:
                print "There aren't that many days in the month!"
                continue
            elif d == 0:
                (m, y) = select_month(y)
                continue
            else:
                return datetime.date(y, m, d)
        except:
            print 'Invalid input.'
            continue


def select_month(y):
    while True:
        try:
            m = int(raw_input('In which month do you want to make your appointment?\n'
                              'Enter 1-12 or 0 for a different year'))
            if 0 < m < 13:
                return (m,y)
            elif m == 0:
                y = select_yr()
                continue
            else:
                print 'Invalid input. '
                continue
        except:
            print 'Invalid input. '
            continue


def select_yr():
    while True:
        try:
            y = int(raw_input('Input a year. '))
            if len(str(y)) == 4:
                return y
            else:
                print 'Invalid input. '
                continue
        except:
            print 'Invalid input. '
            continue


def edit_appointment():
    """Function for editing existing appointments"""
    pass


def view_appts(name):
    """Function to display the calendar"""
    global appts
    while True:
        choice = raw_input('Would you like to see all of your appointments or select a specific day? '
                           '(Input "day", "today" or "all")').lower()
        data = []
        if choice == 'all':
            for appt in appts:
                if appts[appt].patient == name.username or appts[appt].doctor == name.username:
                    data.append([appts[appt].doctor, appts[appt].patient, appts[appt].time, appts[appt].descr])
            break
        elif choice == 'today':
            for appt in appts:
                if (appts[appt].patient == name.username or appts[appt].doctor == name.username) \
                        and appts[appt].time.date() == datetime.date.today():
                    data.append([appts[appt].doctor, appts[appt].patient, appts[appt].time, appts[appt].descr])
        elif choice == 'day':
            day = select_day('Which day would you like to view?')
            for appt in appts:
                if (appts[appt].patient == name.username or appts[appt].doctor == name.username) \
                        and appts[appt].time.date() == day:
                    data.append([appts[appt].doctor, appts[appt].patient, appts[appt].time, appts[appt].descr])
        else:
            print 'Invalid input. '
            continue
    print tabulate(sorted(data, key=lambda appointment: appointment[2]), headers=['Doctor', 'Patient', 'Date and Time', 'Description'], tablefmt='orgtbl')


def add_user():
    """Admin function for creating new users"""
    global user, user_store
    username = raw_input('What is their username? ')  # add check for existing username
    password = raw_input('What is their password? ')
    user_role = raw_input('What is their role? ')
    first_name = raw_input('What is their first name? ')
    surname = raw_input('What is their surname? ')
    if user_role == 'Admin':
        user_store[username] = Admin(username, password, user_role, first_name, surname)
    elif user_role == 'Doctor':
        user_store[username] = Doctor(username, password, user_role, first_name, surname)
    else:
        user_store[username] = Patient(username, password, user_role, first_name, surname)
    print 'New user {username} has been created'.format(username=user_store[username].username)


def remove_user():
    """Admin function for removing users"""
    global user, user_store
    found = False
    check = 'N'
    while found is False:
        del_user = raw_input('Enter the username of the user you would like to remove. ')
        for person in user_store:
            if user_store[person].username == del_user:
                found = True
                print 'Username = {username} \nUser role = {user_role} \nFirst name: {first_name} \n' \
                      'Surname: {surname} \n'.format(username=user_store[person].username,
                                                     user_role=user_store[person].user_role,
                                                     first_name=user_store[person].first_name,
                                                     surname=user_store[person].surname)
                check = yn_input_check('Are you sure you want to delete this user? (Y/N) ')
        if check == 'Y':
            user_store.pop(del_user)
            print 'User deleted.\n'
        if found is False:
            cont = yn_input_check('User not found. Continue ? (Y/N) ')
            if cont == 'Y':
                continue
            else:
                break
        else:
            more = yn_input_check('Do you want to delete another user? (Y/N) ')
            if more == 'Y':
                found = False
                continue
            else:
                break


def edit_profile(name):
    """Admin function for editing the profiles of a user    """
    global user
    attribute = ''
    print '1. Username = {username} \n2. Password = {password} \n3. User role = {user_role} \n' \
          '4. First name: {first_name} \n5. Surname: {surname} \n'.format(username=name.username,
                                                                          password=name.password,
                                                                          user_role=name.user_role,
                                                                          first_name=name.first_name,
                                                                          surname=name.surname)
    while True:
        try:
            edit = int(raw_input('Which attribute would you like to change? Enter a number.'))
            if 0 < edit < 6:
                break
            else:
                print 'Invalid input. '
                continue
        except:
            print 'Invalid input. '
            continue
    new_value = raw_input('Please input a new value ')
    if edit == 1:
        name.username = new_value
        print 'Username successfully updated. \n Username: {value}'.format(value=name.username)
    elif edit == 2:
        name.password = new_value
        print 'Password successfully updated. \n Password: {value}'.format(value=name.password)
    elif edit == 3:
        if user.user_role != 'Admin':
            print "Only admin users may change a user's role"
        else:
            temp = name
            user_store.pop(name)
            if temp.user_role == 'Admin':
                user_store[name] = Admin(temp.username, temp.password, 'Admin', temp.first_name, temp.surname)
            elif temp.user_role == 'Doctor':
                user_store[name] = Doctor(temp.username, temp.password, 'Doctor', temp.first_name, temp.surname)
            elif temp.user_role == 'Patient':
                user_store[name] = Patient(temp.username, temp.password, 'Patient', temp.first_name, temp.surname)
            print 'User role successfully updated. \n User role: {value}'.format(value=name.user_role)
    elif edit == 4:
        name.first_name = new_value
        print 'First name successfully updated. \n First name: {value}'.format(value=name.first_name)
    elif edit == 5:
        name.surname = new_value
        print 'Surname successfully updated. \n Surname: {value}'.format(value=name.surname)
    more = yn_input_check('Do you want to update another attribute? ')
    if more == 'Y':
        edit_profile(name)

"""
def update(name,attribute,new_value):
    name.attribute = new_value
    print '{attr} succesfully updated. \n {attr}: {value}'.format(attr=attribute, value=name.attribute)
"""


def user_list():
    """Function to display a list of all users and their details"""
    global user_store
    data = []
    for p in user_store:
        data.append([user_store[p].username, user_store[p].password, user_store[p].user_role, user_store[p].first_name,
                     user_store[p].surname])
    print tabulate(sorted(data, key=lambda person: person[0]), headers=['Username', 'Password', 'User Role', 'First Name', 'Surname'], tablefmt='orgtbl')
    print'\n'


def yn_input_check(q):
    """Takes a question with Y/N answer and validates that Y or N has been received. If not, repeats the question."""
    while True:
        inp = raw_input(q).upper()
        if inp == 'Y' or inp == 'N':
            return inp
        else:
            print 'Invalid input. \n'


def save_and_exit():
    global user_store
    global appts
    """Function to save the current user and appointment dictionaries to file and exit the program"""
    sure = yn_input_check('Are you sure you want to exit? (Y/N) ')
    if sure == 'Y':
        with open('Doc_users.txt', 'wb') as save_user_list:
            writer = csv.writer(save_user_list, delimiter=',')
            for person in user_store:
                writer.writerow([user_store[person].username, user_store[person].password, user_store[person].user_role,
                                user_store[person].first_name, user_store[person].surname])
        with open('Appointments.txt', 'wb') as save_appts_list:
            writer = csv.writer(save_appts_list, delimiter='\t')
            for appt in appts:
                writer.writerow([appts[appt].doctor, appts[appt].patient, appts[appt].time, appts[appt].descr])
        raise SystemExit


# Program body

user_store = {}
user = ''
appts = {}
cal = {}
count = 0
load_users()
create_cal()
load_appts()
login()
