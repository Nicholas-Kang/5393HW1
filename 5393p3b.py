import numpy as np
import matplotlib.pyplot as plt

def simulate_exp_log(X0, max_steps=5000):
    # intial sate
    state = {'X': X0, 'Y': 1, 'I': 0, 'a': 0, 'b': 1, 'c': 0, 'Xp': 0, 'step': 0, 'Yp': 0}
    
    # magnitudes for reactions
    k = {
        'fastest': 1e8,
        'faster':  1e6,
        'fast':    1e4,
        'medium':  1.0,
        'slow':    1e-2,
        'slowest': 1e-4
    }
    
    for _ in range(max_steps):
        p = [
            # Part A: Logarithm Stage (I = log2 X)
            k['slow'] * state['b'],                                      # 0: b -> a + b
            k['faster'] * state['a'] * state['X'] * (state['X']-1)/2 if state['X'] >= 2 else 0, # 1: a + 2X -> c + Xp + a
            k['faster'] * state['c'] * (state['c']-1)/2 if state['c'] >= 2 else 0, # 2: 2c -> c (OCR FIX)
            k['fast'] * state['a'],                                      # 3: a -> 0
            k['medium'] * state['Xp'],                                   # 4: Xp -> X
            k['medium'] * state['c'],                                    # 5: c -> I
            
            # Part B: Exponentiation Stage (Y = 2^I)
            k['slowest'] * state['I'],                                   # 6: I -> step
            k['faster'] * state['step'] * state['Y'],                    # 7: step + Y -> step + 2Yp
            k['fast'] * state['step'],                                   # 8: step -> 0
            k['medium'] * state['Yp']                                    # 9: Yp -> Y
        ]
        
        total = sum(p)
        if total <= 0: break
        
        # Select reaction
        r = np.random.uniform(0, total)
        curr, idx = 0, -1
        for i, val in enumerate(p):
            curr += val
            if r <= curr:
                idx = i
                break
        
        # Update State
        if idx == 0: state['a'] += 1
        elif idx == 1: state['X'] -= 2; state['c'] += 1; state['Xp'] += 1
        elif idx == 2: state['c'] -= 1
        elif idx == 3: state['a'] -= 1
        elif idx == 4: state['Xp'] -= 1; state['X'] += 1
        elif idx == 5: state['c'] -= 1; state['I'] += 1
        elif idx == 6: state['I'] -= 1; state['step'] += 1
        elif idx == 7: state['Y'] -= 1; state['Yp'] += 2  # Doubling logic
        elif idx == 8: state['step'] -= 1
        elif idx == 9: state['Yp'] -= 1; state['Y'] += 1
        
    return state['Y']

# Run 100 trials
trials = 100
X_input = 64
final_counts = [simulate_exp_log(X_input) for _ in range(trials)]

# printing output stats
print(f"Mean Final Y: {np.mean(final_counts):.2f}")
print(f"Variance: {np.var(final_counts):.2f}")

# making the plot
plt.figure(figsize=(10, 6))
plt.hist(final_counts, bins=range(min(final_counts), max(final_counts) + 2), 
         color='lightgreen', edgecolor='black', align='left')
current_ticks = plt.xticks()[0]
new_ticks = sorted(list(set(current_ticks) | {X_input}))
plt.xticks(new_ticks)
plt.title(f'Distribution of Final Y over {trials} Runs ($Y = 2^{{\\log_2 {X_input}}}$)')
plt.xlabel('Final Value of Y')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.3)
plt.show()