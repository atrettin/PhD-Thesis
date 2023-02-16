import numpy as np
from scipy.interpolate import LinearNDInterpolator
from scipy.optimize import root_scalar
from scipy.stats import chi2
from scipy.spatial import Delaunay

def matelem2angles(u_mu4, u_tau4):
    sin2_th24 = u_mu4
    cos2_th24 = 1 - sin2_th24
    sin2_th34 = u_tau4 / cos2_th24
    th24 = np.arcsin(np.sqrt(sin2_th24))
    th34 = np.arcsin(np.sqrt(sin2_th34))
    return th24, th34


def angles2matelem(th24, th34):
    u_mu4 = np.sin(th24) ** 2
    u_tau4 = np.sin(th34) ** 2 * (1 - u_mu4)
    return u_mu4, u_tau4


if __name__ == "__main__":
    data = np.loadtxt("real_data_v12_metric_diff.csv", skiprows=1, delimiter=",")
    Umu4_sq = data[:,0]
    Utau4_sq = data[:,1]
    metric_diff = data[:,2]

    # The interpolation has to be done on the mixing angles, because the grid is
    # regular in mixing angles only. The Delaunay mesh in the matrix elements will
    # have weird skinny triangles with wrong values.
    th24, th34 = matelem2angles(Umu4_sq, Utau4_sq)
    points = np.vstack((th24, th34)).T
    delaunay = Delaunay(points)
    interp = LinearNDInterpolator(delaunay, metric_diff)

    # interpolate over a fine mesh in matrix elements
    Umu4_plot = np.geomspace(0.001, 0.3, 100)
    Utau4_plot = np.geomspace(0.001, 0.2, 101)
    X, Y = np.meshgrid(Umu4_plot, Utau4_plot)

    th24_plot, th34_plot = matelem2angles(X.ravel(), Y.ravel())

    Z = interp(th24_plot, th34_plot).reshape(X.shape)

    # limit for umu4
    def marginalized_umu4_metric(umu4):
        return np.interp(umu4, Umu4_plot, np.min(Z, axis=0))

    wilks_90pct = chi2.ppf(0.9, df=1)
    wilks_99pct = chi2.ppf(0.99, df=1)

    limit_90 = root_scalar(
        lambda x: marginalized_umu4_metric(x) - wilks_90pct,
        bracket=(1e-2, 0.2)
    ).root

    limit_99 = root_scalar(
        lambda x: marginalized_umu4_metric(x) - wilks_99pct,
        bracket=(1e-2, 0.2)
    ).root

    print(f"Limits for |U_mu4|^2: {limit_90:.4f} (90% C.L.), {limit_99:.4f} (99% C.L.)")

    # limit for utau4
    def marginalized_utau4_metric(utau4):
        return np.interp(utau4, Utau4_plot, np.min(Z, axis=1))

    wilks_90pct = chi2.ppf(0.9, df=1)
    wilks_99pct = chi2.ppf(0.99, df=1)

    limit_90 = root_scalar(
        lambda x: marginalized_utau4_metric(x) - wilks_90pct,
        bracket=(1e-2, 0.2)
    ).root

    limit_99 = root_scalar(
        lambda x: marginalized_utau4_metric(x) - wilks_99pct,
        bracket=(1e-2, 0.2)
    ).root

    print(f"Limits for |U_tau4|^2: {limit_90:.4f} (90% C.L.), {limit_99:.4f} (99% C.L.)")
