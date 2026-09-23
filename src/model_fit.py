from scipy.optimize import curve_fit
from scipy.stats import linregress

def ajuste_lineal(xdata, ydata):
    return linregress(xdata, ydata)

def ajuste_lm(f,x, y, p0, sigma):
    popt, pcov, infodict, mesg, ier = curve_fit(f= f, xdata=x, ydata=y, p0=p0, sigma=sigma, absolute_sigma=True, method='lm', full_output=True, check_finite=True, nan_policy='raise')


def ajuste_Trf(f, x, y, p0, sigma, superior, inferior):
    popt, pcov, infodict, mesg, ier =  curve_fit(f=f, xdata=x, ydata=y, p0=p0, bounds=(superior,inferior),sigma=sigma, absolute_sigma=True, method='trf', full_output=True, check_finite=True, nan_policy='raise')

def ajuste_dogbox(f, x, y, p0, sigma, superior, inferior):
    popt, pcov, infodict, mesg, ier = curve_fit(f=f, xdata=x, ydata=y, p0=p0, bounds=(superior,inferior),sigma=sigma, absolute_sigma=True, method='dogbox', full_output=True, check_finite=True, nan_policy='raise')


def comprobar_ier(ier, metodo, mesg):
    if metodo == 'lm':
        if ier in [0,5,6,7,8]:
            print(mesg)
            return False
        else:
            return True
 
    


