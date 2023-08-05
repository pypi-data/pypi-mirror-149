# Uzbek latin cyrillic converter

This repo is for converting uzbek latin words into cyrillic in a single shot meaning in a single iteration. 

The idea was inspired by the **https://github.com/kodchi/uzbek-transliterator** repo which is extremely slow. 
For example, **kodchi/uzbek-transliterator** repo converts 1.3K characters in about 7.86 seconds while this repo takes about 0.00188 seconds which is about **4180** times faster!
Of course, the performance comes with its own cost that is accuracy. Although, it can convert most of the words, but words with some special morphological structure will be converted wrongly (for example, the word **ashob** will be converted as **ашоб** instead of **асҳоб**, another example is **mayor** which will be converted as **маёр** instead of **майор**)

For now, it only supports latin to cyrillic converter. So your contributions are always welcome.

## Installation and Usage! Install using pip:

`pip install uzbek_latin_cyrillic_converter`

Then use it in your projects:

`import uzbek_latin_cyrillic_converter`

`uzbek_latin_cyrillic_converter.latin_to_cyrillic("salom")`

And the above will output **салом**
## Requirements
This repo requires no additional packages, the only necessary package (for now) is **pytest** which is used  for testing.   

# Tips for contribution
Make sure that your code passes the tests in the **tests** directory, and then send a PR.
## To run the tests:

Create and activate a python environment, and install required packages.

`python3 -m venv ./env`

`source env/bin/activate`

`pip install -r requirements.txt`

From the root folder, just run:

`python -m pytest tests`