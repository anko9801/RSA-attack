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

def gcd(x, y):
	if x < y:
		x, y = y, x
	if y == 0:
		return x
	return gcd(y, x % y)

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

def gen_d(e, l):
	_, x, _ = exgcd(e, l)
	return x % l

def LeakedSecretKey(n, e, d):
	k = d * e - 1
	while True:
		g = random.randint(2, n - 1)
		t = k
		while True:
			if t & 1 == 0:
				t = t // 2
				x = modular_exp(g, t, n)
				p = gcd(x - 1, n)
				if x > 1 and p > 1:
					q = n / p
					return (p, q)
				else:
					continue
			else:
				break

if __name__ == '__main__':
	bits = 256
	p = gen_prime(bits)
	q = gen_prime(bits)
	e = 65537
	d = gen_d(e, (p-1)*(q-1))
	n = p * q
	print("p:", p)
	print("q:", q)
	print("e:", e)
	print("d:", d)
	print("n:", n)
	print()

	m = 123456789
	c = modular_exp(m, e, n)
	_m = modular_exp(c, d, n)
	print("clear text :", m)
	print("secret text:", c)
	print("clear text :", _m)
	print()


	print("その他 Leaked Secret Key: d")
	_q, _p = LeakedSecretKey(n, e, d)
	print("p:", _p)
	print("q:", _q)
	print()
