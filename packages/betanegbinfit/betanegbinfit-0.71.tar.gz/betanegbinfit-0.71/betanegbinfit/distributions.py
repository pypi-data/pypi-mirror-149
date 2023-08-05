# -*- coding: utf-8 -*-
"""Custom pyro-compatiable distribution"""
from jax.scipy.special import betaln, gammaln
from jax import jit
from .betainc import betainc, logbetainc
import jax.numpy as jnp
from scipy import stats
from scipy.stats import nbinom as scipy_nb, beta
from functools import partial
from abc import abstractmethod
from math import ceil
import numpy as np
import gmpy2
import mpmath



class Distribution():
    @staticmethod
    @abstractmethod
    def sample(size: int, **kwargs) -> jnp.ndarray:
        pass
    
    @staticmethod
    @abstractmethod
    def logprob(data: jnp.ndarray, **kwargs) -> jnp.ndarray:
        pass
    
    @staticmethod
    @abstractmethod
    def long_logprob(data, **kwargs) -> list:
        pass
    
    @classmethod
    def long_cdf(cls, x, *args, **kwargs) -> list:
        if type(x) in (np.ndarray, list):
            x = list(x)
        else:
            x = [x]
        logprob = lambda t: cls.long_logprob(t, *args, **kwargs)
        cdfs = dict()
        m = max(x)
        nums = list(range(ceil(m)))
        nums.append(m)
        s = 0
        for v in nums:
            s += gmpy2.exp(logprob(int(v))[0])
            cdfs[v] = s
        return list(map(cdfs.get, x))

    @classmethod
    def long_sf(cls, x, *args, **kwargs) -> list:
        cdf = cls.long_cdf(x, *args, **kwargs)
        one = gmpy2.mpfr('1')
        return [one - cdf for cdf in cdf]

    @staticmethod
    @abstractmethod
    def sample(size: int, *args, **kwargs) -> np.ndarray:
        pass
    
    @staticmethod
    @abstractmethod
    def mean(**kwargs):
        pass
    
    @abstractmethod
    def cdf(**kwargs):
        pass
    
    @abstractmethod
    def sf(**kwargs):
        pass
    

class NB(Distribution):
    @staticmethod
    def sample(r, p, size):
        return scipy_nb.rvs(n=r, p=1.0 - p, size=size)

    @staticmethod
    @jit
    def logprob(x, r, p):
        p = r * jnp.log(p) + x * jnp.log1p(-p)
        return p  + gammaln(x + r) - gammaln(r) - gammaln(x + 1.0)
    
    @staticmethod
    def long_logprob(x, r, p) -> list:
        if type(x) in (np.ndarray, list):
            x = list(x)
        else:
            x = [x]
        res = list()
        for x in x:
            t = r * gmpy2.log(p) + x * gmpy2.log1p(-p)
            res.append(t + gmpy2.lgamma(x + r)[0] - gmpy2.lgamma(r)[0] - gmpy2.lgamma(x + 1.0)[0])
        return res

    @staticmethod
    def mean(r, p):
        return (1.0 - p) * r / p
    
    @staticmethod
    def long_cdf(x, r, p, skip=-1):
        r = gmpy2.mpfr(str(r)); p = gmpy2.mpfr(str(p))
        if type(x) in (np.ndarray, list):
            x = list(x)
        else:
            x = [x]
        cdfs = dict()
        m = max(x)
        nums = list(range(ceil(m)))
        nums.append(m)
        nums = [gmpy2.mpz(int(n)) for n in nums]
        pdf = p ** r
        sp = (gmpy2.mpfr('1') - p)
        if 0 > skip:
            s = pdf
        else:
            s = 0
        cdfs[0] = s
        for v in nums[1:]:
            pdf *= (v + r - 1) / v * sp
            if v > skip:
                s += pdf
            cdfs[v] = s
        return list(map(cdfs.get, x))
    
    @staticmethod
    def cdf(x, r, p):
        return betainc(r, x + 1.0, p)

    @staticmethod
    def sf(x, r, p):
        return betainc(x + 1.0, r, 1.0 - p)

    @staticmethod
    def logsf(x, r, p):
        return logbetainc(x + 1.0, r, 1.0 - p)

        
    
class LeftTruncatedNB(NB):
    def __init__(self, r, probs, left=5, validate_args=None):
        self.left = left
        self.left_vals = jnp.arange(1, left)
        super().__init__(r, probs, validate_args=validate_args)

    @staticmethod
    def sample(r, p, left, size: int):
        u = stats.uniform.rvs(size=size)
        nb = scipy_nb(p=p, n=r)
        cdf = nb.cdf
        a = cdf(left)
        return nb.ppf(a + u * (1.0 - a))

    @staticmethod
    @partial(jit, static_argnames=('left'))
    def logprob(x, r, p, left):
        left = float(left)
        logprob = super(LeftTruncatedNB, LeftTruncatedNB).logprob
        lp = jnp.where(x <= left, -jnp.inf, logprob(x, r, p))
        lp = logprob(x, r, p) - jnp.log1p(-sum(jnp.exp(logprob(i, r, p))
                                               for i in range(int(left) + 1)))
        return jnp.where(x <= left, -jnp.inf, lp)

    @staticmethod
    def long_logprob(x, r, p, left) -> list:
        if type(x) in (np.ndarray, list):
            x = list(x)
        else:
            x = [x]
        res = list()
        logprob = super(LeftTruncatedNB, LeftTruncatedNB).long_logprob
        denom = gmpy2.log1p(-sum(gmpy2.exp(logprob(i, r, p)[0])
                                 for i in range(int(left) + 1)))
        for x in x:
            res.append(logprob(x, r, p)[0] - denom)
        return res

    @staticmethod
    def long_cdf(x, r, p, left):
        s = super(LeftTruncatedNB, LeftTruncatedNB)
        cdf = s.long_cdf
        sm = gmpy2.mpfr('1') - cdf(left, r, p)[0]
        if type(x) in (np.ndarray, list):
            x = list(x)
        else:
            x = [x]
        return [0 if v <= left else c / sm for v, c in zip(x, cdf(x, r, p,
                                                                  skip=left))]    

    @staticmethod
    def mean(r, p, left):
        s = super(LeftTruncatedNB, LeftTruncatedNB)
        m = s.mean(r, p) 
        m -= sum(i * jnp.exp(s.logprob(i, r, p)) for i in range(1, left + 1)) 
        return m / s.sf(left, r, p)

    @staticmethod
    def cdf(x, r, p, left):
        return sum(jnp.exp(LeftTruncatedNB.logprob(i, r, p, left))
                   for i in range(x + 1))

    @staticmethod
    def sf(x, r, p, left):
        return 1 - LeftTruncatedNB.cdf(x, r, p, left)



class BetaNB(Distribution):
    @staticmethod
    def sample(mu, concentration, r, size: int):
        a = mu * concentration
        b = (1.0 - mu) * concentration
        p = beta.rvs(a, b, size=size)
        return scipy_nb.rvs(n=r, p=p)

    @staticmethod
    @jit
    def logprob(x, mu, concentration, r):
        a = mu * concentration
        b = (1.0 - mu) * concentration
        return betaln(a + r, b + x) - betaln(a, b) + gammaln(r + x) -\
               gammaln(x + 1.0) - gammaln(r)

    @staticmethod
    def long_logprob(x, mu, concentration, r) -> list:
        if type(x) in (np.ndarray, list):
            x = list(x)
        else:
            x = [x]
        res = list()
        a = mu * concentration
        b = (1.0 - mu) * concentration
        betaln = BetaNB.long_betaln
        gammaln = gmpy2.lgamma
        for x in x:
            t = betaln(a + r, b + x) - betaln(a, b) + gammaln(r + x)[0] -\
                gammaln(x + 1.0)[0] - gammaln(r)[0]
            res.append(t)
        return res

    @staticmethod
    def mean(mu, concentration, r):
        a = mu * concentration
        b = (1.0 - mu) * concentration
        return r * b / (a - 1)
    
    @staticmethod
    def cdf(x, mu, concentration, r):
        return sum(jnp.exp(BetaNB.logprob(i, mu, concentration, r))
                   for i in range(x + 1))

    @staticmethod
    def sf(x, mu, concentration, r):
        return 1.0 - BetaNB.cdf(x, mu, concentration, r)
    
    @staticmethod
    def long_prob(x, mu, concentration, r, skip=-1):
        mu = gmpy2.mpq(str(mu)); concentration = gmpy2.mpfr(str(concentration))
        r = gmpy2.mpfr(str(r))
        a = mu * concentration
        b = (gmpy2.mpq('1') - mu) * concentration
        if type(x) in (np.ndarray, list):
            x = list(x)
        else:
            x = [x]
        cdfs = dict()
        m = max(x)
        nums = list(range(ceil(m)))
        nums.append(m)
        nums = [gmpy2.mpz(int(n)) for n in nums]
        base = gmpy2.mpfr(str(mpmath.gammaprod(list(map(str, [a + r, a + b])), 
                                                list(map(str, [a + r + b, a])))))
        if 0 > skip:
            s = base
        else:
            s = 0
        cdfs[0] = s
        frac = 1
        for v in nums[1:]:
            frac *= (v + r - 1) / (v + a + b + r - 1)  * ((v + b - 1) / v)
            cdfs[v] = frac * base
        return list(map(cdfs.get, x))
    
    @staticmethod
    def long_cdf(x, mu, concentration, r, skip=-1):
        mu = gmpy2.mpq(str(mu)); concentration = gmpy2.mpfr(str(concentration))
        r = gmpy2.mpfr(str(r))
        a = mu * concentration
        b = (gmpy2.mpq('1') - mu) * concentration
        if type(x) in (np.ndarray, list):
            x = list(x)
        else:
            x = [x]
        cdfs = dict()
        m = max(x)
        nums = list(range(ceil(m)))
        nums.append(m)
        nums = [gmpy2.mpz(int(n)) for n in nums]
        base = gmpy2.mpfr(str(mpmath.gammaprod(list(map(str, [a + r, a + b])), 
                                                list(map(str, [a + r + b, a])))))
        if 0 > skip:
            s = base
        else:
            s = 0
        cdfs[0] = s
        frac = gmpy2.mpfr('1') * base
        for v in nums[1:]:
            frac *= (v + r - 1) / (v + a + b + r - 1)  * ((v + b - 1) / v)
            if v > skip:
                s += frac
            cdfs[v] = s
        return list(map(cdfs.get, x))


    @staticmethod
    def long_betaln(a, b):
       return gmpy2.lgamma(a)[0] + gmpy2.lgamma(b)[0] - gmpy2.lgamma(a + b)[0]


class LeftTruncatedBetaNB(BetaNB):
    def __init__(self, r, mu, concentration, left, validate_args=None):
        self.left_vals = jnp.arange(0, left + 1)
        self.left = left
        super().__init__(r, mu, concentration, validate_args=validate_args)

    @staticmethod
    def sample(mu, concentration, r, left, size: int):
        a = mu * concentration
        b = (1.0 - mu) * concentration
        p = beta.rvs(a, b, size=size)
        return LeftTruncatedNB.sample(r=r, p=p, left=left, size=size)

    @staticmethod
    @partial(jit, static_argnames=('left',))
    def logprob(x, mu, concentration, r, left=4):
        s = super(LeftTruncatedBetaNB, LeftTruncatedBetaNB)
        cdf = s.cdf
        logprob = s.logprob
        sm = -cdf(left, mu, concentration, r)
        lp = jnp.where(x <= left, -jnp.inf, logprob(x, mu, concentration, r))
        return lp - jnp.log1p(sm)

    @staticmethod
    def long_logprob(x, mu, concentration, r, left) -> list:
        if type(x) in (np.ndarray, list):
            x = list(x)
        else:
            x = [x]
        s = super(LeftTruncatedBetaNB, LeftTruncatedBetaNB)
        cdf = BetaNB.long_cdf
        logprob = s.long_logprob(x, mu, concentration, r)
        sm = gmpy2.log1p(-cdf(left, mu, concentration, r)[0])
        return [lp - sm  if left < x else -np.inf for lp, x in zip(logprob, x)]

    @staticmethod
    def cdf(x, mu, concentration, r, left):
        return sum(jnp.exp(LeftTruncatedBetaNB.logprob(i, mu, concentration, r,
                                                       left))
                   for i in range(x + 1))
    
    @staticmethod
    def long_cdf(x, mu, concentration, r, left):
        s = super(LeftTruncatedBetaNB, LeftTruncatedBetaNB)
        cdf = s.long_cdf
        sm = gmpy2.mpfr('1') - cdf(left, mu, concentration, r)[0]
        if type(x) in (np.ndarray, list):
            x = list(x)
        else:
            x = [x]
        return [0 if v <= left else c / sm for v, c in zip(x, cdf(x, mu,
                                                                  concentration,
                                                                  r,
                                                                  skip=left))]

    @staticmethod
    def mean(mu, concentration, r, left):
        s = super(LeftTruncatedBetaNB, LeftTruncatedBetaNB)
        m = s.mean(mu, concentration, r) 
        return (m - sum(i * jnp.exp(s.logprob(i, mu, concentration, r))
                       for i in range(1, left + 1))) / s.sf(left, mu,
                                                            concentration, r)