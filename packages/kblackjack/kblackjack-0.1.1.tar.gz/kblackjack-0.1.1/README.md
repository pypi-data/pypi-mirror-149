# kblackjack
A simple single-player blackjack simulator

---

## Installing

You can install kblackjack using Python's [pip
module](https://pypi.org/project/pip/) following any of these three methods.

### From PyPI

This is by far the easiest method. It just takes one command:

```sh
$ python -m pip install eqnp
```

### From source repository (automatically)

This will clone the repository and build the package automatically.
```sh
$ python -m pip install git+https://git.kasad.com/kblackjack.git
```

### From source repository (manually)

This does the same steps as the last method, but allows more control.
```sh
$ git clone https://git.kasad.com/kblackjack.git
$ cd kblackjack
$ python -m pip install .
```

## Running

To run the blackjack simulator from the command line, either use the
`kblackjack` console entry point or invoke the `kblackjack` package:

```sh
$ kblackjack

# or

$ python -m kblackjack
```

To run from within a Python script, use the `kblackjack.run()` function:

```python
import kblackjack
kblackjack.run()
```

## Contributing

Contributions can be sent in patch form to <dev@kasad.com>.  
See `git-send-email(1)` or <https://git-send-email.io> for information on how
to send patches.
