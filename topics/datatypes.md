### Data Types in Python
#### What is a Data Type?

- A data type is the type of value that can be stored in a variable.

+ Each variable has a data type.

+ Once a value is assigned to a variable (e.g., x = 4 — datatype of 4 is integer), Python automatically decides its datatype.

+ Python first identifies the datatype of a variable and decides what kind of operations can be performed on it.

#### Example 1
```python
x = "Raj"
y = "Sharma"
print(x + y)
> Output: RajSharma
```
#### Example 2
```python
x = 5
y = 4
print(x + y)
> Output: 9
```

### Following are the Data Types in Python
#### 1. None Type

+ Represents the absence of a value.

#### 2. Numeric Types

+ int — There is no limit to the size of the int datatype. You can store both positive and negative numbers.

+ float — Can store numbers with a decimal point. It can also store numbers written in scientific notation.
Example: x = 2.5 × 10^3 is written as 2.5e3 in Python.

+ complex — Numbers with a real and imaginary part.

+ bool — Boolean values True or False.

```python
# Example: Complex Datatype
x = 2.5e3

z = 2+3j
print(z.imag)
z = complex(input("Enter a complex number"))
print(z.real+1)

# Example: Boolean DataType
a = True 
b = False
x=1  # 4 bytes 00000000 00000000 00000000 00000001
x= True # 1 
```

#### 3. Sequence Types

+ str — Strings (text).

+ bytes — Immutable sequences of bytes.

+ bytearray — Mutable sequence of bytes.

+ list — Mutable ordered collection.+ tuple — Immutable ordered collection.

+ range — Represents a sequence of numbers.

#### 4. Mapping Type

+ dict — Key-value pairs (dictionary).
```python
# Syntax - dictionary_name = {key1:value1,key2:value2}
product = {
    'code':'0013',
    'name':'toaster 3 in 1',
    'category':'home applicances',
    'price':4500
}
print('product:',product['name'],'price:',product['price'], 'inr')
> product: toaster 3 in 1 price: 4500 inr
```
### Type Conversion
We can explicitly specify the data type of a value as follows:-
```python
x = float(input("Enter any number:"))
print(type(x))
> Enter any number: 3 
> 3.0
x = 3.6
y = int(x)
print(y)
> 3
name = str('hi my name is Harshal')
> hi my name is Harshal
```