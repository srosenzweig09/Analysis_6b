import numpy as np
import matplotlib.pyplot as plt

def f_Gauss(pt):
    return np.random.normal(0,0.1,len(pt))

ex_loc = '/eos/user/s/srosenzw/SWAN_projects/sixB/Analysis_6b/Machine_Learning/Model_Training/Inputs/'
ex_file = 'MX700_MY400_classifier_allpairs_dR_presel.npz'
examples = np.load(ex_loc + ex_file)

X              = examples['x']
y              = examples['y']
mjj            = examples['mjj']
extra_bkgd_x   = examples['extra_bkgd_x']
extra_bkgd_y   = examples['extra_bkgd_y']
extra_bkgd_mjj = examples['extra_bkgd_mjj']
params         = examples['params']

pt1 = X[:,0]
pt2 = X[:,3]

print(pt1)
# print(pt2)

pt1_smeared = (1+f_Gauss(pt1))*pt1
pt2_smeared = (1+f_Gauss(pt2))*pt2

print(pt1_smeared)

ratio1 = pt1_smeared / pt1
ratio2 = pt2_smeared / pt2

fig, axs = plt.subplots(nrows=2, ncols=1)

ax = axs[0]
ax.set_title(r"jet$_1$ $p_T^\mathrm{smeared}/p_T^\mathrm{gen}$")
ax.hist(ratio1, bins=np.linspace(0,2,50), histtype='step', align='mid', label=r'jet$_1$')
ax = axs[1]
ax.set_title(r"jet$_2$ $p_T^\mathrm{smeared}/p_T^\mathrm{gen}$")
ax.hist(ratio2, bins=np.linspace(0,2,50), histtype='step', align='mid', label=r'jet$_2$')


plt.tight_layout()

fig.savefig("smeared_pt.pdf")

pt1_smeared = pt1_smeared[:,np.newaxis]
pt2_smeared = pt2_smeared[:,np.newaxis]
x = np.hstack(( pt1_smeared, X[:,1:3], pt2_smeared, X[:,4:] ))

assert(np.array_equal(x[:,1:3], X[:,1:3]))
assert(np.array_equal(x[:,4:], X[:,4:]))
assert(not np.array_equal(x[:,0], X[:,0]))
assert(not np.array_equal(x[:,3], X[:,3]))

# np.savez('MX700_MY400_classifier_allpairs_dR_presel_smeared.npz', x=x, y=y, mjj=mjj, extra_bkgd_x=extra_bkgd_x, extra_bkgd_y=extra_bkgd_y, extra_bkgd_mjj=extra_bkgd_mjj, params=params)