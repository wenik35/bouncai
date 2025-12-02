===========
Development
===========

This guide provides best practices for developing with the BouncAI codebase.

Development Environment Setup
----------------------------

Setting up a proper development environment is essential for productive work with BouncAI.

Virtual Environment
~~~~~~~~~~~~~~~~~~

Always use a virtual environment to isolate the development dependencies:

.. code-block:: console

    # Navigate to the BouncAI directory
    cd bouncai

    # Create a virtual environment
    python -m venv dev-env

    # Activate the environment
    # On Windows:
    dev-env\Scripts\activate

    # On macOS/Linux:
    source dev-env/bin/activate

    # Install the package in development mode
    pip install -e .

Virtual environments help keep your project dependencies isolated from your system-wide Python installation and other projects, preventing dependency conflicts.

Development Workflow
-------------------

Follow these steps for a typical development workflow:

1. **Activate your virtual environment** before starting any development work:

   .. code-block:: console

       # On Windows
       dev-env\Scripts\activate

       # On macOS/Linux
       source dev-env/bin/activate

2. **Make your code changes** in the appropriate files

3. **Run tests** to ensure functionality:

   .. code-block:: console

       # Run all tests
       pytest

       # Run tests with coverage
       pytest --cov=bouncai

4. **Format your code** to maintain consistent style:

   .. code-block:: console

       # Format with black
       black bouncai tests

       # Check style with flake8
       flake8 bouncai tests

5. **Build documentation** to preview changes:

   .. code-block:: console

       # Build HTML documentation
       make docs

Managing Dependencies
--------------------

When adding new dependencies to the project:

1. **Add the dependency to setup.py** in the appropriate section:

   .. code-block:: python

       install_requires=[
           'pygame>=2.0.0',
           'new-dependency>=1.0.0',  # Add your new dependency here
       ],

2. **Update your development environment (should not be needed if you already installed it in editable mode)**:

   .. code-block:: console

       pip install -e .

3. **Record the dependency** for reproducibility:

   .. code-block:: console

       pip freeze > requirements.txt

Debugging the Game
-----------------

For debugging BouncAI:

1. **Add debug prints** at strategic points in the code
2. **Use logging** for more structured debugging:

   .. code-block:: python

       import logging

       logging.basicConfig(level=logging.DEBUG)
       logger = logging.getLogger(__name__)

       logger.debug("Player position: %s, %s", player.rect.x, player.rect.y)

3. **Use pygame's debugging tools** for visual debugging:

   .. code-block:: python

       # Draw collision boxes for debugging
       pygame.draw.rect(screen, (255, 0, 0), player.rect, 2)

Version Control Best Practices
-----------------------------

When working with version control:

1. **Create a feature branch** for each new feature or bugfix:

   .. code-block:: console

       git checkout -b feature-name

2. **Make regular commits** with descriptive messages:

   .. code-block:: console

       git commit -m "Add moving platforms with horizontal oscillation"

3. **Write tests** for new features before merging

4. **Keep branches up to date** with the main branch:

   .. code-block:: console

       git pull origin main
       git rebase main

Working with Assets
------------------

When adding or modifying game assets:

1. **Place image assets** in the `assets` directory
2. **Use relative paths** from the package root
3. **Optimize images** before adding them to the repository
4. **Document asset sources** in the code or comments

Performance Considerations
-------------------------

For maintaining good game performance:

1. **Profile the game** to identify bottlenecks:

   .. code-block:: python

       import cProfile

       cProfile.run('bouncai.run()', 'stats.prof')

       # Later analyze with
       # python -m pstats stats.prof

2. **Limit the number of sprites** active at once
3. **Use sprite groups** for efficient rendering
4. **Consider using PyGame's dirty rectangle optimization**

Additional Tips
--------------

- **Use a consistent coding style** throughout the project
- **Document your code** with docstrings and comments
- **Keep the game loop efficient** by minimizing work done each frame
- **Test on multiple platforms** if possible
- **Isolate platform-specific code** when necessary

Happy developing!
