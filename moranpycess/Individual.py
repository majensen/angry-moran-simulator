"""
##############################################################################
#
#   Implementation of the population individuals
#
#   AUTHOR: Maciej_Bak
#   AFFILIATION: University_of_Basel
#   AFFILIATION: Swiss_Institute_of_Bioinformatics
#   CONTACT: wsciekly.maciek@gmail.com
#   CREATED: 20-07-2020
#   LICENSE: MIT
#
##############################################################################
"""

# imports
import copy


class Individual:
    """Abstract representation of an individual in the population."""

    def __init__(self, ID, ind_label):
        """Basic initializer."""
        self.ID = copy.deepcopy(ID)
        self.label = copy.deepcopy(ind_label)
        self.AvgBirthPayoff = None
        self.AvgDeathPayoff = None
        self.BirthFitness = None
        self.DeathFitness = None

    @property
    def ID(self):
        """Python getter."""
        return self._ID

    @ID.setter
    def ID(self, ID):
        """Python setter."""
        self._ID = ID

    @property
    def label(self):
        """Python getter."""
        return self._label

    @label.setter
    def label(self, label):
        """Python setter."""
        self._label = label

    @property
    def BirthFitness(self):
        """Python getter."""
        return self._BirthFitness

    @BirthFitness.setter
    def BirthFitness(self, BirthFitness):
        """Python setter."""
        self._BirthFitness = BirthFitness

    @property
    def DeathFitness(self):
        """Python getter."""
        return self._DeathFitness

    @DeathFitness.setter
    def DeathFitness(self, DeathFitness):
        """Python setter."""
        self._DeathFitness = DeathFitness

    @property
    def AvgBirthPayoff(self):
        """Python getter."""
        return self._AvgBirthPayoff

    @AvgBirthPayoff.setter
    def AvgBirthPayoff(self, AvgBirthPayoff):
        """Python setter."""
        self._AvgBirthPayoff = AvgBirthPayoff

    @property
    def AvgDeathPayoff(self):
        """Python getter."""
        return self._AvgDeathPayoff

    @AvgDeathPayoff.setter
    def AvgDeathPayoff(self, AvgDeathPayoff):
        """Python setter."""
        self._AvgDeathPayoff = AvgDeathPayoff
