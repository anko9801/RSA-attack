# -*- coding: utf-8 -*-
import random

def modular_exp(a, b, n):
	res = 1
	while b > 0:
		if b & 1 == 1:
			res = (res * a) % n
		a = (a * a) % n
		b >>= 1
	return res

def gen_rand(bit_length):
	bits = [random.randint(0,1) for _ in range(bit_length - 2)]
	ret = 1
	for b in bits:
		ret = ret * 2 + int(b)
	return ret * 2 + 1

def mr_primary_test(n, k=100):
	if n == 1:
		return False
	if n == 2:
		return True
	if n % 2 == 0:
		return False
	d = n - 1
	s = 0
	while d % 2 != 0:
		d /= 2
		s += 1

	r = [random.randint(1, n - 1) for _ in range(k)]
	for a in r:
		if modular_exp(a, d, n) != 1:
			pl = [(2 ** rr) * d for rr in range(s)]
			flg = True
			for p in pl:
				if modular_exp(a, p, n) == 1:
					flg = False
					break
			if flg:
				return False
	return True

def gen_prime(bit):
	while True:
		ret = gen_rand(bit)
		if mr_primary_test(ret):
			break
	return ret

if __name__ == '__main__':
	bits = 256
	# n, n2 -> p
	print("その5 Common Factor Attacks")
	p = gen_prime(bits)
	q1 = gen_prime(bits)
	q2 = gen_prime(bits)
	n1 = p * q1 
	n2 = p * q2
	print("prime:", gcd(n1, n2))
	print()
