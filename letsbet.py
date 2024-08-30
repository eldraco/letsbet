import yaml
import csv

def load_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_betting_data(config):
    events = config['events']
    data = []

    while True:
        name = input("Enter name of the person betting: ")
        event_guesses = {}
        for event in events:
            event_name = event['name']
            guess = int(input(f"Enter {name}'s guess for {event_name}: "))
            event_guesses[event_name] = guess

        total_bet = float(input(f"Enter the total bet amount for {name}: "))

        # Store the data
        entry = {
            'name': name,
            'total_bet': total_bet,
        }
        entry.update(event_guesses)
        data.append(entry)

        more = input("Do you want to add more bets? (yes/no): ")
        if more.lower() != 'yes':
            break

    return data

def save_data_to_tsv(data, filename='bets.tsv'):
    keys = data[0].keys()
    with open(filename, 'w', newline='') as file:
        dict_writer = csv.DictWriter(file, fieldnames=keys, delimiter='\t')
        dict_writer.writeheader()
        dict_writer.writerows(data)

if __name__ == "__main__":
    config = load_config()
    data = get_betting_data(config)
    save_data_to_tsv(data)
