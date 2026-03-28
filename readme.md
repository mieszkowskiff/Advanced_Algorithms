# Tree reconstruction

## Introduction

This project is a part of 2024 / 2025 summer semester course in Advanced Algorithms at Warsaw University of Technology, faculty of Mathematics and Information Sciences.

## Description

The main goal of the project is to create an algorithm, that recreates a tree (acyclic, undirected, consistent graph) knowing only the distances between leaves of this tree.

## Environment Setup & Dependencies

It is highly recommended to use a Python virtual environment to keep your dependencies isolated. Follow the instructions below based on your operating system.

### Linux / macOS

```bash
# 1. Create a virtual environment named 'venv'
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Install required dependencies
pip install numpy matplotlib

# 4. Create a folder for the instances of the problem
mkdir instances
```

## Windows

```bash
# 1. Create a virtual environment named 'venv'
python -m venv venv

# 2. Activate the virtual environment
venv\Scripts\activate

# 3. Install required dependencies
pip install numpy matplotlib

# 4. Create a folder for the instances of the problem
mkdir instances
```

## Usage

### Creating instance of the problem

Create an instance of the problem using ```create_instances.py``` program:

```{Bash}
python create_instances.py <node_number> <tree_file.txt> <instance_file.txt>
```

Where ```instance_file.txt``` will be a file
containing instance of the problem, and ```tree_file.txt``` will be a file with the sollution.

Instance of the problem is a matrix of distances between leaves, whereas sollution is the list of neighbours of each node.

### Sollution

Run:

```{Bash}
python solve.py <path_to_instance.txt> <path_to_output.txt>
```

to save sollution of the ```path_to_instance.txt``` problem under ```path_to_output.txt```

### Validation

Names (indexes) of nodes may be permuted between ```tree_file.txt``` and ```path_to_output.txt```, so you can check if the result is actually correct using:

```{Bash}
python valid_check.py <tree1.txt> <tree2.txt>
```

## Algorithm

You can read about the algorithm behind the sollution in the ```tree_recreation_documentation.pdf``` file (written in polish).
