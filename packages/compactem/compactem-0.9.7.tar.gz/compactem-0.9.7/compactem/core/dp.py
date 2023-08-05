import random
from collections import defaultdict
from scipy.stats import beta
import numpy as np


def generic_blackwell_macqueen_sampler(alpha, sample_size):
    """
    Not specific to any base distribution, this just returns how many points from a cluster is needed, using
    the Blackwell-Macqueen Urn scheme or Polya urn scheme. Essentially, this is partition on the set of natural
    number a Dirichlet Process achieves.

    :param alpha: the Dirichlet Process concentration parameter
    :param sample_size: num points to be sampled
    :return: list with entries as number of points in a cluster; len of this list is the number of clusters.
    """
    cluster_number = 0
    density_params = defaultdict(int)
    urn = []
    for n in range(1, sample_size + 1):
        prob_new = 1.0 * alpha / (alpha + n - 1)  # probability of picking a new density param
        if random.random() <= prob_new:
            cluster_number += 1
            density_params_n = cluster_number
            density_params[density_params_n] += 1
            urn.append(cluster_number)
        else:
            density_params_n = random.choice(urn)  # probability of re-assigning to an old cluster
            density_params[density_params_n] += 1
            urn.append(density_params_n)
    clustering_structure = list(density_params.values())
    return clustering_structure


def sample_beta(prior_for_a_beta_A, prior_for_a_beta_B, prior_for_b_beta_A, prior_for_b_beta_B, sample_size,
                scale_a=1.0, scale_b=1.0):
    """
    Given a particular setting of the priors (which also happen to be betas), return parameters of a standard
    beta distribution.Shape parameters to be sampled - a,b - come from beta(prior_for_a_beta_A, prior_for_a_beta_B) and
    beta(prior_for_b_beta_A, prior_for_b_beta_B) respectively.

    :param prior_for_a_beta_A: Beta shape parameter A for the prior to use to sample a
    :param prior_for_a_beta_B: Beta shape parameter B for the prior to use to sample a
    :param prior_for_b_beta_A: Beta shape parameter A for the prior to use to sample b
    :param prior_for_b_beta_B: Beta shape parameter B for the prior to use to sample b
    :param sample_size: number of standard beta distributions to be sampled
    :param scale_a: scaling factor for a
    :param scale_b: scaling factor for b
    :return: list of tuples of the form (a,b), where a,b are parameters of betas. length of list = sample_size
    """
    r_a = beta.rvs(prior_for_a_beta_A, prior_for_a_beta_B, scale=scale_a, size=sample_size)  # random variates for A
    r_b = beta.rvs(prior_for_b_beta_A, prior_for_b_beta_B, scale=scale_b,  size=sample_size)  # random variates for B

    # cant have zeros or low numbers here
    # its not clear *when* scipy.beta gives inf/nan ... to reproduce see
    # try beta(7.90505e-319, 5.6422297e-317).pdf(np.linspace(0,1, 10))
    low_lim = 1e-10
    r_a[r_a < low_lim] = low_lim
    r_b[r_b < low_lim] = low_lim

    return list(zip(r_a, r_b))


