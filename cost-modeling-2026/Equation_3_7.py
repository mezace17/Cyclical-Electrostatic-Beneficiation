def calcAMCM(Q, M, S, IOC, B, D):
    '''
    takes in the current parameter values for the respective project (CEB or MRE)
    and returns the operational cost using NASA's AMCM equation
    '''
    alpha = 5.65*(10**(-4))
    beta = 0.5941
    Xi = 0.6604
    delta = 80.599
    epsilon = 3.8085 * (10**(-55))
    phi = -0.3553
    gamma = 1.5691
    return 2.04*(alpha*(Q**beta)*(M**Xi)*(delta**S)*(epsilon**(1/(IOC-1900)))*(B**phi)*(gamma**D))
