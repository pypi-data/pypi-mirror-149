import numpy as np
import matplotlib.pyplot as plt
import h5py
from .utils import plotJV, getChunk
from datetime import datetime
RTYPES = ["JV","LIGHT","CV","CC","MPP"]
    
class Result:
    """
    Handle Litos Lits .lls result file
    """
    def __init__(self, path):
        """
        Open Litos Lite .lls file
        """
        self.f = h5py.File(path, 'r')
        self.samples = {}
        for x in self.f['Results']['samples']:
            name = self.f['Results']['samples'][x].attrs['name']
            self.samples[name] = x
            
    def getSampleList(self):
        """
        get a list of all samples present in the result.
        The return values containms the name of the sample as well as the number of devices (pixels) present on the sample
        """
        return [{"name":x,"devices":self.f['Results']['samples'][self.samples[x]].attrs['num devices']} for x in self.samples]
            
    def getResultTimestamp(self, sample, resultID, raw=False):
        """
        Return the UNIX Timestamp of the result (start time)
        """
        tc = list(self.__getSample(sample).get('results').keys())[resultID]
        if raw:
            return tc
        return float(tc)-2082844800
        
    def getResultStartTime(self, sample, resultID):
        """
        Return the Start time of the result
        """
        return datetime.fromtimestamp(int(self.getResultTimestamp(sample, resultID)))
        
    def __getSample(self, sample):
        """
        get HDF5 group for a given sample
        """
        s = self.f['Results']['samples']
        return s.get(self.samples[sample])
    
    def getResultsIndicesByType(self, sample, result_type, hr=True):
        """
        return the resultIDs of all results of a given type
        """
        return [i for i,t in enumerate(self.getResultsTypes(sample, hr=hr)) if t==result_type]
        
    def getResultsTypes(self, sample, hr=True):
        """
        Return the type of the result as integer.
        if hr (for human-readble) is True, then the result are strings ("JV","LIGHT","CV","CC","MPP") otherwise they are integer
        """
        r = self.__getSample(sample)['results']
        t=[r[x].attrs['type'] for x in r]
        if hr:
            return [RTYPES[x] for x in t]
        return t
    
    def listSensors(self, sample, resultID):
        """
        List the (name, unit) of sensors recorded for a given sample and resultID
        """
        s = self.__getSample(sample)['results']
        R = s.get(str(self.getResultTimestamp(sample, resultID, raw=True)))
        time = np.array(R['1']['time'])
        names = list(R['1']['variables'])
        return [[x.decode("ansi") for x in n] for n in names]
        
    def getSensorResultByName(self, sample, resultID, sensor_name):
        """
        Return the result for a given Sample, resultID and sensor name
        """
        s = self.__getSample(sample)['results']
        R = s.get(self.getResultTimestamp(sample, resultID, raw=True))
        time = np.array(R['1']['time'])
        names = list(R['1']['variables'])
        for i,n in enumerate(names):
            if n[0].decode()==sensor_name:
                return {'name':n[0].decode('ansi'),'unit':n[1].decode('ansi'),'t':time,'data':np.ravel(R['1']['data'][i,:])}
        return None
    
    def plotSensorResultByName(self, sample, resultID, sensor_name, ax=None):
        if ax is None:
            ax = plt.gca()
        s = self.__getSample(sample)['results']
        R = s.get(self.getResultTimestamp(sample, resultID, raw=True))
        time = np.array(R['1']['time'])
        names = list(R['1']['variables'])
        r = None
        for i,n in enumerate(names):
            if n[0].decode()==sensor_name:
                r = {'name':n[0].decode('ansi'),'unit':n[1].decode('ansi'),'t':time,'data':np.ravel(R['1']['data'][i,:])}
                break
        if r is None:
            return None
        ax.plot(r['t'],r['data'],label=r['name'])
        ax.set_xlabel("Time [min]")
        ax.set_ylabel(f"{r['name']} ({r['unit']})")
        
    def getResult(self, sample, pixelID, resultID, includeSensors=False):
        s = self.__getSample(sample)['results']
        R = s.get(self.getResultTimestamp(sample, resultID, raw=True))
        if R.attrs["type"]==0: #JV
            data = np.array(R['IV'])
            V = data[pixelID,0,:]
            I = data[pixelID,1,:]
            return {'type':"JV",'voltage':(V,'V'),'current':(I*1e3,'mA')}
        elif R.attrs["type"] in [2,3,4]:
            t = np.array(R['0']['time'])
            data = np.array(R['0']['data'])
            V = data[0,pixelID,:]
            I = data[1,pixelID,:]
            if includeSensors:
                sens = {
                    't': np.array(R['1']['time']),
                    'name': list(R['1']['variables']),
                    'data':np.array(R['1']['data'])
                    }
                return {'type':"Stress", 't':t,'voltage':V,'current':I,'start_time':R.attrs.get("start_time"),"sensors":sens}
            return {'type':"Stress", 't':t,'voltage':V,'current':I,'start_time':R.attrs.get("start_time")}

    def plotResult(self, sample, pixelID, resultID, globalTime=False, ax=None, axb=None, col='C0', colb='C1', V=True, I=True, **kargs):
        data = self.getResult(sample, pixelID, resultID)
        if ax is None:
            ax = plt.gca()
        if data["type"] == "Stress":
            if axb is None:
                axb = ax.twinx()
        
        if data["type"] == "JV":
            ax = plotJV(data, ax=ax, **kargs)
            if kargs.get("legend",True):
                ax.legend()
            return ax
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