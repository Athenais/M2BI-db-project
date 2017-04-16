#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################
# DESCRIPTION
######################################

# Ramachandran Module
# Coded by Jean-Charles Carvaillo
# carvaillojeancharles@gmail.com
# Master 2 Bioinformatics
# Copyright 2017, Jean-Charles Carvaillo, All rights reserved.

######################################
# CITATION
######################################

# Package Numpy:
# Stéfan van der Walt, S. Chris Colbert and Gaël Varoquaux.
# The NumPy Array: A Structure for Efficient Numerical Computation, Computing
# in Science & Engineering, Vol. 13. (2011), pp. 22-30,
# DOI:10.1109/MCSE.2011.37

# Package Matplotib:
# J.D. Hunter. Matplotlib: A 2D Graphics Environment,
# Computing in Science & Engineering, Vol. 9, No. 3. (2007), pp. 90-95

# Package Mdtraj:
# Robert T. McGibbon, Kyle A. Beauchamp, Matthew P. Harrigan,
# Christoph Klein, Jason M. Swails, Carlos X. Hernández,
# Christian R. Schwantes, Lee-Ping Wang, Thomas J. Lane, Vijay S. Pande.
# MDTraj: A Modern Open Library for the Analysis of Molecular Dynamics
# Trajectories, Biophysical Journal, Vol. 109, No. 8. (2015), pp. 1528-1532


######################################
# IMPORT
######################################

from app import db
import glob
import numpy as np
import matplotlib.pyplot as plt
import model
import os
from sqlalchemy import or_, and_, func
import sys

######################################
# FUNCTION
######################################


def compute_ramachandran_map(pdb_id, unit="radian"):
    """Method to generate a ramachandran map with a given unit scale
        (radian or degree).

        Arguments:
            pdb_id : id of the pdb in the database
            angles: tuple which contains

        Returns:
            path of Ramachandran map computed

    """
    path = []
    methods =  db.session.query(model.Annotation.method).group_by(model.Annotation.method).all()
    for method in methods:
        # get annotation
        annotation = db.session.query(model.Annotation.result).filter(and_(model.Annotation.pdb_id==pdb_id,
                                                                           model.Annotation.method==method.method))
        print(annotation.scalar())
        # get angles
        angles = db.session.query(model.Angle).filter(model.Angle.pdb_id==pdb_id)
        print(len(angles.all()))
        x = [angles[i].phi for i in range(1,len(angles.all())-2)]
        y = [angles[i].psi for i in range(1,len(angles.all())-2)]
        if unit == "degree":
            # conserve and convert radian angle to degree
            x = np.rad2deg(x)
            y = np.rad2deg(y)
            x_label_in = "Phi(deg)"
            y_label_in = "Psi(deg)"
            plt.plot(x, y, ".")
            # Sets x axis limits
            plt.xlim(-180, 180)
            # Sets y axis limits
            plt.ylim(-180, 180)
            # Sets ticks markers for x axis
            plt.xticks(np.arange(-180.1, 180.1, 30))
            # Sets ticks makers for y axis
            plt.yticks(np.arange(-180.1, 180.1, 30))
            # Adds x axis label
            plt.xlabel(x_label_in)
            # Adds y axis label
            plt.ylabel(y_label_in)
            plt.arrow(-180, 0, 360, 0)
            plt.arrow(0, -180, 0, 360)

        elif unit == "radian":
            x_label_in = "Phi(rad)"
            y_label_in = "Psi(rad)"
            plt.plot(x, y, ".")
            # Sets x axis limits
            plt.xlim(-3.14, 3.14)
            # Sets y axis limits
            plt.ylim(-3.14, 3.14)
            # Sets ticks markers for x axis
            plt.xticks(np.arange(-3, 3.5, 0.5))
            # Sets ticks makers for y axis
            plt.yticks(np.arange(-3, 3.5, 0.5))
            # Adds x axis label
            plt.xlabel(x_label_in)
            # Adds y axis label
            plt.ylabel(y_label_in)
            plt.arrow(-np.pi, 0, 2*np.pi, 0)
            plt.arrow(0, -np.pi, 0, 2*np.pi)

        # Create a file for plot
        # Creates a figure
        fig = plt.gcf()
        # Changes figure size
        fig.set_size_inches(10.0, 10.0)
        # Saves figures

        if not os.path.exists('temp'):
            os.mkdir('temp')

        fig.savefig('temp/' + pdb_id + '_' + method.method + '.png', dpi=300)
        path.append('temp/' + pdb_id + '_' + method.method + '.png')

    return path

  
if __name__ == "__main__":
    pdb_file = sys.argv[1]
    if len(sys.argv) > 2:
        angle_unit = sys.argv[2]
        if angle_unit not in ["degree", "radian"]:
            sys.exit("you need to specify for the angle unit 'degree'" +
                     " or 'radian'\n")
    else:
        angle_unit = "radian"
    try:
        pdb_id = pdb_file[-8:-4]
        print(pdb_id)
    except:
        sys.exit("the specified file is not openable or not" +
                 " a pdb file or just not specified\n")
    path_map = compute_ramachandran_map(pdb_id, angle_unit)
    print(path_map)
