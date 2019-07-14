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

def sqrt(n):
	x = n
	y = (x + 1) // 2
	while y < x:
		x = y
		y = (x + n // x) // 2
	return x

def continued_fraction(n, d):
	cf = []
	while d:
		q = n // d
		cf.append(q)
		n, d = d, n % d
	return cf

def convergents_of_contfrac(cf):
	n0, n1 = cf[0], cf[0] * cf[1] + 1
	d0, d1 = 1, cf[1]
	yield (n0, d0)
	yield (n1, d1)

	for i in range(2, len(cf)):
		n2, d2 = cf[i] * n1 + n0, cf[i] * d1 + d0
		yield (n2, d2)
		n0, n1 = n1, n2
		d0, d1 = d1, d2

def WienersAttack(e, n):
	cf = continued_fraction(e, n)
	convergents = convergents_of_contfrac(cf)

	for k, d in convergents:
		if k == 0:
			continue
		phi, rem = divmod(e*d-1, k)
		if rem != 0:
			continue
		s = n - phi + 1
		# check if x^2 - s*x + n = 0 has integer roots
		D = s*s - 4*n
		sD = sqrt(D)
		if D > 0 and sD * sD == D:
			return d
	return 0

if __name__ == '__main__':
	bits = 256
	p = gen_prime(bits)
	q = gen_prime(bits)
	e = 65537
	d = gen_d(e, (p-1)*(q-1))
	n = p * q

	# n,e -> d
	print("その7 Wiener's Attack")
	n2 = 0x00d91f0102279d099a9aa3a819faefef8e39e71075c5ed59275ae33fd16f10c6b120fbc14f2b0e85b09b7372853c22b359fb4b850e0b66da55585e1221bc23d4a84bc0cce1c1f1c080c74520c3f7cb2d041bc2c372ae96a3b9344dc00b00a75873fd339121804b39b74969ceab850a5ce8c65860fa1e7cfafb052e994a832198ece195ee8bb427a04609b69f052b1d2818741604e2d1fc95008961365f0536f1d3d12b11f3b56f55aa478b18cc5e74918869d9ef8935ce29c66ac5abdde9cc44b8a33c4a3c057624bee9bdfeb8e296798c377110e2209b68fc500d872fd847fe0a7b41c6826b4db3645133a497424b5c111fc661e320b024bccf4b8120847fc92d
	e2 = 0x470a2650f57fed98dbde75761701a2b2711c668dcaf1f58c1e87bd1ff21b19ca107bbf8ae7cfdd31e991a6900aa2e4f24ab20fa291fb014a7a7dc73df4726a057a222aa331726cf9b9ebb22e8b8812025340ed1bdf882eef353f009cbf20c1be0e6231c8021d63e82f66c94118cefb1fd3c155bede6037f822992b8e37cd6a1b011aec6dfeb63079030e1af7fabf53bb625a7c58aceaa5805b59495989965cd62440acaa326bb90ba5d315845ad295eced02a8aca56f479c7ed97cb8dbb48b89366cb0467fa77ddfccfd09d428bc4aa6f5170e68a7c219b4c8bd032dc13946e2e1ab5d18e41eddd2dad1d8cef5e7f45dcd9ada2c696dc16f7510b155d7b72c35
	print("n:", n2)
	print("e:", e2)
	print("d:", WienersAttack(e2, n2))
	print()
