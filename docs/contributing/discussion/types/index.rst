Detection of type hints using mypy
====================================
Python is an explanatory language that does not need to declare the types of variables. 
This facilitates the writing of our program, but it brings inconvenience when reading and understanding the code. 
However, python can still mark the types when writing, which increases the readability of our code. 
`Mypy <https://mypy.readthedocs.io/en/stable/introduction.html>` is a detection of manually marked variable declarations.


Once installed, he will test the artificially marked types. And provide his opinion on whether this type is correct or not. 

Mypy requires Python 3.5 or later to run. Once you've installed Python 3, install mypy using pip::

    $ python -m pip install mypy

Once mypy is installed, run it by using the mypy tool::

    $ mypy test.py

This command makes mypy type check your :code:`test.py` file and print out any errors it finds. Mypy will type check your code statically: this means that it will check for errors without ever running your code, just like a linter.
This means that you are always free to ignore the errors mypy reports and treat them as just warnings, if you so wish: mypy runs independently from Python itself.
However, if you try directly running mypy on your existing Python code, it will most likely report little to no errors: you must add type annotations to your code to take full advantage of mypy.

For example, The following code::
          
             a:str=1
             print(type(a))

As a result, our code type is int::
            <class 'int'>

But here we get a warning from mypy that there is a problem with the variables we marked::

            Incompatible types in assignment (expression has type "int", variable has type "str") (1:7)

If we change the code type to the correct type::
            
           a:int=1
           print(type(a))

Mypy will give us such an answer::

          Mypy found no problems


We declare the correct variable type, which is also consistent with mypy's detection.




