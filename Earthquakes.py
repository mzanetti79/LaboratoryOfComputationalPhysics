#importlib.reload(E)
"""
import numpy as np
import pandas as pd
import scipy as sp
from scipy import linalg as la
from scipy import stats
from scipy.stats import chisquare
import matplotlib as mpl
from decimal import Decimal
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import optimize
from scipy import stats


def ImportDataset():
    file = 'SouthCalifornia-1982-2011_Physics-of-Data.dat'
    data = np.genfromtxt(file, dtype = None, delimiter=' ')
    df = pd.DataFrame(data)
    df.columns = ['event', 'prev_event', 'time', 'magnitude', 'x', 'y', 'z']
    return df

def TimeEventPlot(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(df['event'], df['time'])
    ax.set_xlabel('ID number of event')
    ax.set_ylabel('time of event [s]')
    plt.title("Time event distribution", y = 1.1, fontsize = 18)
    plt.show()

def MagnitudeDistribution(df):
    from scipy import optimize
    from decimal import Decimal
    def my_expon(x, No, alpha):
        return No*np.exp(-alpha*x)

    def my_log_expon(x, Q, alpha):
        return -alpha*x + Q
    fig, ax = plt.subplots(ncols=2, figsize=(14, 6))

    n, bins, _ = ax[0].hist(df['magnitude'], log = False, histtype = 'step')
    ax[1].hist(df['magnitude'], log = True, histtype = 'step')

    bin_centers = (bins[1:] + bins[:-1])/2
    ax[0].errorbar(bin_centers, n, np.sqrt(n), fmt = '.b', label = 'values with \nPoisson error')
    ax[1].errorbar(bin_centers, n, np.sqrt(n), fmt = '.b', label = 'values with \nPoisson error')

    params1, _ = optimize.curve_fit(my_log_expon, bin_centers, np.log(n))
    [Q, alpha] = params1
    No = int(np.exp(Q))
    ax[0].plot(bin_centers, my_expon(bin_centers, No, alpha),
             label = 'f($M_w$) = $N_o$$e^{-aM_w}$ '+'\n$N_o$ =' + '%.2E' % Decimal(No) + '\n a = {}'.format(round(alpha,2)))
    ax[1].plot(bin_centers, my_expon(bin_centers, No, alpha))
    ax[0].set_xlabel('magnitude [$M_w$]')
    ax[0].set_ylabel('occurrencies')
    ax[0].set_ylim(bottom = 1)
    ax[1].set_xlabel('magnitude [$M_w$]')
    ax[1].set_ylabel('occurrencies [log scale]')
    ax[1].set_ylim(bottom = 1)
    ax[0].legend(fontsize = 12)
    fig.suptitle("Magnitude distribution", fontsize = 18)
    plt.show()
    plt.close()


def SpatialDistribution(df):
    from mpl_toolkits.mplot3d import Axes3D
    m_bar = 3
    dfm = df[df['magnitude'] > m_bar]
    x_coord = dfm['x']
    y_coord = dfm['y']
    z_coord = dfm['z']
    magnitude = dfm['magnitude']

    fig = plt.figure(figsize = (7,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_coord/1e06, y_coord/1e06, z_coord/1e06,
               s=np.exp(magnitude*1.5)/np.exp(3), c = magnitude, marker="o", alpha = 0.5,
               label = 'size of marker \nproportional \nto magnitude', cmap = 'plasma')
    ax.set_xlabel("x [$10^6$ m]", fontsize = 12)
    ax.set_ylabel("y [$10^6$ m]", fontsize = 12)
    ax.set_zlabel("z [$10^6$ m]", fontsize = 12)
    ax.set_title('Spatial distribution of events for m > 3', fontsize = 18)
    ax.legend(loc = 'center left', markerscale=0.5)
    ax.view_init(elev = 30, azim = 330)

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    plt.show()


def PCA_plot(X, Xp):
    fig, axes = plt.subplots(nrows=2, ncols=3,
                                   figsize=(12, 6))

    fig.suptitle("Coordinates projections", x=0.5, y=1.05, fontsize=18)

    [[ax00, ax01, ax02],[ax10, ax11, ax12]] = axes

    ax00.scatter(X[0], X[1], s= 5, alpha=0.1)
    ax00.set_title('x-y projection', fontsize = 14)
    ax00.set_xlabel('x')
    ax00.set_ylabel('y')

    ax01.scatter(X[0], X[2], s= 5, alpha=0.1)
    ax01.set_title('x-z projection', fontsize = 14)
    ax01.set_xlabel('x')
    ax01.set_ylabel('z')

    ax02.scatter(X[1], X[2], s= 5, alpha=0.1)
    ax02.set_title('y-z projection', fontsize = 14)
    ax02.set_xlabel('y')
    ax02.set_ylabel('z')

    ax10.scatter(Xp[0], Xp[1], s= 5, alpha=0.1)
    ax10.set_title('$v_0$-$v_1$ projection', fontsize = 14)
    (y_bottom, y_top) = ax01.get_ylim()
    ax10.set_xlabel('$v_0$')
    ax10.set_ylabel('$v_1$')

    ax11.scatter(Xp[0], Xp[2], s= 5, alpha=0.1)
    ax11.set_ylim(y_bottom, y_top)
    ax11.set_title('$v_0$-$v_2$ projection', fontsize = 14)
    ax11.set_xlabel('$v_0$')
    ax11.set_ylabel('$v_2$')

    ax12.scatter(Xp[1], Xp[2], s= 5, alpha=0.1)
    ax12.set_ylim(y_bottom, y_top)
    ax12.set_title('$v_1$-$v_2$ projection', fontsize = 14)
    ax12.set_xlabel('$v_1$')
    ax12.set_ylabel('$v_2$')
    plt.tight_layout()
    plt.show()
    plt.close()


def KDE_plot(Xp):
    import seaborn as sns
    g = sns.jointplot(Xp[0], Xp[1], kind="kde", xlim=[-3,4], ylim=[-2,2], height=7, space=0)
    g.set_axis_labels(xlabel='x', ylabel='y')


def TrasversePlanePlot(df, normal):
    from mpl_toolkits.mplot3d import Axes3D
    xx, yy = np.meshgrid(range(-4,5), range(-4,5))# calculate corresponding z
    z = (-normal[0] * xx - normal[1] * yy ) * 1. /normal[2]
    m_bar = 3
    dfm = df[df['magnitude'] > m_bar]
    x_coord = dfm['x']
    y_coord = dfm['y']
    z_coord = dfm['z']
    x_coord = (x_coord - x_coord.mean())/x_coord.std()
    y_coord = (y_coord - y_coord.mean())/y_coord.std()
    z_coord = (z_coord - z_coord.mean())/z_coord.std()
    magnitude = dfm['magnitude']

    fig = plt.figure(figsize = (7,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(xx, yy, z, alpha=0.3)
    ax.scatter(x_coord, y_coord, z_coord,
               s=np.exp(magnitude*1.5)/np.exp(3), c = magnitude, marker="o", alpha = 0.5,
               label = 'size of marker \nproportional \nto magnitude', cmap = 'plasma')
    ax.set_xlabel("x [$10^6$ m]", fontsize = 16)
    #ax.xaxis.set_label_coords(2, 10)
    #ax.xaxis._axinfo['label']['space_factor'] = 10.0
    #for t in ax.xaxis.get_major_ticks(): t.label.set_fontsize(8)
    #ax.set_xticks([-6, -4, -2, 0, 2])
    ax.set_ylabel("y [$10^6$ m]", fontsize = 16)
    ax.set_zlabel("z [$10^6$ m]", fontsize = 16)
    ax.set_title('Spatial distribution of events for m > 3', fontsize = 20)
    ax.legend(loc = 'center right', markerscale=0.5)
    #print('azim = ', azim)
    ax.view_init(elev = 23, azim = 10)
    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.tight_layout()
    plt.show()
    plt.close()


def HeatmapCoordinatePlot(Xp):
    from matplotlib.colors import LogNorm
    plt.figure(211)
    plt.hist2d(Xp[0], Xp[1], bins = 50, norm = LogNorm(), cmap = "plasma")
    cbar = plt.colorbar()
    cbar.set_label('Event density', fontsize = 14)
    plt.xlabel('First principal component', fontsize = 14)
    plt.ylabel('Second principal component', fontsize = 14)
    plt.title('Heatmap of events in P.C. coordinates',y=1.1,fontsize = 18)
    plt.tight_layout()
    plt.show()
    plt.close()


# SOMETHING IN THERE

def MagnitudeDepthPlot(df):
    sns.lineplot(x="depth", y="magnitude", data=df)
    plt.xlabel('Cause-effect depth', fontsize = 14)
    plt.ylabel('Magnitude [$M_w$]', fontsize = 14)
    plt.title('Magnitude vs Depth',y=1.1,fontsize = 18)
    plt.show()


def EdgesMagnitudePlot(df):
    def my_expon1(x, No, gamma):
        return No*np.exp(gamma*x)

    plt.plot(df['magnitude'], df['edges'] , '.b')
    plt.xlabel('Magnitude [$M_w$]', fontsize = 14)
    plt.ylabel('number of edges', fontsize = 14)

    df5 = df[df['magnitude'] > 5]
    ax = plt.axes([0.3, 0.4, 0.4, 0.4])
    ax.set_title('Zoom for m > 5')
    ax.plot(df5['magnitude'], df5['edges'] , '.g')
    params1, _ = optimize.curve_fit(my_expon1, df5['magnitude'], df5['edges'])
    [No, gamma] = params1
    x_axis = np.linspace(5,7.3,100)
    ax.plot(x_axis, my_expon1(x_axis, *params1), 'r-',
            label = '$N_0$exp($\gamma m$):\n $\gamma$ = {}'.format(round(gamma,2)))
    ax.legend()
    plt.suptitle("Edges vs Magnitude", y=1.02, fontsize = 18)
    plt.show()


def EdgesDepthPlot(df):
    plt.plot(df['depth'], df['edges'], 'b.')
    plt.xlabel('cause-effect depth', fontsize = 14)
    plt.ylabel('number of edges', fontsize = 14)
    plt.title("Edges vs Depth", y = 1.05, fontsize = 18)
    plt.show()


def binning(x, rescaling = False, density = False, verbose = True):

    """Binning for power laws distributions.
        x = entries generated from a power law."""

    # x must have streactly positive values; x isn't normalized in general
    x = x[x>0]
    if rescaling == True:
        x = x/x.max()

    x.sort()

    # empirical method to get a good amount of bins (min 8, max 16), depending on the number of samples
    bin_extremes_number = max( min( int( np.log(len(x))*2 ) , 17), 9)

    # choose the right extreme of the first bin as the one that corresponds to N/bin_extreme_number of samples in the
    #first bin
    first_quantile = x[int(x.shape[0]*(1/bin_extremes_number))]

    # create bins whose widths are constant in the logaritmic scale
    bin_extremes = np.logspace(np.log10(first_quantile), np.log10(x.max()), bin_extremes_number)
    #and then concatenate 0 as a starting point for the first bin
    bin_extremes = np.concatenate((np.array([0]), bin_extremes))

    widths = bin_extremes[1:] - bin_extremes[:-1]
    centers = (bin_extremes[1:] + bin_extremes[:-1])/2

    freq, _, _ = plt.hist(x, bins=bin_extremes)
    plt.close()

    # having unhomogeneous bins the frequencies must be divided for the width of the corresponding bin in order
    # to get an estimator of the probability density in each point (~ bin center), i.e. :
    # weights(bin_center) = Prob(bin_center) , if normalized = True
    weights = freq/widths
    # poissonian errors for the frequencies, then the error is propagated to the weights dividing elementwise for
    # the widths
    sigma_weights = np.sqrt(freq)/widths

    # merging of the first two bins until we get that the first bin represents the max of the PDF
    # this is a useful option to regularize the first bin if we expect it to assume the highest value
    while weights[0] < weights[1]:
        if verbose == True: 
            print('Merging first and second bins.')
        #this is done by removing the second extreme, thus the first bin becomes the one between 0 and 2
        bin_extremes = np.concatenate(([bin_extremes[0]], bin_extremes[2:] ))
        widths = bin_extremes[1:] - bin_extremes[:-1]
        centers = (bin_extremes[1:] + bin_extremes[:-1])/2

        # then of course we need to recompute frequencies and weights for the new bins
        freq, _, _ = plt.hist(x, bins=bin_extremes)
        plt.close()
        weights = freq/widths
        sigma_weights = np.sqrt(freq)/widths

    # adding also the merging of empty bins with the one on the left
    # this avoids the issue of taking the log of 0 in the log-log space where we perform the linear regression
    mask = (freq != np.zeros(len(freq)))
    flag = np.all(mask)
    # should enter in the while loop only in there is at least one bin without counts in it

    while flag == False:
        if verbose == True:
            print('Entered in the while loop.')
            print('Original frequencies: ', freq)
        for i in range(1,len(freq)):
            if freq[i] == 0:
                if verbose == True:
                    print('Merging bin {} (empty) with bin {}.'.format(i,i-1))
                # bin extremes should be of length len(freq) + 1
                # notice that bin_extremes[i] corresponds to the right border of bin[i-1]
                # bin_extremes[:i] excludes the bin_extreme[i] !
                bin_extremes = np.concatenate((bin_extremes[:i], bin_extremes[i+1:] ))
                widths = bin_extremes[1:] - bin_extremes[:-1]
                centers = (bin_extremes[1:] + bin_extremes[:-1])/2
                # call a break of the for because the len frequence changes and can result in index errors
                break

        # update of the frequencies

        freq, _, _ = plt.hist(x, bins=bin_extremes)
        plt.close()
        weights = freq/widths
        sigma_weights = np.sqrt(freq)/widths

        # update of the exit condition
        mask = (freq != np.zeros(len(freq)))
        flag = np.all(mask)

    if density == True:
        #returns normalized weights (with rescaled errors) so that the area of the histogram is 1
        area = np.sum(weights*widths)
        weights = weights / area
        sigma_weights = sigma_weights/area

    return bin_extremes, widths, centers, freq, weights, sigma_weights


def linear_f(x, p, q):
        return p*x+q

def loglog_fitting(x, y, skip_initial_pt = 1, cut_off = False, P0 = 3):
    from scipy import optimize

    # this is used because the first bin is always problematic: in the log space log(0) doesn't exist, but in the
    # original space it is the only non-arbitrary lower bound to the values that are acceptable both for the waiting times
    # and the distances. Thus by default we ignore the first point in the regression
    x = x[skip_initial_pt:]
    y = y[skip_initial_pt:]

    if cut_off == False:
        params, cov = optimize.curve_fit(linear_f, x, y)
        [p,q] = params
        return p, q, cov

    else:
        #notice that we are already working without considering the first skip_initial_pt points
        mean_squared_res = []
        predicted_squared_res = []

        # P is the number of points considered for the fit, used for testing whether the point P+1 is alligned
        # with them or not; the likelihood of not being alligned is given by the ratio between
        # the predicted squared residual of point P+1 (based on the fit on the previous P points)
        # and the mean squared residual computed for the P points
        # P0 is the minumum amount of points that we require to be aligned "a priori" and it is used to calibrate
        # the notion of alligned/not-alligned for the fit (more points, like 5, make the algorithm more stable w.r.t.
        # statistical fluctuations)
        for P in range(P0,len(x)):
            params, cov = optimize.curve_fit(linear_f, x[:P], y[:P])
            [p,q] = params

            squared_residuals = np.power(y[:P] - linear_f(x[:P], *params),2)
            mean_squared_res.append(squared_residuals.mean())

            next_pt_squared_res = np.power(y[P] - linear_f(x[P], *params),2)
            predicted_squared_res.append(next_pt_squared_res)

        predicted_squared_res = np.array(predicted_squared_res)
        mean_squared_res = np.array(mean_squared_res)
        predicted_vs_mean_ratio = predicted_squared_res/mean_squared_res
        predicted_vs_mean_ratio_norm = predicted_vs_mean_ratio/predicted_vs_mean_ratio.max()

        # The index of the array predicted_vs_mean_ratio_norm is shifted by P0 positions, meaning that we consider
        # as the maximal number of alligned points the one corresponding to the index of the max of
        # predicted_vs_mean_ratio_norm + P0 = good_points.

        indexes = np.arange(P0,len(x))
        max_index = indexes[predicted_vs_mean_ratio_norm == predicted_vs_mean_ratio_norm.max()]
        good_points = max_index[0]
        # Then the cut-off is estimated as x_cut = (x[good_points]+ x[good_points+1])/2
        if good_points < len(x):
            # the -1 shift at the index is because the index numeration starts at 0
            x_cut = (x[good_points-1]+ x[good_points])/2
        else:
            print('ATTENTION: all points seem alligned.')
            print('x_cut set to the value of the last point.')
            x_cut = x[-1]

        params, cov = optimize.curve_fit(linear_f, x[:good_points], y[:good_points])
        [p,q] = params

        return p, q, cov, x_cut, 'Good points {} out of {}'.format(good_points, len(x))


def plot_powerlaw_hist(x, suptitle, rescaling = False, density = False, show = True, verbose = True, **kwargs):

    # compute automatically a suitable binning for x and all the associated quantities
    bin_extremes, widths, centers, freq, weights, sigma_weights = binning(x, rescaling, density, verbose)
    bin_number = len(centers)

    if show:
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2,figsize=(12, 5))

        # we plot a single point for each bin with the weight being the probability density estimated for the center
        # of the bin (see binning function)
        ax1.hist(centers, bins = bin_extremes, weights = weights, histtype = 'step')
        ax1.errorbar(centers, weights, sigma_weights, fmt = 'r.')
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel('waiting times [s]', fontsize = 14)
        ax1.set_ylabel('occurrencies [a.u]', fontsize = 14)
        ax1.set_title('Number of events = {}'.format(len(x)))

    # now we need to fit the power law in the log-log space, eventually identifying the points before the cut-off
    # this should work automatically both for the case rescaling = True or False (if True, x is in [0,1])
    # and for the case density = True or False (if True, the area of the histogram is normalized to 1
    # and the weights are rescaled so that np.sum(weights*bin_widths) = 1)
    log_x = np.log(centers)
    log_w = np.log(weights)

    # the idea is to write a function that as a default just fits the (log_x,log_w) with a linear function
    # log_w = p*log_x + q and has 2 flags: one for excluding skip_initial_pt points (set to 1 for default because
    # the first bin is always problematic) and another one to signal that we expect a cut-off at the right side of the
    # distribution (i.e. the tail) and we want to stop fitting just before the cut-off.
    # we want as a return the parameters p and q with their covariance matrix (that is the default return of
    # scipy curve_fit) and, if the cut_off flag is True, also the estimate cut-off (rescaled or not depending on the
    # setting passed before)

    if 'cut_off' in kwargs:
        if kwargs['cut_off'] == True:
             p, q, cov, log_x_cut, title = loglog_fitting(log_x, log_w, **kwargs)
    else:
        p, q, cov, x_cut, title = loglog_fitting(log_x, log_w, **kwargs)

    if show:
        y_errors = sigma_weights/weights

        ax2.errorbar(log_x, log_w, yerr = y_errors ,fmt ='r.', label = 'entries with errors')
        ax2.plot(log_x, linear_f(log_x, p, q),
                 label = 'f(x) = px + q\np = {} \nq = {}'.format(round(p,1),round(q,1)))
        ax2.legend()
        ax2.set_xlabel('waiting times [logscale]', fontsize = 14)
        ax2.set_ylabel('occurrencies [logscale]', fontsize = 14)
        ax2.set_title(title)
        fig.suptitle(suptitle, x=0.5, y=1, fontsize=18)
        plt.show()

    if 'cut_off' in kwargs:
        if kwargs['cut_off'] == True:
            if rescaling == True:
                return p, q, np.sqrt(cov[0,0]), np.exp(log_x_cut)*x.max()
            else:
                return p, q, np.sqrt(cov[0,0]), np.exp(log_x_cut)
    else:
        # returns the slope, the intercept and the error of the slope
        return p, q, np.sqrt(cov[0,0])

def plot_powerlaw_hist_dist(x, suptitle, rescaling = False, density = False, show = True, **kwargs):

    # compute automatically a suitable binning for x and all the associated quantities
    bin_extremes, widths, centers, freq, weights, sigma_weights = binning(x, rescaling, density)
    bin_number = len(centers)

    if show:
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2,figsize=(12, 5))

        # we plot a single point for each bin with the weight being the probability density estimated for the center
        # of the bin (see binning function)
        ax1.hist(centers, bins = bin_extremes, weights = weights, histtype = 'step')
        ax1.errorbar(centers, weights, sigma_weights, fmt = 'r.')
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel('distances [m]', fontsize = 14)
        ax1.set_ylabel('occurrencies [a.u]', fontsize = 14)
        ax1.set_title('Number of events = {}'.format(len(x)))

    # now we need to fit the power law in the log-log space, eventually identifying the points before the cut-off
    # this should work automatically both for the case rescaling = True or False (if True, x is in [0,1])
    # and for the case density = True or False (if True, the area of the histogram is normalized to 1
    # and the weights are rescaled so that np.sum(weights*bin_widths) = 1)
    log_x = np.log(centers)
    log_w = np.log(weights)

    # the idea is to write a function that as a default just fits the (log_x,log_w) with a linear function
    # log_w = p*log_x + q and has 2 flags: one for excluding skip_initial_pt points (set to 1 for default because
    # the first bin is always problematic) and another one to signal that we expect a cut-off at the right side of the
    # distribution (i.e. the tail) and we want to stop fitting just before the cut-off.
    # we want as a return the parameters p and q with their covariance matrix (that is the default return of
    # scipy curve_fit) and, if the cut_off flag is True, also the estimate cut-off (rescaled or not depending on the
    # setting passed before)

    if 'cut_off' in kwargs:
        if kwargs['cut_off'] == True:
             p, q, cov, log_x_cut, title = loglog_fitting(log_x, log_w, **kwargs)
    else:
        p, q, cov, x_cut, title = loglog_fitting(log_x, log_w, **kwargs)

    if show:
        y_errors = sigma_weights/weights

        ax2.errorbar(log_x, log_w, yerr = y_errors ,fmt ='r.', label = 'entries with errors')
        ax2.plot(log_x, linear_f(log_x, p, q),
                 label = 'f(x) = px + q\np = {} \nq = {}'.format(round(p,1),round(q,1)))
        ax2.legend()
        ax2.set_xlabel('distances [logscale]', fontsize = 14)
        ax2.set_ylabel('occurrencies [logscale]', fontsize = 14)
        ax2.set_title(title)
        fig.suptitle(suptitle, x=0.5, y=1, fontsize=18)
        plt.show()

    if 'cut_off' in kwargs:
        if kwargs['cut_off'] == True:
            if rescaling == True:
                return p, q, np.sqrt(cov[0,0]), np.exp(log_x_cut)*x.max()
            else:
                return p, q, np.sqrt(cov[0,0]), np.exp(log_x_cut)
    else:
        # returns the slope, the intercept and the error of the slope
        return p, q, np.sqrt(cov[0,0])


def EsponentMagnitudePlot(ms1, p_time, p_t_errors):
    p_mean = p_time.mean()
    p_std = p_time.std()/np.sqrt(len(p_time))
    slope, intercept, r_value, p_value, std_err = stats.linregress(ms1, p_time)
    plt.errorbar(ms1, p_time, yerr = p_t_errors, fmt = '.r', label = 'estimated exponents \nwith errors' )
    plt.plot(ms1, intercept+slope*ms1, label = 'fit: p(m) = %.2fm%.2f'%(slope,intercept))
    plt.axhline(p_mean, color = 'tab:orange', label = "Mean $<p>_m$ = %.2f $\pm$ %.2f"%(p_mean,p_std))
    plt.ylabel('exponent p', fontsize = 14)
    plt.xlabel('magnitude m', fontsize = 14)
    plt.title('Exponent dependence from magnitude', y=1.1, fontsize = 18)
    plt.legend()
    plt.show()


def WaitingMagnitudePlot(ms1, cut_times):
    slope, intercept, r_value, p_value, std_err = stats.linregress(ms1, np.log(cut_times))
    predicted_cut_times = np.exp(intercept+slope*ms1)
    plt.plot(ms1, predicted_cut_times, label = 'fit: p(m) = %.2fm + %.2f'%(slope,intercept))
    plt.errorbar(ms1, cut_times, fmt = '.r')
    plt.ylabel('Waiting time cut-off [s]', fontsize = 14)
    plt.xlabel('Magnitude m [$T_w$]', fontsize = 14)
    plt.yscale('log')
    plt.title('Waiting time cut-off vs magnitude', y=1.1, fontsize = 18)
    plt.legend()
    plt.show()
    return predicted_cut_times, [slope, intercept]


def WaitingTimeConsequentEvents(df, v_dict):
    N = df.shape[0]
    time_diff_tree = np.zeros(N)
    for d in range(len(v_dict)):
        for k in v_dict[d].keys():
            # previous vertex has id = k, children vertexes have ids [ v_dict[d][k] ]
            for j in v_dict[d][k]:
                #print('Computing {}-> {} waiting time.'.format(k,j))
                time_diff_tree[int(j)] = df['time'].iloc[int(j)] - df['time'].iloc[int(k)]

    time_diff_tree = time_diff_tree[time_diff_tree > 0]
    p_tree, q_tree, p_tree_err, cut_time_tree = plot_powerlaw_hist(time_diff_tree, "Waiting times distribution for consequent events", rescaling = False, density = False, cut_off = True, P0 = 4)


def select_bin_number_mod(x, m = 2, min_nbin = 7, fraction = 0.001):
    """Starts from evenly separed bins and merges the last ones until the tail's counts are
        major or equal to the 'fraction' of the total number of occurrencies, given the
        constraint that the final number of bins has to be min_nbin."""

    # added a factor exp(m-2) to take into account the exponential decrease of total N - empirical formula
    n_min = max([int(fraction*len(x)*np.exp(m-2)),10])
    print('For m = {} and N = {} the minimum number of events in the tail required is : {}'.format(m, len(x), n_min))
    print('Minimum accuracy expected : {}'.format(round(1 - 1/np.sqrt(n_min),2)))

    n, bin_extremes, _ = plt.hist(x, bins = min_nbin )
    plt.close()
    last_n = n[-1]

    if last_n > n_min:
        return min_nbin, bin_extremes
    else:
        i = min_nbin
        nbin = min_nbin
        while last_n < n_min and nbin < 100:
            nbin = nbin + 1
            n, _, _ = plt.hist(x, bins = nbin )
            plt.close()
            last_n = n[i-1:].sum()

        if last_n > n[min_nbin-2]:
            print('-> reducing the final number of bins to {}: \n'.format(min_nbin - 1))
            nbin, bins = select_bin_number_mod(x, m = m, min_nbin = min_nbin - 1)
        else:
            n, bin_extremes, _ = plt.hist(x, bins = nbin )
            plt.close()
            bins = np.concatenate((bin_extremes[:min_nbin],bin_extremes[-1:]))

        return nbin, bins


def plot_Pm_r2(m, df):
    #print('\nDistance distribution for m = ', m, '\n')
    dfm = df[df['magnitude'] > m]
    X = np.array(dfm[['x','y','z']])
    r = np.linalg.norm(X[1:]-X[:-1], axis = 1)
    r_norm = r/r.max()
    # computing suitable sizes of bins
    original_bin_number, bins = select_bin_number_mod(r_norm, m=m, min_nbin = 10)
    bin_number = len(bins) - 1

    fig, ax1 = plt.subplots(nrows=1, ncols=1,figsize=(6, 5))

    n_tailed, bin_extremes, _ = ax1.hist(r_norm, bins = bins, histtype = 'step')

    bin_centers = (bin_extremes[:-1] + bin_extremes[1:])/2

    # rescaling the tail entries with the number of bins merged into the tail
    n = np.concatenate((n_tailed[:-1], n_tailed[-1:]/(original_bin_number+1-bin_number)))

    sigma_n = np.sqrt(n)

    ax1.errorbar(bin_centers, n, sigma_n, fmt = 'r.')
    ax1.set_xlabel('normalized distances', fontsize = 14)
    ax1.set_ylabel('occurrencies', fontsize = 14)
    ax1.set_title('Number of events = {}'.format(len(r_norm)))
    fig.suptitle("Distance distribution for m = " + str(m), fontsize = 18)
    plt.show()
    plt.close()
    return r.mean(), r.std()/np.sqrt(len(r))


def DistanceDistributionPlot(df, ms):
    r_mean = np.zeros(len(ms))
    r_std = np.zeros(len(ms))
    for i in range(len(ms)):
        m = ms[i]
        r_mean[i], r_std[i] = plot_Pm_r2(m, df)


def poissonian4(x, A=1, l=1):
    from scipy.special import gamma
    return A*np.float_power(l,x)/gamma(x)*np.exp(-l)

import scipy.stats as st
from scipy.integrate import quad

class my_pdf(st.rv_continuous):
    def _pdf(self,x, A, l):
        return poissonian4(x, A, l)  # Normalized over its range, in this case [0,1]


def plot_Pm_r_poisson(m, df):
    dfm = df[df['magnitude'] > m]
    X = np.array(dfm[['x','y','z']])
    r = np.linalg.norm(X[1:]-X[:-1], axis = 1)
    r_norm = r/r.max()


    # computing suitable sizes of bins
    original_bin_number, bins = select_bin_number_mod(r_norm, m=m, min_nbin = 10)

    bin_number = len(bins) - 1

    fig, ax1 = plt.subplots(nrows=1, ncols=1,figsize=(6, 5))

    n_tailed, bin_extremes, _  = ax1.hist(r_norm, bins = bins, histtype = 'step', density=True)

    bin_centers = (bin_extremes[:-1] + bin_extremes[1:])/2
    area = len(r)*(bin_extremes[1] - bin_extremes[0])
    # rescaling the tail entries with the number of bins merged into the tail
    n = np.concatenate((n_tailed[:-1], n_tailed[-1:]/(original_bin_number+1-bin_number)))

    sigma_n = np.sqrt(n/area)
    ax1.errorbar(bin_centers, n, sigma_n, fmt = 'r.', label = 'entries with \npoissonian errors')
    ax1.set_xlabel('normalized distances', fontsize = 14)
    ax1.set_ylabel('occurrencies', fontsize = 14)
    ax1.set_title('Number of events = {}'.format(len(r_norm)))
    fig.suptitle("Distance distribution for m = " + str(m), fontsize = 18)
    print('Number of bins merged into the tail: {}'.format(original_bin_number - bin_number), '\n')

    #print('bin_centers: ', bin_centers, '\n')
    params1, cov1 = optimize.curve_fit(poissonian4, bin_centers, n, p0 = [n[0], 1])
    [A,l] = params1

    # tecnical stuff to create a continuous probability distribution in scipy, that allows for the method .expect
    # to compute the expected value of the distribution; the origin of the complication is the fact that poissonians
    # usually are discrete and in the continuous case the the parameter lambda doesn't represent anymore the expected value
    Area = quad(poissonian4, 0, 1, args=(A, l))[0]
    my_cv = my_pdf(a=0, b=1)

    C = A/Area

    x_axis = np.linspace(bin_extremes[0], bin_extremes[-1],100)
    ax1.plot(x_axis, my_cv.pdf(x_axis, A=C, l=l), label = 'poissonian \n $\lambda$ = %.3f '%l)
    x_expected = my_cv.expect(args=(C, l))
    x_err = r_norm.std()/np.sqrt(len(r))
    ax1.axvline(x_expected, label = 'expected value = %.2f'%x_expected)

    ax1.legend()
    plt.show()
    plt.close()

    # parameters of the poissonian, expected value, error of the mean, max distance for scaling back normalized distances
    return C, l, x_expected, x_err, r.max()


def PrimeEventsDistanceDistributionPlot(df):
    prime_df = df[df['prev_event'] == -1]
    # reduced the range of m to [2,4] due to insufficient samples for higher magnitudes
    pr_ms = np.linspace(2,4,9)
    pr_Cs = np.zeros(len(pr_ms))
    pr_ls_r = np.zeros(len(pr_ms))
    pr_r_expected = np.zeros(len(pr_ms))
    pr_r_exp_err = np.zeros(len(pr_ms))
    pr_r_max = np.zeros(len(pr_ms))

    for i in range(len(pr_ms)):
        m = pr_ms[i]
        pr_Cs[i], pr_ls_r[i], pr_r_expected[i], pr_r_exp_err[i], pr_r_max[i] = plot_Pm_r_poisson(m, prime_df)

    return pr_r_expected, pr_r_exp_err, pr_r_max, pr_ms


def ExpectedMagnitudePlot(pr_r_expected, pr_r_exp_err, pr_r_max, pr_ms):
    rescaled_peaks = pr_r_expected*pr_r_max
    rescaled_errors = pr_r_exp_err*pr_r_max
    plt.errorbar(pr_ms, rescaled_peaks, rescaled_errors, fmt = 'r.', label = '$E[x]$')
    plt.xlabel('magnitude [$T_w$]', fontsize = 14)
    plt.ylabel('$E[x]$ of poissonian', fontsize = 14)
    plt.title("Magnitude expected values", y=1.1, fontsize = 18)
    plt.legend(loc = 2)
    plt.show()


def plot_PmR_t(df, m, U, Rs, n=100, verbose=True, **kwargs):
    print('\nAnalyzing time distribution for every r and m =', round(m,1))
    # waiting time for events of magnitude > m
    #Xp = np.dot(Vt,X) # last coordinate should be small
    #Xpp = np.dot(U, Xp)
    centers = np.dot(U, np.array([np.random.uniform(-3,4, n), np.random.uniform(-2,2, n), np.zeros(n)])).T
    dfm = df[df['magnitude'] > m]

    X = dfm[['x','y','z']].values.T
    X = X.astype("float64")
    # centering and rescaling the coordinates
    for i in range(3):
        X[i] = (X[i] - X[i].mean())/X[i].std()

    distances = np.linalg.norm((X.T[:,np.newaxis,:] - centers[np.newaxis,:,:]), axis=2)
    #print("Max distance uning centered and rescaled coordinates: ", round(distances.max(),2))
    distances = distances / distances.max()
    timem = np.array(dfm['time'])
    timeM = np.tile(timem[:, np.newaxis], [1,n]).T

    #vector for fit parameters for each R_max fraction
    ps = []
    qs = []
    p_errors = []
    cut_off_times = []

    for i in range(len(Rs)):
        #print(timeM.shape)

        timeM_filtered = timeM[distances.T < Rs[i]]
        #print(timeM.shape)
        #print(distances.T.shape)
        time_d = (timeM_filtered[1:] - timeM_filtered[:-1])
        time_d = time_d[time_d>0]

        title_plot = 'Powerlaw hist for m = %.1f and r = %.2f'%(m, Rs[i])
        p, q, p_err, cut_times = plot_powerlaw_hist(time_d, suptitle=title_plot, verbose=verbose, **kwargs)

        ps.append(p); qs.append(q); p_errors.append(p_err), cut_off_times.append(cut_times)

    return ps, qs, p_errors, cut_off_times


def RangeMagnitudePlot(ms, Rs, t_cutoff):
    plt.figure(figsize = (10,8))
    ax = sns.heatmap(np.log10(t_cutoff).T, annot = False, cbar_kws = {'label' : '$log_{10}(t_{cut}[s]) $'})
    m_index = ['%.1f'%m for m in ms]
    ax.set_xticklabels(m_index, rotation = 45)
    ax.set_xlabel('magnitude m [$T_w$]', fontsize = 16)
    #R_index = ['%.2f'%((i+1)/20) for i in range(len(Rs))]
    R_index = ['%.2f'%r for r in Rs]
    ax.set_yticklabels(R_index, rotation = 0)
    ax.set_ylabel('fraction $R/R_{max}$', fontsize = 16)
    ax.figure.axes[-1].yaxis.label.set_size(18)
    plt.title("Range conditioned waiting time\n", fontsize = 18)
    plt.show()

    

def filtered_linear_fit(x, y):
    # first linear fit, used to exclude from the final fit the points that are completely misalligned
    preliminary_params, _ = optimize.curve_fit(linear_f, x, y)
    # compute squared residues of each point
    sq_residues = np.power(y - linear_f(x, *preliminary_params) ,2)
    mean_sq_res = sq_residues.mean()
    # if the sqaured residual of a point is greater than 3 times the mean squared residual the point is removed from
    # the ones used for the final fit
    mask = sq_residues < 3*mean_sq_res
    x_filtered = x[mask]
    y_filtered = y[mask]
    # fit only of the alligned points (more or less)
    params, _ = optimize.curve_fit(linear_f, x_filtered, y_filtered)
    return params


def Tcutoff_over_R_plots(t_cutoff, Rs, ms, trunc=4, show=True):
    scaling_parameters = np.zeros((len(ms),2))
    for i in range(len(ms)):
        
        # 'trunc' is the number of points that are excluded from the fit starting from the tail
        Rs_trunc = Rs[:-trunc]
        t_cut_trunc = t_cutoff[i][:-trunc]

        # filtered fit between T_cutoff and Rs
        params = filtered_linear_fit(np.log(Rs_trunc), np.log(t_cut_trunc))
        # IF slope is positive, remove first point until it becomes negative, as it should be (any better solution?)
        while(params[0]>0):
            Rs_trunc = Rs_trunc[1:]
            t_cut_trunc = t_cut_trunc[1:]
            params = filtered_linear_fit(np.log(Rs_trunc), np.log(t_cut_trunc))

        scaling_parameters[i] = params
        
        if ( show==True ) or ( show==round(ms[i],1) ):
            # plot the original points and the linear fit
            plt.plot(Rs,t_cutoff[i], 'x', label = 'm = %.1f'%ms[i]) 
            plt.plot(Rs_trunc, np.exp(linear_f(np.log(Rs_trunc), *params)) )

            plt.xlabel('fraction of distance $R/R_{max}$', fontsize = 13)
            plt.ylabel('Wating time cutoff [s]', fontsize = 13)
            plt.title('Wating time cutoff vs $R/R_{max}$', fontsize = 16)
            plt.yscale('log')
            plt.xscale('log')
            plt.legend()
            plt.show()
        elif i == len(Rs)-1:
            print('Computed scaling parameters for every m fitting T_cutoff over Rs')
    return scaling_parameters
    
    
def Tcutoff_over_m_plots(t_cutoff, Rs, ms, show=True):
    scaling_parameters = np.zeros((len(ms),2))
    for i in range(len(Rs)):
        
        # filtered fit between T_cutoff and Rs
        params = filtered_linear_fit(ms, np.log(t_cutoff[:,i]))
        scaling_parameters[i] = params

        if show == True:
            # plot the original points and the linear fit
            plt.plot(ms,t_cutoff[:,i], 'x', label = '$R/R_{max}$ = %.2f'%Rs[i]) 
            plt.plot(ms, np.exp(linear_f(ms, *params)) ) 

            plt.xlabel('Magnitude m', fontsize = 13)
            plt.ylabel('Wating time cutoff [s]', fontsize = 13)
            plt.title('Wating time cutoff vs magnitude', fontsize = 16)
            plt.yscale('log')
            #plt.xscale('log')
            plt.legend()
            plt.show()
        elif i == len(Rs)-1:
            print('Computed scaling parameters for every R fitting T_cutoff over ms')
    return scaling_parameters 
   


"""
def collapsed_distributions(x, rescaling = False, density = False, show = True, **kwargs):

    bin_extremes, widths, centers, freq, weights, sigma_weights = binning(x, rescaling, density)
    bin_number = len(centers)

    if show:
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2,figsize=(11, 5))

        ax1.hist(centers, bins = bin_extremes, weights = weights, histtype = 'step')
        ax1.errorbar(centers, weights, sigma_weights, fmt = 'r.')
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel('waiting times [s]', fontsize = 14)
        ax1.set_ylabel('occurrencies', fontsize = 14)
        ax1.set_title('Number of events = {}'.format(len(x)))

    # now we need to fit the power law in the log-log space, eventually identifying the points before the cut-off
    # this should work automatically both for the case rescaling = True or False (if True, x is in [0,1])
    # and for the case density = True or False (if True, the area of the histogram is normalized to 1
    # and the weights are rescaled so that np.sum(weights*bin_widths) = 1)
    log_x = np.log(centers)
    log_w = np.log(weights)

    # the idea is to write a function that as a default just fits the (log_x,log_w) with a linear function
    # log_w = p*log_x + q and has 2 flags: one for excluding skip_initial_pt points (set to 1 for default because
    # the first bin is always problematic) and another one to signal that we expect a cut-off at the right side of the
    # distribution (i.e. the tail) and we want to stop fitting just before the cut-off.
    # we want as a return the parameters p and q with their covariance matrix (that is the default return of
    # scipy curve_fit) and, if the cut_off flag is True, also the estimate cut-off (rescaled or not depending on the
    # setting passed before)

    if 'cut_off' in kwargs:
        if kwargs['cut_off'] == True:
             p, q, cov, log_x_cut = loglog_fitting(log_x, log_w, **kwargs)
    else:
        p, q, cov = loglog_fitting(log_x, log_w, **kwargs)

    if show:
        y_errors = sigma_weights/weights

        ax2.errorbar(log_x, log_w, yerr = y_errors ,fmt ='r.', label = 'entries with errors')
        ax2.plot(log_x, linear_f(log_x, p, q),
                 label = 'f(x) = px + q\np = {} \nq = {}'.format(round(p,1),round(q,1)))
        ax2.legend()
        ax2.set_xlabel('waiting times [logscale]', fontsize = 14)
        ax2.set_ylabel('occurrencies [logscale]', fontsize = 14)

        plt.show()

    if 'cut_off' in kwargs:
        if kwargs['cut_off'] == True:
            if rescaling == True:
                return p, q, np.sqrt(cov[0,0]), np.exp(log_x_cut)*x.max()
            else:
                return p, q, np.sqrt(cov[0,0]), np.exp(log_x_cut)
    else:
        # returns the slope, the intercept and the error of the slope
        return p, q, np.sqrt(cov[0,0])
"""


def ScalingPlot(df, ms1, predicted_cut_times):
    m_extremes= []
    m_centers = []
    m_weights =[]
    m_sigma= []
    for i in range(len(ms1)):

        m = ms1[i]
        dfm = df[df['magnitude'] > m]
        timem = np.array(dfm['time'])
        timem.sort()
        time_d = timem[1:] - timem[:-1]

        # eliminating a couple of anomalous events
        temp = time_d[time_d != time_d.max()]
        maximum = temp.max()
        if time_d.max()*3/4 > maximum:
            time_d = temp

        bin_extremes, widths, centers, freq, weights, sigma_weights = binning(time_d, rescaling = False, density = True)
        m_extremes.append(bin_extremes)
        m_centers.append(centers)
        m_weights.append(weights)
        m_sigma.append(sigma_weights)

    extremes_rescaled = []
    centers_rescaled = []
    weights_rescaled = []
    sigma_rescaled = []
    widths_rescaled = []

    plt.figure(figsize = (8,6))
    for i in range(len(ms1)):
        resc_extremes      = m_extremes[i] / predicted_cut_times[i]; extremes_rescaled.append(resc_extremes)
        resc_centers       = m_centers[i] / predicted_cut_times[i];  centers_rescaled.append(resc_centers)
        resc_weights       = m_weights[i] * predicted_cut_times[i];  weights_rescaled.append(resc_weights)
        resc_sigma_weights = m_sigma[i] * predicted_cut_times[i];    sigma_rescaled.append(resc_sigma_weights)
        resc_widths        = resc_extremes[1:] - resc_extremes[:-1]; widths_rescaled.append(resc_widths)

        #centers = m_centers_rescaled[i]/cut_times[i]
        #weights = m_weights_rescaled[i]*cut_times[i]
        #sigma_weights = m_sigma_rescaled[i]*cut_times[i]
        plt.errorbar(resc_centers, resc_weights, yerr = resc_sigma_weights, label = 'm = %.1f'%ms1[i], alpha = 0.9)
    plt.xlabel('rescaled waiting times '+r'$\tau$'+' [a.u.]',  fontsize = 16)
    plt.ylabel('PDF of '+r'$\tau$', fontsize = 16)
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Time scaling plot', y=1.05, fontsize = 18)
    plt.legend()
    plt.show()

    
    
def Compare_scaling_methods(ms_R, scaling_params_R, scaling_params_orig):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2,figsize=(14,5))
   
    # plot params of linear fit between t_cut and R/R_max for every m
    """#TOGLIEREI, DAL GRAFICO DELLE ALPHA NON SI RICAVA NULLA
    plt.plot(ms_R,scaling_params_R[:,0], 'x')
    plt.xlabel('m')
    plt.ylabel(r'$\alpha$ (m)')
    plt.show()
    """
    # linear fit between beta and m (removing outliers)
    params = filtered_linear_fit(ms_R, scaling_params_R[:,1])
    ax1.plot(ms_R,scaling_params_R[:,1],'x')
    ax1.plot(ms_R,linear_f(ms_R, *params), label = r'$\beta$ = %.2f + %.2f*m'%(params[0], params[1]))
    ax2.set_title('Relation between coefficient $\beta$ and m')
    ax1.set_xlabel('m')
    ax1.set_ylabel(r'$\beta$ (m)')
    ax1.legend()

    # compare results with the ones obtained in point 2
    ax2.plot(ms_R, np.exp(linear_f(ms_R, *scaling_params_orig)), label='$t_{cut}$ from point (2)')
    ax2.plot(ms_R, np.exp(linear_f(ms_R, *params)), label=r'$t_{cut} = e^{\beta (m)}$')
    ax2.set_title('Comparison of methods for computing cutoff')
    ax2.set_xlabel('m')
    ax2.set_ylabel('Predicted $t_{cut}$ for $r = 1$')
    ax2.set_yscale('log')
    ax2.legend()
    plt.show()
    

def compute_every_rescaled_hist(df, Rs, ms, scaling_parameters, U, n=50):
    extremes_rescaled = []
    centers_rescaled = []
    weights_rescaled = []
    sigma_rescaled = []
    widths_rescaled = []

    for k in range(len(ms)):
        m = ms[k]

        # scaling parameters for m = 2 correspond to index 0 of the array
        predicted_cut_times = np.exp(linear_f(np.log(Rs), *scaling_parameters[k])) 

        # Rs are already defined, here we generate centers in the PCA plane
        centers = np.dot(U, np.array([np.random.uniform(-3,4, n), np.random.uniform(-2,2, n), np.zeros(n)])).T
        dfm = df[df['magnitude'] > m] 

        X = dfm[['x','y','z']].values.T
        X = X.astype("float64")
        # centering and rescaling the coordinates
        for i in range(3):
            X[i] = (X[i] - X[i].mean())/X[i].std()

        # Compute distances between the center and each event (for R condition)
        distances = np.linalg.norm((X.T[:,np.newaxis,:] - centers[np.newaxis,:,:]), axis=2)
        distances = distances / distances.max()
        #print("Max distance : ", distances.max())
        timem = np.array(dfm['time'])
        timeM = np.tile(timem[:, np.newaxis], [1,n]).T

        m_extremes_rescaled = []
        m_centers_rescaled = []
        m_weights_rescaled = []
        m_sigma_rescaled = []

        # Build hist with every event inside the radios R (removing some strange events with time)
        for i in range(len(Rs)):
            timeM_filtered = timeM[distances.T < Rs[i]]
            time_d = (timeM_filtered[1:] - timeM_filtered[:-1])
            time_d = time_d[time_d>0]

            bin_extremes, widths, centers, freq, weights, sigma_weights = binning(time_d, rescaling = False, density = True, verbose = False)
            
            # Rescale every hist using the corresponding predicted cutoff time
            m_extremes_rescaled.append( bin_extremes / predicted_cut_times[i] )
            m_centers_rescaled.append( centers / predicted_cut_times[i] )
            m_weights_rescaled.append( weights * predicted_cut_times[i] )
            m_sigma_rescaled.append( sigma_weights * predicted_cut_times[i] )

        # save results in matrixes (values for every m and every R)
        extremes_rescaled.append(m_extremes_rescaled)
        centers_rescaled.append(m_centers_rescaled)
        weights_rescaled.append(m_weights_rescaled)
        sigma_rescaled.append(m_sigma_rescaled)
        
    rescaled_hists_data = {'extremes' : extremes_rescaled,
                           'centers'  : centers_rescaled,
                           'weights'  : weights_rescaled,
                           'sigmas'   : sigma_rescaled}
    return rescaled_hists_data
         
    
            
def ScalingPlot_single_R(hists_data, ms, Rs, R_fraction): 
    # check if R/Rmax is a valid value
    if (R_fraction >= 0) and (R_fraction <= 1):
        R_index = np.argwhere(Rs >= R_fraction)[0,0] #taking the first R after the one specified in the function
        
        # for every value of m, plot hist with magnitude R/R_max in the same figure
        plt.figure(figsize = (8,6))
        for i in range(len(ms)):
            plt.errorbar(hists_data['centers'][i][R_index], 
                         hists_data['weights'][i][R_index], 
                         yerr=hists_data['sigmas'][i][R_index], alpha = 0.9)

        plt.xlabel('Rescaled waiting times '+r'$\tau$'+' [a.u.]',  fontsize = 16)
        plt.ylabel('PDF of '+r'$\tau$', fontsize = 16)
        plt.xscale('log')
        plt.yscale('log')
        plt.title('Time scaling plot for $R/R_{max}$ = %.2f'%Rs[R_index], y=1.05, fontsize = 18)
        #plt.legend()
        plt.show()
        
    else:
        print('ERROR:\nThe value of R_fraction must be between 0 and 1')
    
    
def ScalingPlot_single_m(hists_data, ms, Rs, m):
    # check if m is a valid value
    if (m >= 2) and (m <=4.5):
        m_index = np.argwhere(np.round(ms,1) == m)[0,0]
        
        # for every value of R/R_max, plot hist with magnitude m in the same figure
        plt.figure(figsize = (8,6))
        for k in range(len(Rs)):
            plt.errorbar(hists_data['centers'][m_index][k],
                         hists_data['weights'][m_index][k],
                         yerr=hists_data['sigmas'][m_index][k], alpha = 0.9)

        plt.xlabel('Rescaled waiting times '+r'$\tau$'+' [a.u.]',  fontsize = 16)
        plt.ylabel('PDF of '+r'$\tau$', fontsize = 16)
        plt.xscale('log')
        plt.yscale('log')
        plt.title('Time scaling plot for m = %.1f'%m, y=1.05, fontsize = 18)
        #plt.legend()
        plt.show()
     
    else:
        print('ERROR:\nThe value of m must be between 2 and 4.5, and it can contain at max 1 digit after the decimal point')
        
