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

# ロー法
def rho_algo(n, x, y, i):
	d = 1
	while d == 1:
		x = (x * x + 1) % n
		y = (y * y + 1) % n
		y = (y * y + 1) % n
		d = gcd(abs(x - y), n)
	return d

def sqrt(n):
	x = n
	y = (x + 1) // 2
	while y < x:
		x = y
		y = (x + n // x) // 2
	return x

# フェルマー法 √nから探索
def fermat(n):
	x = sqrt(n) + 1
	y = sqrt(x * x - n)
	while True:
		w = x * x - n - y * y
		if w == 0:
			break
		elif w > 0:
			y += 1
		else:
			x += 1
	return (x + y, x - y)

# 逆元
def invert(x, n):
	(a, b, c) = exgcd(x, n)
	if a != 1:
		print("nashi")
		return 0
	return b

def simple(n, e, c):
	p = rho_algo(n, 2, 2, 0)
	q = n / p
	print(p, q)
	d = e
	phi = (p - 1) * (q - 1)
	while d % phi != 1:
		d += e
	return (p, q, d // e)

# c1 = m^e1 mod n
# c2 = m^e2 mod n
# e1s1 + e2s2 = 1
# c1^s1 c2^s2 = m^(e1s1 + e2s2) mod n = m
def CommonModulusAttack(e1, e2, c1, c2, n):
	a, s1, s2 = exgcd(e1, e2)
	if s1 < 0:
		s1 = -s1
		c1 = invert(c1, n)
	if s2 < 0:
		s2 = -s2
		c2 = invert(c2, n)
	v = modular_exp(c1, s1, n)
	w = modular_exp(c2, s2, n)
	m = (v * w) % n
	return m

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

def LSBLeakAttack(e, n, c, oracle):
	l, r = 0.0, n
	i = 1
	m = 0.0
	while r - l >= 1:
		m = (l + r) / 2
		if oracle(modular_exp(2, i * e, n) * c % n) == 0:
			r = m
		else:
			l = m
		i += 1
	return l

if __name__ == '__main__':
	bits = 256
	p = gen_prime(bits)
	q = gen_prime(bits)
	n = p * q
	e = 3
	d = gen_d(e, (p-1)*(q-1))
	m = 123456
	c = modular_exp(m, e, n)
	print("p:", p)
	print("q:", q)
	print("e:", e)
	print("d:", d)
	print("n:", n)
	print()
	
	# c = m^e mod n
	# nが十分小さい時
	# m = c^1/e
	# c, e -> m
	print("その6 Low Public-Exponent Attack")
	
	print("clear text :", m)
	print("secret text:", c)
	print("clear text :", c ** (1.0 / e))
	print()
