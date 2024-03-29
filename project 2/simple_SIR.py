import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from SIR import SIR



def test_disease(name, beta, gamma, time):
    sir = SIR(name, beta, gamma)
    
    # Making simulations
    S_stoch_sum, I_stoch_sum, R_stoch_sum = np.zeros(time), np.zeros(time), np.zeros(time)
    S_ODE, I_ODE, R_ODE = sir.simulate_ODE(1000, 10, time)
    S_stoch, I_stoch, R_stoch = sir.simulate_stochastic(1000, 10, time)

    # Plotting
    # All on the same plot, with different shades of the same color for each S, I, R
    plt.style.use('ggplot')
    plt.plot(S_ODE, color='darkblue', label='Deterministic S')
    plt.plot(I_ODE, color='darkred', label='Deterministic I')
    plt.plot(R_ODE, color='darkgreen',  label='Deterministic R')
    num_sim = 100
    for _ in range(num_sim):
        S_stoch, I_stoch, R_stoch = sir.simulate_stochastic(1000, 10, time)
        S_stoch_sum += S_stoch
        I_stoch_sum += I_stoch
        R_stoch_sum += R_stoch
        plt.plot(S_stoch, color='lightsteelblue', alpha=0.1)
        plt.plot(I_stoch, color='lightcoral', alpha=0.1)
        plt.plot(R_stoch, color='palegreen', alpha=0.1)
    plt.plot(S_stoch_sum/num_sim, color='dodgerblue', label='Average S', linestyle='--')
    plt.plot(I_stoch_sum/num_sim, color='red', label='Average I', linestyle='--')
    plt.plot(R_stoch_sum/num_sim, color='seagreen', label='Average R', linestyle='--')
    plt.legend()
    # plt.grid()
    plt.title(f"{name}")
    plt.xlabel(r"$t$")
    plt.ylabel("Population")
    plt.show()
    print(f"MSE S: {np.mean((S_stoch_sum/num_sim - S_ODE)**2)}")
    print(f"MSE I: {np.mean((I_stoch_sum/num_sim - I_ODE)**2)}")
    print(f"MSE R: {np.mean((R_stoch_sum/num_sim - R_ODE)**2)}")

def measure_effect_of_beta_gamma():
    
    betas = np.linspace(0.1, 1, 10)
    gammas = np.linspace(0.1, 1, 10)
    time = 100

    S_stoch_sum, I_stoch_sum, R_stoch_sum = np.zeros(time), np.zeros(time), np.zeros(time)
    MSE_beta_S = []
    MSE_beta_I = []
    MSE_beta_R = []



    # Measuring the effect of beta on the MSE
    
    for beta in betas:
        for _ in range(50):
            sir = SIR("", beta, 0.2)
            S_ODE, I_ODE, R_ODE = sir.simulate_ODE(1000, 10, time)
            S_stoch, I_stoch, R_stoch = sir.simulate_stochastic(1000, 10, time)
            S_stoch_sum += S_stoch
            I_stoch_sum += I_stoch
            R_stoch_sum += R_stoch
        MSE_beta_S.append(np.mean((S_stoch_sum/50 - S_ODE)**2))
        MSE_beta_I.append(np.mean((I_stoch_sum/50 - I_ODE)**2))
        MSE_beta_R.append(np.mean((R_stoch_sum/50 - R_ODE)**2))
    
    plt.plot(betas, MSE_beta_S, label="S", color='darkblue')
    plt.plot(betas, MSE_beta_I, label="I", color='darkred')
    plt.plot(betas, MSE_beta_R, label="R", color='darkgreen')
    plt.title("MSEs for different beta")
    plt.xlabel(r"$\beta$")
    plt.legend()
    plt.ylabel("MSE")
    plt.show()

    # Measuring the effect of gamma on the MSE

    MSE_gamma_S = []
    MSE_gamma_I = []
    MSE_gamma_R = []


    for gamma in gammas:
        for _ in range(50):
            sir = SIR("", 0.5, gamma)
            S_ODE, I_ODE, R_ODE = sir.simulate_ODE(1000, 10, time)
            S_stoch, I_stoch, R_stoch = sir.simulate_stochastic(1000, 10, time)
            S_stoch_sum += S_stoch
            I_stoch_sum += I_stoch
            R_stoch_sum += R_stoch
        MSE_gamma_S.append(np.mean((S_stoch_sum/50 - S_ODE)**2))
        MSE_gamma_I.append(np.mean((I_stoch_sum/50 - I_ODE)**2))
        MSE_gamma_R.append(np.mean((R_stoch_sum/50 - R_ODE)**2))

    plt.plot(gammas, MSE_gamma_S, label="S", color='darkblue')
    plt.plot(gammas, MSE_gamma_I, label="I", color='darkred')
    plt.plot(gammas, MSE_gamma_R, label="R", color='darkgreen')
    plt.legend()
    plt.title("MSEs for different gamma")
    plt.xlabel(r"$\gamma$")
    plt.ylabel("MSE")
    plt.show()

        

def measure_effect_of_total_population():
    populations = np.linspace(100, 10000, 10)
    time = 100

    S_stoch_sum, I_stoch_sum, R_stoch_sum = np.zeros(time), np.zeros(time), np.zeros(time)
    MSE_pop_S = []
    MSE_pop_I = []
    MSE_pop_R = []

    for pop in populations:
        for _ in range(50):
            sir = SIR("", 0.4, 0.2)
            S_ODE, I_ODE, R_ODE = sir.simulate_ODE(pop, pop/100, time)
            S_stoch, I_stoch, R_stoch = sir.simulate_stochastic(pop, pop/100, time)
            S_stoch_sum += S_stoch
            I_stoch_sum += I_stoch
            R_stoch_sum += R_stoch
        MSE_pop_S.append(np.mean((S_stoch_sum/50 - S_ODE)**2))
        MSE_pop_I.append(np.mean((I_stoch_sum/50 - I_ODE)**2))
        MSE_pop_R.append(np.mean((R_stoch_sum/50 - R_ODE)**2))
    plt.style.use("ggplot")
    plt.plot(populations, MSE_pop_S, label="S", color='darkblue')
    plt.plot(populations, MSE_pop_I, label="I", color='darkred')
    plt.plot(populations, MSE_pop_R, label="R", color='darkgreen')
    plt.legend()
    plt.title("MSEs for different population sizes")
    plt.xlabel("Population size")
    plt.ylabel("MSE")
    plt.show()
        

def measure_effect_of_starting_infected():
    starting_infected = np.linspace(1, 100, 10)
    time = 100

    S_stoch_sum, I_stoch_sum, R_stoch_sum = np.zeros(time), np.zeros(time), np.zeros(time)
    MSE_starting_S = []
    MSE_starting_I = []
    MSE_starting_R = []

    for infected in starting_infected:
        for _ in range(50):
            sir = SIR("", 0.4, 0.2)
            S_ODE, I_ODE, R_ODE = sir.simulate_ODE(1000, infected, time)
            S_stoch, I_stoch, R_stoch = sir.simulate_stochastic(1000, infected, time)
            S_stoch_sum += S_stoch
            I_stoch_sum += I_stoch
            R_stoch_sum += R_stoch
        MSE_starting_S.append(np.mean((S_stoch_sum/50 - S_ODE)**2))
        MSE_starting_I.append(np.mean((I_stoch_sum/50 - I_ODE)**2))
        MSE_starting_R.append(np.mean((R_stoch_sum/50 - R_ODE)**2))
    plt.style.use("ggplot")
    plt.plot(starting_infected/1000, MSE_starting_S, label="S", color='darkblue')
    plt.plot(starting_infected/1000, MSE_starting_I, label="I", color='darkred')
    plt.plot(starting_infected/1000, MSE_starting_R, label="R", color='darkgreen')
    plt.legend()
    plt.title("MSEs for different starting infected")
    plt.xlabel("Starting infected (% of population)")
    plt.ylabel("MSE")
    plt.show()

    







if __name__=="__main__":
    # test_disease("Ebola", 0.71, 0.4152, 100)
    """
    "Estimating the Reproduction Number of Ebola Virus (EBOV) during the 2014 Outbreak in West Africa"
    published in PLOS Currents Outbreaks in 2014
    (doi: 10.1371/currents.outbreaks.91afb5e0f279e7f29e7056095255b288)
    """
    test_disease("COVID-19", 0.328, 0.1, 100)
    """"The Novel Coronavirus, 2019-nCoV, Is Highly Contagious and More Infectious Than Initially Estimated"
    published in the journal MedRxiv in 2020
    (doi: 10.1101/2020.02.07.20021154)."""
    # test_disease("Influenza", 0.4, 0.3, 100)
    """
    Different Epidemic Curves for Severe Acute Respiratory Syndrome Reveal Similar Impacts of Control Measures"
    published in the Proceedings of the National Academy of Sciences in 2004 
    (doi: 10.1073/pnas.0402950101).
    """
    # test_disease("Measles", 0.857, 0.0714, 100)
    """"Infectious Diseases of Humans: Dynamics and Control" published in 1992."""
    # test_disease("Test 1", 0.5, 0.02, 200)
    # test_disease("Test", 0.0800, 0.0681, 1000)

    # measure_effect_of_total_population()
    # measure_effect_of_starting_infected()