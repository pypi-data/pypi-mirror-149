# NeuralSpace CLI
This is a command line tool to access NeuralSpace APIs. Checkout our [docs here](https://docs.neuralspace.ai) 

## Prerequisites

- Python3.7+

## Install

```shell script
pip install neuralspace
```

## Usage

### Login

Login to the NeuralSpace platform from your shell.

```shell script
NEURALSPACE_EMAIL_ID="YOUR-NEURALSPACE-EMAIL-ID"
NEURALSPACE_PASSWORD="YOUR-NEURALSPACE-PASSWORD"

neuralspace login -e $NEURALSPACE_EMAIL_ID -p $NEURALSPACE_PASSWORD
```

### Supported Apps

- `nlu`

[Build your first NLU model with the NeuralSpace platform](docs.neuralspace.ai/natural-language-understanding/quickstarts/python)

### NLU

Supported commands

```shell script
neuralspace nlu
```

use the `--help` argument to get a list of command arguments



# TODO:
- type in training data after conversion