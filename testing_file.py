#!/usr/bin/env python3

def is_even(n):
	if n % 2 == 0:
		return True
	else:
		return False

number = int(input("Enter a number: "))

if is_even(number):
	print("This is an even number.")
else:
	print("This is an odd number.")


