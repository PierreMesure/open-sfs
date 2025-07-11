# Open SFS

This repository contains code to download texts, PDF documents and associated metadata from the Swedish code of statutes (*svensk författningssamling*).

To understand what data is available and in which format, read the documentation on [HuggingFace](https://huggingface.co/datasets/PierreMesure/open-sfs), where the data is also made available in an optimised format.

## Usage

It can now be used as a package:

```shell
pip install git+https://github.com/PierreMesure/python-sfs
```

Then, you can use the function:

```python
import sfs

test = sfs.get_newer_items("2025-06-20")
```

You can also just use the `sfs` command in your terminal:

```shell
sfs
```

The repository contains a lot more code to download PDF versions but I haven't had time to create public functions for it.

## License

This code is licensed under AGPLv3. Feel free to reuse and improve it provided you publish your improvements.
