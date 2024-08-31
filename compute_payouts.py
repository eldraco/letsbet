import yaml
import csv
from math import floor
from rich.console import Console
from rich.table import Table

def load_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_bets(filename='bets.tsv'):
    bets = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:  # Corrected line, removed the extra closing parenthesis
            bet = {}
            for key, value in row.items():
                if key == 'name' or key == 'unit':
                    bet[key] = value  # Keep 'name' and 'unit' as strings
                elif key == 'total_bet':
                    bet[key] = float(value)  # Keep total_bet as float
                else:
                    bet[key] = int(value)  # Convert event guesses to int
            bets.append(bet)
    return bets

def calculate_payouts(bets, actual_results):
    total_pool = sum(bet['total_bet'] for bet in bets)
    weighted_scores = []
    
    # Calculate weighted score for each participant
    for bet in bets:
        total_difference = sum(abs(bet[event] - actual_results[event]) for event in actual_results)
        weighted_score = total_difference / bet['total_bet']  # Lower score is better
        weighted_scores.append((bet['name'], weighted_score, bet['total_bet']))

    # Calculate the inverse weighted scores
    inverse_scores = [(name, 1 / score) for name, score, bet_amount in weighted_scores]
    total_inverse_score = sum(inverse_score for _, inverse_score in inverse_scores)
    
    payouts = {}
    
    # Calculate each participant's payout based on their inverse score
    for name, inverse_score in inverse_scores:
        payout = (inverse_score / total_inverse_score) * total_pool
        payouts[name] = payout

    return payouts

def settle_debts(bets, payouts, unit):
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

    payments = []
    
    # Match payments to cancel out debts
    while creditors and debtors:
        creditor_name, creditor_amount = creditors.pop(0)
        debtor_name, debtor_amount = debtors.pop(0)

        # Use floor to calculate the number of beers (ignore fractions)
        creditor_beers = floor(creditor_amount)
        debtor_beers = floor(debtor_amount)

        if creditor_beers > debtor_beers:
            payments.append(f"{debtor_name} should pay {creditor_name} {format_payment(debtor_beers, unit)}")
            creditors.insert(0, (creditor_name, creditor_amount - debtor_beers))
        elif debtor_beers > creditor_beers:
            payments.append(f"{debtor_name} should pay {creditor_name} {format_payment(creditor_beers, unit)}")
            debtors.insert(0, (debtor_name, debtor_amount - creditor_beers))
        else:
            payments.append(f"{debtor_name} should pay {creditor_name} {format_payment(debtor_beers, unit)}")

    # If there are remaining fractional beers that were not fully paid, process them
    while creditors:
        creditor_name, creditor_amount = creditors.pop(0)
        remaining_beers = floor(creditor_amount)
        if remaining_beers > 0:
            payments.append(f"{creditor_name} is still owed {format_payment(remaining_beers, unit)}")
    
    while debtors:
        debtor_name, debtor_amount = debtors.pop(0)
        remaining_beers = floor(debtor_amount)
        if remaining_beers > 0:
            payments.append(f"{debtor_name} still owes {format_payment(remaining_beers, unit)}")

    return payments

def format_payment(amount, unit):
    if unit == "beers":
        return "🍺" * int(amount)
    else:
        return f"${amount:.2f}"

if __name__ == "__main__":
    console = Console()

    config = load_config()
    events = config['events']

    # Load bets
    bets = load_bets()

    # Load the unit choice
    with open('unit_choice.txt', 'r') as file:
        unit = file.read().strip()

    # Get actual results
    actual_results = {}
    for event in events:
        event_name = event['name']
        actual_results[event_name] = int(input(f"Enter the actual result for {event_name}: "))

    # Print the original bets and predictions
    table_bets = Table(title="Original Bets and Predictions", show_header=True, header_style="bold blue")
    table_bets.add_column("Participant", justify="left", style="cyan", no_wrap=True)
    for event in events:
        table_bets.add_column(f"Prediction: {event['name']}", justify="right", style="magenta")
    table_bets.add_column("Total Bet", justify="right", style="green")

    for bet in bets:
        row = [bet['name']]
        for event in events:
            row.append(str(bet[event['name']]))
        if unit == "beers":
            row.append("🍺" * int(bet['total_bet']))
        else:
            row.append(f"${bet['total_bet']:.2f}")
        table_bets.add_row(*row)

    console.print(table_bets)

    # Calculate payouts
    payouts = calculate_payouts(bets, actual_results)

    # Create a pretty table for results
    table_payouts = Table(title="Betting Results", show_header=True, header_style="bold magenta")
    table_payouts.add_column("Participant", justify="left", style="cyan", no_wrap=True)
    table_payouts.add_column("Original Bet", justify="right", style="green")
    table_payouts.add_column("Net Gain/Loss", justify="right", style="red")

    # Populate the table with participant data
    for bet in bets:
        name = bet['name']
        original_bet = bet['total_bet']
        final_payout = payouts.get(name, 0)
        net_gain_loss = final_payout - original_bet

        if unit == "beers":
            net_gain_loss_str = "🍺" * int(net_gain_loss) if net_gain_loss >= 0 else "-" + "🍺" * int(abs(net_gain_loss))
            original_bet_str = "🍺" * int(original_bet)
        else:
            net_gain_loss_str = f"+${net_gain_loss:.2f}" if net_gain_loss >= 0 else f"-${abs(net_gain_loss):.2f}"
            original_bet_str = f"${original_bet:.2f}"

        table_payouts.add_row(name, original_bet_str, net_gain_loss_str)

    console.print(table_payouts)

    # Settle debts
    payments = settle_debts(bets, payouts, unit)

    # Print settlement instructions in a styled format
    console.print("\n[bold underline]Settlement Instructions:[/bold underline]", style="blue")
    for payment in payments:
        console.print(payment, style="yellow")

