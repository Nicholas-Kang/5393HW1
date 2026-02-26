import numpy as np
import matplotlib.pyplot as plt

def simulate_z_log_y_strict(X0, Y0, max_steps=4000):

    #initial state
    state = {'X': X0, 'Y': Y0, 'Z': 0, 'b': 1, 'a': 0, 'c': 0, 'L': 0, 'amp': 0, 'Xp': 0, 'Yp': 0}
    
    #reaction magnitudes
    k = {
        'fastest': 1e8,
        'faster':  1e6,
        'fast':    1e4,
        'medium':  1.0,
        'slow':    1e-2,
        'slowest': 1e-4
    }
    
    for _ in range(max_steps):
        #calculating likelihood of each of the 10 reactions
        p = [
            k['slow'] * state['b'],
            k['faster'] * state['a'] * state['Y'] * (state['Y']-1)/2 if state['Y'] >= 2 else 0,
            k['faster'] * state['c'] * (state['c']-1)/2 if state['c'] >= 2 else 0,
            k['fast'] * state['a'],
            k['medium'] * state['Yp'],
            k['medium'] * state['c'],
            k['slowest'] * state['L'],
            k['fastest'] * state['amp'] * state['X'],
            k['fast'] * state['amp'],
            k['medium'] * state['Xp'] 
        ]
        
        total = sum(p) # sum of all rates
        if total <= 0: break
        
        #determine next reaction
        r = np.random.uniform(0, total)
        curr, idx = 0, -1
        for i, val in enumerate(p):
            curr += val #loops through list of rates and add them up
            if r <= curr:
                idx = i #index slsected after curr exceeds rand num
                break
        
        #updating state
        if idx == 0: state['a'] += 1
        elif idx == 1: state['Y'] -= 2; state['c'] += 1; state['Yp'] += 1
        elif idx == 2: state['c'] -= 1 
        elif idx == 3: state['a'] -= 1
        elif idx == 4: state['Yp'] -= 1; state['Y'] += 1
        elif idx == 5: state['c'] -= 1; state['L'] += 1
        elif idx == 6: state['L'] -= 1; state['amp'] += 1
        elif idx == 7: state['X'] -= 1; state['Xp'] += 1; state['Z'] += 1
        elif idx == 8: state['amp'] -= 1
        elif idx == 9: state['Xp'] -= 1; state['X'] += 1
        
    return state['Z']

# 100 trials for computations
trials = 100
X_input, Y_input = 4, 64
final_results = [simulate_z_log_y_strict(X_input, Y_input) for _ in range(trials)]

#printing results
print(f"Mean: {np.mean(final_results):.2f}, Variance: {np.var(final_results):.2f}")

#plotting results
plt.figure(figsize=(10, 6))
plt.hist(final_results, bins=range(min(final_results), max(final_results) + 2), 
         color='orange', edgecolor='black', align='left')
plt.title(f'Distribution of Final Z over {trials} Runs ($Z = {X_input} \\times \\log_2 {Y_input}$)')
plt.xlabel('Final Value of Z')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.3)
plt.show()