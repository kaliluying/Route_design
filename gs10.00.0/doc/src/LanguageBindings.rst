.. title:: Language Bindings

.. meta::
   :description: The Ghostscript documentation
   :keywords: Ghostscript, documentation, ghostpdl





Language Bindings
=======================

The core of Ghostscript is written in C, but also supports language bindings for the following programming languages:

- C#
- Java
- Python


All of the above languages have equivalent methods as defined in the :ref:`C API<API.htm>`. Java and C# provide additional helper methods to make the use of the API easier for certain applications. These languages also provide example viewers that make use of these methods.

This developer documentation is organized by programming language type and includes API reference and sample code.

Before using the language bindings first ensure that Ghostscript is built for your platform before proceeding. See:

- :ref:`Building with Visual Studio<Make Building with Visual Studio>`

- :ref:`Building with MacOS<Make Building with MacOS>`

- :ref:`Building with Unix<Make Building with Unix>`



The C API
--------------

Ghostscript has been in development for over thirty years and is written in C. The API has evolved over time and is continually being developed. The language bindings into Ghostscript will attempt to mirror this evolution and match the current :ref:`C API<API.htm>` as much as possible.

Licensing
-----------------

Before using Ghostscript, please make sure that you have a valid license to do so. There are two available licenses; make sure you pick the one whose terms you can comply with.


Open Source license
~~~~~~~~~~~~~~~~~~~~~~~

If your software is open source, you may use Ghostscript under the terms of the GNU Affero General Public License.

This means that all of the source code for your complete app must be released under a compatible open source license!

It also means that you may not use any proprietary closed source libraries or components in your app.

Please read the full text of the AGPL license agreement from the FSF web site

If you cannot or do not want to comply with these restrictions, you must acquire a `commercial license`_ instead.

.. raw:: html

   <button class="cta orange" onclick="window.location='https://artifex.com/licensing/'">Find out more about Licensing</button>
   <p></p>


Commercial license
~~~~~~~~~~~~~~~~~~~~~~

If your project does not meet the requirements of the AGPL, please contact our sales team to discuss a commercial license. Each Artifex commercial license is crafted based on your individual use case.

.. raw:: html

   <button class="cta orange" onclick="window.location='https://artifex.com/contact/'">CONTACT US</button>
   <p></p>





Demo code
-----------

Please locate the ``demos`` folder in your ``ghostpdl`` source code download from the `GhostPDL repository`_ to find sample code demonstrating the language bindings in action.





C#
-----------

.. toctree::

  LanguageBindingsCSharp.rst


Java
-----------

.. toctree::

  LanguageBindingsJava.rst


Python
-----------

.. toctree::

  LanguageBindingsPython.rst















.. External links

.. _commercial license: https://artifex.com/licensing/commercial/
.. _.NET: https://dotnet.microsoft.com/
.. _Visual Studio: https://visualstudio.microsoft.com/
.. _Mono: https://www.mono-project.com/
.. _GhostPDL repository: https://ghostscript.com/releases/gpdldnld.html
