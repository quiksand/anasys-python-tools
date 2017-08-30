# -*- encoding: utf-8 -*-
#
#  heightmap.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.

import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use("TkAgg") #Keeps tk from crashing on fial dialog open
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
# from . import anasysfile
import anasysfile

class IRRenderedSpectra(anasysfile.AnasysElement):
    """A data structure for holding HeightMap data"""

    def __init__(self, irrenderedspectra):
        # self._parent = parent #parent object (Document)
        self._special_write = {'DataChannels': self._write_data_channels}
        self._special_read = {'DataChannels': self._get_data_channels}
        self._skip_on_write = ['Background'] #objects to skip when writing back to xml
        # a=irrenderedspectra
        self._wrangle_data_channels(irrenderedspectra)
        # b=irrenderedspectra
        # print(a==b)
        anasysfile.AnasysElement.__init__(self, etree=irrenderedspectra)
        self.Background = self._get_background() #get bg associated with this spectra

    def _wrangle_data_channels(self, irrenderedspectra):
        new_datachannels = ET.SubElement(irrenderedspectra, 'temp_DataChannels')
        for dc in irrenderedspectra.findall('DataChannels'):
            dc.tag = 'DataChannel'
            new_datachannels.append(dc)
            irrenderedspectra.remove(dc)
        new_datachannels.tag = 'DataChannels'

    def _get_data_channels(self, datachannels):
        """Returns a list of the DataChannel objects"""
        dcdict = {}
        for dc in datachannels:
            new_dc = DataChannel(dc)
            key = new_dc.Name
            key = self._check_key(key, dcdict)
            dcdict[key] = new_dc
        return dcdict

    def _write_data_channels(self, *args, **kwargs):
        pass

    def _get_background(self):
        pass
        # return self._parent.Backgrounds[self.BackgroundID]

class DataChannel(anasysfile.AnasysElement):
    """Data structure for holding spectral Data"""

    def __init__(self, datachannels):
        anasysfile.AnasysElement.__init__(self, etree=datachannels)

class Background(anasysfile.AnasysElement):
    """Data structure for holding background data"""

    def __init__(self, background):
        self._special_write = {'Table': self._nparray_to_serial_tags,
                              'AttenuatorPower': self._nparray_to_serial_tags}
        self._special_read = {'Table': self._serial_tags_to_nparray,
                              'AttenuatorPower': self._serial_tags_to_nparray}
        anasysfile.AnasysElement.__init__(self, etree=background)

    # def _get_table(self, table): # 126
    #     table_data = []
    #     for double in table:
    #         table_data.append(float(double.text))
    #         table.remove(double)
    #     table_data = np.array(table_data)
    #     return table_data

    # def _get_attenuatorPower(self, atpow):
    #     pewerdata = []
    #     for double in atpow:
    #         at
