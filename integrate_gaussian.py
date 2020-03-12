
import scipy.integrate as integrate
import numpy as np


def parse_basisfile(basisfile):
    widthO = []
    widthH = []
    readnextline = False
    with open(basisfile,'r') as f:
        for line in f.readlines():
            if line.strip():
                tag = line.split()[0]
                if readnextline:
                    scinotation = line.split()[0].replace("D", "E")
                    if (mode == 'O'):
                        widthO.append([float(scinotation), orbital_type])
                    if (mode == 'H'):
                        widthH.append([float(scinotation), orbital_type])
                    readnextline = False
                if (tag == 'S') or (tag == 'SP'):
                    readnextline = True
                    orbital_type = tag
                if (tag == 'O'):
                    mode = 'O'
                if (tag == 'H'):
                    mode = 'H'
    return widthO, widthH


def integrate_yo_stuff(basis,coeffs):
    total = 0.0
    wO, wH = basis
    widths = []
    for a in coeffs:
        # based on the number of S orbitals (assumes a2 basis)
        if len(a) == 8:
            widths.append(wO)
        elif len(a) == 4:
            widths.append(wH)
    for i, atom in enumerate(widths):
        for j, value in enumerate(atom):
            w = value[0]
            orbital_type = value[1]
            c = coeffs[i][j]

            ## not necessary. there are no 2s GTOs!
            #if orbital_type == 'S':
            #    integrand = lambda r:gaussian(c,w)(r)*r**2
            #elif orbital_type == 'SP':
            #    integrand = lambda r:gaussian(c,w)(r)*r**4

            #integrand = lambda r:gaussian(c,w)(r)*r**2
            #integral, error = integrate.quad(integrand,0.0,np.inf)
            
            # integral(r^2*exp(-ar^2)) = 1/(4w) * sqrt(pi/w)
            
            normalization = (2*w/(np.pi))**(0.75)
            integral = c*normalization*(1/(4*w))*np.sqrt(np.pi/w)
            
            # not needed, y00 = 1
            #y00 = 0.5*np.sqrt(1/np.pi)
            #solidharmonic = np.sqrt(4*np.pi)
            
            space = 4*np.pi
            num_ele = integral*space
            total += num_ele
            #print (j,num_ele)
        #print (total)
    return total