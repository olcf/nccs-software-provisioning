import datetime as dt

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "NCCS Software Provisioning"
copyright = f"{dt.datetime.now().year}, NCCS"
author = "NCCS"
release = "0.dev"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_copybutton"
]

templates_path = ["_templates"]
exclude_patterns = []

# copybutton configuration
copybutton_prompt_text = r"^\$ "
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
