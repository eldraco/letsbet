# letsbet
A program to manage bets of multiple events between multiple people

# Configure the events

Edit `config.yaml`

<img width="332" alt="image" src="https://github.com/user-attachments/assets/1d871268-5807-4af0-9680-d0c778a299d6">


# Add the bets
run `python letsbet.py` 
You can choose as unit of bets money or beers. Here is money.

<img width="391" alt="image" src="https://github.com/user-attachments/assets/25a4c68d-6490-4166-9439-60b5cc7e334d">


# Result computation

Just run `python compute_payouts.py` and add the correct final values to let the program compute how won or lost

<img width="411" alt="image" src="https://github.com/user-attachments/assets/060ec535-1c2e-46b1-9b6b-628912e54343">

# Example betting beers

<img width="470" alt="image" src="https://github.com/user-attachments/assets/f0eacc7c-69bf-4488-9966-07b8c884635c">

And setting the bet

<img width="1250" alt="image" src="https://github.com/user-attachments/assets/a236130d-ddde-447b-a21a-259c8eaec641">



# Explanation of the Algorithm
## Input Data

Each participant places a bet and makes predictions for the outcomes of each events.
The actual outcomes of the events are provided later, after the predictions are made.
Participants also choose whether their bets are in money or beers.

## Calculate Differences

For each participant, the algorithm calculates how far their predictions are from the actual outcomes. This is done by adding up the differences between their guesses and the actual results.

## Determine Payouts

The more accurate a participant's predictions, the higher their share of the total betting pool. If someone guesses perfectly, they get the entire pool.
Each participant's share is calculated based on how small their prediction error is compared to others.
Calculate Gains and Losses:

After determining each participant's share of the pool, the algorithm calculates whether they gained or lost money (or beers) compared to their original bet.

## Settle Debts

If some participants lost and others gained, the algorithm figures out who should pay whom to balance everything out. It creates a list of instructions for settling these debts.

# Example

- Participants: Alice and Bob.
- Predictions: Alice predicts 50 for the first event and 30 for the second. Bob predicts 60 and 20.
- Bets: Alice bets 10 beers, Bob bets 5 beers.
- Actual Results: The actual outcomes are 55 and 25.

Step-by-Step:
- Calculate Differences: Alice is off by a total of 10, and Bob is off by a total of 10 as well.
- Determine Payouts: Since both have equal errors, they split the pool. Alice gets 7.5 beers, and Bob gets 7.5 beers.
- Gains/Losses: Alice gains 7.5 - 10 = -2.5 beers (loss), Bob gains 7.5 - 5 = +2.5 beers (gain).
- Settle Debts: Alice should give Bob 2.5 beers to balance everything out.
