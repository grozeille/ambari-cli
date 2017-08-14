from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
#use_plugin("python.coverage")
use_plugin("python.distutils")


name = "ambari-cli"
default_task = "publish"
version = "1.4"
summary = "useful scripts to use the Ambari API"
description = "useful scripts to use the Ambari API"
author = "mathias.kluba@gmail.com"

@init
def set_properties(project):
    project.depends_on_requirements("requirements.txt")
    pass
