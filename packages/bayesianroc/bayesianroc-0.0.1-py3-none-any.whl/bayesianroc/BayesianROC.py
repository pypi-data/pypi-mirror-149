#!/usr/bin/env python
# BayesianROC.py
# by André Carrington and Franz Mayr

from deeproc.DeepROC import DeepROC

class BayesianROC(DeepROC):

    def __init__(self, predicted_scores=None, labels=None, poslabel=None, BayesianPrior=None,
                 costs=None, quiet=False):
        '''BayesianROC constructor. If predicted_scores and labels are
           empty then it returns an empty object.'''

        super().__init__(predicted_scores=predicted_scores, labels=labels, poslabel=poslabel, quiet=quiet)

        #   Bayesian ROC...
        self.BayesianPrior  = BayesianPrior
        self.costs          = costs
    #enddef

    def analyzeGroupFoldsVsChance(self, groupIndex, prevalence, costs):
        prior    = (0.5, 0.5)
        forFolds = True
        return self.analyzeGroupVs(groupIndex, prevalence, costs, prior, forFolds)
    #enddef

    def analyzeGroupVsChance(self, groupIndex, prevalence, costs):
        prior    = (0.5, 0.5)
        forFolds = False
        return self.analyzeGroupVs(groupIndex, prevalence, costs, prior, forFolds)
    #enddef

    def analyzeGroupFoldsVsPrior(self, groupIndex, prevalence, costs, prior):
        forFolds = True
        return self.analyzeGroupVs(groupIndex, prevalence, costs, prior, forFolds)
    # enddef

    def analyzeGroupVsPrior(self, groupIndex, prevalence, costs, prior):
        forFolds = False
        return self.analyzeGroupVs(groupIndex, prevalence, costs, prior, forFolds)
    #enddef

    def analyzeGroupVs(self, groupIndex, prevalence, costs, prior, forFolds):
        from bayesianroc.Helpers.BayesianROCFunctions import BayesianAUC

        returnValues     = self.getGroupForAUCi(groupIndex, forFolds)
        groupByOtherAxis = returnValues[2]
        if self.groupAxis == 'FPR':
            group = dict(x1=self.groups[groupIndex][0],
                         x2=self.groups[groupIndex][1],
                         y1=groupByOtherAxis[0],
                         y2=groupByOtherAxis[1])
        elif self.groupAxis == 'TPR':
            group = dict(y1=self.groups[groupIndex][0],
                         y2=self.groups[groupIndex][1],
                         x1=groupByOtherAxis[0],
                         x2=groupByOtherAxis[1])
        else:
            SystemError(f'This function has not been implemented yet for groupAxis=={self.groupAxis}.')
            group = None
        #endif

        if forFolds:
            measures_dict = BayesianAUC(self.mean_fpr, self.mean_tpr, group, prevalence, costs, prior)
        else:
            measures_dict = BayesianAUC(self.full_fpr, self.full_tpr, group, prevalence, costs, prior)
        #endif

        # # to compute Bhattacharyya Dissimilarity (1 - Bhattacharyya Coefficient) we need to
        # # put the posScores and negScores into bins, and then into dictionaries
        # #    first determine if the distributions are linearly separable, because badly chosen bins
        # #    could hide that. So, we need to choose bins wisely, if they are separable.
        # #
        # # first sort elements, high to low, by score, and within equal scores, by label (in descending order)
        # self.predicted_scores, self.newlabels, self.labels, self.sorted_full_slope_factors = \
        #     sortScoresAndLabels4(self.predicted_scores, self.newlabels, self.labels, self.full_slope_factor)
        # # second, determine seperability
        # # third, get the posScores and negScores so that we can make two binned distributions
        # bDissimilar   = BhattacharyyaDissimilarity()

        return measures_dict
    #enddef

    def __str__(self):
        '''This method prints the object as a string of its content re 
           predicted scores, labels, full fpr, full tpr, full thresholds.'''
        super().__str__()

        rocdata = f'BayesianPrior = {self.BayesianPrior}\n'
        return rocdata
    #enddef 
