import random

from integrate_gaussian import parse_basisfile
from integrate_gaussian import integrate_yo_stuff


def testnumelectrons(net,n_dimers,basisset,dataset_onehot,dataset_geom,dataset_typemap,coeff_by_type):
    print('\nNow testing number of electrons on {0} randomly selected dimers'.format(n_dimers))

    basisfuncs = parse_basisfile(basisset)
    for i in range(n_dimers):
        j = random.randint(3000, len(dataset_geom) - 1)
        onehot = dataset_onehot[j]
        points = dataset_geom[j]
        atom_type_map = dataset_typemap[j]
        outputO, outputH = net(onehot.to('cuda'),points.to('cuda'),atom_type_map)
        outputO = outputO.squeeze().tolist()
        outputH = outputH.squeeze().tolist()
        newoutputO = []
        for item in outputO:
            newitem = item[:8]
            newoutputO.append(newitem)
        newoutputH = []
        for item in outputH:
            newitem = item[:4]
            newoutputH.append(newitem)
        newoutputO.extend(newoutputH)
        ml_coeffs = newoutputO

        #with open('ml_coeffs_' + str(i) + '_.dat','wb') as f:
        #    pickle.dump(ml_coeffs, f)

        coeffs = coeff_by_type[j]
        s_coeffs = []
        for atom in coeffs:
            atom_s_coeffs = []
            for shell in atom:
                if len(shell) == 1:
                    atom_s_coeffs.append(shell[0])
            s_coeffs.append(atom_s_coeffs)

        #with open('real_coeffs_' + str(i) + '_.dat','wb') as f:
        #    pickle.dump(s_coeffs, f)

        true_tot = integrate_yo_stuff(basisfuncs,s_coeffs)
        ml_tot = integrate_yo_stuff(basisfuncs,ml_coeffs)

        print('\nNumber of electrons for structure {0}:'.format(j))
        print('   True: {0}'.format(true_tot*2))
        print('     ML: {0}'.format(ml_tot*2))
