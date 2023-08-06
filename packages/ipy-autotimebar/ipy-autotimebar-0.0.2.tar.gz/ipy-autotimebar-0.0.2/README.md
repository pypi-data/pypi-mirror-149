# ipy-autotimebar
Project is an extension based on [autotime](https://github.com/cpcloud/ipython-autotime) 
library extended by an add-on activated only in jupyter notebook.
The notebook displays the current cell execution time, which is updated on the fly.
(similar to VSC jupyter explorer)

## Installation:

```console
$ pip install ipy-autotimebar
```

## Examples

### jupyter notebook/Pycharm/dataspell
![jupyter](images/ezgif.com-gif-maker.gif)

### Ipython
```python
In [1]: %load_ext autotimebar
time: 676 µs (started: 2022-05-03 17:58:02 +00:00)

In [2]: import time
time: 744 µs (started: 2022-05-03 17:58:15 +00:00)

In [3]: time.sleep(5)
time: 5 s (started: 2022-05-03 17:58:21 +00:00)

In [4]: 1/0
Traceback (most recent call last):
File ".../python3.9/site-packages/IPython/core/interactiveshell.py", line 3397, in run_code
exec(code_obj, self.user_global_ns, self.user_ns)
File "<ipython-input-6-9e1622b385b6>", line 1, in <cell line: 1>
1/0
ZeroDivisionError: division by zero
time: 1.46 ms (started: 2022-05-03 18:00:56 +00:00)
```

## Want to turn it off?

```python
In [4]: %unload_ext autotimebar
```
