# LetsBet
LetsBet is a program for people to bet on the outcome of different events and bet on their predictions.

It is designed to distribute the winnings from a bet among participants based on both how accurate their predictions were and how much they bet. The goal is to ensure that participants who made more accurate predictions and bet more confidently are rewarded fairly, while others may owe beers or money.


# First, define the events

Edit `config.yaml`

<img width="332" alt="image" src="https://github.com/user-attachments/assets/1d871268-5807-4af0-9680-d0c778a299d6">


# Second, make people bet
run `python letsbet.py` 
You can choose as unit of bets money or beers. Here is money.

<img width="391" alt="image" src="https://github.com/user-attachments/assets/25a4c68d-6490-4166-9439-60b5cc7e334d">


# Finally, compute results

Just run `python compute_payouts.py` and add the correct final values to let the program compute how won or lost

<img width="411" alt="image" src="https://github.com/user-attachments/assets/060ec535-1c2e-46b1-9b6b-628912e54343">

# Example betting beers

<img width="470" alt="image" src="https://github.com/user-attachments/assets/f0eacc7c-69bf-4488-9966-07b8c884635c">

And setting the bet

<img width="1250" alt="image" src="https://github.com/user-attachments/assets/a236130d-ddde-447b-a21a-259c8eaec641">



# Explanation of the Algorithm

## Collect Bets and Predictions
Each participant makes a prediction about the outcomes of some events and places a bet, either in beers or money.

## Calculate the Accuracy of Predictions
After the actual results of the events are known, the algorithm calculates how far off each participant’s predictions were from the actual results.
For each participant, it sums up the differences between their predictions and the actual results.

## Determine Weighted Scores
The algorithm divides each participant’s total difference by the amount they bet. This gives a "weighted score" that reflects both the accuracy of their predictions and their confidence (how much they bet).
Lower weighted scores are better, meaning the participant was both accurate and confident.

## Distribute the Winnings

The total pool (of beers or money) is divided among the participants based on their weighted scores. Participants with better (lower) scores get a larger share of the pool.

## Calculate Net Gain or Loss
For each participant, the algorithm calculates whether they gained or lost compared to what they originally bet.
Participants with a positive net gain will receive beers or money, while those with a negative net gain will owe beers or money.

## Settle Debts
Finally, the algorithm figures out who should pay whom. It ensures that everyone pays or receives the correct amount, rounding down to whole beers to avoid fractional payments.
If there are any remaining unpaid or unreceived beers, the algorithm tracks them separately.

# Example
- First event: How many meteors will be seen?
- Second event: How many will explode?

## Bets
- Miriam
  - Predicted 234 and 22. Bets 5 beers
- Duncan
  - Predicted 554 and 432. Bets 5 beers
- Dominik
  - Predicted 900 and 233. Bets 8 beers

Total Pool: 18 beers

## Predictions vs. Actual

- Miriam: Predicted 234 seen, 22 exploded; Actual real value: 1500 seen, 200 exploded
  - Difference: 1978 total
  - Weighted Score: 1978 / 5 = 395.6
- Duncan: Predicted 554 seen, 432 exploded; Actual real value: 1500 seen, 200 exploded
  - Difference: 1778 total
  - Weighted Score: 1778 / 5 = 355.6
- Dominik: Predicted 900 seen, 233 exploded; Actual real value: 1500 seen, 200 exploded
  - Difference: 600 total
  - Weighted Score: 600 / 8 = 75

## Inverse Weighted Scores

- Miriam: 1 / 395.6 ≈ 0.0025
- Duncan: 1 / 355.6 ≈ 0.0028
- Dominik: 1 / 75 ≈ 0.0133

Total Inverse Weighted Score: 0.0025 + 0.0028 + 0.0133 ≈ 0.0186

## Payout Distribution

- Dominik: (0.0133 / 0.0186) * 18 ≈ 12.87 beers (rounded down to 12)
- Duncan: (0.0028 / 0.0186) * 18 ≈ 2.71 beers (rounded down to 2)
- Miriam: (0.0025 / 0.0186) * 18 ≈ 2.42 beers (rounded down to 2)

## Net Gain/Loss

- Dominik: Receives 12 beers, net gain of 4 beers.
- Duncan: Owes 3 beers (5 - 2).
- Miriam: Owes 3 beers (5 - 2).

## Settlement

- Dominik receives 2 beers from Miriam and 2 beers from Duncan.




