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

- **Objective**: Determine the payout distribution among participants based on the accuracy of their predictions and the amounts they bet.

#### 1. **Input Data**
   - Each participant provides:
     - A **bet amount** $\( B_i \)$.
     - Predictions for the outcomes of two events.
   - The actual outcomes of the events are given.

#### 2. **Calculate Total Difference** $\( D_i \)$
   - For each participant $\( i \)$:
     $\[
     D_i = \sum_{j=1}^{n} \left| \text{Prediction}_{ij} - \text{Actual Outcome}_j \right|
     \]$
     - $\( D_i \)$ is the sum of the absolute differences between each participant's predictions and the actual outcomes across all events.

#### 3. **Calculate Inverse Difference** $\( I_i \)$
   - Compute the inverse difference for each participant:
     \[$I_i = \frac{1}{D_i}$ \quad \text{(if $\( D_i \)$ is not zero)}\]

     - If $\( D_i = 0 \)$ (perfect prediction), assign $\( I_i = \infty \)$ (this participant should receive the entire pool).

#### 4. **Compute Total Inverse Score**
   - Sum the inverse differences of all participants:
     $\[
     T_I = \sum_{i=1}^{m} I_i
     \]$
     - $\( T_I \)$ represents the total of all inverse differences.

#### 5. **Determine Payouts** $\( P_i \)$
   - For each participant:
     $\[
     P_i = \frac{I_i}{T_I} \times \text{Total Pool}
     \]$
     - Each participant's payout $\( P_i \)$ is proportional to their inverse difference relative to the total.

#### 6. **Calculate Net Gain/Loss** $\( G_i \)$
   - Determine how much each participant gained or lost:
     $\[
     G_i = P_i - B_i
     \]$
     - $\( G_i \)$ represents the net gain (if positive) or loss (if negative).

#### 7. **Settle Debts**
   - Identify **creditors** (participants with $\( G_i > 0 \)$) and **debtors** (participants with $\( G_i < 0 \)$).
   - Debtors should pay creditors until all debts are settled:
     - Match payments between debtors and creditors based on the amounts owed.

This algorithm ensures a fair distribution of the betting pool based on prediction accuracy and helps settle any outstanding balances between participants.
