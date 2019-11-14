import numpy as np
import torch
import utils
import se3cnn.SO3

__authors__  = "Tess E. Smidt, Mario Geiger"

torch.set_default_dtype(torch.float64)

def direct_sum(*matrices):
    # Slight modification of se3cnn.SO3.direct_sum
    """
    Direct sum of matrices, put them in the diagonal
    """

    front_indices = matrices[0].shape[:-2]
    m = sum(x.size(-2) for x in matrices)
    n = sum(x.size(-1) for x in matrices)
    total_shape = list(front_indices) + [m, n]
    out = matrices[0].new_zeros(*total_shape)
    i, j = 0, 0
    for x in matrices:
        m, n = x.shape[-2:]
        out[..., i: i + m, j: j + n] = x 
        i += m
        j += n
    return out 


def adjusted_projection(vectors, L_max, sum_points=True, radius=True):
    radii = vectors.norm(2, -1)
    vectors = vectors[radii > 0.]

    if radius:
        radii = radii[radii > 0.]
    else:
        radii = torch.ones_like(radii[radii > 0.])

    angles = se3cnn.SO3.xyz_to_angles(vectors)
    coeff = se3cnn.SO3.spherical_harmonics_dirac(L_max, *angles)
    coeff *= radii.unsqueeze(-2)
    
    A = torch.einsum("ia,ib->ab", (se3cnn.SO3.spherical_harmonics(list(range(L_max + 1)), *angles), coeff))
    try:
        coeff *= torch.lstsq(radii, A).solution.view(-1)
    except:
        coeff *= torch.gels(radii, A).solution.view(-1)
    return coeff.sum(-1) if sum_points else coeff


class SphericalTensor():
    def __init__(self, signal, Rs):
        self.signal = signal
        self.Rs = Rs
    
    @classmethod
    def from_geometry(cls, vectors, L_max, sum_points=True, radius=True):
        Rs = [(1, L) for L in range(L_max + 1)]
        signal = adjusted_projection(vectors, L_max, sum_points=sum_points, radius=radius)
        return cls(signal, Rs)

    @classmethod
    def from_decorated_geometry(cls, vectors, features, L_max,
                                features_Rs=None, sum_points=True,
                                radius=True):
        Rs = [(1, L) for L in range(L_max + 1)]
        # [Rs, points]
        geo_signal = adjusted_projection(coords, L_max, sum_points=False, radius=radius)
        # Keep Rs index for geometry and features
        new_signal = torch.einsum('gp,pf->fg', (geo_signal, features))
        new_signal = cls(new_signal, Rs)
        new_signal.feature_Rs = features_Rs
        return new_signal

    def sph_norm(self):
        Rs = self.Rs
        signal = self.signal
        n_mul = sum([mul for mul, L in Rs])
        # Keep shape after Rs the same
        norms = torch.zeros(n_mul, *signal.shape[1:])
        sig_index = 0
        norm_index = 0
        for mul, L in Rs:
            for m in range(mul):
                norms[norm_index] = signal[sig_index: sig_index +
                                           (2 * L + 1)].norm(2, 0)
                norm_index += 1
                sig_index += 2 * L + 1
        return norms

    def signal_on_sphere(self, which_mul=None, n=100, radius=True):
        n_mul = sum([mul for mul, L in self.Rs])
        if which_mul:
            if len(which_mul) != n_mul:
                raise ValueError("which_mul and number of multiplicities is " +
                                 "not equal.")
        else:
            which_mul = [1 for i in range(n_mul)]

        # Need to handle if signal is featurized
        x, y, z = (None, None, None)
        Ys = []
        for mul, L in self.Rs:
            # Using cache-able function
            x, y, z, Y = utils.spherical_harmonics_on_grid(L, n)
            Ys += [Y] * mul

        f = self.signal.unsqueeze(1).unsqueeze(2) * torch.cat(Ys, dim=0)
        f = f.sum(0)
        return x, y, z, f

    def plot(self, which_mul=None, n=100, radius=True, center=None, relu=True):
        """
        surface = self.plot()
        fig = go.Figure(data=[surface])
        fig.show()
        """
        import plotly.graph_objs as go

        x, y, z, f = self.signal_on_sphere(which_mul, n, radius)
        f = f.relu() if relu else f

        if radius:
            r = f.abs()
            x = x * r
            y = y * r
            z = z * r

        if center is not None:
            x = x + center[0]
            y = y + center[1]
            z = z + center[2]

        return go.Surface(x=x.numpy(), y=y.numpy(), z=z.numpy(), surfacecolor=f.numpy())

    def wigner_D_on_grid(self, n):
        try:
            return getattr(self, "wigner_D_grid_{}".format(n))
        except:
            blocks = [utils.wigner_D_on_grid(L, n)
                      for mul, L in self.Rs for m in range(mul)]
            wigner_D = direct_sum(*blocks)
            setattr(self, "wigner_D_grid_{}".format(n), wigner_D)
            return getattr(self, "wigner_D_grid_{}".format(n))

    def cross_correlation(self, other, n, normalize=True):
        if self.Rs != other.Rs:
            raise ValueError("Rs must match")
        wigner_D = self.wigner_D_on_grid(n)
        normalize_by = (self.signal.norm(2, 0) * other.signal.norm(2, 0))
        cross_corr =  torch.einsum(
            'abcji,j,i->abc', (wigner_D, self.signal, other.signal)
        )
        return cross_corr / normalize_by if normalize else cross_corr

    def find_peaks(self, n=100, min_height=0.1):
        # Taken from se3cnn.spherical_harmonics
        x, y, z, f = self.signal_on_sphere(which_mul, n, radius)
        xyz = torch.stack([x, y, z])

        beta_pass = []
        for i in range(f.size(0)):
            jj, _ = scipy.signal.find_peaks(f[i])
            beta_pass += [(i, j) for j in jj]

        alpha_pass = []
        for j in range(f.size(1)):
            ii, _ = scipy.signal.find_peaks(f[:, j])
            alpha_pass += [(i, j) for i in ii]

        peaks = list(set(beta_pass).intersection(set(alpha_pass)))

        radius = torch.stack([f[i, j] for i, j in peaks]) if peaks else torch.empty(0)
        peaks = torch.stack([xyz[i, j] for i, j in peaks]) if peaks else torch.empty(0, 3)
        return peaks, radius

    def __add__(self, other):
        if self.Rs == other.Rs:
            from copy import deepcopy
            return SphericalTensor(self.signal + other.signal,
                                   deepcopy(self.Rs))

    def __mul__(self, other):
        # Dot product if Rs of both objects match
        # Add check for feature_Rs.
        if self.Rs == other.Rs:
            dot = (self.signal * other.signal).sum(-1)
            dot /= (self.signal.norm(2, 0) * other.signal.norm(2, 0))
            return dot

    def __matmul__(self, other):
        # Tensor product
        # Assume first index is Rs
        # Better handle mismatch of features indices
        Rs_out, C = se3cnn.SO3.reduce_tensor_product(self.Rs, other.Rs)
        Rs_out = [(mult, L) for mult, L, parity in Rs_out]
        new_signal = torch.einsum('ijk,i...,j...->k...', 
                                  (C, self.signal, other.signal))
        return SphericalTensor(new_signal, Rs_out)

    def __rmatmul__(self, other):
        # Tensor product
        return self.__matmul__(self, other)
