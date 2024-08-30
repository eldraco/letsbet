import yaml
import csv

def load_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_bets(filename='bets.tsv'):
    bets = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            bet = {}
            for key, value in row.items():
                if key == 'name':
                    bet[key] = value
                elif key == 'total_bet':
                    bet[key] = float(value)  # Keep total_bet as float
                else:
                    bet[key] = int(value)  # Convert event guesses to int
            bets.append(bet)
    return bets

def calculate_payouts(bets, actual_results):
    total_pool = sum(bet['total_bet'] for bet in bets)
    weighted_scores = []
    exact_matches = []
    
    for bet in bets:
        total_difference = sum(abs(bet[event] - actual_results[event]) for event in actual_results)
        
        if total_difference == 0:
            exact_matches.append((bet['name'], bet['total_bet']))
        else:
            weighted_score = total_difference / bet['total_bet']
            weighted_scores.append((bet['name'], weighted_score))

    payouts = {}

    if exact_matches:
        # If there are exact matches, they split the total pool
        exact_total_bet = sum(bet for _, bet in exact_matches)
        for name, bet in exact_matches:
            payouts[name] = (bet / exact_total_bet) * total_pool
    else:
        # If no exact matches, proceed with weighted score calculations
        total_inverse_weighted_score = sum(1 / score for _, score in weighted_scores)
        
        for name, score in weighted_scores:
            inverse_score = 1 / score
            payout = (inverse_score / total_inverse_weighted_score) * total_pool
            payouts[name] = payout

    return payouts

if __name__ == "__main__":
    config = load_config()
    events = config['events']

    # Load bets
    bets = load_bets()

    # Get actual results
    actual_results = {}
    for event in events:
        event_name = event['name']
        actual_results[event_name] = int(input(f"Enter the actual result for {event_name}: "))

    # Calculate payouts
    payouts = calculate_payouts(bets, actual_results)

    # Display the results
    for name, payout in payouts.items():
        print(f"{name} should receive: ${payout:.2f}")

