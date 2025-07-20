import numpy as np
import matplotlib.pyplot as plt

#TODO ADDS: 
"""
    
    Adding in standard deviation
    
    Implementing a cost analyzer. It must track how many boosts were used and at what stage.
    It must get user input on cost values of raw materials and gold (can be separate items)
    
    it would then have to iterate through a normal runthrough without boosts (potent on last hit is constant imo)
    to see what the difference would have been, then calculate raw costs saved.
"""



# Simulation parameters
NUM_SIMULATIONS = 10000

def reset_fail_counters(fail_counters: list, num_stars: int):
    for i in range(num_stars):
        fail_counters[i] = 0
    return fail_counters

def reset_boost_counters(boost_counters: list, num_stars: int):
    for i in range(num_stars):
        boost_counters[i] = 0
    return boost_counters

def create_new_fail_counters(new_fail_counters: list, num_stars: int):
    for i in range(num_stars):
        new_fail_counters.append(0)
    return new_fail_counters

def populate_boost_choice(cata_choice: list, num_stars: int, boost_choice: list):
    for i in range(num_stars):
        boost_choice.append(0)
        while True:
            star_choice = input(f"Use boost for star #{i+1}? Enter 'p' (potent), 'c' (cata), or 'n' (none): ").lower()
            if star_choice in ("p", "c", "n"):
                break
            print("Invalid input. Enter 'p', 'c', or 'n'.")
        if star_choice == "p":
            cata_choice.append(2)
        elif star_choice == "c":
            cata_choice.append(1)
        else:
            cata_choice.append(0)

        if (num_stars == 3 or num_stars == 4) and i == num_stars - 1:
            while True:
                amp_choice = input("Use 3/4 star amp? Enter 'y' or 'n': ").lower()
                if amp_choice == 'y':
                    cata_choice[-1] = 3
                    break
                elif amp_choice == 'n':
                    break
                else:
                    print("Invalid input. Enter 'y' or 'n'.")
    while True:
        final_boost = input("Use boost for final stage? Enter 'p' (potent), 'c' (cata), or 'n' (none): ").lower()
        if final_boost in ("p", "c", "n"):
            break
        print("Invalid input. Enter 'p', 'c', or 'n'.")
    match final_boost:
        case 'p':
            final_stage_boost = 2
        case 'c':
            final_stage_boost = 1
        case 'n':
            final_stage_boost = 0
    return cata_choice, boost_choice, final_stage_boost

def seed_final_stage_probs():
    while True:
        enhance_level = int(input("Enter gear's STARTING enhance level (15–24): "))
        if 15 <= enhance_level <= 24:
            break
        print("Invalid input, enter a level from 15 to 24.")
    
    match enhance_level:
        case 15:
            base_probs = [0.18, 0.22, 0.26, 0.30, 0.40, 0.50, 1.0]
            num_stars = 3
        case 16:
            base_probs = [0.16, 0.20, 0.25, 0.30, 0.40, 0.50, 1.0]
            num_stars = 3
        case 17:
            base_probs = [0.14, 0.19, 0.24, 0.30, 0.40, 0.50, 1.0]
            num_stars = 3
        case 18:
            base_probs = [0.12, 0.18, 0.24, 0.30, 0.40, 0.50, 1.0]
            num_stars = 4
        case 19:
            base_probs = [0.11, 0.17, 0.23, 0.30, 0.40, 0.50, 1.0]
            num_stars = 4
        case 20:
            base_probs = [0.10, 0.15, 0.20, 0.25, 0.35, 0.50, 1.0]
            num_stars = 5
        case 21:
            base_probs = [0.08, 0.13, 0.19, 0.25, 0.35, 0.50, 1.0]
            num_stars = 5
        case 22:
            base_probs = [0.06, 0.10, 0.15, 0.20, 0.30, 0.50, 1.0]
            num_stars = 6
        case 23:
            base_probs = [0.04, 0.08, 0.12, 0.18, 0.25, 0.50, 1.0]
            num_stars = 6
        case 24:
            base_probs = [0.02, 0.04, 0.08, 0.12, 0.25, 0.50, 1.0]
            num_stars = 6

    return [p + 0.07 for p in base_probs], num_stars

def simulate_attempt(new_fail_counters: list, num_stars: int, cata_choice: list, final_stage_probs: list, new_boost_counters: list, final_stage_boost: int):
    total_attempts = 0
    final_stage_fail_count = 0
    boost_use_tracker = reset_boost_counters(new_boost_counters, num_stars)

    while True:
        fail_counters = reset_fail_counters(new_fail_counters, num_stars)

        while True:
            for i in range(num_stars):
                total_attempts += 1
                if fail_counters[i] >= 6:
                    # print(f"pity stage {i+1} {boost_use_tracker[i]}")
                    prob = 1.0
                elif cata_choice[i] == 3:
                    prob = 1.0
                    boost_use_tracker[i] += 1
                elif cata_choice[i] == 1:
                    prob = 0.24
                    boost_use_tracker[i]+= 1
                    # print(f"used a boost, num used for stage {i+1}: {boost_use_tracker[i]}")
                elif cata_choice[i] == 2:
                    prob = 0.27
                    boost_use_tracker[i]+= 1
                    # print(boost_use_tracker[i])
                else:
                    prob = 0.2

                if np.random.rand() < prob:
                    # print(f"stage {i+1} pass attempt {total_attempts} ")
                    fail_counters[i] = 0
                else:
                    # print(f"stage {i+1} fail attempt {total_attempts} ")
                    fail_counters[i] += 1
                    break
            else:
                break

        total_attempts += 1
        # print("---------")
        base_prob = final_stage_probs[min(final_stage_fail_count, len(final_stage_probs) - 1)]
        if final_stage_boost == 2:
            prob = base_prob + 0.07
        elif final_stage_boost == 1:
            prob = base_prob + 0.03
        if np.random.rand() < prob:
            
            return {
                "total_attempts": total_attempts,
                "final_stage_fail_count": final_stage_fail_count,
                "boost_uses": boost_use_tracker,
                "final_stage_boost_uses": final_stage_fail_count + 1
            }
        else:
            final_stage_fail_count += 1

# === MAIN RUN ===

final_stage_probs, num_stars = seed_final_stage_probs()
fail_counters = create_new_fail_counters([], num_stars)
cata_option, boost_option, final_stage_boost_choice = populate_boost_choice([], num_stars, [])
# print(cata_option)

results = [
    simulate_attempt(fail_counters, num_stars, cata_option, final_stage_probs, [0] * num_stars, final_stage_boost_choice)
    for _ in range(NUM_SIMULATIONS)
]
# print(results)
# Extract metrics

attempts_list = [res["total_attempts"] for res in results]
final_fails_list = [res["final_stage_fail_count"] for res in results]
boost_uses_list = [res["boost_uses"] for res in results]
# Averages
avg_attempts = np.mean(attempts_list)
avg_fails = np.mean(final_fails_list)
boost_array = np.array(boost_uses_list)
avg_boosts_per_stage = np.mean(boost_array, axis=0)




# Print results
print(f"\nSimulations: {NUM_SIMULATIONS:,}")
print(f"Average total attempts to complete all {num_stars+1} stages: {avg_attempts:.2f}")
print(f"Average final stage fails before success: {avg_fails:.2f}")

boost_labels = {
    0: "No Boost",
    1: "Catalyst",
    2: "Potent Catalyst",
    3: "Amplification Catalyst"
}

print("\nAverage boosts used per stage:")
for i, avg in enumerate(avg_boosts_per_stage):
    boost_type = boost_labels.get(cata_option[i], "Unknown")
    print(f"Stage {i+1}: {avg:.2f} uses ({boost_type})")
final_boost_count = sum(res["final_stage_boost_uses"] for res in results)
avg_final_boosts = final_boost_count / NUM_SIMULATIONS

boost_labels = {
    0: "No Boost",
    1: "Catalyst",
    2: "Potent Catalyst"
}
print(f"\nFinal stage average boost uses: {avg_final_boosts:.2f} ({boost_labels[final_stage_boost_choice]})")




# Convert attempt list to NumPy array for analysis
attempts_array = np.array(attempts_list)

# Histogram
# plt.figure(figsize=(12, 7))
# counts, bins, patches = plt.hist(
#     attempts_array,
#     bins=range(min(attempts_list), max(attempts_list)+2),  # dynamic bins
#     color='skyblue',
#     edgecolor='black',
#     density=True
# )

# # Mean line
# mean_attempts = np.mean(attempts_array)
# plt.axvline(mean_attempts, color='green', linestyle='-', linewidth=2, label=f"Mean: {mean_attempts:.2f}")

# # Quartiles
# q1, q2, q3 = np.percentile(attempts_array, [25, 50, 75])
# for q, label in zip([q1, q2, q3], ["Q1", "Q2 (Median)", "Q3"]):
#     plt.axvline(q, color='red', linestyle='--', alpha=0.6)
#     plt.text(q, plt.ylim()[1]*0.9, f'{label}\n{q:.0f}', color='red', ha='center')

# # Labels & Layout
# plt.title(f"Distribution of Total Attempts\nAverage: {mean_attempts:.2f} over {NUM_SIMULATIONS:,} simulations")
# plt.xlabel("Total Attempts to Complete All Stages")
# plt.ylabel("Probability Density")
# plt.legend()
# plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.show()
