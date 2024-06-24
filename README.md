Setting up a Python project involves several steps to ensure your project is organized, manageable, and ready for development. Here’s a step-by-step guide to setting up a Python project:

### 1. Create a Project Directory

First, create a directory for your project.

```sh
mkdir my_python_project
cd my_python_project
```

### 2. Set Up a Virtual Environment

A virtual environment helps to manage dependencies and avoid conflicts with other projects.

```sh
python -m venv venv
```

Activate the virtual environment:

- On Windows:
  ```sh
  .\venv\Scripts\activate
  ```
- On macOS/Linux:
  ```sh
  source venv/bin/activate
  ```

### 3. Create Essential Files

Create the essential files and directories to structure your project.

```sh
touch README.md
touch .gitignore
mkdir src
```

### 4. Initialize a Git Repository

If you plan to use version control (highly recommended):

```sh
git init
```

Add a `.gitignore` file to exclude unnecessary files from your repository. A basic `.gitignore` for Python projects might include:

```
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
dist/
*.egg-info/
```

### 5. Create a Requirements File

Create a `requirements.txt` file to list your project dependencies. You can add dependencies manually or use `pip` to generate this file.

```sh
pip freeze > requirements.txt
```

### 6. Create a Setup File

If you plan to distribute your project or make it installable, create a `setup.py` file.

```python
from setuptools import setup, find_packages

setup(
    name='my_python_project',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your project dependencies here, e.g.
        # 'numpy>=1.18.0',
    ],
)
```

### 7. Organize Your Source Code

Organize your source code in the `src` directory. A typical structure might look like this:

```
my_python_project/
│
├── src/
│   ├── my_module/
│   │   ├── __init__.py
│   │   └── main.py
│   └── tests/
│       ├── __init__.py
│       └── test_main.py
│
├── README.md
├── .gitignore
├── requirements.txt
└── setup.py
```

### 8. Add Tests

Testing is crucial for maintaining code quality. Use a testing framework like `unittest` or `pytest`.

Install `pytest` if you haven’t already:

```sh
pip install pytest
```

Create a test file in the `tests` directory:

```python
# src/tests/test_main.py
def test_example():
    assert True
```

Run tests using:

```sh
pytest src/tests
```

### 9. Write Documentation

Document your code to make it easier for others (and yourself) to understand. Use docstrings and update your `README.md` with instructions on how to install and use your project.

### 10. Use Linting and Formatting Tools

Use tools like `flake8` for linting and `black` for code formatting.

Install the tools:

```sh
pip install flake8 black
```

Run linting and formatting checks:

```sh
flake8 src/
black src/
```


In a Python project, the `requirements.txt` file is typically updated manually rather than automatically. Here’s how and when to update this file:

### 1. **After Installing New Dependencies**

Whenever you install a new package using `pip`, you should update your `requirements.txt` file to include the new dependency. For example, if you install `requests`:

```sh
pip install requests
```

You should then update `requirements.txt`:

```sh
pip freeze > requirements.txt
```

### 2. **After Updating Existing Dependencies**

If you update any existing dependencies to newer versions, you should also update `requirements.txt`. For example:

```sh
pip install --upgrade requests
```

Then, update `requirements.txt`:

```sh
pip freeze > requirements.txt
```

### 3. **Regular Maintenance**

Even if no new packages are added or updated, it’s good practice to periodically regenerate the `requirements.txt` file to ensure it accurately reflects your environment. This can be particularly important if you’re working in a team or if your project has been inactive for a while.

### 4. **Automating Updates**

While the `pip` tool itself doesn’t automatically update `requirements.txt`, you can use additional tools to help manage and update dependencies:

- **`pip-tools`**: This package helps you manage `requirements.txt` with ease. You can install it using `pip install pip-tools`.

  - To create or update `requirements.txt`, use:
    ```sh
    pip-compile
    ```

  - To install dependencies from `requirements.txt`, use:
    ```sh
    pip-sync
    ```

- **`pipdeptree`**: This tool provides a visual representation of your dependencies and can help identify which packages need to be updated. Install it using `pip install pipdeptree`.

  - To display the dependency tree, use:
    ```sh
    pipdeptree
    ```

### Example Workflow

Here’s a practical example of how you might work with `requirements.txt`:

1. **Create a Virtual Environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use .\venv\Scripts\activate
    ```

2. **Install Packages**:
    ```sh
    pip install requests
    ```

3. **Update `requirements.txt`**:
    ```sh
    pip freeze > requirements.txt
    ```

4. **Install New Package and Update `requirements.txt`**:
    ```sh
    pip install numpy
    pip freeze > requirements.txt
    ```

5. **Upgrade a Package and Update `requirements.txt`**:
    ```sh
    pip install --upgrade requests
    pip freeze > requirements.txt
    ```

6. **Use `pip-tools` for Better Management**:
    ```sh
    pip install pip-tools
    pip-compile  # This will generate the requirements.txt file
    pip-sync     # This will install/update dependencies according to requirements.txt
    ```

By following these practices, you ensure that your `requirements.txt` file stays up-to-date with the packages your project depends on, facilitating easier collaboration and deployment.


### Commands

python3 ./src/generator/main.py -org="" -input="" -output=""