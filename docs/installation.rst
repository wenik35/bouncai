.. highlight:: shell

============
Installation
============

Prerequisites
-------------

Before installing BouncAI, ensure you have the following prerequisites:

- Python 3.6 or higher
- pip (Python package installer)
- Git
- virtualenv or venv (recommended for creating virtual environments)

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

Using Virtual Environments
-------------------------

It's strongly recommended to use a virtual environment when working with Python packages to isolate dependencies and avoid conflicts between projects.

What is a virtual environment?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A virtual environment is a self-contained directory that contains a Python installation for a particular version of Python, plus a number of additional packages. Using a virtual environment for BouncAI ensures that its dependencies won't interfere with other Python projects on your system.

Creating a virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create a virtual environment using either the built-in `venv` module (Python 3.3+) or the `virtualenv` package:

Using venv (recommended for Python 3.3+):

.. code-block:: console

    $ python -m venv bouncai-env

Using virtualenv (if you have it installed):

.. code-block:: console

    $ virtualenv bouncai-env

Activating the virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before installing BouncAI, you need to activate the virtual environment:

On Windows:

.. code-block:: console

    $ bouncai-env\Scripts\activate

On macOS and Linux:

.. code-block:: console

    $ source bouncai-env/bin/activate

Your command prompt should change to indicate that the virtual environment is active, typically by adding the environment name to the beginning of the prompt.

Windows PowerShell Installation Guide
------------------------------------

For Windows users using PowerShell, here's a comprehensive step-by-step installation guide:

**Prerequisites Check**

First, verify that Python and Git are installed on your system:

.. code-block:: powershell

    PS> python --version
    PS> git --version

If either command fails, install the missing components:
- Download Python from https://www.python.org/downloads/ (ensure "Add to PATH" is checked during installation)
- Download Git from https://git-scm.com/download/win

**Step 1: Open PowerShell**

Open PowerShell as a regular user (Administrator privileges are not required). You can do this by:
- Pressing `Win + X` and selecting "Windows PowerShell"
- Or searching for "PowerShell" in the Start menu

**Step 2: Navigate to your desired directory**

.. code-block:: powershell

    PS> cd C:\Users\YourUsername\Documents
    # Or navigate to any directory where you want to install BouncAI

**Step 3: Clone the repository**

.. code-block:: powershell

    PS> git clone https://gitlab.hrz.tu-chemnitz.de/vorlesungen/kuenstliche_intelligenz/ws25-26/bouncai.git
    PS> cd bouncai

**Step 4: Create a virtual environment**

.. code-block:: powershell

    PS> python -m venv bouncai-env

**Step 5: Activate the virtual environment**

.. code-block:: powershell

    PS> .\bouncai-env\Scripts\Activate.ps1

**Note**: If you encounter an execution policy error, you may need to temporarily allow script execution:

.. code-block:: powershell

    PS> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

After activation, your prompt should change to show `(bouncai-env)` at the beginning.

**Step 6: Upgrade pip (recommended)**

.. code-block:: powershell

    PS> python -m pip install --upgrade pip

**Step 7: Install BouncAI**

.. code-block:: powershell

    PS> pip install -e .

**Step 8: Verify installation**

.. code-block:: powershell

    PS> python -m bouncai

This should launch the BouncAI game window.

**Step 9: Deactivate when finished**

When you're done working with BouncAI:

.. code-block:: powershell

    PS> deactivate

**Future Usage**

To run BouncAI again in the future:

.. code-block:: powershell

    PS> cd C:\Users\YourUsername\Documents\bouncai
    PS> .\bouncai-env\Scripts\Activate.ps1
    PS> bouncai

Installation Steps (General)
---------------------------

For non-Windows systems or users preferring command-line instructions, the general installation steps are:

1. Clone the repository:

.. code-block:: console

    $ git clone https://gitlab.hrz.tu-chemnitz.de/vorlesungen/kuenstliche_intelligenz/ws25-26/bouncai.git
    $ cd bouncai

2. With your virtual environment activated, install in development mode:

.. code-block:: console

    $ pip install -e .

This will install the package in development mode, which means any changes you make to the code will be immediately reflected when you run the game.

Deactivating the virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you're done working with BouncAI, you can deactivate the virtual environment by simply running:

.. code-block:: console

    $ deactivate

Verifying Installation
---------------------

To verify that BouncAI is correctly installed, make sure your virtual environment is activated and then run:

.. code-block:: console

    $ python -m bouncai

This should launch the game window if the installation was successful.

Development Workflow
------------------

When developing or extending BouncAI, follow these best practices:

1. Always activate your virtual environment before working:

   .. code-block:: console

       $ source bouncai-env/bin/activate  # macOS/Linux
       $ bouncai-env\Scripts\activate     # Windows

2. Install any additional development dependencies:

   .. code-block:: console

       $ pip install pytest pytest-cov black flake8

3. Make your code changes and test them immediately (thanks to the development installation with `-e`).

4. When adding new dependencies to the project, update `setup.py` and then run:

   .. code-block:: console

       $ pip install -e .

5. Record your dependencies for reproducibility:

   .. code-block:: console

       $ pip freeze > requirements.txt

Troubleshooting
--------------

**Windows PowerShell Specific Issues:**

- **Execution Policy Error**: If you get "cannot be loaded because running scripts is disabled", run:

  .. code-block:: powershell

      PS> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

- **Python not found**: Ensure Python is added to your PATH. Reinstall Python with "Add to PATH" checked.

- **Git not found**: Install Git for Windows from https://git-scm.com/download/win

- **Virtual environment activation fails**: Make sure you're using the correct path:

  .. code-block:: powershell

      PS> .\bouncai-env\Scripts\Activate.ps1

- **Permission denied errors**: Ensure you're not running PowerShell as Administrator unless necessary.

**General Issues:**

If you encounter issues with Pygame installation, ensure you have the necessary system dependencies installed. These vary by operating system:

- **Ubuntu/Debian**: `sudo apt-get install python3-pygame`
- **macOS**: You may need to install SDL dependencies via brew
- **Windows**: The pip installation should handle all dependencies

Virtual Environment Issues:
- If you see "command not found" for `virtualenv`, install it with `pip install virtualenv`
- If your virtual environment isn't isolating packages properly, try recreating it
- If you're working with multiple Python versions, ensure you're creating the environment with the correct version

For other issues, check the project repository for known problems and solutions.
