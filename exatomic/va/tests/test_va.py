import numpy as np
import pandas as pd
from unittest import TestCase
from os import sep

#from exatomic import va
from exatomic.base import resource
from exatomic.va import VA, get_data, gen_delta
from exatomic.gaussian import Fchk
from exatomic.nwchem import Output

class TestGetData(TestCase):
    def setUp(self):
        pass

    def test_getter_small(self):
        path = sep.join(resource('va-roa-h2o2-def2tzvp-514.5-00.out').split(sep)[:-1])+sep+'*'
        df = get_data(path=path, attr='roa', soft=Output, f_start='va-roa-h2o2-def2tzvp-514.5-',
                      f_end='.out')
        self.assertEqual(df.shape[0], 130)
        df = get_data(path=path, attr='gradient', soft=Output, f_start='va-roa-h2o2-def2tzvp-514.5-',
                      f_end='.out')
        self.assertEqual(df.shape[0], 52)

    def test_getter_large(self):
        path = sep.join(resource('va-roa-methyloxirane-def2tzvp-488.9-00.out').split(sep)[:-1])+sep+'*'
        df = get_data(path=path, attr='roa', soft=Output, f_start='va-roa-methyloxirane-def2tzvp-488.9-',
                      f_end='.out')
        self.assertEqual(df.shape[0], 160)
        df = get_data(path=path, attr='gradient', soft=Output, f_start='va-roa-methyloxirane-def2tzvp-488.9-',
                      f_end='.out')
        self.assertEqual(df.shape[0], 160)

class TestVROA(TestCase):
    def setUp(self):
        self.h2o2_freq = Fchk(resource('g16-h2o2-def2tzvp-freq.fchk'))
        self.methyloxirane_freq = Fchk(resource('g16-methyloxirane-def2tzvp-freq.fchk'))

    def test_vroa(self):
        self.h2o2_freq.parse_frequency()
        self.h2o2_freq.parse_frequency_ext()
        delta = gen_delta(delta_type=2, freq=self.h2o2_freq.frequency.copy())
        va_corr = VA()
        path = sep.join(resource('va-roa-h2o2-def2tzvp-514.5-00.out').split(sep)[:-1])+sep+'*'
        va_corr.roa = get_data(path=path, attr='roa', soft=Output, f_start='va-roa-h2o2-def2tzvp-514.5-',
                               f_end='.out')
        va_corr.roa['exc_freq'] = np.tile(514.5, len(va_corr.roa))
        va_corr.gradient = get_data(path=path, attr='gradient', soft=Output, 
                                    f_start='va-roa-h2o2-def2tzvp-514.5-', f_end='.out')
        va_corr.gradient['exc_freq'] = np.tile(514.5, len(va_corr.gradient))
        va_corr.vroa(uni=self.h2o2_freq, delta=delta['delta'].values)
        roa_data = np.array([[-3.36769948e+02,  4.41928437e+01, -8.18695910e+00,
         4.41928437e+01,  6.29746625e+00,  4.08559110e+00,
        -8.18695910e+00,  4.08559110e+00,  1.35153161e-01],
       [-7.11404867e-01,  8.41408563e-02,  2.21705569e-02,
         8.41408563e-02,  2.07593082e-02, -4.48400801e-03,
         2.21705569e-02, -4.48400801e-03, -3.15495282e-03],
       [-2.25308312e+01, -1.86464130e+02,  5.49841755e+01,
        -1.86464130e+02,  1.19223305e+02, -1.53137381e+01,
         5.49841755e+01, -1.53137381e+01,  3.56422905e+00],
       [-7.11500765e-02, -4.72167789e-01,  2.18770839e-01,
        -4.72167789e-01,  3.08237735e-01, -6.38468860e-02,
         2.18770839e-01, -6.38468860e-02,  6.04579734e-03],
       [-1.32384022e+01,  5.60616522e+01, -2.51508923e+02,
         5.60616522e+01, -3.52317537e+01,  8.21381741e+01,
        -2.51508923e+02,  8.21381741e+01,  8.39266717e+00],
       [ 5.26242475e-02,  2.05354470e-01, -6.60461260e-01,
         2.05354470e-01, -1.43880128e-01,  2.19904436e-01,
        -6.60461260e-01,  2.19904436e-01,  3.27496018e-02],
       [ 1.06850749e+01,  7.35868345e-01,  3.63887143e-01,
         7.35868345e-01,  1.20809919e+01, -3.39150354e+00,
         3.63887143e-01, -3.39150354e+00,  1.60335357e+01],
       [ 2.24386374e-02,  2.36379194e-03, -1.82319296e-03,
         2.36379204e-03,  3.03934789e-02, -1.33732209e-02,
        -1.82319294e-03, -1.33732207e-02,  4.16925211e-02],
       [-6.30347802e-02, -1.68378073e-01,  2.96829152e+00,
         7.81451352e-01,  2.18913131e+00,  8.42429914e+00,
        -3.19125923e+00, -1.10262773e+01, -2.13064766e+00],
       [-7.70868642e-04,  8.07396587e-04,  5.75769040e-02,
         3.46198096e-02,  9.48085883e-02,  1.31889682e-01,
        -6.12555374e-02, -2.32032295e-01, -9.64666793e-02],
       [-3.37457573e+02,  4.32441667e+01, -9.17246000e+00,
         4.32441667e+01,  6.97352700e+00,  4.38077686e+00,
        -9.17246000e+00,  4.38077686e+00,  1.69572521e-01],
       [-7.11691414e-01,  8.20078043e-02,  2.00687666e-02,
         8.20078043e-02,  2.21498868e-02, -3.86010954e-03,
         2.00687666e-02, -3.86010954e-03, -3.07599110e-03],
       [-2.44715878e+01, -1.85486587e+02,  5.51892206e+01,
        -1.85486587e+02,  1.18790189e+02, -1.53952705e+01,
         5.51892206e+01, -1.53952705e+01,  3.46848118e+00],
       [-7.50291368e-02, -4.69590618e-01,  2.19231464e-01,
        -4.69590618e-01,  3.06805922e-01, -6.40166324e-02,
         2.19231464e-01, -6.40166324e-02,  5.95007176e-03],
       [-1.52711095e+01,  5.65997447e+01, -2.51827347e+02,
         5.65997447e+01, -3.53155670e+01,  8.21597728e+01,
        -2.51827347e+02,  8.21597728e+01,  8.19950991e+00],
       [ 4.84817348e-02,  2.06463015e-01, -6.60707778e-01,
         2.06463015e-01, -1.43979596e-01,  2.19608411e-01,
        -6.60707778e-01,  2.19608411e-01,  3.19691738e-02],
       [ 1.07089822e+01,  7.97095232e-01,  4.29914563e-01,
         7.97095232e-01,  1.20440608e+01, -3.40586641e+00,
         4.29914563e-01, -3.40586641e+00,  1.60589821e+01],
       [ 2.24566034e-02,  2.48310002e-03, -1.68565472e-03,
         2.48310015e-03,  3.02911815e-02, -1.34089205e-02,
        -1.68565473e-03, -1.34089203e-02,  4.17338736e-02],
       [-7.67161566e-02, -2.16307615e-01,  3.01215251e+00,
         7.86010367e-01,  2.20381334e+00,  8.41580214e+00,
        -3.20710488e+00, -1.10458000e+01, -2.13227070e+00],
       [-1.34212371e-03, -1.04981355e-03,  5.92472187e-02,
         3.47411447e-02,  9.52684259e-02,  1.31503164e-01,
        -6.17662710e-02, -2.32456031e-01, -9.66920797e-02],
       [-3.31973880e+02,  4.60138926e+01, -1.12995108e+01,
         4.60138926e+01,  4.59998313e+00,  5.10397033e+00,
        -1.12995108e+01,  5.10397033e+00,  2.19373013e-02],
       [-6.96694097e-01,  1.04595390e-01, -6.03596980e-03,
         1.04595390e-01,  5.66817017e-03,  5.11784942e-03,
        -6.03596980e-03,  5.11784942e-03, -4.27064237e-03],
       [-1.73160343e+01, -1.80630555e+02,  4.93929552e+01,
        -1.80630555e+02,  1.15087879e+02, -1.37531105e+01,
         4.93929552e+01, -1.37531105e+01,  3.62224258e+00],
       [-2.78785124e-02, -4.38786560e-01,  1.77281072e-01,
        -4.38786560e-01,  2.82699967e-01, -5.19847426e-02,
         1.77281072e-01, -5.19847426e-02,  8.55705372e-03],
       [-1.94211112e+01,  5.14568836e+01, -2.44826959e+02,
         5.14568836e+01, -3.18554878e+01,  8.00675859e+01,
        -2.44826959e+02,  8.00675859e+01,  8.61454773e+00],
       [ 4.39307923e-04,  1.71401862e-01, -6.24778397e-01,
         1.71401862e-01, -1.20590059e-01,  2.10300822e-01,
        -6.24778397e-01,  2.10300822e-01,  3.86778272e-02],
       [ 1.05346732e+01,  5.69519390e-01,  5.61464887e-01,
         5.69519390e-01,  1.16520460e+01, -3.02865969e+00,
         5.61464887e-01, -3.02865969e+00,  1.55975738e+01],
       [ 2.19777262e-02,  9.86953100e-04, -1.63316832e-04,
         9.86953280e-04,  2.77340960e-02, -1.05875656e-02,
        -1.63316844e-04, -1.05875654e-02,  3.92692282e-02],
       [-1.03418613e-01, -3.01442279e-01,  2.82305878e+00,
         6.89649008e-01,  1.93009789e+00,  8.08570946e+00,
        -3.06692920e+00, -1.07098796e+01, -1.82528131e+00],
       [-2.54578173e-03, -5.28113219e-03,  5.19903152e-02,
         3.02591376e-02,  8.39298148e-02,  1.19135302e-01,
        -5.65243559e-02, -2.20848870e-01, -8.22892487e-02],
       [-3.36187976e+02,  4.44127558e+01, -8.82872145e+00,
         4.44127558e+01,  6.02817799e+00,  4.46731143e+00,
        -8.82872145e+00,  4.46731143e+00, -7.56738588e-02],
       [-7.17815742e-01,  8.83302660e-02,  1.92685794e-02,
         8.83302660e-02,  1.87627700e-02, -3.07986003e-03,
         1.92685794e-02, -3.07986003e-03, -4.36997474e-03],
       [-2.20310300e+01, -1.87591188e+02,  5.55039294e+01,
        -1.87591188e+02,  1.19890698e+02, -1.53990657e+01,
         5.55039294e+01, -1.53990657e+01,  3.59931019e+00],
       [-6.64804550e-02, -4.73888496e-01,  2.22342816e-01,
        -4.73888496e-01,  3.09643147e-01, -6.49949808e-02,
         2.22342816e-01, -6.49949808e-02,  5.15172743e-03],
       [-1.44707541e+01,  5.67528111e+01, -2.51049105e+02,
         5.67528111e+01, -3.54336920e+01,  8.21052719e+01,
        -2.51049105e+02,  8.21052719e+01,  7.86667164e+00],
       [ 4.86115843e-02,  2.09461973e-01, -6.58027514e-01,
         2.09461973e-01, -1.45387867e-01,  2.19160638e-01,
        -6.58027514e-01,  2.19160638e-01,  3.03901101e-02],
       [ 1.06695693e+01,  7.20301224e-01,  4.03855475e-01,
         7.20301224e-01,  1.21448472e+01, -3.41543870e+00,
         4.03855475e-01, -3.41543870e+00,  1.59964994e+01],
       [ 2.26537872e-02,  2.21937660e-03, -1.69968413e-03,
         2.21937672e-03,  3.04520802e-02, -1.35669767e-02,
        -1.69968401e-03, -1.35669765e-02,  4.15044713e-02],
       [-6.95548196e-02, -1.91782243e-01,  2.95465091e+00,
         7.87181609e-01,  2.19749447e+00,  8.46269442e+00,
        -3.19345163e+00, -1.09924674e+01, -2.13249857e+00],
       [-1.01330700e-03,  1.32606824e-04,  5.71034988e-02,
         3.47030692e-02,  9.51578851e-02,  1.33207001e-01,
        -6.13622289e-02, -2.30801176e-01, -9.65448698e-02],
       [-3.37816377e+02,  4.36029507e+01, -7.58587215e+00,
         4.36029507e+01,  6.84573492e+00,  3.83378086e+00,
        -7.58587215e+00,  3.83378086e+00,  2.58661933e-01],
       [-7.00647496e-01,  8.17709642e-02,  2.23153353e-02,
         8.17709642e-02,  2.14877340e-02, -4.88251754e-03,
         2.23153353e-02, -4.88251754e-03, -2.47666408e-03],
       [-2.40165054e+01, -1.86264733e+02,  5.40466873e+01,
        -1.86264733e+02,  1.19225979e+02, -1.48797714e+01,
         5.40466873e+01, -1.48797714e+01,  3.46465491e+00],
       [-7.18014214e-02, -4.63334062e-01,  2.13860696e-01,
        -4.63334062e-01,  3.02841438e-01, -6.19697607e-02,
         2.13860696e-01, -6.19697607e-02,  4.89570980e-03],
       [-1.20871962e+01,  5.49366974e+01, -2.49032422e+02,
         5.49366974e+01, -3.45529019e+01,  8.13450749e+01,
        -2.49032422e+02,  8.13450749e+01,  8.11343879e+00],
       [ 5.16733497e-02,  2.00856257e-01, -6.47070329e-01,
         2.00856257e-01, -1.40290889e-01,  2.15379127e-01,
        -6.47070329e-01,  2.15379127e-01,  3.08067471e-02],
       [ 1.07166012e+01,  7.82569481e-01,  3.28188631e-01,
         7.82569481e-01,  1.20866925e+01, -3.33451086e+00,
         3.28188631e-01, -3.33451086e+00,  1.58811314e+01],
       [ 2.20938505e-02,  2.37875545e-03, -1.78778654e-03,
         2.37875557e-03,  2.98591790e-02, -1.30929144e-02,
        -1.78778641e-03, -1.30929142e-02,  4.08642608e-02],
       [-5.52407070e-02, -1.44059984e-01,  3.00473735e+00,
         7.72589228e-01,  2.15433378e+00,  8.43895220e+00,
        -3.16732490e+00, -1.09258500e+01, -2.10179721e+00],
       [-5.38429571e-04,  1.52221890e-03,  5.84720328e-02,
         3.41795862e-02,  9.35807571e-02,  1.31816894e-01,
        -6.03593145e-02, -2.28138454e-01, -9.52405726e-02],
       [-3.31308286e+02,  4.14442319e+01, -7.16408915e+00,
         4.14442319e+01,  7.35420869e+00,  3.84250317e+00,
        -7.16408915e+00,  3.84250317e+00,  6.60412033e-01],
       [-6.86260021e-01,  6.84387909e-02,  3.13723303e-02,
         6.84387909e-02,  2.75086143e-02, -7.41389511e-03,
         3.13723303e-02, -7.41389511e-03, -5.43982474e-04],
       [-2.59355688e+01, -1.86337972e+02,  5.23670175e+01,
        -1.86337972e+02,  1.19418705e+02, -1.43101075e+01,
         5.23670175e+01, -1.43101075e+01,  3.88556261e+00],
       [-9.15645875e-02, -4.64896269e-01,  2.01175044e-01,
        -4.64896269e-01,  3.04891483e-01, -5.77622312e-02,
         2.01175044e-01, -5.77622312e-02,  8.22510609e-03],
       [-1.19681708e+01,  5.31143813e+01, -2.54501209e+02,
         5.31143813e+01, -3.37376002e+01,  8.34473292e+01,
        -2.54501209e+02,  8.34473292e+01,  9.71990561e+00],
       [ 6.62034322e-02,  1.85120381e-01, -6.84330452e-01,
         1.85120381e-01, -1.35557279e-01,  2.30180658e-01,
        -6.84330452e-01,  2.30180658e-01,  4.22256017e-02],
       [ 1.05188114e+01,  8.40963511e-01,  3.28801643e-01,
         8.40963511e-01,  1.21124485e+01, -3.22796001e+00,
         3.28801643e-01, -3.22796001e+00,  1.62578559e+01],
       [ 2.16581419e-02,  2.99265727e-03, -2.23049033e-03,
         2.99265741e-03,  3.01845398e-02, -1.23275160e-02,
        -2.23049030e-03, -1.23275159e-02,  4.34234424e-02],
       [-4.72838879e-02, -1.75364447e-01,  2.99323494e+00,
         7.62887019e-01,  2.08507833e+00,  8.46886070e+00,
        -3.19693827e+00, -1.12072348e+01, -2.04262444e+00],
       [-2.56239710e-04,  5.26105921e-04,  5.85509435e-02,
         3.40543020e-02,  9.13678963e-02,  1.33014544e-01,
        -6.11458058e-02, -2.38978797e-01, -9.35267812e-02],
       [-3.28434984e+02,  4.19377357e+01, -4.60441626e+00,
         4.19377357e+01,  6.85254107e+00,  2.83542518e+00,
        -4.60441626e+00,  2.83542518e+00,  1.80758490e-01],
       [-6.70931250e-01,  6.77922320e-02,  4.24857833e-02,
         6.77922320e-02,  2.70969344e-02, -1.15520842e-02,
         4.24857833e-02, -1.15520842e-02, -2.52176309e-03],
       [-2.39419130e+01, -1.84597760e+02,  5.49704547e+01,
        -1.84597760e+02,  1.18285485e+02, -1.54120836e+01,
         5.49704547e+01, -1.54120836e+01,  3.11188026e+00],
       [-8.80180841e-02, -4.59777779e-01,  2.17971784e-01,
        -4.59777779e-01,  3.02623378e-01, -6.37871143e-02,
         2.17971784e-01, -6.37871143e-02,  3.57089177e-03],
       [-6.74494567e+00,  5.51317939e+01, -2.45813287e+02,
         5.51317939e+01, -3.51483946e+01,  8.00061122e+01,
        -2.45813287e+02,  8.00061122e+01,  7.67098499e+00],
       [ 8.85938491e-02,  1.99732123e-01, -6.25464866e-01,
         1.99732123e-01, -1.41994993e-01,  2.06776415e-01,
        -6.25464866e-01,  2.06776415e-01,  2.72805837e-02],
       [ 1.04285715e+01,  7.77224800e-01,  1.63302984e-01,
         7.77224800e-01,  1.19848119e+01, -3.40815692e+00,
         1.63302984e-01, -3.40815692e+00,  1.56793615e+01],
       [ 2.11811686e-02,  2.88097358e-03, -2.93959146e-03,
         2.88097366e-03,  2.98541383e-02, -1.34609862e-02,
        -2.93959143e-03, -1.34609861e-02,  3.95628029e-02],
       [-2.53861572e-02, -5.00980715e-02,  2.91707879e+00,
         7.77556313e-01,  2.22137523e+00,  8.37319555e+00,
        -3.14987386e+00, -1.07904872e+01, -2.20094487e+00],
       [ 5.21989185e-04,  4.78409289e-03,  5.61867151e-02,
         3.45405541e-02,  9.60573632e-02,  1.30412170e-01,
        -6.01128622e-02, -2.23701830e-01, -9.90420296e-02],
       [-3.36258148e+02,  4.52044142e+01, -7.24818443e+00,
         4.52044142e+01,  5.59579008e+00,  3.80381041e+00,
        -7.24818443e+00,  3.80381041e+00,  9.78354399e-02],
       [-7.12062459e-01,  8.66608257e-02,  2.38016155e-02,
         8.66608257e-02,  1.92040303e-02, -4.94806687e-03,
         2.38016155e-02, -4.94806687e-03, -3.23435788e-03],
       [-2.05262619e+01, -1.87515401e+02,  5.47608472e+01,
        -1.87515401e+02,  1.19697583e+02, -1.52262381e+01,
         5.47608472e+01, -1.52262381e+01,  3.66357499e+00],
       [-6.68572548e-02, -4.75000242e-01,  2.18182603e-01,
        -4.75000242e-01,  3.09777443e-01, -6.36327592e-02,
         2.18182603e-01, -6.36327592e-02,  6.19267771e-03],
       [-1.12968137e+01,  5.55188803e+01, -2.51322861e+02,
         5.55188803e+01, -3.51400853e+01,  8.21613888e+01,
        -2.51322861e+02,  8.21613888e+01,  8.59614035e+00],
       [ 5.59009950e-02,  2.04247309e-01, -6.61019706e-01,
         2.04247309e-01, -1.43737162e-01,  2.20490366e-01,
        -6.61019706e-01,  2.20490366e-01,  3.36358794e-02],
       [ 1.06667908e+01,  6.72714786e-01,  3.00822015e-01,
         6.72714786e-01,  1.21215807e+01, -3.37596432e+00,
         3.00822015e-01, -3.37596432e+00,  1.60162586e+01],
       [ 2.24504807e-02,  2.23162087e-03, -1.93334770e-03,
         2.23162099e-03,  3.05062501e-02, -1.33279207e-02,
        -1.93334772e-03, -1.33279206e-02,  4.17007495e-02],
       [-4.99098718e-02, -1.22294817e-01,  2.92464734e+00,
         7.76678289e-01,  2.17333124e+00,  8.43481517e+00,
        -3.17654155e+00, -1.10122386e+01, -2.12732863e+00],
       [-2.15245764e-04,  2.60273481e-03,  5.59001508e-02,
         3.44795583e-02,  9.42942338e-02,  1.32349936e-01,
        -6.07728165e-02, -2.31782241e-01, -9.61740417e-02],
       [-3.41780532e+02,  4.25541300e+01, -5.24235973e+00,
         4.25541300e+01,  7.90106571e+00,  3.11977128e+00,
        -5.24235973e+00,  3.11977128e+00,  2.40616235e-01],
       [-7.37278692e-01,  6.78129629e-02,  5.03795972e-02,
         6.78129629e-02,  3.43193456e-02, -1.41197216e-02,
         5.03795972e-02, -1.41197216e-02, -2.18033994e-03],
       [-2.74680640e+01, -1.92635257e+02,  6.09973639e+01,
        -1.92635257e+02,  1.23548917e+02, -1.70044053e+01,
         6.09973639e+01, -1.70044053e+01,  3.51432929e+00],
       [-1.09924256e-01, -5.18292348e-01,  2.70055523e-01,
        -5.18292348e-01,  3.41827081e-01, -7.87550032e-02,
         2.70055523e-01, -7.87550032e-02,  3.32138749e-03],
       [-7.34377371e+00,  6.11200224e+01, -2.59265130e+02,
         6.11200224e+01, -3.89038460e+01,  8.45838087e+01,
        -2.59265130e+02,  8.45838087e+01,  8.26621440e+00],
       [ 1.05480952e-01,  2.48800954e-01, -7.20586290e-01,
         2.48800954e-01, -1.74148350e-01,  2.37974717e-01,
        -7.20586290e-01,  2.37974717e-01,  2.88628776e-02],
       [ 1.08418268e+01,  8.93799129e-01,  1.75222878e-01,
         8.93799129e-01,  1.25274473e+01, -3.77905146e+00,
         1.75222878e-01, -3.77905146e+00,  1.65363014e+01],
       [ 2.32442695e-02,  3.60605868e-03, -3.50674029e-03,
         3.60605889e-03,  3.37951318e-02, -1.67380583e-02,
        -3.50674019e-03, -1.67380580e-02,  4.56237764e-02],
       [-2.27595294e-02, -3.50486259e-02,  3.11460483e+00,
         8.83097349e-01,  2.46044209e+00,  8.77088420e+00,
        -3.32112049e+00, -1.13881724e+01, -2.44889217e+00],
       [ 1.02210286e-03,  7.24092962e-03,  6.35351055e-02,
         3.99452841e-02,  1.06569607e-01,  1.45633140e-01,
        -6.65180864e-02, -2.46522289e-01, -1.11929024e-01],
       [-3.37462066e+02,  4.40084246e+01, -7.60363708e+00,
         4.40084246e+01,  6.55386337e+00,  3.72558544e+00,
        -7.60363708e+00,  3.72558544e+00,  3.41877431e-01],
       [-7.06497364e-01,  8.05647286e-02,  2.44188774e-02,
         8.05647286e-02,  2.24918911e-02, -5.64542461e-03,
         2.44188774e-02, -5.64542461e-03, -1.98067536e-03],
       [-2.29993208e+01, -1.85409082e+02,  5.45438801e+01,
        -1.85409082e+02,  1.18600667e+02, -1.52547792e+01,
         5.45438801e+01, -1.52547792e+01,  3.53730691e+00],
       [-7.51671509e-02, -4.71045493e-01,  2.15224335e-01,
        -4.71045493e-01,  3.07128073e-01, -6.27177917e-02,
         2.15224335e-01, -6.27177917e-02,  7.07386806e-03],
       [-1.21126669e+01,  5.54646482e+01, -2.52212814e+02,
         5.54646482e+01, -3.50841459e+01,  8.22534216e+01,
        -2.52212814e+02,  8.22534216e+01,  8.93978963e+00],
       [ 5.54789207e-02,  2.01430700e-01, -6.64447758e-01,
         2.01430700e-01, -1.42436985e-01,  2.21189634e-01,
        -6.64447758e-01,  2.21189634e-01,  3.53191441e-02],
       [ 1.07039606e+01,  7.50508626e-01,  3.27265377e-01,
         7.50508626e-01,  1.20212373e+01, -3.37224675e+00,
         3.27265377e-01, -3.37224675e+00,  1.60858620e+01],
       [ 2.22708063e-02,  2.48800040e-03, -1.91035047e-03,
         2.48800053e-03,  3.03639908e-02, -1.31777342e-02,
        -1.91035050e-03, -1.31777340e-02,  4.19772117e-02],
       [-5.70138718e-02, -1.46807273e-01,  2.98231881e+00,
         7.77061592e-01,  2.18374902e+00,  8.38845222e+00,
        -3.19180226e+00, -1.10704929e+01, -2.13129119e+00],
       [-5.52309465e-04,  1.40557495e-03,  5.80546503e-02,
         3.45685214e-02,  9.44993340e-02,  1.30654998e-01,
        -6.12146386e-02, -2.33589627e-01, -9.64537791e-02],
       [-3.35811663e+02,  4.48077982e+01, -8.83666868e+00,
         4.48077982e+01,  5.74037550e+00,  4.35629553e+00,
        -8.83666868e+00,  4.35629553e+00,  7.11974030e-03],
       [-7.23782239e-01,  8.69763321e-02,  2.15556388e-02,
         8.69763321e-02,  1.98737317e-02, -3.89074353e-03,
         2.15556388e-02, -3.89074353e-03, -3.90801700e-03],
       [-2.10276557e+01, -1.86729855e+02,  5.60075207e+01,
        -1.86729855e+02,  1.19263692e+02, -1.57762958e+01,
         5.60075207e+01, -1.57762958e+01,  3.67254518e+00],
       [-7.01639456e-02, -4.81794370e-01,  2.23936916e-01,
        -4.81794370e-01,  3.14087047e-01, -6.58276592e-02,
         2.23936916e-01, -6.58276592e-02,  7.36089871e-03],
       [-1.44759957e+01,  5.72839914e+01, -2.54213267e+02,
         5.72839914e+01, -3.59690463e+01,  8.30084224e+01,
        -2.54213267e+02,  8.30084224e+01,  8.69338005e+00],
       [ 5.28003525e-02,  2.10192626e-01, -6.75479717e-01,
         2.10192626e-01, -1.47665564e-01,  2.24991364e-01,
        -6.75479717e-01,  2.24991364e-01,  3.49274422e-02],
       [ 1.06562167e+01,  6.88686144e-01,  4.02291723e-01,
         6.88686144e-01,  1.20791757e+01, -3.45357681e+00,
         4.02291723e-01, -3.45357681e+00,  1.62001808e+01],
       [ 2.28343464e-02,  2.33893420e-03, -1.83468117e-03,
         2.33893417e-03,  3.09727819e-02, -1.36653634e-02,
        -1.83468101e-03, -1.36653632e-02,  4.26227101e-02],
       [-7.13209639e-02, -1.94396543e-01,  2.93271625e+00,
         7.91609994e-01,  2.22698728e+00,  8.41233954e+00,
        -3.21769377e+00, -1.11364540e+01, -2.16226071e+00],
       [-1.02360616e-03,  2.47037838e-05,  5.67244430e-02,
         3.50947010e-02,  9.60867232e-02,  1.32083780e-01,
        -6.22200708e-02, -2.36254781e-01, -9.77674479e-02],
       [-3.42529494e+02,  4.70367179e+01, -9.38648582e+00,
         4.70367179e+01,  5.21116051e+00,  4.39205700e+00,
        -9.38648582e+00,  4.39205700e+00, -3.87598658e-01],
       [-7.40645792e-01,  1.01611327e-01,  1.06055858e-02,
         1.01611327e-01,  1.32768968e-02, -7.43377621e-04,
         1.06055858e-02, -7.43377621e-04, -5.78098716e-03],
       [-1.90398247e+01, -1.86667663e+02,  5.75767826e+01,
        -1.86667663e+02,  1.19068247e+02, -1.63007319e+01,
         5.75767826e+01, -1.63007319e+01,  3.27329012e+00],
       [-4.86623549e-02, -4.81071972e-01,  2.36543560e-01,
        -4.81071972e-01,  3.12370502e-01, -6.99162230e-02,
         2.36543560e-01, -6.99162230e-02,  4.22296001e-03],
       [-1.48388372e+01,  5.90290507e+01, -2.48894857e+02,
         5.90290507e+01, -3.67095707e+01,  8.09778893e+01,
        -2.48894857e+02,  8.09778893e+01,  7.13520122e+00],
       [ 3.47392177e-02,  2.26318264e-01, -6.43566486e-01,
         2.26318264e-01, -1.52524731e-01,  2.12255925e-01,
        -6.43566486e-01,  2.12255925e-01,  2.44561270e-02],
       [ 1.08602392e+01,  6.28349626e-01,  4.09212057e-01,
         6.28349626e-01,  1.20533287e+01, -3.55242346e+00,
         4.09212057e-01, -3.55242346e+00,  1.58335248e+01],
       [ 2.33440641e-02,  1.67300325e-03, -1.28187238e-03,
         1.67300327e-03,  3.06781741e-02, -1.44131171e-02,
        -1.28187240e-03, -1.44131168e-02,  4.04025375e-02],
       [-8.05068243e-02, -1.67628990e-01,  2.94469380e+00,
         8.00107301e-01,  2.29010187e+00,  8.38150592e+00,
        -3.18720589e+00, -1.08616663e+01, -2.21450013e+00],
       [-1.37288118e-03,  7.81957999e-04,  5.66766972e-02,
         3.51954546e-02,  9.81063596e-02,  1.30865511e-01,
        -6.14372530e-02, -2.26012782e-01, -9.91659689e-02],
       [-3.45553273e+02,  4.66219447e+01, -1.20232777e+01,
         4.66219447e+01,  5.67785064e+00,  5.42349937e+00,
        -1.20232777e+01,  5.42349937e+00,  8.39287388e-02],
       [-7.57763552e-01,  1.03419537e-01, -1.77162209e-03,
         1.03419537e-01,  1.31316623e-02,  3.83547531e-03,
        -1.77162209e-03,  3.83547531e-03, -3.89670361e-03],
       [-2.09339460e+01, -1.88436007e+02,  5.50511342e+01,
        -1.88436007e+02,  1.20209278e+02, -1.52277056e+01,
         5.50511342e+01, -1.52277056e+01,  4.04137429e+00],
       [-5.06906713e-02, -4.86934356e-01,  2.21100638e-01,
        -4.86934356e-01,  3.14985069e-01, -6.43966474e-02,
         2.21100638e-01, -6.43966474e-02,  8.83918787e-03],
       [-2.01995817e+01,  5.71141766e+01, -2.57616218e+02,
         5.71141766e+01, -3.53501235e+01,  8.44248053e+01,
        -2.57616218e+02,  8.44248053e+01,  9.15845574e+00],
       [ 1.01190912e-02,  2.13438732e-01, -7.02783182e-01,
         2.13438732e-01, -1.46929046e-01,  2.35707999e-01,
        -7.02783182e-01,  2.35707999e-01,  3.90162060e-02],
       [ 1.09549222e+01,  6.89044709e-01,  5.78729442e-01,
         6.89044709e-01,  1.21814745e+01, -3.37692920e+00,
         5.78729442e-01, -3.37692920e+00,  1.64129385e+01],
       [ 2.38757288e-02,  1.73755203e-03, -5.05693738e-04,
         1.73755206e-03,  3.10346420e-02, -1.33582711e-02,
        -5.05693673e-04, -1.33582710e-02,  4.42662014e-02],
       [-1.03109731e-01, -2.94177714e-01,  3.02047486e+00,
         7.85981995e-01,  2.15623099e+00,  8.47635802e+00,
        -3.23464811e+00, -1.12776784e+01, -2.05725599e+00],
       [-2.17765512e-03, -3.52570830e-03,  5.90286545e-02,
         3.47295838e-02,  9.35359880e-02,  1.33436565e-01,
        -6.24805823e-02, -2.41209796e-01, -9.37020799e-02]])
        gradient_data = np.array([[-1.0000e-06,  0.0000e+00, -1.0000e-06],
       [-0.0000e+00, -0.0000e+00, -0.0000e+00],
       [ 1.0000e-06, -0.0000e+00,  1.0000e-06],
       [-0.0000e+00,  0.0000e+00,  1.0000e-06],
       [ 2.2600e-04,  1.3700e-04,  1.7900e-04],
       [-2.6900e-04, -8.5000e-05, -1.5100e-04],
       [-1.8800e-04, -1.0600e-04, -1.8000e-04],
       [ 2.3200e-04,  5.4000e-05,  1.5200e-04],
       [-5.0740e-03, -1.2210e-02,  1.4884e-02],
       [ 4.7030e-03,  1.2658e-02, -1.4632e-02],
       [ 5.6000e-05, -2.9700e-04, -1.8800e-04],
       [ 3.1500e-04, -1.5200e-04, -6.4000e-05],
       [-1.6720e-03, -4.0000e-04,  2.4130e-03],
       [ 1.8900e-04, -2.8410e-03,  6.6100e-04],
       [ 7.2900e-04,  1.4690e-03, -1.6830e-03],
       [ 7.5500e-04,  1.7720e-03, -1.3910e-03],
       [ 2.7620e-03,  7.0500e-04,  1.8800e-03],
       [-2.3450e-03, -1.2090e-03, -2.1700e-03],
       [-1.0820e-03, -1.6010e-03,  2.1310e-03],
       [ 6.6600e-04,  2.1040e-03, -1.8410e-03],
       [-1.5810e-02,  3.2290e-03, -6.2560e-03],
       [-5.7160e-03, -1.0003e-02, -1.4238e-02],
       [ 1.5754e-02, -3.1280e-03,  6.3540e-03],
       [ 5.7720e-03,  9.9010e-03,  1.4140e-02],
       [-1.9610e-02,  4.0620e-03, -8.5710e-03],
       [ 5.6810e-03,  9.0710e-03,  1.4137e-02],
       [ 1.9494e-02, -3.7000e-03,  7.7980e-03],
       [-5.5640e-03, -9.4330e-03, -1.3364e-02],
       [ 1.9500e-04, -2.3300e-04, -1.0000e-06],
       [ 1.2900e-04, -1.6100e-04, -2.2500e-04],
       [-2.2400e-04,  1.8700e-04,  4.0000e-05],
       [-1.0100e-04,  2.0700e-04,  1.8600e-04],
       [ 4.5050e-03,  9.7860e-03, -1.1756e-02],
       [-3.9920e-03, -1.0409e-02,  1.1400e-02],
       [-3.9900e-04,  2.3000e-04,  1.1200e-04],
       [-1.1300e-04,  3.9300e-04,  2.4500e-04],
       [ 1.9660e-03,  2.2800e-04, -2.1490e-03],
       [-2.6500e-04,  2.7460e-03, -1.0770e-03],
       [-1.0470e-03, -1.4150e-03,  1.5920e-03],
       [-6.5400e-04, -1.5600e-03,  1.6340e-03],
       [-2.5480e-03, -8.4500e-04, -1.6040e-03],
       [ 2.2610e-03,  1.1890e-03,  1.7990e-03],
       [ 8.3900e-04,  1.6110e-03, -2.2230e-03],
       [-5.5200e-04, -1.9550e-03,  2.0270e-03],
       [ 1.3937e-02, -2.7650e-03,  5.4090e-03],
       [ 6.6440e-03,  1.1594e-02,  1.6743e-02],
       [-1.3851e-02,  2.7270e-03, -5.5690e-03],
       [-6.7300e-03, -1.1555e-02, -1.6582e-02],
       [ 1.6818e-02, -3.3950e-03,  7.3190e-03],
       [-5.0670e-03, -8.0200e-03, -1.2399e-02],
       [-1.6663e-02,  3.1060e-03, -6.6220e-03],
       [ 4.9130e-03,  8.3090e-03,  1.1702e-02]])
        delta_data = np.array([[0.05671023, 0.        ],
       [0.05960412, 1.        ],
       [0.05672138, 2.        ],
       [0.05669342, 3.        ],
       [0.05189421, 4.        ],
       [0.05188801, 5.        ]])
        rmass_data = np.array([ 1.08264229, 14.5069513 ,  1.0996286 ,  1.08476642,  1.0675996 ,
        1.07009031])
        scatter_data = np.array([[ 3.47311779e+02,  0.00000000e+00, -3.27390198e+02,
                                  -8.44921542e+01, -4.22102267e-02, -3.41332079e-02,
                                  -3.91676006e-03,  5.14500000e+02],
                                 [ 8.60534577e+02,  1.00000000e+00,  1.75268228e+02,
                                  -8.09603043e+00, -8.26286589e+00,  1.65666769e-02,
                                  -3.01543530e-03,  5.14500000e+02],
                                 [ 1.24319010e+03,  2.00000000e+00, -3.35605422e+02,
                                  -7.26516978e+01,  1.06370293e-06, -3.45429748e-02,
                                  -4.20725882e-03,  5.14500000e+02],
                                 [ 1.37182002e+03,  3.00000000e+00,  2.20210484e+02,
                                   5.78999940e+01, -4.46257676e+00,  2.29930063e-02,
                                  -6.16087427e-04,  5.14500000e+02],
                                 [ 3.59750268e+03,  4.00000000e+00, -3.50819253e+03,
                                  -3.90826518e+02,  5.90325028e-02, -3.49292932e-01,
                                  -4.98353528e-02,  5.14500000e+02],
                                 [ 3.59821746e+03,  5.00000000e+00,  5.05236006e+03,
                                   4.00023286e+02,  6.60389814e+00,  4.97827311e-01,
                                   7.91921951e-02,  5.14500000e+02]])
        raman_data = np.array([[3.47311779e+02, 0.00000000e+00, 3.42307581e-05, 6.38955258e-01,
                                2.04527298e+01, 5.14500000e+02],
                               [8.60534577e+02, 1.00000000e+00, 1.90190339e-01, 1.07090867e+00,
                                6.85033386e+01, 5.14500000e+02],
                               [1.24319010e+03, 2.00000000e+00, 1.27606294e-08, 3.46909710e-01,
                                1.11011130e+01, 5.14500000e+02],
                               [1.37182002e+03, 3.00000000e+00, 3.94139588e-02, 1.19286864e+00,
                                4.52663091e+01, 5.14500000e+02],
                               [3.59750268e+03, 4.00000000e+00, 1.52822910e-02, 6.21166773e+00,
                                2.01524180e+02, 5.14500000e+02],
                               [3.59821746e+03, 5.00000000e+00, 1.60412161e+00, 5.19841596e+00,
                                4.55091201e+02, 5.14500000e+02]])
        scatter_data = scatter_data.T
        raman_data = raman_data.T
        print(va_corr.scatter.to_string())
        print(va_corr.roa.to_string())
        roa_cols = ['xx','xy','xz','yx','yy','yz','zx','zy','zz']
        gradient_cols = ['fx','fy','fz']
        # test all columns of the respective dataframe to get a better sense of what is broken
        self.assertTrue(np.allclose(va_corr.roa[roa_cols].values, roa_data))
        self.assertTrue(np.allclose(va_corr.gradient[gradient_cols].values, gradient_data))
        self.assertTrue(np.allclose(delta.values, delta_data))
        self.assertTrue(np.allclose(self.h2o2_freq.frequency_ext['r_mass'].values, rmass_data))

        self.assertTrue(np.allclose(va_corr.scatter['freq'].values,           scatter_data[0]))
        self.assertTrue(np.allclose(va_corr.scatter['freqdx'].values,         scatter_data[1]))
        self.assertTrue(np.allclose(va_corr.scatter['beta_g*1e6'].values,     scatter_data[2]))
        self.assertTrue(np.allclose(va_corr.scatter['beta_A*1e6'].values,     scatter_data[3]))
        self.assertTrue(np.allclose(va_corr.scatter['alpha_g*1e6'].values,    scatter_data[4]))
        self.assertTrue(np.allclose(va_corr.scatter['backscatter'].values,    scatter_data[5]))
        self.assertTrue(np.allclose(va_corr.scatter['forwardscatter'].values, scatter_data[6]))
        self.assertTrue(np.allclose(va_corr.scatter['exc_freq'].values,       scatter_data[7]))

        self.assertTrue(np.allclose(va_corr.raman['freq'].values,          raman_data[0]))
        self.assertTrue(np.allclose(va_corr.raman['freqdx'].values,        raman_data[1]))
        self.assertTrue(np.allclose(va_corr.raman['alpha_squared'].values, raman_data[2]))
        self.assertTrue(np.allclose(va_corr.raman['beta_alpha'].values,    raman_data[3]))
        self.assertTrue(np.allclose(va_corr.raman['raman_int'].values,     raman_data[4]))
        self.assertTrue(np.allclose(va_corr.raman['exc_freq'].values,      raman_data[5]))

    def test_select_freq(self):
        self.methyloxirane_freq.parse_frequency()
        self.methyloxirane_freq.parse_frequency_ext()
        delta = gen_delta(delta_type=2, freq=self.methyloxirane_freq.frequency.copy())
        va_corr = VA()
        path = sep.join(resource('va-roa-methyloxirane-def2tzvp-488.9-00.out').split(sep)[:-1])+sep+'*'
        va_corr.roa = get_data(path=path, attr='roa', soft=Output, 
                               f_start='va-roa-methyloxirane-def2tzvp-488.9-', f_end='.out')
        va_corr.roa['exc_freq'] = np.tile(488.9, len(va_corr.roa))
        va_corr.gradient = get_data(path=path, attr='gradient', soft=Output, 
                                    f_start='va-roa-methyloxirane-def2tzvp-488.9-', f_end='.out')
        va_corr.gradient['exc_freq'] = np.tile(488.9, len(va_corr.gradient))
        va_corr.vroa(uni=self.methyloxirane_freq, delta=delta['delta'].values)
        scatter_data = np.array([[ 1.12639199e+03,  1.00000000e+01, -6.15736884e+01,
                                  -1.53103521e+01, -1.68892383e-01, -6.40100535e-03,
                                  -8.61815897e-04,  4.88900000e+02],
                                 [ 1.15100631e+03,  1.10000000e+01, -1.06898371e+02,
                                  -2.76794343e+01,  3.53857297e+00, -1.11479855e-02,
                                   1.28026956e-03,  4.88900000e+02],
                                 [ 1.24937064e+03,  1.20000000e+01,  5.23431984e+01,
                                   5.17874012e+00, -8.24615516e+00,  5.19066673e-03,
                                  -5.18260038e-03,  4.88900000e+02],
                                 [ 1.37094149e+03,  1.30000000e+01,  3.49746537e+01,
                                  -9.43653998e+00, -8.72689935e-02,  3.05559747e-03,
                                   6.47745423e-04,  4.88900000e+02],
                                 [ 1.39064221e+03,  1.40000000e+01, -5.31532967e+01,
                                  -5.65151249e+00, -6.11336634e+00, -5.28356488e-03,
                                  -5.16165231e-03,  4.88900000e+02],
                                 [ 1.44754882e+03,  1.50000000e+01, -1.25064010e+02,
                                  -2.49033712e+01, -8.12931706e-02, -1.28030529e-02,
                                  -1.66110131e-03,  4.88900000e+02]])
        raman_data = np.array([[1.12639199e+03, 1.00000000e+01, 3.61528920e-04, 5.94192417e-01,
                                1.90792325e+01, 4.88900000e+02],
                               [1.15100631e+03, 1.10000000e+01, 3.36862711e-02, 1.62723253e-01,
                                1.12706729e+01, 4.88900000e+02],
                               [1.24937064e+03, 1.20000000e+01, 3.10356963e-01, 1.61670230e+00,
                                1.07598727e+02, 4.88900000e+02],
                               [1.37094149e+03, 1.30000000e+01, 6.63217766e-03, 2.37302109e-01,
                                8.78745947e+00, 4.88900000e+02],
                               [1.39064221e+03, 1.40000000e+01, 6.30361373e-02, 8.04145907e-01,
                                3.70791737e+01, 4.88900000e+02],
                               [1.44754882e+03, 1.50000000e+01, 5.36564516e-05, 1.07944901e+00,
                                3.45520265e+01, 4.88900000e+02]])
        scatter_data = scatter_data.T
        raman_data = raman_data.T

        # test all columns of the respective dataframe to get a better sense of what is broken
        self.assertTrue(np.allclose(va_corr.scatter['freq'].values,           scatter_data[0]))
        self.assertTrue(np.allclose(va_corr.scatter['freqdx'].values,         scatter_data[1]))
        self.assertTrue(np.allclose(va_corr.scatter['beta_g*1e6'].values,     scatter_data[2]))
        self.assertTrue(np.allclose(va_corr.scatter['beta_A*1e6'].values,     scatter_data[3]))
        self.assertTrue(np.allclose(va_corr.scatter['alpha_g*1e6'].values,    scatter_data[4]))
        self.assertTrue(np.allclose(va_corr.scatter['backscatter'].values,    scatter_data[5]))
        self.assertTrue(np.allclose(va_corr.scatter['forwardscatter'].values, scatter_data[6]))
        self.assertTrue(np.allclose(va_corr.scatter['exc_freq'].values,       scatter_data[7]))

        self.assertTrue(np.allclose(va_corr.raman['freq'].values,          raman_data[0]))
        self.assertTrue(np.allclose(va_corr.raman['freqdx'].values,        raman_data[1]))
        self.assertTrue(np.allclose(va_corr.raman['alpha_squared'].values, raman_data[2]))
        self.assertTrue(np.allclose(va_corr.raman['beta_alpha'].values,    raman_data[3]))
        self.assertTrue(np.allclose(va_corr.raman['raman_int'].values,     raman_data[4]))
        self.assertTrue(np.allclose(va_corr.raman['exc_freq'].values,      raman_data[5]))

