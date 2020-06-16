import json
import random
import datetime


class RandomTweetMetricsEstimator:

    def randCoeff(self):
        return 1 - random.random()*0.5

    def noise(self,x):
        return random.randint(0,int(x))

    def estimateTweetMetrics(self,X):
        w = [0.5,0.25,0.25]
        fmx = 250000
        wsmx = 21326287/1000000
        ws = 0
        for i in range(3): ws += w[i]*X[i]
        fv = fmx * (1/(1 + wsmx - ws/1000000))
        fv = fv*self.randCoeff()
        fv = self.noise(fv)
        rt = fv*(1/3)*self.randCoeff()
        rt = self.noise(rt)
        rp = rt*(1/3)*self.randCoeff()
        rp = self.noise(rp)
        return [ int(i) for i in [fv,rt,rp]]

    def process(self, tw):
        X = [int(tw['user']['followers_count']), int(tw['user']['statuses_count']), int(tw['user']['listed_count'])]
        Y = self.estimateTweetMetrics(X)
        return Y
