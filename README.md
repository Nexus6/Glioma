Glioma: Collections classes for Python, inspired by the Scala Standard Library.

* Implements a subset of the Map, List, Set, Option, and Either classes from the Scala Standard Library
* All collections classes are immutable.
* Collections can be initialized with generators for lazy evaluation.
* This library has no external dependencies other than the py.test package for testing.
* Python 3.5 (unofficial support for 2.7 and PyPy)
* To run tests, execute "py.test ./tests.py" or "make test-all"
* License: Apache 2.03

Examples:
* The List class, basic usage

 *  **Instantiation**
```
    List(1,2,3)
    List(source=[1,2,3])
    List(source=(x for x in [1,2,3])
```
 *  **Mapping**
```
    List(1,2,3).map(lambda _: _ * 2) == List(2,4,6)
    List(1,2,3).map(lambda _: _ * 2).map(lambda _: _ * 3) == List(6, 12, 18)
    List(List(1,2,3), List(4,5,6)).flatMap(lambda _: _.map(lambda _: _*2))  == List(2,4,6,8,10,12)
```
 *  **Filtering**
```
    List(2,4,6,8).filter(lambda _ : _ < 5) == List(2,4)
    List(1,2,3,4).map(lambda _ : _ * 2).filter(lambda _ : _ < 5) == List(2,4)
```
 *  **Indexing**
```
    List(1,2,3)(1) == 2
```
 *  **Zipping**
```
    List(1,2).zip(List(3,4)) == List((1,3),(2,4))
    List(1,2).zip(List(3,4,5,6)) == List((1,3),(2,4))
    List(1,2).zipWithIndex() == List((1,0),(2,1))
```    
 *  **Manipulation**
```
    List(1,2,3).takeWhile(lambda _: _ < 3) == List(1,2)
    List(1,2,3,4).takeRight(0) == List()
    List(1,2,3,4).takeRight(2) == List(3,4)
    List(1, 2, 3).forall(lambda _ : _ < 4) is True
    List(1, 2, 3).forall(lambda _ : _ < 2) is False
    List(3,4,5).find(lambda _:_==4) == Some(4)
    List(3,4,5).find(lambda _:_==10) is Nothing
```
 *  **Pipeline sugar**
```
    List('a','b','c') >> (lambda _ : _*2) >> (lambda _ : _.upper()) == List('AA', 'BB', 'CC')
```
 *  **Methods exposed as properties**
```
     foo = List(5,4,3,2,1)
     foo.head == 5
     foo.tail == List(4,3,2,1)
     foo.length == foo.size == 5
     bar = List(List(1,2,3),List("A","B","C")
     bar.flatten == List(1,2,3,"A","B","C")
```

Contribution guidelines:

* Please write tests for all new functionality and modifications to existing functionality.
* Please do not make bulk formatting changes.  Instead follow the general formatting approach in use currently. Adoption of the PEP8 orthodoxy will happen eventually.
* Please stick to the Scala-esque naming conventions rather than Python ones.  For example, Set().toList rather than Set().to_list().
* Represent methods as properties as appropriate to match the Scala containers.  For example, List.length not List.length().
* The greatest needs right now, apart from new development and documentation, are 1) code-reviews to ensure that class member functions are in fact "work-alikes" for the corresponding Scala library classes, 2) that Python standard libraries and idioms are being used correctly and efficiently, and 3) that the library classes are feature-complete.  More type-checking of input parameters would be nice to have.  Python performance gurus are especially needed as few optimizations have been attempted in the code.

* Contact Nexus6 (repo owner) with questions and comments
