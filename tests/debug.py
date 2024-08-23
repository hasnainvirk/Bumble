import pkg_resources

script = pkg_resources.load_entry_point("bumble", "console_scripts", "bumble")
script()
