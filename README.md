# pandas read_csv demo

This repository demonstrates the behavior covered in my [Issue](https://github.com/pandas-dev/pandas/issues/48487) which was later addressed in a [PR](https://github.com/pandas-dev/pandas/pull/48597) by @AlexKirko

Pandas has a great function for reading data from a csv into a dataframe and automatically assigning datatypes to the columns. I do, however, have one issue with how this function handles certain keywords in string fields. Let's look at an example.

## Example

I get a csv from another piece of software that outputs strings, ints, floats, and enums. It also can output just the integer and string portions of an enum.

| stringField | intField | floatField | enumField | enumField_int | enumField_str |
| ----------- | -------- | ---------- | --------- | ------------- | ------------- |
| pandas      | 0        | 0.5        | 0:false   | 0             | false         |
| hello       | 1        | 1.5        | 1:true    | 1             | true          |
| world       | 2        | 2.5        | 2:unknown | 2             | unknown       |

To read this csv into a dataframe, first import pandas.

```
#!/usr/bin/python3

import pandas as pd
```

Then use the read_csv function to read the table into a dataframe.

```
df = pd.read_csv('demo_more.csv')
```

Check the types assigned with the dtypes function.

```
print(df.dtypes)
```

The following will be returned.

```
stringField       object
intField           int64
floatField       float64
enumField         object
enumField_int      int64
enumField_str     object
dtype: object
```

As expected, stringField is a string, intField is an int, floatField is a float, enumField is a string, enumField_int is an int, and enumField_str is a string.

This behavior should be the same for a smaller set of data, like the following.

| stringField | intField | floatField | enumField | enumField_int | enumField_str |
| ----------- | -------- | ---------- | --------- | ------------- | ------------- |
| pandas      | 0        | 0.5        | 0:false   | 0             | false         |
| hello       | 1        | 1.5        | 1:true    | 1             | true          |

```
df = pd.read_csv('demo_less.csv')
print(df.dtypes)
```

However, the following is returned instead.

```
stringField       object
intField           int64
floatField       float64
enumField         object
enumField_int      int64
enumField_str       bool
dtype: object
```

## The Problem

When read_csv sees a column of string values that could all represent a boolean value, it interprets that field as a boolean. This feature could potentially be useful for some applications, but in my case, booleans will always be represented as 0 and 1 and the only time true and false will appear in my data is when they are values in a string field.

I would expect there to be a parameter to read_csv to disable this behavior, but there is not.

There _are_ parameters that allow for more keywords to be interpretted as true and false (true_values, false_values) but the default value of these parameters is none, and setting them to an empty list doesn't disable this behavior either.

__This__ is the only way to disable this behavior purely with the pandas library

```
df = pd.read_csv('demo_less.csv', dtype=str).apply(pd.to_numeric, errors='ignore')
```

read_csv will interpret every column as a string, then the to_numeric function can be applied to each column to attempt to convert it to a numeric type. to_numeric does _not_ treat string values as booleans even though read_csv does.

Now if the types are checked.

```
print(df.dtypes)
```

The following will be returned.

```
stringField       object
intField           int64
floatField       float64
enumField         object
enumField_int      int64
enumField_str     object
dtype: object
```
