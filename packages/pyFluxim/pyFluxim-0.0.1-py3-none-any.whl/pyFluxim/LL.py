import numpy as np
import matplotlib.pyplot as plt
import h5py
from .utils import plotJV, getChunk
from datetime import datetime
RTYPES = ["JV","LIGHT","CV","CC","MPP"]
    
class Result:
    def __init__(self, path):
        self.f = h5py.File(path, 'r')
        self.samples = {}
        for x in self.f['Results']['samples']:
            name = self.f['Results']['samples'][x].attrs['name']
            self.samples[name] = x
    def getDeviceList(self):
        for x in self.samples:
            dev = self.f['Results']['samples'][self.samples[x]].attrs['num devices']
            print("- {} ({})".format(x, dev))
            
    def getResultTimestamp(self, sample, resultID):
        tc = list(self.getSample(sample).get('results').keys())[resultID]
        return tc
        
    def getResultStartTime(self, sample, resultID):
        return datetime.fromtimestamp(int(float(list(self.getSample(sample).get('results').keys())[resultID]))-2082844800)
        
    def getSample(self, sample):
        s=self.f['Results']['samples']
        return s.get(self.samples[sample])
    
    def getResultsTypes(self, sample, hr=False):
        r = self.getSample(sample)['results']
        t=[r[x].attrs['type'] for x in r]
        if hr:
            return [RTYPES[x] for x in t]
        return t
    
    def getSensorResultByName(self, sample, resultID, sensor_name):
        s = self.getSample(sample)['results']
        R = s.get(self.getResultTimestamp(sample, resultID))
        time = np.array(R['1']['time'])
        names = list(R['1']['variables'])
        for i,n in enumerate(names):
            if n[0].decode()==sensor_name:
                return {'name':n[0].decode('ansi'),'unit':n[1].decode('ansi'),'t':time,'data':np.ravel(R['1']['data'][i,:])}
        return None
    
    def getResult(self, sample, pixelID, resultID):
        s = self.getSample(sample)['results']
        R = s.get(self.getResultTimestamp(sample, resultID))
        if R.attrs["type"]==0: #JV
            data = np.array(R['IV'])
            V = data[pixelID,0,:]
            I = data[pixelID,1,:]
            return {'voltage':(V,'V'),'current':(I*1e3,'mA')}
        elif R.attrs["type"] in [2,3,4]:
            t = np.array(R['0']['time'])
            data = np.array(R['0']['data'])
            V = data[0,pixelID,:]
            I = data[1,pixelID,:]
            sens = {
                't': np.array(R['1']['time']),
                'name': list(R['1']['variables']),
                'data':np.array(R['1']['data'])
                }
            return {'t':t,'voltage':V,'current':I,'start_time':R.attrs.get("start_time"),"sensors":sens}
        
    def plotResult(self, sample, pixelID, resultID, globalTime=False, ax=None, axb=None, col='C0', colb='C1', V=True, I=True):
        if ax is None:
            ax = plt.gca()
        if axb is None:
            axb = ax.twinx()
        data = self.getResult(sample, pixelID, resultID)
        if len(data)==2:
            ax.plot(data['voltage'],data['current']*1e3,color=col)
            ax.set_xlabel("Voltage [V]")
            ax.set_ylabel("Current [mA]")
        else:
            if globalTime:
                t0 = np.datetime64('1904-01-01 00:00:00.000') + np.timedelta64(int(data['start_time'][1]),'s')
                dt = np.vectorize(lambda x: np.timedelta64(int(x),'s'))(data['t'])
                t = t0 + dt
                ax.set_xlabel("Date")
            else:
                t = data['t']
                ax.set_xlabel("Time [s]")

            if V:
                ax.plot(t,data['voltage'],color=col)
                ax.set_ylabel("Voltage [V]", color=col)
                ax.tick_params(axis='y', colors=col)
                ax.grid(color=col, alpha=.2)
            if I:
                axb.tick_params(axis='y', colors=colb)
                axb.plot(t,data['current']*1e3,color=colb)
                axb.set_ylabel("Current [mA]", color=colb);
                axb.grid(color=colb, alpha=.2)
        return ax,axb

    def plotResults(self, sample, pixelID, Rtype, globalTime=False, ax=None, axb=None, col='C0', colb='C1',I=True, V=True):
        if ax is None:
            ax = plt.gca()
        if axb is None:
            axb = ax.twinx()
        if type(Rtype) is not int:
            Rtype = RTYPES.index(Rtype)
        for i,t in enumerate(self.getResultsTypes(sample)):
            if t==Rtype:
                self.plotResult(sample, pixelID, i, globalTime, ax=ax, axb=axb, col=col, colb=colb,I=I,V=V)
        if globalTime: plt.gcf().autofmt_xdate();
        return ax, axb
        
    def close(self):
        self.f.close()