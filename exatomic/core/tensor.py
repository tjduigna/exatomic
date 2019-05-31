# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0

from exa import DataFrame
import numpy as np
import pandas as pd
from exatomic import plotter

# changing this so that tensor refers to a base class of attributes that all
# tensor property dataframes should have
class Tensor(DataFrame):
    """
    The tensor dataframe.

    +---------------+----------+-----------------------------------------+
    | Column        | Type     | Description                             |
    +===============+==========+=========================================+
    | xx            | float    | 0,0 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | xy            | float    | 0,1 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | xz            | float    | 0,2 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | yx            | float    | 1,0 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | yy            | float    | 1,1 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | yz            | float    | 1,2 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | zx            | float    | 3,0 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | zy            | float    | 3,1 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | zz            | float    | 3,2 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | frame         | category | frame value to which atach tensor       |
    +---------------+----------+-----------------------------------------+
    | atom          | int      | atom index of molecule to place tensor  |
    +---------------+----------+-----------------------------------------+
    | label         | category | label of the type of tensor             |
    +---------------+----------+-----------------------------------------+
    """
    _index = 'tensor'
    _columns = ['xx','xy','xz','yx','yy','yz','zx','zy','zz',
                'frame','atom','label']
    _categories = {'frame': np.int64, 'label': str}

    #@property
    #def _constructor(self):
    #    return Tensor

    @classmethod
    def from_file(cls, filename):
        """
        A file reader that will take a tensor file and extract all
        necessary information. There is a specific file format in place
        and is as follows

        frame label atom
        xx xy xz
        yx yy yz
        zx zy zz

        For multiple tensors just append the same format as above without
        whitespace unless leaving the frame, label, atom attributes as empty.

        Args:
            filename (str): file pathname

        Returns:
            tens (:class:`~exatomic.tensor.Tensor`): Tensor table with the tensor attributes
        """
        df = pd.read_csv(filename, delim_whitespace=True, header=None,
                         skip_blank_lines=False)
        meta = df[::4]
        idxs = meta.index.values
        n = len(idxs)
        df = df[~df.index.isin(idxs)]
        df[1] = df[1].astype(np.float64)
        df['grp'] = [i for i in range(n) for j in range(3)]
        df = pd.DataFrame(df.groupby('grp').apply(lambda x:
                     x.unstack().values[:-3]).values.tolist(),
                     columns=['xx','xy','xz','yx','yy','yz','zx','zy','zz'])
#        scale = []
#        for i in df.index.values:
#            scale.append(5./abs(df.loc[i,:]).max().astype(np.float64))
        meta.reset_index(drop=True, inplace=True)
        meta.rename(columns={0: 'frame', 1: 'label', 2: 'atom'}, inplace=True)
        df = pd.concat([meta, df], axis=1)
        df['atom'] = df['atom'].astype(np.int64)
        df['frame'] = df['frame'].astype(np.int64)
        df['symbols'] = np.repeat('', n)
#        df['scale'] = scale
#        print(df)
        return cls(df)

class Polarizability(Tensor):
    _index = 'polarizability'
    _columns = ['xx', 'xy', 'xz', 'yx', 'yy', 'yz', 'zx', 'zy', 'zz',
                'frame', 'label', 'type']
    _categories = {'frame': np.int64, 'label': str}

class NMRShielding(Tensor):
    """
    The NMR Shielding tensor dataframe.

    +---------------+----------+-----------------------------------------+
    | Column        | Type     | Description                             |
    +===============+==========+=========================================+
    | xx            | float    | 0,0 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | xy            | float    | 0,1 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | xz            | float    | 0,2 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | yx            | float    | 1,0 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | yy            | float    | 1,1 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | yz            | float    | 1,2 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | zx            | float    | 3,0 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | zy            | float    | 3,1 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | zz            | float    | 3,2 position in tensor                  |
    +---------------+----------+-----------------------------------------+
    | frame         | category | frame value to which atach tensor       |
    +---------------+----------+-----------------------------------------+
    | atom          | int      | atom index of molecule to place tensor  |
    +---------------+----------+-----------------------------------------+
    | label         | category | label of the type of tensor             |
    +---------------+----------+-----------------------------------------+
    | symbol        | category | atom symbol the tensor is attached to   |
    +---------------+----------+-----------------------------------------+
    | isotropic     | float    | isotropic shift value of the tensor     |
    +---------------+----------+-----------------------------------------+
    """
    _index = 'nmr_shielding'
    _columns = ['xx','xy','xz','yx','yy','yz','zx','zy','zz',
                'frame','atom','label','symbol','isotropic']
    _categories = {'frame': np.int64, 'label': str, 'symbol': str}

    def nmr_spectra(self, fwhm=1, ref=None, atom='H', lineshape='lorentzian', **kwargs):
        '''
        Generate NMR spectra with the plotter class. We can define a gaussian or lorentzian
        lineshape function. For the most part we pass all of the kwargs directly into the
        plotter.Plot class.

        Args:
            fwhm (float): Full-width at half-maximum
            ref (float): Isotropic shift of the reference compound
            atom (str): Atom that we want to display the spectra for
            lineshape (str): Switch beteen the different lineshape functions available
        '''
        # define the lineshape and store the function call in the line variable
        if lineshape == 'lorentzian':
            line = plotter.lorentzian
        elif lineshape == 'gaussian':
            line = plotter.gaussian
        else:
            raise NotImplementedError("Sorry we have not yet implemented the lineshape {}.".format(lineshape))
        if not "plot_width" in kwargs:
            kwargs.update(plot_width=900)
        # define the class
        plot = plotter.Plot(**kwargs)
        # this is designed for a single frame
        if self['frame'].drop_duplicates().values[-1] != 0:
            raise NotImplementedError("We have not yet expanded to include multiple frames")
        # grab the locations of the peaks
        shifts = self.groupby('symbol').get_group(atom)['isotropic'].astype(np.float64)
        if ref is not None:
            # we just try to take care of any possible types for the ref variable
            # its a bit of overkill but just want to make sure we can deal with them
            if isinstance(ref, float) or isinstance(ref, int):
                shifts = ref - shifts
            elif isinstance(ref, list) or isinstance(ref, np.ndarray):
                shifts = ref[0] - shifts
            else:
                raise TypeError("Could not understand type ref type {}.".format(type(ref)))
        x_data = np.arange(shifts.min()-10*fwhm, shifts.max()+10*fwhm, fwhm/50)
        # get the y data by calling the lineshape function generator
        y_data = line(freq=shifts.values, x=x_data, fwhm=fwhm)
        # plot the lineshape data
        plot.fig.line(x_data, y_data)
        # plot the points on the plot to show were the frequency values are
        # more useful when we have nearly degenerate vibrations
        plot.fig.scatter(shifts, line(freq=shifts, x=shifts, fwhm=fwhm))
        # just to make sure the plot is oriemted correctly
        # typically 0 is on the left when we have a reference compound god knows why
        if ref is not None:
            plot.set_xrange(xmin=max(x_data), xmax=min(x_data))
        # display the figure with our generated method
        plot.show()

def add_tensor(uni, fp):
    """
    Simple function to add a tensor object to the universe.

    Args:
        uni (universe): Universe object
        fp (str): file pathname
    """
    uni.tensor = Tensor.from_file(fp)
#    if fp != None:
#        uni.tensor = Tensor.from_file(fp)
#    if any('tensor' in x for x in vars(uni)):
#        tmp = [x for x in vars(uni) if 'tensor' in x]
#        uni.tensor = pd.concat([uni[i] for i in tmp], sort=False).reset_index(drop=True)
