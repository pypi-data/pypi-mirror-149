# telescope-distance

Telescope-distance is a Python package for time-series clustering based on the telescope distance [[1]](#1) 
as a metric over the space of infinite dimensional measures.


## Installation

### Dependencies

telescope-distance requires:

- Python (>= 3.5)
- NumPy 
- SciPy
- SciKit-learn

### User installation
Make sure that you have Python 3.5+ and pip installed. We recommend installing the stable version of 
telescope-distance with ``pip``:

    $ pip install telescope-distance

Alternatively, you can also clone the source of the latest version with:
    
    $ git clone https://github.com/soheil-arab/telescope-distance

Then install directly from source with:

    $ python setup.py install    

## Examples
A **short example** is as below.
```python
import functools
from sklearn import svm
from telescope_distance import telescope
from telescope_distance.generators import generators

#generates two sample path from two arbitrary 3rd order markov chain 
mc_1 = generators.MarkovChain(2,3) 
x = mc_1.generate_sample_path(1000)
mc_2 = generators.MarkovChain(2,3)
y = mc_2.generate_sample_path(1000)

weights_fn = lambda k: k**-2
clf_constructor = functools.partial(svm.SVC,
                                    kernel='rbf',
                                    max_iter=-1)
TD = telescope.TelescopeDistance(clf_constructor, weights_fn)

print(f'empirical estimate of TD between MC_1 and MC_2 is {TD.distance(x,y)}')
```
## References
<a id="1">[1]</a> Ryabko, Daniil, and Jérémie Mary. "A binary-classification-based metric between time-series distributions and its use in statistical and learning problems." The Journal of Machine Learning Research 14.1 (2013): 2837-2856.