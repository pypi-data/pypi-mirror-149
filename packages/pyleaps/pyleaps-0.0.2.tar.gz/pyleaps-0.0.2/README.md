## PYLEAPS

This package wants to be a simple porting of the regsubset function from R.
Unlike `leaps` in `R`, the package is not optimized yet, and requires extra work to improve code readability.
For now, I have implemented forward/backward/best subset selection for linear regression, building on top
of the excellent `statsmodels` package.

In addition, for now, the user needs to manually code the categorical variable contrasts. This will be fixed in the future.

The package can be easily installed through pip. Check out https://pypi.org/project/pyleaps/ for details

## TO INSTALL

`pip install pyleaps`

The relevant dependencies should automatically get installed, in case they are not present in the environment

## COLLABORATION

Any help/collaboration is very welcome. Just let me know what kind of edits you propose and I will be very happy to discuss them.

## TO DOs
This section contains a list of future edits:

1. Improve general code readability  
1. Figure out a way to speed up best subset section. So far, it is way slower than the R counterpart.
