import pandas
import sunpy
import sunpy.map
import numpy as np
import matplotlib.pyplot as plt

class Foxsi2PhotonList():

    def __init__(self, filename):
        self.data = pandas.DataFrame.from_csv(filename)
        self.detector = self.data['detector_number'].values[0]
        self.number_of_hits = len(self.data)

    def get_image(self,time_range = [69100,69600], energy_range = [0,100]):

        bins=[np.linspace(-1000,1000,201),np.linspace(-1000,1000,201)]
        image_hits = self.data.query('energy2 > ' +str(energy_range[0]) +
                                                        ' and energy2 < ' + str(energy_range[1]) +
                                                        ' and wsmr_time > ' + str(time_range[0]) +
                                                        ' and wsmr_time < ' + str(time_range[1]))
          
        h = plt.hist2d(image_hits['hit_xy_solar_x'],image_hits['hit_xy_solar_y'], bins=bins)
        img=h[0].swapaxes(0,1)
        
        dict_header = {
        "cdelt1": 10.0,
        "naxis1": 201,
        "crval1": 0.0,
        "crpix1": 100,
        "cunit1": "arcsec",
        "ctype1": "HPLN-TAN",
        "cdelt2": 10.0,
        "naxis2": 201,
        "crval2": 0.0,
        "crpix2": 100,
        "cunit2": "arcsec",
        "ctype2": "HPLT-TAN",
        "observatory":"FOXSI",
        "detector":self.detector
}
        
        foxsi_map = sunpy.map.GenericMap(img, dict_header)
        
        return foxsi_map

    def get_spectrum(self, time_range=[69100,69600], ebins = np.linspace(1,100,100)):
        foxsi_spec = Foxsi2Spectrum(self, time_range = time_range, ebins = ebins)

        return foxsi_spec
        
        
        
class Foxsi2Spectrum():
    def __init__(self,Foxsi2PhotonList, time_range=[69100,69600], ebins = np.linspace(1,100,100)):

        spectrum_hits = Foxsi2PhotonList.data.query('wsmr_time > ' + str(time_range[0]) +
                                        ' and wsmr_time < ' + str(time_range[1]))

        h = np.histogram(spectrum_hits,bins = ebins)
        self.data = h[0]
        self.energies = h[1][0:-1]
        self.time_range = time_range

    def plot(self):
        plt.loglog(self.energies,self.data,linestyle='steps-mid')
        plt.xlabel('energy (keV')
        plt.ylabel('Counts')
        plt.show()

        
class Foxsi2LightCurve():
    def __init__(self, Foxsi2PhotonList, time_range=[69100,69600], energy_range = [0,100]):

        lightcurve_hits = Foxsi2PhotonList.data.query('energy2 > ' +str(energy_range[0]) +
                                                        ' and energy2 < ' + str(energy_range[1]) +
                                                        ' and wsmr_time > ' + str(time_range[0]) +
                                                        ' and wsmr_time < ' + str(time_range[1]))
          

        tbins = np.linspace(int(time_range[0]), int(time_range[1], int(time_range[1]) - int(time_range[0]) + 1 ) )
        
        h = np.histogram(lightcurve_hits, bins = tbins)

        self.data = h[0]
        self.times = h[1][0:-1]

    def plot(self):
        plt.plot(self.times,self.data,linestyle='steps-mid')
        plt.xlabel('WSMR time')
        plt.ylabel('Counts')
        plt.show()
        

        
        
