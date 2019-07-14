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

def exgcd(x, y):
	c0, c1 = x, y
	a0, a1 = 1, 0
	b0, b1 = 0, 1

	while c1 != 0:
		m = c0 % c1
		q = c0 // c1

		c0, c1 = c1, m
		a0, a1 = a1, (a0 - q * a1)
		b0, b1 = b1, (b0 - q * b1)

	return c0, a0, b0
def ChineseRem(pairs):
	N = 1
	for a, n in pairs:
		N *= n

	result = 0
	for a, n in pairs:
		m = N // n
		d, r, s = exgcd(n, m)
		if d != 1:
			print("Input not pairwise co-prime")
		result += a * s * m
	return result % N, N

def HastadsBroadcastAttack(m):
	e = 17
	pairs = []
	for i in range(0, e-1):
		p = gen_prime(20)
		q = gen_prime(20)
		n = p*q
		c = modular_exp(m, e, n)
		pairs.append((c, n))

	crt, n = ChineseRem(pairs)
	print("clear text:", crt ** (1.0 / e))

if __name__ == '__main__':
	print("その9 Hastad's Broadcast Attack")
	HastadsBroadcastAttack(123456789)
	print()