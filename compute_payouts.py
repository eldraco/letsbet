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
    inverse_differences = []
    
    for bet in bets:
        total_difference = sum(abs(bet[event] - actual_results[event]) for event in actual_results)
        if total_difference == 0:
            inverse_difference = float('inf')  # Perfect prediction should get the whole pot
        else:
            inverse_difference = 1 / total_difference
        inverse_differences.append((bet['name'], inverse_difference, bet['total_bet']))

    total_inverse = sum(inverse for _, inverse, _ in inverse_differences if inverse != float('inf'))
    payouts = {}
    
    for name, inverse_difference, bet_amount in inverse_differences:
        if inverse_difference == float('inf'):
            payout = total_pool  # If someone had a perfect prediction, they take the whole pot
        else:
            payout = (inverse_difference / total_inverse) * total_pool
        payouts[name] = payout

    return payouts

def settle_debts(bets, payouts):
    creditors = []
    debtors = []

    # Separate creditors and debtors
    for bet in bets:
        name = bet['name']
        original_bet = bet['total_bet']
        final_payout = payouts.get(name, 0)
        net_gain_loss = final_payout - original_bet

        if net_gain_loss > 0:
            creditors.append((name, net_gain_loss))
        elif net_gain_loss < 0:
            debtors.append((name, -net_gain_loss))

    # Match payments to cancel out debts
    payments = []
    while creditors and debtors:
        creditor_name, creditor_amount = creditors.pop(0)
        debtor_name, debtor_amount = debtors.pop(0)

        if creditor_amount > debtor_amount:
            payments.append(f"{debtor_name} should pay {creditor_name} ${debtor_amount:.2f}")
            creditors.insert(0, (creditor_name, creditor_amount - debtor_amount))
        elif debtor_amount > creditor_amount:
            payments.append(f"{debtor_name} should pay {creditor_name} ${creditor_amount:.2f}")
            debtors.insert(0, (debtor_name, debtor_amount - creditor_amount))
        else:
            payments.append(f"{debtor_name} should pay {creditor_name} ${debtor_amount:.2f}")

    return payments

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

    # Display the results on a single line per participant
    for bet in bets:
        name = bet['name']
        original_bet = bet['total_bet']
        final_payout = payouts.get(name, 0)
        net_gain_loss = final_payout - original_bet
        
        # Format the output as a single line
        if net_gain_loss >= 0:
            print(f"{name} originally bet: ${original_bet:.2f}, should receive: +${net_gain_loss:.2f}")
        else:
            print(f"{name} originally bet: ${original_bet:.2f}, should pay: -${abs(net_gain_loss):.2f}")
    
    # Settle debts
    payments = settle_debts(bets, payouts)
    print("\nSettlement Instructions:")
    for payment in payments:
        print(payment)

