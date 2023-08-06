import pkg_resources
import numpy as np


class GMM():
    """docstring for GMM
    """

    def __init__(self):
        self.name = "There's Nothing here!"


class AkkarEtAl_2014(GMM):
    """docstring for AkkarEtAl_2014
    """

    def __init__(self, vs30, dist='repi', Fm='N'):
        GMM.__init__(self)
        self.dist = dist
        self.Fm = Fm
        self.vs30 = vs30
        self.focMecs = {'N': [1, 0], 'R': [0, 1], 'SS': [0, 0]}
        self.Fn, self.Fr = self.focMecs[self.Fm]
        self.Vref = 750.0
        self.Vcon = 1000.0

        self.name = 'Akkar et al. (2014)'

        stream = pkg_resources.resource_stream(
            __name__, 'data/AkkarEtAl_2014_1.dat')
        self.indT = np.loadtxt(stream, delimiter='\t')

        stream = pkg_resources.resource_stream(
            __name__, 'data/AkkarEtAl_2014_repi.dat')
        repi = np.loadtxt(stream, delimiter='\t')

        stream = pkg_resources.resource_stream(
            __name__, 'data/AkkarEtAl_2014_rhyp.dat')
        rhyp = np.loadtxt(stream, delimiter='\t')

        stream = pkg_resources.resource_stream(
            __name__, 'data/AkkarEtAl_2014_rjb.dat')
        rjb = np.loadtxt(stream, delimiter='\t')

        self.tables = {'repi': repi, 'rhyp': rhyp, 'rjb': rjb}

        self.table = self.tables[self.dist]

        self.T = self.table[:, 0]
        self.nT = len(self.T)

    def run(self, ss):
        meanLnSa = np.zeros([ss.nm, ss.nr, self.nT])
        sigmaLnSa = self.table[:, 8]
        meanSa = np.zeros([ss.nm, ss.nr, self.nT])
        medianSa = np.zeros([ss.nm, ss.nr, self.nT])
        ln_yref = np.zeros([ss.nm, ss.nr, self.nT])
        for i in range(self.nT):
            for z in range(ss.nr):
                for k in range(ss.nm):
                    p1 = self.table[i, 1]
                    c1 = self.indT[4]
                    p2 = self.indT[0]*(ss.m[k]-c1)
                    p3 = self.table[i, 2]*(8.5-ss.m[k])**2
                    p4 = self.table[i, 1]
                    p5 = self.indT[1]*(ss.m[k]-c1)
                    p6 = np.log((ss.r[z]**2+self.indT[2]**2)**0.5)
                    p7 = self.indT[3]*(ss.m[k]-c1)
                    p8 = self.table[i, 4]*self.Fn
                    p9 = self.table[i, 5]*self.Fr
                    b1 = self.table[i, 6]
                    b2 = self.table[i, 7]

                    c = self.indT[5]
                    n = self.indT[6]

                    if ss.m[k] <= self.indT[4]:
                        ln_yref[k, z, i] = p1 + p2 + \
                            p3 + (p4 + p5)*p6 + p8 + p9
                    else:
                        ln_yref[k, z, i] = p1 + p7 + \
                            p3 + (p4 + p5)*p6 + p8 + p9
                    median_pga = np.exp(ln_yref[k, z, i])

                    if self.vs30 < self.Vref:
                        ln_S = b1*np.log(self.vs30/self.Vref)+b2*np.log((median_pga+c*(
                            self.vs30/self.Vref)**n)/((median_pga+c)*(self.vs30/self.Vref)**n))
                    elif self.Vref <= self.vs30 and self.vs30 < self.Vcon:
                        ln_S = b1*np.log(self.vs30/self.Vref)
                    else:
                        ln_S = b1*np.log(self.Vcon/self.Vref)
                    meanLnSa[k, z, i] = ln_yref[k, z, i] + ln_S
                    meanSa[k, z, i] = np.exp(
                        meanLnSa[k, z, i]+1/2*sigmaLnSa[i]**2)
                    medianSa[k, z, i] = np.exp(meanLnSa[k, z, i])

        return meanLnSa, sigmaLnSa, meanSa, medianSa
