# -*- coding: utf-8 -*-
"""Mixture of two (beta)negative-binomial components."""
from .. import distributions as dist
from functools import partial
from .model import Model, Parameter
from jax.scipy.special import logsumexp
from jax import jit
import jax.numpy as jnp
import numpy as np
from gmpy2 import mpfr


class ModelMixture(Model):
    def __init__(self, bad: float, left: int, dist='BetaNB',
                 estimate_p=False, fix_params=None, use_masking=True,
                 left_k=1):
        """
        Construct a (Beta)Negative-Binomial mixture model.

        w * F(bad/(bad + 1), r,...) + (1 - w) F(1/(bad + 1), r,...)
        w and r are active parameters. F is either NB or BetaNB, both are
        left-truncated.
        Parameters
        ----------
        dist: str
            Distribution for mixture components. Can be either 'NB' or 'BetaNB'.
            The default is 'BetaNB'.
        bad : float, optional
            Background Allelic Dosage value.
        left : int, optional
            Left-bound for truncation.
        estimate_p : bool, optional
            If True, then p is estimated. If False, then then p's (plural) are
            fixed to [bad/(bad + 1), 1 / (bad + 1)]. The default is False.
        fix_params : dict, optional
            Mapping param_name -> fixed_value that will fix active parameters.
            The default is None.
        use_masking : bool, optional
            Masking and padding will be used to avoid JIT performance penalty
            due to changing data vector lengths. Usually results in a much
            greater performance. If True, it is advised to start with
            the most abudant with observations piece of data. The default is
            True.

        Returns
        -------
        None.

        """
        self.bad = bad
        self.left = left
        bad = mpfr(str(bad))
        self.ps = np.array([float(bad / (bad + 1)), float(1 / (bad + 1))])
        self.dist = dist
        parameters = [
            Parameter('r', [left + 1, 2 * (left + 1), (left + 1) * 5, (left + 1) * 10], None, (0.1, None)),
            Parameter('w', [0.02, 0.3, 0.7, 0.98], 1 if bad == 1 else None, (0.0, 1.0)),       
            ]
        if dist == 'BetaNB':
            m = left_k + 26.0
            parameters.append(Parameter('k', [m, 10 * m], None,
                                        (left_k, None)))
        p1 = Parameter('p1', [self.ps[0]],
                      None if estimate_p else self.ps[0], (0.0, 1.0))
        parameters.append(p1)
        if bad != 1:
            p2 = Parameter('p2', [self.ps[1]],
                           None if estimate_p else self.ps[1], (0.0, 1.0))
            parameters.append(p2)
        self.estimate_p = estimate_p
        super().__init__(parameters=parameters, use_masking=use_masking,
                         fix_params=fix_params, _allowed_const=left + 1)

    def logprob_mode(self, params: jnp.ndarray,
                     data: jnp.ndarray, p: float) -> jnp.ndarray:
        """
        Log probability of a single mode given parameters vector.

        Parameters
        ----------
        params : jnp.ndarray
            1d param vector.
        data : jnp.ndarray
            Data.
        p : float
            Rate prob.

        Returns
        -------
        Logprobs of data.

        """
        r = self.get_param('r', params)
        if self.dist == 'NB':
            lp = dist.LeftTruncatedNB.logprob
            lp = lp(data, r, p, self.left)
        elif self.dist == 'BetaNB':
            k = self.get_param('k', params)
            lp = dist.LeftTruncatedBetaNB.logprob
            lp = lp(data, p, k, r, self.left)
        return lp


    @partial(jit, static_argnums=(0,))
    def logprob(self, params: jnp.ndarray, data: jnp.ndarray) -> jnp.ndarray:
        """
        Log probability of data given a parameters vector.

        Should be jitted for the best performance.
        Parameters
        ----------
        paprams : jnp.ndarray
            1D param vector.
        data : jnp.ndarray
            Data.

        Returns
        -------
        Logprobs of data.

        """
        p1 = self.get_param('p1', params)
        if self.bad == 1:
            return self.logprob_mode(params, data, p1)
        else:
            w = self.get_param('w', params)
            p2 = self.get_param('p2', params)
            lp1 = self.logprob_mode(params, data, p1)
            lp2 = self.logprob_mode(params, data, p2)
            return logsumexp(jnp.array([lp1, lp2]).T, axis=1,
                             b=jnp.array([w, 1-w]))

    @partial(jit, static_argnums=(0,))
    def logprob_modes(self, params: jnp.ndarray,
                      data: jnp.ndarray) -> jnp.ndarray:
        """
        Modes probabilities of data given a parameters vector.

        Should be jitted for the best performance.
        Parameters
        ----------
        paprams : jnp.ndarray
            1D param vector.
        data : jnp.ndarray
            Data.

        Returns
        -------
        Tuple of probabilities, each for a mixture component.

        """
        p1 = self.get_param('p1', params)
        lp1 = self.logprob_mode(params, data, p1)
        if self.bad == 1:
            lp2 = lp1
        else:
            p2 = self.get_param('p2', params)
            lp2 = self.logprob_mode(params, data, p2)
        return lp1, lp2
    
    def cdf_mode(self, params: jnp.ndarray,
                     data: list, p: float) -> list:
        """
        cdf of a single mode given parameters vector.

        Parameters
        ----------
        params : jnp.ndarray
            1d param vector.
        data : list
            Data.
        p : float
            Rate prob.

        Returns
        -------
        cdf of data.

        """
        r = self.get_param('r', params)
        if self.dist == 'NB':
            lp = dist.LeftTruncatedNB.long_cdf
            lp = lp(data, r, p, self.left)
        elif self.dist == 'BetaNB':
            k = self.get_param('k', params)
            lp = dist.LeftTruncatedBetaNB.long_cdf
            lp = lp(data, p, k, r, self.left)
        return lp
    
    def cdf_modes(self, params: jnp.ndarray,
                      data: list) -> list:
        """
        Modes cdfs of data given a parameters vector.

        Parameters
        ----------
        paprams : jnp.ndarray
            1D param vector.
        data : list
            Data.

        Returns
        -------
        Tuple of cdfs, each for a mixture component.

        """
        p1 = self.get_param('p1', params)
        lp1 = self.cdf_mode(params, data, p1)
        if self.bad == 1:
            lp2 = lp1
        else:
            p2 = self.get_param('p2', params)
            lp2 = self.cdf_mode(params, data, p2)
        return lp1, lp2

    def mean(self, params=None):
        if params is None:
            params = self.last_result.x
        p1 = self.get_param('p1', params)
        if self.bad == 1:
            p2 = p1
        else:
            p2 = self.get_param('p2', params)
        w = self.get_param('w', params)
        r = self.get_param('r', params)
        if self.dist == 'BetaNB':
            k = self.get_param('k', params)
            l1 = dist.LeftTruncatedBetaNB.mean(p1, k, r, self.left)
            l2 = dist.LeftTruncatedBetaNB.mean(p2, k, r, self.left)
        else:
            l1 = dist.LeftTruncatedNB.mean(r, p1, self.left)
            l2 = dist.LeftTruncatedNB.mean(r, p2, self.left)
        return w * l1 + (1.0 - w) * l2
