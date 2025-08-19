import numpy as np
from .models import tau_ratio, g_field

def _log_normal_likelihood(y, yhat, sigma):
    # Gaussian errors with known sigma (can be scalar or vector)
    r = (y - yhat) / sigma
    return -0.5*np.sum(r*r) - np.sum(np.log(sigma*np.sqrt(2*np.pi)))

def _mh_sampler(logpost, theta0, step, n_samples, burn=1000, thin=1, rng=None):
    rng = np.random.default_rng() if rng is None else rng
    theta = np.array(theta0, dtype=float)
    d = theta.size
    chain = []
    cur_lp = logpost(theta)
    for i in range(n_samples+burn):
        prop = theta + rng.normal(0.0, step, size=d)
        lp = logpost(prop)
        if np.isfinite(lp) and (lp - cur_lp) > np.log(rng.random()):
            theta, cur_lp = prop, lp
        if i >= burn and ((i-burn) % thin == 0):
            chain.append(theta.copy())
    return np.asarray(chain)

# Priors (log-uniform within bounds)
def _log_prior(theta, bounds):
    for val, (lo,hi) in zip(theta, bounds):
        if not (lo <= val <= hi):
            return -np.inf
    # Jeffreys-like: log-uniform over each parameter
    return -np.sum(np.log([hi-lo for (lo,hi) in bounds]))

def mcmc_tau(r, tau_obs, C, sigma_tau=1e-6, rc_bounds=(1e-17,1e-13),
             n_samples=5000, burn=2000, thin=5, step=0.05):
    """
    Posterior over r_c using τ(r). Parameterization is log10(r_c) for positivity.
    """
    r = np.asarray(r, dtype=float); tau_obs = np.asarray(tau_obs, dtype=float)
    lb, ub = np.log10(rc_bounds[0]), np.log10(rc_bounds[1])
    bounds = [(lb, ub)]
    def logpost(theta):
        (log10_rc,) = theta
        rc = 10.0**log10_rc
        C["r_c"]["value"] = rc
        like = _log_normal_likelihood(tau_obs, tau_ratio(r, C), sigma_tau)
        prior = _log_prior([log10_rc], bounds)
        return like + prior
    # init around current rc
    theta0 = [np.log10(C["r_c"]["value"])]
    chain = _mh_sampler(logpost, theta0, step=step, n_samples=n_samples, burn=burn, thin=thin)
    # restore
    return chain

def mcmc_g(r, g_obs, C, sigma_g=1e-9, rho_bounds=(1e-9,1e-5),
           n_samples=5000, burn=2000, thin=5, step=0.1):
    """
    Posterior over rho_ae using g(r). Parameterization is log10(rho).
    """
    r = np.asarray(r, dtype=float); g_obs = np.asarray(g_obs, dtype=float)
    lb, ub = np.log10(rho_bounds[0]), np.log10(rho_bounds[1])
    bounds = [(lb, ub)]
    def logpost(theta):
        (log10_rho,) = theta
        rho = 10.0**log10_rho
        C["rho_ae_fluid"]["value"] = rho
        like = _log_normal_likelihood(g_obs, g_field(r, C), sigma_g)
        prior = _log_prior([log10_rho], bounds)
        return like + prior
    theta0 = [np.log10(C["rho_ae_fluid"]["value"])]
    chain = _mh_sampler(logpost, theta0, step=step, n_samples=n_samples, burn=burn, thin=thin)
    return chain

def mcmc_joint(r_tau, tau_obs, r_g, g_obs, C,
               sigma_tau=1e-6, sigma_g=1e-9,
               rc_bounds=(1e-17,1e-13), rho_bounds=(1e-9,1e-5),
               n_samples=8000, burn=3000, thin=5, step=(0.05,0.1)):
    """
    Joint posterior over (r_c, rho) from τ and g. Parameters are (log10 r_c, log10 rho).
    """
    r_tau = np.asarray(r_tau); tau_obs = np.asarray(tau_obs)
    r_g = np.asarray(r_g); g_obs = np.asarray(g_obs)
    lb_rc, ub_rc = np.log10(rc_bounds[0]), np.log10(rc_bounds[1])
    lb_rho, ub_rho = np.log10(rho_bounds[0]), np.log10(rho_bounds[1])
    bounds = [(lb_rc, ub_rc), (lb_rho, ub_rho)]
    s_rc, s_rho = step

    def logpost(theta):
        log10_rc, log10_rho = theta
        rc  = 10.0**log10_rc
        rho = 10.0**log10_rho
        C["r_c"]["value"] = rc
        C["rho_ae_fluid"]["value"] = rho
        lp = _log_normal_likelihood(tau_obs, tau_ratio(r_tau, C), sigma_tau)
        lp += _log_normal_likelihood(g_obs, g_field(r_g, C), sigma_g)
        lp += _log_prior([log10_rc, log10_rho], bounds)
        return lp

    theta0 = [np.log10(C["r_c"]["value"]), np.log10(C["rho_ae_fluid"]["value"])]
    chain = _mh_sampler(
        logpost, theta0,
        step=np.array([s_rc, s_rho]),
        n_samples=n_samples, burn=burn, thin=thin
    )
    return chain