import random

balance = 100
autopark = []
vehicle = {
                'Car': 20,
                'Bus': 50,
                'Truck': 80
            }

affordable_vehicle = {}


greetings = f"Hi there! Now, you are in the game. You have {balance} gold coins and you need to create your own auto-park."
print(greetings)

vehicle_one = input(f"You can choose your vehicle from this list: {vehicle}")

balance -= vehicle[vehicle_one]
autopark.append(vehicle_one)

while balance >= min(vehicle.values()):
    vehicle_new = input(f'Good deal! Now, your balance is {balance} and you own {autopark}. Do you wanna buy something else?')
    if vehicle_new == 'Yes':
        vehicle_new = input(f"You can choose your vehicle from this list: {vehicle}")
        if vehicle[vehicle_new] <= balance:
            balance -= vehicle[vehicle_new]
            autopark.append(vehicle_new)
        else:
            for k, v in vehicle.items():
                if vehicle[k] <= balance:
                    affordable_vehicle[k] = v
            vehicle_new = input(f"Ops! You don't have enough gold coins. You can not buy {vehicle_new}, but you can choose vehicle from this list {affordable_vehicle}")
            balance -= vehicle[vehicle_new]
            autopark.append(vehicle_new)
    elif vehicle_new != 'Yes' and vehicle_new != 'No':
        vehicle_new = input(f'Sorry, I can not understand you:( Please enter "Yes" or "No"')
    else:
        break

# when I don't have enough money it gives me wrong choice of transport. I have 30 coins, I can buy only car, but it suggests me car and bus.


print(f"Congratulations! You built your own auto-park. Your balance is {balance} gold coins. You own {autopark}.")

task_acceptance = input(f"Now, it's time to complete 1st task. Do you want to start?")


state = {
    "task_number": 0,
    "task_acceptance": ''
}

state["task_acceptance"] = task_acceptance

def task_creation():

    state["task_number"] += 1

    if state["task_number"] == 1:
        task_number = '1st'
    elif state["task_number"] == 2:
        task_number = '2nd'
    elif state["task_number"] == 3:
        task_number = '3rd'
    else:
        task_number = str(state["task_number"])+ 'th'

    task_type = ['passengers', 'tons of goods']
    task_choice = random.choice(task_type)

    if task_choice == 'passengers':
        task_size = random.randrange(50)
        task_price = 3*task_size
        task_cost = 1.25*task_size
        task_distance = random.randrange(3000)
        if task_size <= 3:
            task_vehicle = 'Car'
            task_time = task_distance / 120
        else:
            task_vehicle = 'Bus'
            task_time = task_distance / 80

    else:
        task_size = random.randrange(60)
        task_price = 10*task_size
        task_cost = 6.75 * task_size
        task_distance = random.randrange(7000)
        task_vehicle = 'Truck'
        task_time = task_distance / 100

    task = (f'This is your {task_number} task. You have to deliver {task_size} {task_choice}.'
            f'You will earn {task_price} gold coins. It will cost {task_cost}. Your profit is {task_price - task_cost} gold coins.'
            f'You have to use {task_vehicle}, delivery distance is {task_distance} and it will take {task_time} hours.')
    print(task)
    task_acceptance = input(f"Do you want to accept this task?")
    state["task_acceptance"] = task_acceptance


while state["task_acceptance"] == 'Yes':
    task_creation()






