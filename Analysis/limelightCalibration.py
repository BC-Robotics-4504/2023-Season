from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

def ft_to_m(ft):
    return ft*12*25.4e-3

def func(x, a, b):
    f = lambda x: a*np.sqrt(1/(x + b))
    if isinstance(x, list):
        return [f(xi) for xi in x]
    return f(x)

if __name__ == '__main__':
    data = [(0.555, 2),
            (0.237, 3),
            (0.119, 4),
            (0.078, 5),
            (0.050, 6),
            (0.029, 7),
            (0.022, 8),
            (0.02, 9)]

# %% Format data and perform unit conversions
    area = []
    distance_m = []
    for (area_percent, distance_ft) in data:
        area.append(area_percent)
        distance_m.append(ft_to_m(distance_ft))

# %% Fit data
    popt, pcov = curve_fit(func, area, distance_m)
    x = np.linspace(min(area), max(area), 1001)

    plt.figure(figsize=(4,3))
    plt.plot(area, distance_m, marker='.', linestyle='', linewidth=1.0, label='Measurements')   

    plt.plot(x, func(x, *popt), linestyle='--', color='k', linewidth=1.0, label=fr'${popt[0]:0.3f}/(x+{popt[1]:0.3f})$'+r'$^{-1/2}$' )
    plt.legend(loc='upper right')
    plt.grid(which='both', alpha=0.15)
    plt.ylabel(r'Distance to Tape, $d$ (m)')
    plt.xlabel(r'Tape Area (%)')
    plt.tight_layout()
    plt.savefig('tape_calibration.png', dpi=300)
    plt.show() 