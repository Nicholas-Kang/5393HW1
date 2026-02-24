import numpy as np
import random
import matplotlib.pyplot as plt
from collections import defaultdict
import re

def parse_reactions(filepath):
    #code to go through txt file
    reactions = []
    with open(filepath, 'r') as f:
        text = f.read()

    #finding words and numbers
    text = re.sub(r'\\', '', text)
    text = text.replace(':', ' : ')
    tokens = text.split()
    
    #keep track of reactances products and rate
    state = 0
    current_reactants = []
    current_products = []
    
    def parse_species_list(species_tokens):
        #converting list
        species_dict = {}
        for i in range(0, len(species_tokens) - 1, 2):
            try:
                species_dict[species_tokens[i]] = int(species_tokens[i+1])
            except ValueError:
                continue
        return species_dict
    #look through every word in file
    for token in tokens:
        if state == 0: #looking at reactants
            if token == ':': state = 1
            else: current_reactants.append(token)
        elif state == 1: #products
            if token == ':': state = 2
            else: current_products.append(token)
        elif state == 2: #reading rate
            try: rate = float(token)
            except ValueError: rate = 0.0
            
            react_dict = parse_species_list(current_reactants)
            prod_dict = parse_species_list(current_products)
            
            reactions.append({ #put reaction in to list
                'reactants': list(react_dict.items()),
                'products': list(prod_dict.items()),
                'rate': rate
            })
            
            current_reactants = []
            current_products = []
            state = 0
            
    return reactions

def parse_initial_state(filepath): #read file for starting state for each molecule
    initial_state = defaultdict(int)
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                species = parts[0]
                try:
                    count = int(parts[1])
                    initial_state[species] = count
                except ValueError:
                    pass
    return initial_state

#calculating probablities
def calc_probs(state, reactions):
    probs = np.zeros(len(reactions))
    for i, rxn in enumerate(reactions):
        a = rxn['rate']
        for species, stoich in rxn['reactants']: #look at reactant for specific reaction
            count = state.get(species, 0)
            if count < stoich:
                a = 0.0
                break
            
            #scale rate
            if stoich == 1:
                a *= count
            elif stoich == 2:
                a *= count * (count - 1) * 0.5
            elif stoich == 3:
                a *= count * (count - 1) * (count - 2) / 6.0
                
        probs[i] = a
    return probs

def run_sim(reactions, initial_state, moi_value, max_steps=100000):

    #run simulation 100000 steps
    state = initial_state.copy()
    state['MOI'] = moi_value 
    
    for step in range(max_steps):
        #conditions
        if state.get('cI2', 0) > 145:
            return 'stealth'
        if state.get('Cro2', 0) > 55:
            return 'hijack'
            
        probs = calc_probs(state, reactions)
        a0 = np.sum(probs)
        
        if a0 == 0: #if no reaction happens
            break 
            
        #rolling dice
        r2 = random.random()
        cumulative = np.cumsum(probs)
        rxn_idx = np.searchsorted(cumulative, r2 * a0)
        
        #UPDATE
        rxn = reactions[rxn_idx]
        for species, stoich in rxn['reactants']:
            state[species] -= stoich
        for species, stoich in rxn['products']:
            state[species] += stoich
            
    return 'timeout'

def main():
    #running experiment
    reactions = parse_reactions(r'c:\Users\kangl\Downloads\5393p2.txt')
    base_initial_state = parse_initial_state(r'c:\Users\kangl\Downloads\5393p2_2.pl')
    
    total_trials = 100  # 100 trials
    results_stealth = []
    results_hijack = []
    
    print(f"{'MOI':<5} | {'Stealth Prob':<15} | {'Hijack Prob'}")
    print("-" * 40)
    
    #test MOI 1-10
    for moi in range(1, 11):
        stealth_count = 0
        hijack_count = 0
        
        #100 times
        for trial in range(total_trials):
            print(f"\rComputing MOI {moi:<2} | Trial {trial+1:<3}/100 ...", end="", flush=True)
            outcome = run_sim(reactions, base_initial_state, moi)
            
            if outcome == 'stealth':
                stealth_count += 1
            elif outcome == 'hijack':
                hijack_count += 1
            # non reactions ignored and not added to  count
                
        # Calculate probability
        valid_trials = stealth_count + hijack_count
        
        if valid_trials > 0:
            p_stealth = stealth_count / valid_trials
            p_hijack = hijack_count / valid_trials
        else:
            p_stealth = 0.0
            p_hijack = 0.0
            
        results_stealth.append(p_stealth)
        results_hijack.append(p_hijack)
        
        print(f"\r{moi:<5} | {p_stealth:<15.2f} | {p_hijack:.2f}               ")

    #plotting
    plt.plot(range(1, 11), results_stealth, marker='o', label='Stealth (Lysogenic)')
    plt.plot(range(1, 11), results_hijack, marker='s', label='Hijack (Lytic)')
    plt.xlabel('MOI (Multiplicity of Infection)')
    plt.ylabel('Probability (Disregarding Timeouts)')
    plt.ylim(0, 1.05) 
    plt.title('Lambda Phage Strategy vs MOI')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()