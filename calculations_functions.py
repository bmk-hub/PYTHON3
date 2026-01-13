#!/usr/bin/env python3

#Exercise 1:
def cube(n):
	return n ** 3
x = cube(3)
print(x)


#Exercise 2:
def area_of_triangle(width, height):
	return 0.5 * width * height

width = float(input("Enter the width: "))
height = float(input(" Enter the height: "))

area = area_of_triangle(width, height)


print(f"The area of the triangle is: {area}.")


#Exercise 3:
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

#Exercise 4:
def calculate_risk(open_ports, has_smb, has_ssh):
	risk = min(open_ports, 6)
	if has_smb:
		risk = risk + 3
	if has_ssh:
		risk = risk + 2
	if risk < 1:
		risk = 1
	if risk > 10:
		risk = 10
	return risk
	
risk_a = calculate_risk(3, True, False)
risk_b = calculate_risk(10, False, True)

print(f"Host A risk score: {risk_a}/10")
print(f"Host B risk score: {risk_b}/10")

#Exercise 5:
def password_strength(length, has_uppercase, has_symbols):
	strength = min(length, 7)
	if has_uppercase:
		strength = strength + 2
	if has_symbols:
		strength = strength + 3
	if strength < 1:
		strength = 1
	if strength > 10:
		strength = 10
	return strength
		
strength_a = password_strength(6, False, False)
strength_b = password_strength(10, True, True)
strength_c = password_strength(12, True, False)

print(f"Password A strength: {strength_a}/10")
print(f"password B strength: {strength_b}/10")
print(f"password C strength: {strength_c}/10")

#Exercise 6:

