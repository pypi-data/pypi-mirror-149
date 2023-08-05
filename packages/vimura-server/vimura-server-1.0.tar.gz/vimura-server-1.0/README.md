# Vimura server

This is an alternative server for Emacs
[pdf-tools](https://github.com/vedang/pdf-tools).

The motivation for creating this alternative extra server, is that it lowers the
barrier for adding extra features (like arrow and free text annotations) into
the server. The [PyMuPDF](https://pypi.org/project/PyMuPDF/) is a great and
powerful library, which uses python as a wrapper language for using the Poppler
library. It is still very fast as it just provides a convenient scripting
language for using the underlying C code. No advanced C knowledge is required
because these 'hard parts' have been taken care of by its maintainers.

Many thanks to Jorj X. McKie, for creating the PyMuPDF library and providing
assistance.
