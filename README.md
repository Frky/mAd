# mAd

Simple arithmetics in Markdown -- gonna be a thing

In a few words, the idea here is to add simple arithmetics to markdown.
It works as follows:

1. You write a mAd file (.mad or .mAd) embedding expressed arithmetic expressions and variable manipulations, plus other markdown content
1. You render a markdown file (.md) from the mAd file - this actually computes every expression and generate a static md file

## Arithmetics

### General 

`$( arithmetics )` -> compute the value inside $( )

`$(( arithmetics ))` -> compute the value and print the result

### Examples

`$(2 + 3)` -> compute 5

`$(( 2 + 3 ))` -> compute 5 and print it into the output file

`$(a = 50)` -> affect variable a w/ value 50

`$(( a = 50 ))` -> affect variable a w/ value 50 and print its value into the output file

### Work in Progress

* Variable manipulation
* Computations in tabulars (simplified excel style)
