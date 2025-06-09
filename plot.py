import create_instances
import utils
from valid_check import validate_solution
import solve
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def quadratic(n, a): return a * n**2
def nlogn(n, b): return b * n * np.log(n)

def main():
    gammas = [0.65]
    rng = range(100, 6000, 100)
    stat = 5
    x_values = []
    y_plots1 = []
    y_plots2 = []
    y_plots3 = []
    
    for g in gammas:    
        for n in rng:
            print(f"Number of nodes: {n}")
            ends1 = []
            ends2 = []
            ends3 = []

            for it in range(stat):        
                start_time1 = time.time()
                tree = create_instances.generate_tree(n=n, gamma=g, max_weight=10)
                instance = create_instances.create_instance(tree)
                ends1.append(time.time() - start_time1)

                start_time2 = time.time()
                adjacency_list, valid_check = solve.solve(instance)
                ends2.append(time.time() - start_time2)
                if not valid_check:
                    print("Valid check failed")
                    return 0
                
                start_time3 = time.time()
                leaf_nodes = instance.keys()
                if not validate_solution(adjacency_list, leaf_nodes, instance):
                    print("The solution does NOT satisfy the instance constraints.")
                    return 0
                ends3.append(time.time() - start_time3)

            # Save partial data to files
            with open("phase1.txt", "a") as f1:
                f1.write(f"{n} " + " ".join(f"{v:.6f}" for v in ends1) + "\n")
            with open("phase2.txt", "a") as f2:
                f2.write(f"{n} " + " ".join(f"{v:.6f}" for v in ends2) + "\n")
            with open("phase3.txt", "a") as f3:
                f3.write(f"{n} " + " ".join(f"{v:.6f}" for v in ends3) + "\n")

            x_values.append(n)
            y_plots1.append(ends1)
            y_plots2.append(ends2)
            y_plots3.append(ends3)

    # Compute mean and std for each x
    means1 = [np.mean(y) for y in y_plots1]
    stds1 = [np.std(y) for y in y_plots1]
    means2 = [np.mean(y) for y in y_plots2]
    stds2 = [np.std(y) for y in y_plots2]
    means3 = [np.mean(y) for y in y_plots3]
    stds3 = [np.std(y) for y in y_plots3]

    x = np.array(x_values)

    # Plot 1: Error bars for all phases
    plt.figure(figsize=(10, 6))
    plt.errorbar(x, means1, yerr=stds1, fmt='o', capsize=3, markersize=8, label='Phase 1: Instance Creation')
    plt.errorbar(x, means2, yerr=stds2, fmt='s', capsize=3, markersize=8, label='Phase 2: Solving')
    plt.errorbar(x, means3, yerr=stds3, fmt='^', capsize=3, markersize=8, label='Phase 3: Validation')
    plt.xlabel('Number of Nodes (n)')
    plt.ylabel('Time (s)')
    plt.title('Mean Execution Time per Phase with Standard Deviation')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_all_phases.png")

    # Plot 2: Phase 1 with O(n^2) fit
    y1 = np.array(means1)
    params_quad1, _ = curve_fit(quadratic, x, y1)

    plt.figure(figsize=(10, 6))
    plt.errorbar(x, y1, yerr=stds1, fmt='o', capsize=3, markersize=8, label='Phase 1: Data', color='blue')
    plt.plot(x, quadratic(x, *params_quad1), '--', label='Fit $O(n^2)$', color='red')
    plt.xlabel('Number of Nodes (n)')
    plt.ylabel('Time (s)')
    plt.title('Phase 1: Fit $O(n^2)$ with Error Bars')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_phase1_fit.png")

    # Plot 3: Phase 2 with O(n^2) and O(n log n) fits
    y2 = np.array(means2)
    params_quad2, _ = curve_fit(quadratic, x, y2)
    params_nlogn2, _ = curve_fit(nlogn, x, y2)

    plt.figure(figsize=(10, 6))
    plt.errorbar(x, y2, yerr=stds2, fmt='s', capsize=3, markersize=8, label='Phase 2: Data', color='orange')
    plt.plot(x, quadratic(x, *params_quad2), '--', label='Fit $O(n^2)$', color='red')
    plt.plot(x, nlogn(x, *params_nlogn2), '--', label='Fit $O(n \\log n)$', color='green')
    plt.xlabel('Number of Nodes (n)')
    plt.ylabel('Time (s)')
    plt.title('Phase 2: Comparing Fits $O(n^2)$ vs $O(n \\log n)$')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_phase2_fits.png")

    # Plot 4: Phase 3 with O(n^2) fit
    y3 = np.array(means3)
    params_quad3, _ = curve_fit(quadratic, x, y3)

    plt.figure(figsize=(10, 6))
    plt.errorbar(x, y3, yerr=stds3, fmt='^', capsize=3, markersize=8, label='Phase 3: Data', color='green')
    plt.plot(x, quadratic(x, *params_quad3), '--', label='Fit $O(n^2)$', color='red')
    plt.xlabel('Number of Nodes (n)')
    plt.ylabel('Time (s)')
    plt.title('Phase 3: Fit $O(n^2)$ with Error Bars')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_phase3_fit.png")

    # Optional: Print residuals for fit comparison
    ssr_quad2 = np.sum((y2 - quadratic(x, *params_quad2))**2)
    ssr_nlogn2 = np.sum((y2 - nlogn(x, *params_nlogn2))**2)
    print("Phase 2 - Sum of Squared Residuals:")
    print(f"  O(n^2):     {ssr_quad2:.6e}")
    print(f"  O(n log n): {ssr_nlogn2:.6e}")

if __name__ == "__main__":
    main()
