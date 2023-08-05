#!/usr/bin/env python3
#
# GlobalChemExtensions - ZMatrix Store

# ------------------------------------

class ZMatrixStore(object):

    '''

    A ZMatrix Store that will house molecules for people to keep downloading if they need it. Will put here in extensions
    to allow for the any conversions later on.

    '''

    __MOLECULES__ = [
        'water',
        'benzene',
    ]

    __DIMERS__ = {
        'benzene-benzene': {
            'ADT': 1, # Aromatic Ring T-Shaped
            'ADP': 2  # Aromatic Ring P-Shaped
        },
        'water-water': {
        }

    }

    def __init__(self):

        self.store = {}
        self.build_coordinate_store()

    def get_molecule(self, molecule):

        '''

        Fetch the Molecule

        '''

        if molecule not in self.__MOLECULES__:
            return None
        else:
            return self.store[molecule]

    def build_zmatrix_store(self):

        '''

        Builds the ZMatrix Store

        '''

        water = """\
        O
        H 1 1.08
        H 1 1.08 2 107.5
        """

        benzene = """\
        H
        C 1 a2bd
        C 2 a3bd 1 a3angle
        C 3 a4bd 2 a4angle 1 a4dihedral
        H 4 a5bd 3 a5angle 2 a5dihedral
        C 4 a6bd 3 a6angle 2 a6dihedral
        H 6 a7bd 4 a7angle 3 a7dihedral
        C 6 a8bd 4 a8angle 3 a8dihedral
        H 8 a9bd 6 a9angle 4 a9dihedral
        C 2 a10bd 3 a10angle 4 a10dihedral
        H 10 a11bd 2 a11angle 1 a11dihedral
        H 3 a12bd 2 a12angle 1 a12dihedral
        a2bd = 1.0853
        a3bd = 1.3800
        a4bd = 1.3787
        a5bd = 1.0816
        a6bd = 1.3795
        a7bd = 1.0844
        a8bd = 1.3872
        a9bd = 1.0847
        a10bd = 1.3812
        a11bd = 1.0838
        a12bd = 1.0818
        a3angle = 119.8001
        a4angle = 121.2010
        a5angle = 121.0431
        a6angle = 121.7007
        a7angle = 122.4276
        a8angle = 116.6791
        a9angle = 118.3291
        a10angle = 117.8148
        a11angle = 117.3613
        a12angle = 117.2942
        a4dihedral = -180
        a5dihedral = -180
        a6dihedral = 0
        a7dihedral = 180
        a8dihedral = 0
        a9dihedral = 180
        a10dihedral = 0
        a11dihedral = 0
        a12dihedral = 0
        """

        molecules = [
            water,
            benzene,
        ]


        for i, molecule in enumerate(molecules):

            self.store[self.__MOLECULES__[i]] = molecule

    def get_dimer_zmatrix(self):

        benzene_benzene_adt = """\
        H
        C 1 a2bd
        C 2 a3bd 1 a3angle
        C 3 a4bd 2 a4angle 1 a4dihedral
        H 4 a5bd 3 a5angle 2 a5dihedral
        C 4 a6bd 3 a6angle 2 a6dihedral
        H 6 a7bd 4 a7angle 3 a7dihedral
        C 6 a8bd 4 a8angle 3 a8dihedral
        H 8 a9bd 6 a9angle 4 a9dihedral
        C 2 a10bd 3 a10angle 4 a10dihedral
        H 10 a11bd 2 a11angle 1 a11dihedral
        H 3 a12bd 2 a12angle 1 a12dihedral
        X1 1 a13bd 2 a13angle 3 a13dihedral
        X2 13 a14bd 1 a14angle 2 a14dihedral
        H 14 a15bd 13 a15angle 12 a15dihedral
        C 15 a16bd 14 a16angle 13 a16dihedral
        C 16 a17bd 15 a17angle 14 a17dihedral
        C 17 a18bd 16 a18angle 15 a18dihedral
        H 18 a19bd 17 a19angle 16 a19dihedral
        C 18 a20bd 17 a20angle 16 a20dihedral
        H 20 a21bd 18 a21angle 17 a21dihedral
        C 20 a22bd 18 a22angle 17 a22dihedral
        H 22 a23bd 20 a23angle 18 a23dihedral
        C 16 a24bd 17 a24angle 18 a24dihedral
        H 24 a25bd 16 a25angle 15 a25dihedral
        2a2bd = 1.0853
        a3bd = 1.3800
        a4bd = 1.3787
        a5bd = 1.0816
        a6bd = 1.3795
        a7bd = 1.0844
        a8bd = 1.3872
        a9bd = 1.0847
        a10bd = 1.3812
        a11bd = 1.0838
        a12bd = 1.0818
        a13bd = 2.4944
        a14bd = 2.5
        a15bd = 0.8399
        a16bd = 1.1009
        a17bd = 1.3849
        a18bd = 1.3870
        a19bd = 1.0919
        a20bd = 1.3801
        a21bd = 1.0937
        a22bd = 1.3828
        a23bd = 1.0942
        a24bd = 1.3842
        a25bd = 1.0750
        a26bd = 1.0824
        a3angle = 119.8001
        a4angle = 121.2010
        a5angle = 121.0431
        a6angle = 121.7007
        a7angle = 122.4276
        a8angle = 116.6791
        a9angle = 118.3291
        a10angle = 117.8148
        a11angle = 117.3613
        a12angle = 117.2942
        a13angle = 0.8682
        a14angle = 90
        a15angle = 180
        a16angle = 180.0
        a17angle = 118.5310
        a18angle = 119.0903
        a19angle = 118.7242
        a20angle = 119.3608
        a21angle = 120.5722
        a22angle = 122.2840
        a23angle = 119.5657
        a24angle = 120.0003
        a25angle = 119.8988
        a26angle = 117.7874
        a4dihedral = -180
        a5dihedral = -180
        a6dihedral = 0
        a7dihedral = 180
        a8dihedral = 0
        a9dihedral = 180
        a10dihedral = 0
        a11dihedral = 0
        a12dihedral = 0
        a13dihedral = 0
        a14dihedral = 90
        a15dihedral = 90
        a16dihedral = 90
        a17dihedral = 180
        a18dihedral = 180
        a19dihedral = -180
        a20dihedral = 0
        a21dihedral = -180
        a22dihedral = 0
        a23dihedral = 180
        a24dihedral = 0
        a25dihedral = 0
        a26dihedral = 0
        """

    def get_store(self):

        '''

        Returns the ZMatrix Store

        '''

        return self.store