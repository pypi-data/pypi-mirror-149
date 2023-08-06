# GUnit
App for executing C/C++ unit tests using GDB.

Documentation: https://github.com/estcube/GUnit/wiki
## Installation
The easiest way to install Gunit is through pip: https://pypi.org/project/gunit/

```bash
pip install gunit
```

## Example
For example if OpenOCD is used as GDB server and we are testing on an ARM chip.
Please note that you need to have the openOCD server running in the background.

Secondly, all the outputs will be put into ``gunit`` directory.
To specify where the directory will be generated, define ``build_dir`` argument for the constructor.
By default, it will be your current working directory.

```python
from gunit import GUnit

# Create a GUnit object for OpenOCD
gunit = GUnit.openOCD("localhost:9000", executable='arm-none-eabi-gdb')

# Execute the tests in the compiled file
gunit.test("test.elf")

# Construct a JUnit test report
gunit.junit()
```

Here you can see a simple example of the .cpp file that could be used with the python example above.
```cpp
#include "GUnit.hpp"

gunit::test t1(
  "test1",                  // Name of the test case
  [](){                     // Lambda expression
    gunit::affirm(20) > 10; // The test case to check
  }
);

gunit::test t2("test2", [](){
  gunit::affirm(10) > 20;
  gunit::affirm(11) > 20;
});

gunit::test t3("test3", [](){
  std::list l1 = std::list<int>();
  l1.push_back(10);
  l1.push_back(12);
  l1.push_back(14);

  std::list l2 = std::list<int>();
  l2.push_back(10);
  l2.push_back(12);
  l2.push_back(14);

  gunit::affirm(l1) == l2;
});

gunit::test t4("test4", [](){
  std::list l1 = std::list<int>();
  l1.push_back(10);
  l1.push_back(12);
  l1.push_back(14);

  std::list l2 = std::list<int>();
  l2.push_back(10);
  l2.push_back(22);
  l2.push_back(34);

  gunit::affirm(l1) == l2;
});

gunit::test t5("test5", [](){
  struct a {
    int b;
    char c;
    char d;
    char e;
    char f;
  };

  struct a one(10, 'a', 'e', 'i', 'o');
  struct a two(10, 'a', 'e', 'i', 'o');

  gunit::affirm(one) == two;
});

gunit::test t6("test6", [](){
  struct a {
    int b;
    char c;
    char d;
    char e;
    char f;
  };

  struct a one(10, 'a', 'e', 'i', 'o');
  struct a two(22, 'x', 'e', 'o', 'm');

  gunit::affirm(one) == two;
});

gunit::test t7("test7", [](){
  gunit::affirm(10) > 5;
  gunit::affirm(10) >= 10;
  gunit::affirm(10) <= 10;
  gunit::affirm(10) <= 15;
  gunit::affirm(1.0) == 1.0;
  gunit::affirm(2.0) != 1.0;
});

int main() {
  gunit::suite::run(); // The test are added into the global test list on creation of the test struct
  gunit::end();        // Signal the end of the unit test
  while(1);
}
```
