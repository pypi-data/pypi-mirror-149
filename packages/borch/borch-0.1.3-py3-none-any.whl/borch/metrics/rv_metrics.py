"""
This module supports calculating different metrics for observed random variables.

One can use a specific metric like
    >>> from borch import distributions
    >>> import torch
    >>> rv = distributions.Normal(torch.randn(10), torch.randn(10).exp())
    >>> mse = mean_squared_error(rv)

one can use ``all_metrics`` to get all valid metrics for that random variable.
    >>> all = all_metrics(rv)

"""
from torch.distributions import constraints
from borch.metrics import metrics

METRICS = {
    constraints.real.__class__: (metrics.mean_squared_error,),
    constraints.greater_than: (metrics.mean_squared_error,),
    constraints.real_vector.__class__: (metrics.mean_squared_error,),
    constraints.greater_than_eq: (metrics.mean_squared_error,),
    constraints.less_than: (metrics.mean_squared_error,),
    constraints.integer_interval: (metrics.accuracy,),
    constraints.positive_integer.__class__: (metrics.accuracy,),
    constraints.unit_interval.__class__: (metrics.mean_squared_error,),
}


def _call_metric(rv, metric):
    return metric(rv.tensor, rv)


def all_metrics(rv):
    """
    Calculates all valid performance metrics of an observed RandomVariable,
        rv (borch.RandomVariable): an observed `RandomVariable`.

    Returns:
        dict, with performance measures

    Notes:
        If no performance measures is defined for the support of the distribution,
        an empty dict will be returned.

    Examples:
        >>> import torch
        >>> from borch import distributions
        >>> rv = distributions.Normal(0, 1)
        >>> met = all_metrics(rv)

    """
    return {
        met.__name__: _call_metric(rv, met) for met in METRICS.get(type(rv.support), [])
    }


def mean_squared_error(rv):
    """
    Measures the averaged element-wise mean squared error of an observed RandomVariable
    Args:
        rv(borch.RandomVariable): an observed `RandomVariable`.

    Returns:
        tensor, with the mean squared error
    Examples:
        >>> from borch import RandomVariable, distributions
        >>> import torch
        >>> rv = distributions.Normal(torch.randn(10), torch.randn(10).exp())
        >>> mse = mean_squared_error(rv)
    """
    return _call_metric(rv, metrics.mean_squared_error)


def accuracy(rv):
    """
    Calculates the accuracy, i.e. how much agreement between two long tensors. It will
    return values between 0 and 1.
    Args:
        rv(borch.RandomVariable): an observed `RandomVariable`.

    Returns:
        tensor, with the calculated accuracy

    Examples:
        >>> from borch import RandomVariable, distributions
        >>> import torch
        >>> rv = distributions.Categorical(logits=torch.randn(4))
        >>> acc = accuracy(rv)

    Notes:
        This function does not support gradient trough it
    """
    return _call_metric(rv, metrics.accuracy)
