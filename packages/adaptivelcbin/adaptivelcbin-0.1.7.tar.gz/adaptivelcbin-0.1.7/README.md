# adaptivelcbin

__CAUTION__: this is a simple functional project, although it should work as generally expected, do make sanity checks 
and make sure you understand what the adaptive binning is 

It makes adaptive binning and hardness ratio of two light curves (XMM-Newton input tested)

## Installation
```bash
$ pip install adaptivelcbin
```
## Help
```bash
$ hratio --help
```

## Example:
```bash
$ hratio PNsrc_lc_01s_005-030.fits PNsrc_lc_01s_030-100.fits hratio4.qdp 15.0 --flag_rebin=4
```

```python
import hratio
hratio.hratio_func('data/PNsrc_lc_01s_005-030.fits', 'data/PNsrc_lc_01s_030-100.fits', 'test1.qdp', 15.0)
```