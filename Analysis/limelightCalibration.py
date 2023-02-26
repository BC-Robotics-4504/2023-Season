from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

def ft_to_m(ft):
    return ft*12*25.4e-3

def func(x, a, b):
    f = lambda x: a/x**2 - b
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
    popt, pcov = curve_fit(func, distance_m, area)
    x = np.linspace(min(distance_m), max(distance_m), 1001)

    plt.figure(figsize=(4,3))
    plt.plot(distance_m, area, marker='.', linestyle='', linewidth=1.0, label='Measurements')   

    plt.plot(x, func(x, *popt), linestyle='--', color='k', linewidth=1.0, label=f'{popt[0]:0.3f}'+r'$x-$'+f'{popt[1]:0.3f}' )
    plt.legend(loc='upper right')
    plt.grid(which='both', alpha=0.15)
    plt.xlabel(r'Distance to April Tag, $d$ (m)')
    plt.ylabel(r'Tape Area (%)')
    plt.tight_layout()
    plt.savefig('tape_calibration.png', dpi=300)
    plt.show() 