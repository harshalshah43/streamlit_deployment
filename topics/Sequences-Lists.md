### Lists
+ Lists are indexed and ordered collection of values.
+ Values stored in the lists are modifiable.
+ Lists are iterable objects i.e they contain values that can be looped over.
+ Unlike arrays, lists allows values of multiple data types to be stored in it.

```python
x = [1,2,3.5,4.66666667,'Ubed',True,3+5j]
print(x[0])
1
print(x[3])
4.666667
print(x[-1]) # -1 means the last element, -2 means 2nd last and so on
3+5j    
```

### Slicing A List
+ x[start:stop:step]
+ Two important points
    + start and stop are index values not positions. index of first element is 0.
    + slicing always excludes element at index: stop

```python
# Examples of slicing a list
print(x[2:5]) # Display all elements from index 2 to 4
