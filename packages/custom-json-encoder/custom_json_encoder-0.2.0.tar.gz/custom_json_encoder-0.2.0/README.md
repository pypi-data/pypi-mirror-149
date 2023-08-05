# Custom JSON Encoder

A JSON encoder that allows customizing the indentation based on the content and the width of the line.

See [the command-line tool](custom_json_encoder/__main__.py) to understand how to use the [CustomJSONEncoder class](custom_json_encoder/__init__.py). This tool is a patch from [json/tool.py](https://github.com/python/cpython/blob/3.10/Lib/json/tool.py), so follow the `#region` and `#endregion` comments to understand the differences.

## Command Line Interface

Instead of using the standard [JSON tool](https://docs.python.org/3/library/json.html#module-json.tool)

```bash
$ python -m json.tool demo.json --indent 4
{
    "menu": {
        "id": "file",
        "value": "File",
        "popup": {
            "menuitem": [
                {
                    "value": "New",
                    "onclick": "CreateNewDoc()"
                },
                {
                    "value": "Open",
                    "onclick": "OpenDoc()"
                },
                {
                    "value": "Close",
                    "onclick": "CloseDoc()"
                }
            ]
        }
    }
}
```

you can use the [custom JSON encoder](custom_json_encoder/__main__.py) instead with the same flags

```bash
$ python -m custom_json_encoder demo.json --indent 4
{
    "menu": {
        "id": "file",
        "value": "File",
        "popup": {
            "menuitem": [
                {
                    "value": "New",
                    "onclick": "CreateNewDoc()"
                },
                {
                    "value": "Open",
                    "onclick": "OpenDoc()"
                },
                {
                    "value": "Close",
                    "onclick": "CloseDoc()"
                }
            ]
        }
    }
}
```

This tool provides the same functionality as the standard JSON tool

```bash
$ python -m custom_json_encoder -h
usage: custom_json_encoder [-h] [--sort-keys] [--no-ensure-ascii] [--json-lines] [--indent INDENT | --indent-after KEY | --tab | --compact] [--indent-after-width AMOUNT]
                           [--indent-after-indentation AMOUNT]
                           [infile] [outfile]

A simple command line interface for json module to validate and pretty-print JSON objects.

positional arguments:
  infile                a JSON file to be validated or pretty-printed
  outfile               write the output of infile to outfile

options:
  -h, --help            show this help message and exit
  --sort-keys           sort the output of dictionaries alphabetically by key
  --no-ensure-ascii     disable escaping of non-ASCII characters
  --json-lines          parse input using the JSON Lines format. Use with --no-indent or --compact to produce valid JSON Lines output.
  --indent INDENT       separate items with newlines and use this number of spaces for indentation
  --indent-after KEY    indent after the given key using --indent-after-indentation spaces
  --tab                 separate items with newlines and use tabs for indentation
  --compact             suppress all whitespace separation (most compact)
  --indent-after-width AMOUNT
                        set the width of the output line when --indent-after is active
  --indent-after-indentation AMOUNT
                        use this number of spaces for indentation when --indent-after is active
```

except for the `--indent-after`, `--indent-after-width` and `--indent-after-indentation` flags, which allow indenting ONLY after the given key or after reaching the given width.

```bash
$ python -m custom_json_encoder demo.json --indent-after menuitem --indent-after-width 50 --indent-after-indentation 4
{
    "menu": {"id": "file", "value": "File",
        "popup": {"menuitem": [
                {"value": "New", "onclick":
                    "CreateNewDoc()"},
                {"value": "Open", "onclick":
                    "OpenDoc()"},
                {"value": "Close", "onclick":
                    "CloseDoc()"}
            ]}}
}
```
