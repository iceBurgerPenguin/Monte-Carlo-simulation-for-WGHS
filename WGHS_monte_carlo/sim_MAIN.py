import calculation as calc
import numpy as np
import matplotlib.pyplot as plt
import random


def random_color():
    color = ('blue','orange','green','red','purple','brown','pink','gray','olive','cyan')
    rand_color = random.choice(color)
    return rand_color


def single_simulation(start_amount = 500000, years = 10):
    amt = start_amount
    portfolio_values = [amt] #modify


    for year in range(years):
        if year<=4:
            mean,std = high_mean, high_std
        elif year<=8:
            mean,std = mid_mean, mid_std
        else:
            mean,std = low_mean, low_std

        rate = np.random.default_rng().normal(loc=mean, scale=std)
        amt *= (1+rate)
        portfolio_values.append(amt) #modify


    return portfolio_values


# def multiple_simulations_spec(goal = 1500000, iterations = 2):
#
#     iter_x = [0]
#     prob_y = [0]
#     success = 0
#     for i in range(iterations):
#
#         final_amount = single_simulation()
#         if final_amount >= goal:
#             success += 1
#
#         if i%100 == 0 and i!= 0:
#             print(f'Iteration {i} / {iterations} completed.')
#             iter_x.append(i)
#             prob_y.append(success/i)
#
#     success_rate = success/iterations
#     return success_rate


def multiple_simulations(goal = 1500000, iterations = 50000, years = 10):

    iter_x = [0]
    prob_y = [0]
    success = 0
    time_points = range(years + 1)

    plt.figure(figsize=(10, 6))

    for i in range(iterations):

        portfolio_values = single_simulation(years=years)
        final_amount = portfolio_values[-1]


        rand_color = random_color()
        plt.plot(time_points, portfolio_values, alpha=0.3, color=rand_color)

        if final_amount >= goal:
            success += 1

        if (i%100 == 0 or i==iterations) and i!= 0 :
            print(f'Iteration {i} / {iterations} completed.')
            iter_x.append(i)
            prob_y.append(success/i)

    plt.xlabel("Year")
    plt.ylabel("Portfolio Value")
    plt.title(f"Monte Carlo Simulation of Portfolio Growth ({iterations} Iterations)")
    plt.savefig(f"graphs/portfolio_growth_{iterations}_monte_carlo.png")
    plt.show()


    # Optional: plot probability vs iterations
    plt.figure(figsize=(8, 4))
    plt.plot(iter_x, prob_y, color='green')
    plt.xlabel("Iteration")
    plt.ylabel(f"Probability of Reaching ${goal}")
    plt.title(f"Probability of Reaching Investment Goal vs Iterations ({iterations})")
    plt.savefig(f"graphs/portfolio_probability_{iterations}.png")
    plt.show()


    success_rate = success/iterations
    return success_rate




if __name__ == "__main__":

    high_mean,high_std = calc.high_mean, calc.high_std
    mid_mean,mid_std = calc.mid_mean, calc.mid_std
    low_mean,low_std = calc.low_mean, calc.low_std

    rate = multiple_simulations()
    print(rate)





