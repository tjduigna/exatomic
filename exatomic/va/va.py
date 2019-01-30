# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Vibrational Averaging
#########################
Collection of classes for VA program
"""
import numpy as np
import pandas as pd
import csv
import os
import glob
import re
from numba import jit, prange
from exa.util.constants import speed_of_light_in_vacuum as C
from exa.util.units import Length, Energy, Mass, Time
from exa.util.utility import mkp
from exatomic.core import Atom, Gradient
from exa import TypedMeta
import warnings
warnings.simplefilter("default")

def get_data(path, attr, soft, f_end='', f_start='', sort_index=['']):
    # TODO: Make something so that we do not have to set the type of output parser by default
    #       allow the user to specify which it is based on the file.
    #       Consider just using soft as an input of a class
    if not isinstance(sort_index, list):
        raise TypeError("Variable sort_index must be of type list")
    if not hasattr(soft, attr):
        raise NotImplementedError("parse_{} is not a method of {}".format(attr, soft))
    files = glob.glob(path)
    array = []
    for file in files:
        if file.split('/')[-1].endswith(f_end) and file.split('/')[-1].startswith(f_start):
            ed = soft(file)
            try:
                df = getattr(ed, attr)
            except AttributeError:
                raise AttributeError("The property {} cannot be found in output {}".format(
                                                                                        attr, file))
            fdx = list(map(int, re.findall('\d+', file.split('/')[-1].replace(
                                                                   f_start, '').replace(f_end, ''))))
            df['file'] = np.tile(fdx, len(df))
        else:
            continue
        array.append(df)
    cdf = pd.concat([arr for arr in array])
    if sort_index[0] == '':
        if 'file' in cdf.columns.values:
            if 'label' in cdf.columns.values or 'atom' in cdf.columns.values:
                try:
                    cdf.sort_values(by=['file', 'label'], inplace=True)
                except KeyError:
                    cdf.sort_values(by=['file', 'atom'], inplace=True)
            else:
                warnings.warn("Sorting only by file label on DataFrame. Be careful if there is "+ \
                              "some order dependent function that is being used later based off"+ \
                              " this output.", Warning)
                cdf.sort_values(by=['file'], inplace=True)
    else:
        try:
            cdf.sort_values(by=sort_index, inplace=True)
        except KeyError:
            raise KeyError("Please make sure that the keys {} exist in the dataframe "+ \
                                        "created by {}.parse_{}.".format(sort_values, soft, attr))
    cdf.reset_index(drop=True, inplace=True)
    return cdf

@jit(nopython=True)
def _backscat(C_au, beta_g, beta_A):
    return 4./C_au * (24 * beta_g + 8 * beta_A)

@jit(nopython=True)
def _forwscat(C_au, alpha_g, beta_g, beta_A):
    return 4./C_au * (180 * alpha_g + 4 * beta_g - 4 * beta_A)

@jit(nopython=True)
def _make_derivatives(dalpha_dq, dg_dq, dA_dq, frequencies, epsilon, nmodes, conver):
    alpha_squared = np.zeros(nmodes,dtype=np.complex128)
    for fdx in prange(nmodes):
        for al in prange(3):
            for be in prange(3):
                alpha_squared[fdx] += (1./9.)*(dalpha_dq[fdx][al*3+al]* \
                                                    np.conj(dalpha_dq[fdx][be*3+be]))
    alpha_squared = np.real(alpha_squared).astype(np.float64)

    beta_alpha = np.zeros(nmodes,dtype=np.complex128)
    for fdx in prange(nmodes):
        for al in prange(3):
            for be in prange(3):
                beta_alpha[fdx] += 0.5*(3*dalpha_dq[fdx][al*3+be]*np.conj(dalpha_dq[fdx][al*3+be])- \
                                            dalpha_dq[fdx][al*3+al]*np.conj(dalpha_dq[fdx][be*3+be]))
    beta_alpha = np.real(beta_alpha).astype(np.float64)

    beta_g = np.zeros(nmodes,dtype=np.complex128)
    for fdx in prange(nmodes):
        for al in prange(3):
            for be in prange(3):
                beta_g[fdx] += 1j*0.5*(3*dalpha_dq[fdx][al*3+be]*np.conj(dg_dq[fdx][al*3+be])- \
                                           dalpha_dq[fdx][al*3+al]*np.conj(dg_dq[fdx][be*3+be]))
    beta_g = np.imag(beta_g).astype(np.float64)*conver

    beta_A = np.zeros(nmodes,dtype=np.complex128)
    for fdx in prange(nmodes):
        for al in prange(3):
            for be in prange(3):
                for de in prange(3):
                    for ga in prange(3):
                        beta_A[fdx] += 0.5*frequencies[fdx]*dalpha_dq[fdx][al*3+be]* \
                                              epsilon[al][de*3+ga]*np.conj(dA_dq[fdx][de*9+ga*3+be])
    beta_A = np.real(beta_A).astype(np.float64)*conver

# Just a whole bunch of test code ############################################################
#    alpha_g = np.zeros(nmodes, dtype=np.complex128)
##    alpha_g = np.zeros(nmodes, dtype=np.float64)
#    for fdx in prange(nmodes):
#        tmp_alpha = 0.0
#        tmp_beta = 0.0
#        for al in prange(3):
#        #    tmp_alpha += np.real(dalpha_dq[fdx][al*3+al])
#        #    tmp_beta += np.real(dg_dq[fdx][al*3+al])
#        #print(fdx, tmp_beta, tmp_alpha)
#        #alpha_g[fdx] = tmp_alpha*tmp_beta/3.*conver
#            #alpha_g[fdx] += dalpha_dq[fdx][al*3+al]*np.conj(dg_dq[fdx][al*3+al])/3.
#            #print(dalpha_dq[fdx][al*3+al],dalpha_dq[fdx][al*3+al]/np.sqrt(Mass['u','au_mass']), fdx, al)
#            for be in prange(3):
#                alpha_g[fdx] += dalpha_dq[fdx][al*3+al]*np.conj(dg_dq[fdx][be*3+be])/3.
#                #alpha_g[fdx] += np.real(dalpha_dq[fdx][al*3+al])*np.real(dg_dq[fdx][be*3+be])/3.
#    alpha_g = np.real(alpha_g).astype(np.float64)*conver
##    alpha_g = np.imag(alpha_g).astype(np.float64)*conver
##############################################################################################
    alpha_g = np.zeros(nmodes, dtype=np.complex128)
    for fdx in prange(nmodes):
        tmp_alpha = 0.0
        tmp_beta = 0.0
        for al in prange(3):
            for be in prange(3):
                # This equation seems to match the resonance ROA calculation by movipac
                #alpha_g[fdx] += np.real(dalpha_dq[fdx][al*3+al])*np.real(dg_dq[fdx][be*3+be])/3.
                # This equation matches what is on the listed paper in the docs (equation 9)
                alpha_g[fdx] += dalpha_dq[fdx][al*3+al]*np.conj(dg_dq[fdx][be*3+be])/9.
    alpha_g = np.real(alpha_g).astype(np.float64)*conver
    return alpha_squared, beta_alpha, beta_g, beta_A, alpha_g

@jit(nopython=True)
def _sum(arr, out, labels, files):
    for fdx in range(0,len(arr),2):
        if arr[fdx][-2] == 0:
            out[int(fdx/2)] += arr[fdx][:9].astype(np.complex128)
            out[int(fdx/2)] += 1j*arr[fdx+1][:9].astype(np.complex128)
        else:
            out[int(fdx/2)] += 1j*arr[fdx][:9].astype(np.complex128)
            out[int(fdx/2)] += arr[fdx+1][:9].astype(np.complex128)
        labels[int(fdx/2)] = arr[fdx][-3]
        files[int(fdx/2)] = arr[fdx][-1]

class VAMeta(TypedMeta):
    grad_0 = Gradient
    grad_plus = Gradient
    grad_minus = Gradient
    gradient = Gradient

class VA(metaclass=VAMeta):
    """
    Administrator class for VA to perform all initial calculations of necessary variables to pass
    for calculations.
    """
#    @staticmethod
#    def _calc_kp(lambda_0, lambda_p):
#        '''
#        Function to calculate the K_p value as given in equation 2 on J. Chem. Phys. 2007, 127, 134101.
#        We assume the temperature to be 298.15 as a hard coded value. Must get rid of this in future
#        iterations. The final units of the equation is in m^2.
#        Input values lambda_0 and lambda_p must be in the units of m^-1
#        '''
#        # epsilon_0 = 1/(4*np.pi*1e-7*C**2)
#        # another hard coded value
#        temp = 298.15 # Kelvin
#        boltz = 1.0/(1.0-np.exp(-H*C*lambda_p/(KB*temp)))
#        constants = H * np.pi**2 / C
#        variables = (lambda_0 - lambda_p)**4/lambda_p
#        kp = 2 * variables * constants * boltz * (Length['au', 'm']**4 / Mass['u', 'kg'])
#        return kp

    def vroa(self, uni, delta):
        """
        Here we implement the Vibrational Raman Optical Activity (VROA) equations as outlined in
        the paper J. Chem. Phys. 2007, 127,
        134101. The general workflow is that we must read in the data from a Raman Optical Activity
        calculation with your software of choice and this script will take that data and generate
        the forward and back scattering intensities for VROA. From here you will be able to plot
        the spectra with another method in this same class.

        Note:
            It is extremely important that the delta values that you pass into the function are the
            exact same as the ones that were used to generate the displaced structures. We do not
            currently have a method to do this automatically but we are working on it.

        Args:
            uni (:class:`~exatomic.Universe`): Universe containing all dataframes from the
                                               frequency calculation
            delta (np.ndarray): Array containing all of the delta values used for the generation
                                of the displaced structures.
        """
        if not hasattr(self, 'roa'):
            raise AttributeError("Please set roa attribute.")
        if not hasattr(uni, 'frequency_ext'):
            raise AttributeError("Please compute frequency_ext dataframe.")
        if not hasattr(uni, 'frequency'):
            raise AttributeError("Please compute frequency dataframe.")
        # we must remove the 0 index file as by default our displaced coordinate generator will
        # include these values and they have no significane in this code as of yet
        try:
            roa_0 = self.roa.groupby('file').get_group(0)
            idxs = roa_0.index.values
            roa = self.roa.loc[~self.roa.index.isin(idxs)]
        except KeyError:
            roa = self.roa.copy()
        # set some variables that will be used throughout
        # Number of normal modes
        nmodes = len(uni.frequency_ext.index.values)
        # a conversion factor for the beta_g beta_A and alpha_g tensor invariants
        # TODO: make the conversion for the alha_squared and beta_alpha invariants
        conver = Length['au', 'Angstrom']**4/(C*Length['m', 'au']/Time['s','au'])
        print(conver)
        # speed of light in au
        C_au = C*Length['m', 'au']/Time['s','au']
        # get the aquare roots of the reduced masses
        rmass = np.sqrt(uni.frequency_ext['r_mass'].values).reshape(nmodes,1)
        # reshape the delta array
        delta = delta.reshape(nmodes,1)
        # get frequencies
        frequencies = uni.frequency_ext['freq'].values
        # generate a Levi Civita 3x3x3 tensor
        epsilon = np.array([[0,0,0,0,0,1,0,-1,0],[0,0,-1,0,0,0,1,0,0],[0,1,0,-1,0,0,0,0,0]])
        # some dictionaries to replace the string labels with integers
        # this is important so we can speed up the code with jit
        rep_label = {'Ax': 0, 'Ay': 1, 'Az': 2, 'alpha': 3, 'g_prime': 4}
        rep_type = {'real': 0, 'imag': 1}
        # replace the columns
        roa.replace(rep_label, inplace=True)
        roa.replace(rep_type, inplace=True)
        # get rid of the frame column serves no purpose here
        roa.drop('frame', axis=1, inplace=True)
        # create a numpy array with the necessary dimensions
        # number_of_files/2 x 9
        value_complex = np.zeros((int(len(roa)/2),9), dtype=np.complex128)
        labels = np.zeros(int(len(roa)/2), dtype=np.int8)
        files = np.zeros(int(len(roa)/2), dtype=np.int8)
        _sum(roa.values, value_complex, labels, files)
        labels = pd.Series(labels)
        files = pd.Series(files)
        # replace the integer labels with the strings again
        # TODO: is this really necessary?
        labels.replace({v: k for k, v in rep_label.items()}, inplace=True)
        complex_roa= pd.DataFrame(value_complex)
        complex_roa.index = labels
        complex_roa['file'] = np.repeat(range(2*nmodes),5)
        # because I could not use range(9)............ugh
        cols = [0,1,2,3,4,5,6,7,8]
        # splice the data into the respective tensor dataframes
        # we want all of the tensors in a 1d vector like form
        A = pd.DataFrame.from_dict(complex_roa.loc[['Ax','Ay','Az']].groupby('file').
                                   apply(lambda x: np.array([x[cols].values[0], x[cols].values[1], 
                                                             x[cols].values[2]]).flatten()).
                                   reset_index(drop=True).to_dict()).T
        alpha = pd.DataFrame.from_dict(complex_roa.loc['alpha',range(9)].reset_index(drop=True).
                                       to_dict())
        g_prime = pd.DataFrame.from_dict(complex_roa.loc['g_prime',range(9)].reset_index(drop=True).
                                         to_dict())
        #***********DEBUG***********#
        #self.A = A
        #self.alpha = alpha
        #self.g_prime = g_prime
        #********END DEBUG**********#

        # separate tensors into positive and negative displacements
        # highly dependent on the value of the index
        # we neglect the equilibrium coordinates
        # 0 corresponds to equilibrium coordinates
        # 1 - nmodes corresponds to positive displacements
        # nmodes+1 - 2*nmodes corresponds to negative displacements
        alpha_plus = np.divide(alpha.loc[range(0,nmodes)].values, rmass)
        alpha_minus = np.divide(alpha.loc[range(nmodes, 2*nmodes)].values, rmass)
        g_prime_plus = np.divide(g_prime.loc[range(0,nmodes)].values, rmass)
        g_prime_minus = np.divide(g_prime.loc[range(nmodes, 2*nmodes)].values, rmass)
        A_plus = np.divide(A.loc[np.arange(nmodes)].values, rmass)
        A_minus = np.divide(A.loc[np.arange(nmodes, 2*nmodes)].values, rmass)

        # generate derivatives by two point difference method
        dalpha_dq = np.divide((alpha_plus - alpha_minus), 2 * delta)
        dg_dq = np.divide((g_prime_plus - g_prime_minus), 2 * delta)
        dA_dq = np.array([np.divide((A_plus[i] - A_minus[i]), 2 * delta[i]) for i in range(nmodes)])
        #***********DEBUG***********#
        self.dalpha_dq = dalpha_dq
        self.dg_dq = dg_dq
        #self.dA_dq = dA_dq
        #********END DEBUG**********#

        # generate properties as shown on equations 5-9 in paper
        # J. Chem. Phys. 2007, 127, 134101
        alpha_squared, beta_alpha, beta_g, beta_A, alpha_g = _make_derivatives(dalpha_dq,
                                                dg_dq, dA_dq, frequencies, epsilon, nmodes, conver)

        #********************************DEBUG**************************************************#
        #self.alpha_squared = pd.Series(alpha_squared*Length['au', 'Angstrom']**4)
        #self.beta_alpha = pd.Series(beta_alpha*Length['au', 'Angstrom']**4)
        #self.beta_g = pd.Series(beta_g*Length['au', 'Angstrom']**4/
        #                                                    (C*Length['m', 'au']/Time['s','au']))
        #self.beta_A = pd.Series(beta_A*Length['au', 'Angstrom']**4/
        #                                                    (C*Length['m', 'au']/Time['s','au']))
        #self.alpha_g = pd.Series(alpha_g*Length['au', 'Angstrom']**4/
        #                                                    (C*Length['m', 'au']/Time['s','au']))
        #*******************************END DEBUG***********************************************#

        # calculate VROA back scattering and forward scattering intensities
        backscat_vroa = _backscat(C_au, beta_g, beta_A)
        forwscat_vroa = _forwscat(C_au, alpha_g, beta_g, beta_A)
        # we set this just so it is easier to view the data
        pd.options.display.float_format = '{:.6f}'.format
        self.backscat_vroa = pd.DataFrame.from_dict({"freq": frequencies*Energy['Ha', 'cm^-1'],
                                                     "beta_g*1e6":beta_g*1e6, "beta_A": beta_A,
                                                     "backscatter*1e4": backscat_vroa*1e4})
        self.forwscat_vroa = pd.DataFrame.from_dict({"freq": frequencies*Energy['Ha', 'cm^-1'],
                                                     "alpha_g*1e6": alpha_g*1e6,
                                                     "beta_g*1e6": beta_g*1e6, "beta_A": beta_A,
                                                     "forwardscatter*1e4": forwscat_vroa*1e4})

    def init_va(self, uni, delta=None):
        """
        This is a method to initialize all of the variables that will be needed to execute the VA
        program. As a sanity check we calculate the frequencies from the force constants. If we
        have any negative force constants the results may not be as reliable.

        Args:
            uni (:class:`~exatomic.Universe`): Universe object containg pertinent data from
                                               frequency calculation
        """
        if delta is None:
            delta_df = gen_delta(freq=uni.frequency.copy(), delta_type=2)
            delta = delta_df['delta'].values
        if not hasattr(self, "gradient"):
            raise AttributeError("Please set gradient attribute first")
        if not hasattr(uni, "frequency_ext"):
            raise AttributeError("Cannot find frequency extended dataframe in universe")
        if not hasattr(uni, "frequency"):
            raise AttributeError("Cannot find frequency dataframe in universe")
        # check that all attributes to be used exist
        # group the gradients by file (normal mode)
        grouped = self.gradient.groupby('file')
        # get number of normal modes
        nmodes = len(uni.frequency_ext.index.values)
        # generate delta dataframe
        # TODO: make something so delta can be set
        #       possible issues are a user using a different type of delta
        # get gradient of the equilibrium coordinates
        grad_0 = grouped.get_group(0)
        # get gradients of the displaced coordinates in the positive direction
        grad_plus = grouped.filter(lambda x: x['file'].drop_duplicates().values in
                                                                        range(1,nmodes+1))
        # get number of selected normal modes
        # TODO: check stability of using this parameter
        snmodes = len(grad_plus['file'].drop_duplicates().values)
        # get gradients of the displaced coordinates in the negative direction
        grad_minus = grouped.filter(lambda x: x['file'].drop_duplicates().values in
                                                                        range(nmodes+1, 2*nmodes+1))
        # TODO: Check if we can make use of numba to speed up this code
        delfq_zero = uni.frequency.groupby('freqdx')[['dx', 'dy', 'dz']].apply(lambda x:
                                    np.sum(np.multiply(grad_0[['fx', 'fy', 'fz']].values, x.values)))
        delfq_zero = np.tile(delfq_zero, nmodes).reshape(snmodes, nmodes)

        delfq_plus = grad_plus.groupby('file')[['fx', 'fy', 'fz']].apply(lambda x:
                                uni.frequency.groupby('freqdx')[['dx', 'dy', 'dz']].apply(lambda y:
                                    np.sum(np.multiply(y.values, x.values))))
        delfq_plus.reset_index(drop=True, inplace=True)

        delfq_minus = grad_minus.groupby('file')[['fx', 'fy', 'fz']].apply(lambda x:
                                uni.frequency.groupby('freqdx')[['dx', 'dy', 'dz']].apply(lambda y:
                                    np.sum(np.multiply(y.values, x.values))))
        delfq_minus.reset_index(drop=True, inplace=True)

        # get diagonal elements of respqective matrix
        diag_plus = np.diag(delfq_plus)
        diag_minus = np.diag(delfq_minus)
        diag_zero = np.diag(delfq_zero)

        # calculate force constants
        kqi   = np.divide(diag_plus - diag_minus, 2.0*delta)
        kqiii = np.divide(diag_plus - 2.0 * diag_zero + diag_minus, np.multiply(delta, delta))
        kqijj = np.divide(delfq_plus - 2.0 * delfq_zero + delfq_minus,
                                                    np.multiply(delta, delta).reshape(snmodes, 1))

        # convert force constants to reduced normal coordinate force constants
        redmass = uni.frequency_ext['r_mass'].values*Mass['u', 'au_mass']
        vqi = np.divide(kqi, redmass)
        vqijj = np.divide(kqijj, np.sqrt(np.power(redmass, 3)).reshape(snmodes,1))

        # TODO: Check if we want to exit the program if we get a negative force constant
        n_force_warn = vqi[vqi < 0.]

        # calculate frequencies
        calcfreq = np.sqrt(vqi)
        calcfreq *= Energy['Ha', 'cm^-1']
        self.calcfreq = pd.DataFrame.from_dict({'calc_freq': calcfreq,
                                      'real_freq': uni.frequency_ext['freq']*Energy['Ha', 'cm^-1']})


