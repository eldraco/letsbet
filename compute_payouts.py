import yaml
import csv
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
        for row in reader:
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

    # Match payments to cancel out debts
    payments = []
    while creditors and debtors:
        creditor_name, creditor_amount = creditors.pop(0)
        debtor_name, debtor_amount = debtors.pop(0)

        if creditor_amount > debtor_amount:
            payment_amount = debtor_amount
            payments.append(f"{debtor_name} should pay {creditor_name} {format_payment(payment_amount, unit)}")
            creditors.insert(0, (creditor_name, creditor_amount - debtor_amount))
        elif debtor_amount > creditor_amount:
            payment_amount = creditor_amount
            payments.append(f"{debtor_name} should pay {creditor_name} {format_payment(payment_amount, unit)}")
            debtors.insert(0, (debtor_name, debtor_amount - creditor_amount))
        else:
            payment_amount = debtor_amount
            payments.append(f"{debtor_name} should pay {creditor_name} {format_payment(payment_amount, unit)}")

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

    # Calculate payouts
    payouts = calculate_payouts(bets, actual_results)

    # Create a pretty table for results
    table = Table(title="Betting Results", show_header=True, header_style="bold magenta")
    table.add_column("Participant", justify="left", style="cyan", no_wrap=True)
    table.add_column("Original Bet", justify="right", style="green")
    table.add_column("Net Gain/Loss", justify="right", style="red")

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

        table.add_row(name, original_bet_str, net_gain_loss_str)

    console.print(table)

    # Settle debts
    payments = settle_debts(bets, payouts, unit)

    # Print settlement instructions in a styled format
    console.print("\n[bold underline]Settlement Instructions:[/bold underline]", style="blue")
    for payment in payments:
        console.print(payment, style="yellow")

