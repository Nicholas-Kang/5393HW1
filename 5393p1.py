import numpy as np

def run_simulation():
    
    #x1, x2, x3 = 110, 26, 55 
    # Initial state
    x1 = 110
    x2 = 26
    x3 = 55
    while True:
        # Check for outcomes C1, C2, C3
        if x1 >= 150:
            return 'C1' #C1 result
        if x2 < 10:
            return 'C2' #C2 result
        if x3 > 100:
            return 'C3' #C3 result
            
        # probabilities
        a1 = 0.5 * x1 * (x1 - 1) * x2
        a2 = x1 * x3 * (x3 - 1)
        a3 = 3 * x2 * x3
        
        a0 = a1 + a2 + a3
        
        # check for deadlock
        if a0 == 0:
            return 'Deadlock'
        r = np.random.uniform(0, a0)# picking random number
        
        #updating states
        if r < a1:
            # R1: 2X1 + X2 -> 4X3
            x1 -= 2
            x2 -= 1
            x3 += 4
        elif r < a1 + a2:
            # R2: X1 + 2X3 -> 3X2
            x1 -= 1
            x2 += 3
            x3 -= 2
        else:
            # R3: X2 + X3 -> 2X1
            x1 += 2
            x2 -= 1
            x3 -= 1

def estimate_probabilities(num_trials=10000):
    #calculating probs
    results = {'C1': 0, 'C2': 0, 'C3': 0, 'Deadlock': 0}
    for _ in range(num_trials):
        outcome = run_simulation()
        results[outcome] += 1

    probabilities = {k: v / num_trials for k, v in results.items()}
    
    print(f"Estimated Probabilities over {num_trials} trials:")
    print(f"Pr(C1) [x1 >= 150]: {probabilities['C1']:.4f}")
    print(f"Pr(C2) [x2 < 10]:   {probabilities['C2']:.4f}")
    print(f"Pr(C3) [x3 > 100]:  {probabilities['C3']:.4f}")

if __name__ == "__main__":
    estimate_probabilities(10000)