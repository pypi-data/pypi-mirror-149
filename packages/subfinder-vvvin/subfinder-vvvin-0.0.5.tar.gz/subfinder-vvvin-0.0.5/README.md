# subfinder

A Python library for offline reverse geocoding to find Suburb, City and State in Australia.

### Author

Mian Chen & Kuizong Wu

### Installation

For first time installation,

```shell
$ pip install subfinder-vvvin
```

Or upgrade an existing installation using,

```shell
$ pip install --upgrade subfinder-vvvin
```

Package can be found on [PyPI](https://pypi.python.org/pypi/reverse_geocoder/).

### Dependencies

- reverse_geocoder

### Usage

1. Import the subfinder in the python file to be used

   ```python
   import subfinder
   ```

2. Initialize a subfinder class object and call the GetPlace() function

   ```python
   a = subfinder.subfinder()
   address = s.GetPlace(-37.96944, 145.04806)
   ```

3. Received parameters and return values
   - GetPlace(float(latitute), float(longtitute)): Pass in the latitute and longtitude parameters, of type float
   - Return: The return value will be a variable of dictionary type, containing three keys
     - "suburb"
     - "state"
     - "city"