import numpy as np

def estimate_mean_and_variance(num_trials=100000):
    # store final counts
    final_x1 = np.zeros(num_trials)
    final_x2 = np.zeros(num_trials)
    final_x3 = np.zeros(num_trials)
    
    for i in range(num_trials):
        # initial states
        x1 = 9
        x2 = 8
        x3 = 7
        
        #7 steps
        for step in range(7):
            # probability eqns
            a1 = 0.5 * x1 * (x1 - 1) * x2
            a2 = x1 * x3 * (x3 - 1)
            a3 = 3 * x2 * x3
            a0 = a1 + a2 + a3

            if a0 == 0:
                break
                
            # next random reaction
            r = np.random.uniform(0, a0)
            
            # update steps
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
                
        # 4. record values in arrays
        final_x1[i] = x1
        final_x2[i] = x2
        final_x3[i] = x3

    # 5. Finding the statistics
    print(f"Results over {num_trials} trials (after exactly 7 steps):")
    print(f"X1 -> Mean: {np.mean(final_x1):.4f} | Variance: {np.var(final_x1):.4f}")
    print(f"X2 -> Mean: {np.mean(final_x2):.4f} | Variance: {np.var(final_x2):.4f}")
    print(f"X3 -> Mean: {np.mean(final_x3):.4f} | Variance: {np.var(final_x3):.4f}")

if __name__ == "__main__":
    # running 100,000 trials
    estimate_mean_and_variance(100000)