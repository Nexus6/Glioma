from glioma.containers import   Map, List, Set
from glioma.option import       Option, Some, Nothing
from glioma.either import       Left, Right

#from glioma_extras import match
from collections import namedtuple
import pytest

def timestwo(x) : return x * 2
def lessten(x)  : return x < 10

def test_option():
    assert Option("foo")                                == Option("foo")
    assert Option("foo")                                != Option("bar")
    assert Option(None)                                 is Nothing
    assert Some(1).toList                               == List(1)
    assert Some("foo").get                              == "foo"
    assert Some("foo").orElse(Some("bar"))              == Some("foo")
    assert Some("foo").orElse(lambda: Some("bar"))      == Some("foo")
    assert Some("foo").getOrElse(lambda: "bar")         == "foo"
    assert Some("foo").getOrElse("bar")                 == "foo"
    assert Some(1).mkString("+")                        == "1"
    assert Some(2).orNone                               == Some(2)
    assert Some("abc").orElse(lambda: Some("foo"))      == Some("abc")
    assert Some("abc").orElse(Some("foo"))              == Some("abc")
    assert Some("abc").orElse("foo")                    == Some("abc")
    assert Some("foo").map(lambda _: _.upper())         == Some("FOO")
    assert Some(1).takeWhile(lambda _ : True)           == List(1)
    assert Some(1).takeWhile(lambda _ : False)          == List()
    assert [x for x in Some(1)]                         == [1]
    assert Nothing.orNone                               is None
    assert Nothing.getOrElse(lambda: "bar")             == "bar"
    assert Nothing.getOrElse("bar")                     == "bar"
    assert Nothing.orElse(lambda: Option("abc"))        == Some("abc")
    assert Nothing.orElse(Option("abc"))                == Some("abc")
    assert Nothing.mkString("+")                        == ""
    assert Nothing.toString                             == "Nothing"
    assert Nothing.toList                               == List()
    assert Nothing.takeWhile(lambda _ : True)           == List()
    assert Nothing.takeWhile(lambda _: False)           == List()
    assert [x for x in Nothing]                         == []
    with   pytest.raises(TypeError):                    Nothing.get
    with   pytest.raises(TypeError):                    Nothing.orElse("abc").get

def test_map():
    def plusX(k, v): return (k, str(v) + 'X')
    def plusY(k, v): return (k, str(v) + 'Y')

    assert Map()                                        == Map()
    assert Map().length                                 == 0
    assert Map().forall(lambda x,y: True)               is True
    assert Map().forall(lambda x,y: False)              is True
    assert Map().mkString("+")                          == ""
    assert Map(('a',1),('b', 2))                        == Map(source={'a':1,'b':2})
    assert Map(source={"a": 1, "b":2})                  == Map(source={"a": 1, "b":2})
    assert Map(source={"a": 1, "b":3})                  != Map(source={"a": 1, "b":2})
    assert Map(source={"a": 1, "b":2}).map(lambda x,y: (x+x,2*y))  == Map(source={"aa":2, "bb": 4})
    assert Map(source={"a": 1, "b": 2}) >> (lambda x, y: (x + x, 2 * y)) == Map(source={"aa": 2, "bb": 4})
    assert Map(("a", 1), ("b", 2)).map(lambda x,y: (x + x, 2 * y)) == Map(source={"aa": 2, "bb": 4})
    assert Map(("a", 1), ("b", 2)) >> (lambda x, y: (x + x, 2 * y)) == Map(source={"aa": 2, "bb": 4})
    assert Map(source={"a": 1, "b":2}).filter(lambda x,y: (y > 1)) == Map(source={"b": 2})
    assert Map().filter(lambda x,y : (y > 1))         == Map()
    m = Map(source={1:2,3:4})

    assert m(1)                                         == 2
    assert m(3)                                         == 4
    with pytest.raises(KeyError):                       m(5)
    assert m.get(1)                                     == Some(2)
    assert m.get(5)                                     is Nothing
    assert m.mkString("+")                              == "(1, 2)+(3, 4)"
    assert m.getOrElse(1,10)                            == 2
    assert m.getOrElse(10,20)                           == 20
    assert Map().getOrElse(10,20)                       == 20
    assert m.contains(1)                                is True
    assert m.isDefinedAt(1)                             is True
    assert m.isDefinedAt(20)                            is False
    assert Map().isDefinedAt(20)                        is False
    assert m.toList                                     == List((1,2),(3,4))
    m = Map((1,2),(3,4))
    assert m(1)                                         == 2
    assert m(3)                                         == 4
    assert m.head                                       == (1,2)
    assert m.last                                       == (3,4)
    assert m.size                                       == 2
    assert m.find(lambda k,v: k == 3)                 == Some((3,4))
    assert m.find(lambda k,v: k == 5)                 is Nothing
    assert Map().find(lambda k,v: k == 5)             is Nothing
    assert m.count(lambda k,v: k > 0)                 == 2
    assert m.count(lambda k,v: k > 1)                 == 1
    assert m.count(lambda k,v: k > 10)                == 0
    assert m.count(lambda k,v: v == 4)                == 1
    assert m.count(lambda k,v: True)                  == 2
    assert m.count(lambda k,v: False)                 == 0
    assert m.forall(lambda k,v: k <10)                is True
    assert m.forall(lambda k,v: k < 3)                is False
    assert m.takeWhile(lambda k,v : k < 3)            == Map((1,2))
    assert m.takeWhile(lambda k,v: k < 1)             == Map()
    assert m.toString                                   == "Map((1, 2), (3, 4))"
    assert m.zipWithIndex                               == Map(((1,2), 0), ((3,4), 1))
    assert m.zip(List('c', 'd'))                        == Map(((1,2), 'c'), ((3,4), 'd'))
    assert Map().toString                               == "Map()"
    assert Map().takeWhile(lambda k,v : k < 3)        == Map()
    assert Map().count(lambda k,v: k > 10)            == 0
    assert Map().count(lambda k,v: True)              == 0
    assert Map().count(lambda k,v: False)             == 0
    assert (Map(('a',1), ('b',2)) >> plusX >> plusY).dict == {'a' : '1XY', 'b' : '2XY'}

def test_list():
    def plusX(v):   return str(v) + 'X'
    def plusY(v):   return str(v) + 'Y'

    assert List()                                       == List()
    assert List().length                                == 0
    assert List().forall(lambda _ : True)               is True
    assert List().forall(lambda _ : False)              is True
    assert List().count(lambda _: _ > 2)                == 0
    assert List().mkString("+")                         == ""
    assert List().mkString()                            == ""
    assert List().takeWhile(lambda _: True)             == List()
    assert List().takeWhile(lambda _: False)            == List()
    assert List(1,2,3).takeWhile(lambda _: _ < 3)       == List(1,2)
    assert List(3,2,1).takeWhile(lambda _: _ < 3)       == List()
    assert List(source=[1,2,3])                         == List(source=(1,2,3))
    assert List(source=[1,2,3])                         == List(1,2,3)
    assert List(source=[])                              == List()
    assert List(source=())                              == List()
    assert List(1,2,3)                                  != List(1,2,4)
    assert List(1, 2, 3).forall(lambda _ : _ < 4)       is True
    assert List(1, 2, 3).forall(lambda _ : _ < 2)       is False
    assert [x for x in List(1,2)]                       == [1,2]
    assert List(1,2,3).map(timestwo)                    == List(2,4,6)
    assert List(1,2,3,4,5,6).map(timestwo).filter(lessten).map(timestwo) == List(4, 8, 12, 16)

    def less20(_): return _ < 20
    assert (List(1, 2, 3, 4, 5, 6) >> timestwo >> timestwo >= less20) == List(4, 8, 12, 16)
    assert (List(1, 2, 3, 4, 5, 6) >> timestwo >> timestwo).filter(lambda _:_<20) == List(4, 8, 12, 16)

    assert List(1,2,3).filter(lambda _: _ <= 2)         == List(1,2)
    assert List().filter(lambda _: _ <= 2)              == List()
    assert List().find(lambda _: _>0)                   is Nothing
    assert List(1,2,3).find(lambda _: _ == 2)           == Some(2)
    assert List(1,2,3).find(lambda _: _ == 10)          is Nothing
    assert List(1,2,3).reduce(lambda x,y: x+y)          == 6
    assert List(1,2,3,4).mkString("+")                  == "1+2+3+4"
    assert List(1,2,3,4).mkString()                     == "1234"
    assert List(1,2,3,4).count(lambda _: _>2)           == 2
    assert List(1,2,3,4).count(lambda _: _>0)           == List(1,2,3,4).length
    assert List(1,2,3,4).count(lambda _: _>5)           == 0
    assert List(1,2,3,4).head                           == 1
    assert List(1,2,3,4).last                           == 4
    assert List(1,2,3,4).tail                           == List(2,3,4)
    assert List(1,2,3,4).size                           == 4
    assert List(3,2,1).sorted                           == List(1,2,3)
    assert List(3,2,1).sortedWith(key=lambda _:_)       == List(1,2,3)
    assert List(1,2,3,4).take(0)                        == List()
    assert List(1,2,3,4).take(1)                        == List(1)
    assert List(1,2,3,4).take(2)                        == List(1,2)
    assert List(1,2,3,4).take(7)                        == List(1,2,3,4)
    assert List(1,2,3,4).take(-1)                       == List()
    assert List(1,2,3,4).takeRight(0)                   == List()
    assert List(1,2,3,4).takeRight(2)                   == List(3,4)
    assert List(1,2,3,4).takeRight(-1)                  == List()
    assert List(1,2,3,4).takeRight(10)                  == List(source=List(1,2,3,4).list)
    assert List(1,2,3,4).sum                            == 10
    listlist = List(List(1,2,3), List(4,5,6))
    assert listlist                                     != List(1,2,3)
    assert listlist(0)(1)                               == 2
    assert listlist.flatten                             == List(1,2,3,4,5,6)
    assert listlist.flatMap(lambda _: _.map(lambda _: _*2))  == List(2,4,6,8,10,12)
    assert List(1,2).length                             == 2
    assert List(1,2).toString                           == 'List(1, 2)'
    assert List(1,2).zip(List(3,4))                     == List((1,3),(2,4))
    assert List(1,2).zip(List(3,4,5,6))                 == List((1,3),(2,4))
    assert List(1,2).zipWithIndex()                     == List((1,0),(2,1))
    
    chars = List('a','b','c','d')
    assert chars.indexWhere(lambda _ : _ == 'c')        == 2
    assert chars.indexWhere(lambda _ : _ == 'z')        == -1
    assert chars.indexWhere(lambda _ : _ == 'c', 0)     == 2
    assert chars.indexWhere(lambda _ : _ == 'c', 1)     == 2
    assert chars.indexWhere(lambda _ : _ == 'c', 2)     == 2
    assert chars.indexWhere(lambda _ : _ == 'c', 3)     == -1
    assert chars.indexWhere(lambda _ : _ == 'c', 10)    == -1
    assert chars.indexWhere(lambda _ : _ == 'c', -1)    == -1
    assert chars.indexOf('c')                           == 2
    assert chars.indexOf('z')                           == -1
    assert chars.indexOf('c', 0)                        == 2
    assert chars.indexOf('c', 1)                        == 2
    assert chars.indexOf('c', 2)                        == 2
    assert chars.indexOf('c', 3)                        == -1
    assert chars.indexOf('c', 10)                       == -1
    assert chars.indexOf('c', -1)                       == -1

    assert List(1,2).toSet                              == Set(1,2)
    assert List(1,2).sum                                == 3
    assert List(1,2).contains(2)                        is True
    assert List(1,2).contains(100)                      is False
    assert List(Some(123), Some(456)).flatten           == List(123, 456)
    assert List(Some(123), Set(None)).flatten           == List(123,None)
    assert List(Some(123), Set(Nothing)).flatten        == List(123,Nothing)
    assert List().flatten                               == List()
    assert List(1).tail                                 == List()
    with   pytest.raises(IndexError):                   List()(1)
    with   pytest.raises(IndexError):                   List().head
    with   pytest.raises(IndexError):                   List().tail

    assert List().contains(1)                           is False
    assert (List(1,2,3) >> plusX >> plusY).list         == ['1XY', '2XY', '3XY']

def test_set():
    def plusX(v):   return str(v) + 'X'
    def plusY(v):   return str(v) + 'Y'

    assert Set()                                        == Set()
    assert Set().forall(lambda _: True)                 is True
    assert Set().forall(lambda _: False)                is True
    assert Set().contains(1)                            is False
    assert Set().mkString("+")                          == ""
    assert Set().mkString()                             == ""
    assert Set().takeWhile(lambda _: True)              == Set()
    assert Set().takeWhile(lambda _: False)             == Set()
    assert Set(1,2).takeWhile(lambda _: True)           == Set(1,2)
    assert Set().takeWhile(lambda _: False)             == Set()
    assert [x for x in List(1, 2)]                      == [1, 2]
    assert Set(1,2,3,4).sum                             == 10
    assert Set(1,2,3,4).length                          == 4
    assert Set(1,2)(2)                                  is True
    assert Set().forall(lambda _ : _ < 2)               is True
    assert Set(1,2,3).map(lambda _: _*2)                == Set(2,4,6)
    assert Set(1,2,3,4,5,6).map(timestwo).filter(lessten).map(timestwo) == Set(4,8,12,16)
    assert Set(1,2,3).reduce(lambda x,y: x+y)           == 6
    assert Set(1,2,3,4,5).filter(lambda _: _ < 4)       == Set(1,2,3)
    assert Set(1,2,3,4,5).filter(lambda _: _ < 4)       == Set(source={1,2,3})
    assert Set().filter(lambda _: _ < 4)                == Set(source=set(()))
    assert Set().find(lambda _: _ > 0)                  is Nothing
    assert Set(1, 2, 3).find(lambda _: _ == 2)          == Some(2)
    assert Set(1, 2, 3).find(lambda _: _ == 10)         is Nothing
    assert Set(source=set([List(1, 2, 3), Set(4, 5, 6)])).flatten == Set(1,2,3,4,5,6)
    assert Set(source={List(1, 2, 3), Set(4, 5, 6),}).flatten\
                                                        == Set(1, 2, 3, 4, 5, 6)
    assert Set(source={List(1, 2, 3), Set(4, 5, 6)},).flatten \
                                                        == Set(1, 2, 3, 4, 5, 6)
    assert Set(Set(1,2,3), Set(4,5,6)).zipWithIndex     == Set((Set(4, 5, 6), 1), (Set(1, 2, 3), 0))
    assert Set(source={Set(1,2,3), Set(4,5,6)}).flatMap(lambda _: _.map(lambda _: Nothing)) == Set(Nothing)
    assert Set(source={Set(1, 2, 3), Set(4, 5, 6)}).flatMap(lambda _: _.map(lambda _: None)) == Set(None)

    s1 =   Set(source={Set(1, 2, 3), Set(4, 5, 6)}).flatMap(lambda _: _.map(lambda _: _ * 2))
    s2 =   Set(2,4,6,8,10,12)
    assert (2 in s2)                                    == True
    assert s1                                           == s2
    assert s2.head                                      == 2
    assert s2.tail.size                                 == 5
    assert s2.tail.tail.size                            == 4
    assert s2.last                                      == 12
    assert s2.contains(2)                               is True
    assert s2.contains(100)                             is False
    assert s2.forall(lambda _ : _ < 20)                 is True
    assert s2.forall(lambda _ : _ < 10)                 is False
    assert s2.toString                                  == 'Set(2, 4, 6, 8, 10, 12)'
    assert s2.takeWhile(lambda _ : _ < 8)               == Set(2,4,6)
    assert s2.count(lambda _: _ > 8)                    == 2
    assert s2.length                                    == 6
    assert s2.count(lambda _: _ > 0)                    == s2.length
    assert s2.count(lambda _: _ > 20)                   == 0
    assert Set().count(lambda _: _ > 2)                 == 0
    assert Set().length                                 == 0
    assert Set(1,2).length                              == 2
    assert Set(1,2).size                                == 2
    assert Set(1,2).mkString("+")                       == "1+2"
    assert Set(1,2).mkString()                          == "12"
    assert Set(1,2).zip(List(3,4))                      == Set((1,3),(2,4))
    assert Set(1,2).zip(List(3,4,5,6))                  == Set((1,3),(2,4))
    assert Set(1,2).zipWithIndex                        == Set((1,0),(2,1))
    assert Set().union(Set())                           == Set()
    assert Set(1,2).union(Set())                        == Set(1,2)
    assert Set().union(Set(1,2))                        == Set(1,2)
    assert Set(1,2).union(Set(3,4))                     == Set(1,2,3,4)
    assert Set(1,2).union(Set(2,3))                     == Set(1,2,3)
    assert Set().intersect(Set())                       == Set()
    assert Set(1, 2).intersect(Set())                   == Set()
    assert Set().intersect(Set(1, 2))                   == Set()
    assert Set(1, 2).intersect(Set(3, 4))               == Set()
    assert Set(1, 2).intersect(Set(2, 3))               == Set(2)
    
    s3 = Set(source=(x for x in [1,2,3]))
    assert s3.toString                                  != "Set(1, 2, 3)"
    assert (Set(1, 2, 3) >> plusX >> plusY).set         == set(['1XY', '2XY', '3XY'])
    with   pytest.raises(IndexError):                   Set().head
    with   pytest.raises(IndexError):                   Set().last

def test_either():
    assert Left()                                       == Left()
    assert Left("foo")                                  != Left("bar")
    assert Right("foo")                                 != Right("bar")
    assert Left()                                       != Right()
    assert Right()                                      != Left()
    assert Left()                                       != Right()
    assert Left().isLeft                                is True
    assert Left().isRight                               is False
    assert Right().isLeft                               is False
    assert Right().isRight                              is True

    assert Left("ab") .fold(lambda _ : 1, lambda _ : 2) == 1
    assert Right("ab").fold(lambda _ : 1, lambda _ : 2) == 2
