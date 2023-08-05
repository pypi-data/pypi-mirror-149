# The MIT License (MIT)
#
# Copyright (c) 2012-2022 Thorsten Simons (sw@snomis.eu)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

class Gvars:
    """
    Holds version related constants.
    """

    # version control
    s_version = "2.0.11"
    s_builddate = '2022-05-03'
    s_build = "{}/Sm".format(s_builddate)
    s_minPython = "3.7"
    s_description = "HCP Metadata Query Tool"
    s_dependencies = ['']

    # constants
    Version = "v.{} ({})".format(s_version, s_build)
    Description = 'hcpmqe - HCP Metadata Query Tool'
    Author = "Thorsten Simons"
    AuthorMail = "sw@snomis.eu"
    AuthorCorp = ""
    AppURL = "https://hcpmqe.readthedocs.io"
    License = "MIT"
    Executable = "hcpmqe"
