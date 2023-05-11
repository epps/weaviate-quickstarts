# Weaviate Quickstart Tutorials Evaluation

This repo hold some exploratory code that's largely copied wholesale from [Weaviate's Quickstart tutorials](https://weaviate.io/developers/weaviate/quickstart) while evaluating it.

## Prerequisites

### Virtual environment

Create a virtual environment by running:

```shell
python -m venv .venv
```

Then activate the virtual environment and install all requirements:

```shell
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Credentials

To use this repo, you'll need:

* A sandbox [Weaviate Cloud Services (WCS)](https://weaviate.io/developers/wcs/quickstart) instance with authentication enabled
* An [OpenAI API key](https://platform.openai.com/docs/api-reference/authentication)

With these prereqs in hand, run:

```shell
cp template.env .env
```

Then populate the required environment variables.

## Running the Examples

You're now ready to run `quickstart.py` with one of the following flags:

* `--load`: runs the data loader script to populate the cluster; this should only be run once
* `--neartext`: runs the `nearText` example
* `--nearvector`: runs the `nearVector` example

For example:

```shell
python quickstart.py --neartext
```
