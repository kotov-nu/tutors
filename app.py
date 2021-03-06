from flask import Flask, render_template, request
from data import goals, teachers
from json import dumps, loads
from random import shuffle

with open('teachers.json', 'w') as f:
    teachers_json = dumps(teachers)
    f.write(teachers_json)

app = Flask(__name__)


with open('teachers.json', 'r') as f:
    teachers_dict = loads(f.read())

    teachers_list = []
    for i, value in teachers_dict.items():
        teachers_list.append(value)

    shuffle(teachers_list)


def time_table(id):

    time_table = {
        '8:00': [],
        '10:00': [],
        '12:00': [],
        '14:00': [],
        '16:00': [],
        '18:00': [],
        '20:00': [],
        '22:00': [],

    }

    free = teachers_list[id]['free']
    for value in free.values():
        time_table['8:00'].append(value['8:00'])
        time_table['10:00'].append(value['10:00'])
        time_table['12:00'].append(value['12:00'])
        time_table['14:00'].append(value['14:00'])
        time_table['16:00'].append(value['16:00'])
        time_table['18:00'].append(value['18:00'])
        time_table['20:00'].append(value['20:00'])
        time_table['22:00'].append(value['22:00'])

    return time_table


def selection_teachers_by_goal(goal, teachers_list):
    suitable_teachers = []
    for teacher in teachers_list:
        if goal in teacher['goals']:
            suitable_teachers.append(teacher)

    return suitable_teachers


def save_booking_info(id, name, phone):

    with open('booking.json', 'r') as f:

        all_info = f.read()
        if all_info:
            loads(all_info).update({id: {'name': name, 'phone': phone}})
        else:
            all_info = {}
            all_info.update({id: {'name': name, 'phone': phone}})

    with open('booking.json', 'w') as f:
        f.write(dumps(all_info))


def save_pick_info(name, phone, goal, time):

    with open('request.json', 'r') as f:

        all_info = f.read()
        if all_info:
            loads(all_info).update({'name': name, 'phone': phone, 'goal': goal, 'time': time})
        else:
            all_info = {}
            all_info.update({'name': name, 'phone': phone, 'goal': goal, 'time': time})

    with open('request.json', 'w') as f:
        f.write(dumps(all_info))


@app.route('/')
def index():
    return render_template('index.html', teachers=teachers_list[:6], goals=goals)


@app.route('/profiles/<int:id>')
def profiles(id):
    return render_template('profile.html', teacher=teachers_list[id], time_table=time_table(id + 1), id=id)


@app.route('/goal/<goal>')
def goal(goal):
    suitable_teachers = selection_teachers_by_goal(goal, teachers_list)
    return render_template('goal.html', suitable_teachers=suitable_teachers, goal=goals[goal].split())


@app.route('/booking/<int:id>')
def booking(id):
    return render_template('booking.html', teacher=teachers_list[id], id=id)


@app.route('/sent/<int:id>', methods=['GET', 'POST'])
def sent(id):

    name = request.form.get('name')
    phone = request.form.get('phone')
    save_booking_info(id, name, phone)

    return render_template('sent.html', teacher=teachers_list[id], name=name, phone=phone)


@app.route('/pick/')
def pick():
    return render_template('pick.html')


@app.route('/sent_pick/', methods=['POST'])
def sent_pick():

    name = request.form.get('name')
    phone = request.form.get('phone')
    goal = request.form.get('goal')
    time = request.form.get('time')
    save_pick_info(name, phone, goal, time)

    return render_template('sent_pick.html', name=name, phone=phone)


if __name__ == '__main__':
    app.run()