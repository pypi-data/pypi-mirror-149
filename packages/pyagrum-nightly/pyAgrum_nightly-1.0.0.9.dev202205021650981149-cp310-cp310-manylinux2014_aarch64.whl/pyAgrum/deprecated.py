# - * - coding : utf - 8 - * -
"""
Deprecated for older pyAgrum
"""
import warnings

from .pyAgrum import GibbsSampling, Potential
from .pyAgrum import Arc, Edge, DiGraph, UndiGraph, MixedGraph, DAG, CliqueGraph
from .pyAgrum import BayesNet, EssentialGraph, MarkovBlanket
from .pyAgrum import InfluenceDiagram, ShaferShenoyLIMIDInference
from .pyAgrum import ExactBNdistance, GibbsBNdistance
from .pyAgrum import BNLearner, JunctionTreeGenerator


def InfluenceDiagramInference(infdiag):
  """
  Deprecated class. Use pyAgrum.ShaferShenoyIDInference instead.
  """
  warnings.warn("""
  ** pyAgrum.InfluenceDiagramInference is deprecated in pyAgrum>0.18.2.
  ** A pyAgrum.ShaferShenoyLIMIDInference has been created.
  """, DeprecationWarning, stacklevel=2)
  return ShaferShenoyLIMIDInference(infdiag)


def ShaferShenoyIDInference(infdiag):
  """
  Deprecated class. Use pyAgrum.ShaferShenoyIDInference instead.
  """
  warnings.warn(""""
  ** pyAgrum.InfluenceDiagramInference is deprecated in pyAgrum>0.18.2.
  ** A pyAgrum.ShaferShenoyLIMIDInference has been created.
  """, DeprecationWarning, stacklevel=2)
  return ShaferShenoyLIMIDInference(infdiag)


def JTGenerator():
  """
  Deprecated class. Use pyAgrum.JunctionTreeGenerator instead.
  """
  warnings.warn("""
  ** pyAgrum.JTGenerator is deprecated in pyAgrum>0.12.6.
  ** A pyAgrum.JunctionTreeGenerator has been created.
  """, DeprecationWarning, stacklevel=2)
  return JunctionTreeGenerator()


def GibbsKL(p, q):
  """
  Deprecated class. Use pyAgrum.GibbsBNdistance instead.
  """
  warnings.warn("""
  ** pyAgrum.GibbsKL is deprecated in pyAgrum>0.12.6.
  ** A pyAgrum.GibbsBNdistance has been created.
  """, DeprecationWarning, stacklevel=2)
  return GibbsBNdistance(p, q)


def BruteForceKL(p, q):
  """
  Deprecated class. Use pyAgrum.ExactBNdistance instead.
  """
  warnings.warn("""
  ** pyAgrum.BruteForceKL is deprecated in pyAgrum>0.12.6.
  ** A pyAgrum.ExactBNdistance has been created.
  """, DeprecationWarning, stacklevel=2)
  return ExactBNdistance(p, q)


def _addDeprecatedMethods():
  def deprecated_setAprioriWeight(learner, weight):
    """
    Deprecated methods in BNLearner for pyAgrum>0.14.0
    """
    warnings.warn("""
    ** pyAgrum.BNLearner.setAprioriWeight() is removed in pyAgrum>0.14.0.
    ** Please use the weight argument in `useApriori...` methods instead.
    """, DeprecationWarning, stacklevel=2)
    return

  BNLearner.setAprioriWeight = deprecated_setAprioriWeight

def getNumberOfRunningThreads():
  warnings.warn(""""
  ** pyAgrum.getNumberOfRunningThreads is obsolete in pyAgrum>0.22.7.
  """)

def getDynamicThreadsNumber():
  warnings.warn(""""
  ** pyAgrum.getDynamicThreadsNumber is obsolete in pyAgrum>0.22.7.
  """)

def setDynamicThreadsNumber(n):
  warnings.warn(""""
  ** pyAgrum.setDynamicThreadsNumber is obsolete in pyAgrum>0.22.7.
  """)

def getNestedParallelism():
  warnings.warn(""""
  ** pyAgrum.getNestedParallelism is obsolete in pyAgrum>0.22.7.
  """)

def setNestedParallelism(n):
  warnings.warn(""""
  ** pyAgrum.setNestedParallelism is obsolete in pyAgrum>0.22.7.
  """)

def getThreadNumber():
  warnings.warn(""""
  ** pyAgrum.getThreadNumber is obsolete in pyAgrum>0.22.7.
  """)


_addDeprecatedMethods()
