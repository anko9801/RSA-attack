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
	e = 65537
	p = 8337989838551614633430029371803892077156162494012474856684174381868510024755832450406936717727195184311114937042673575494843631977970586746618123352329889
	q = 7755060911995462151580541927524289685569492828780752345560845093073545403776129013139174889414744570087561926915046519199304042166351530778365529171009493
	e = 65537
	c = 7022848098469230958320047471938217952907600532361296142412318653611729265921488278588086423574875352145477376594391159805651080223698576708934993951618464460109422377329972737876060167903857613763294932326619266281725900497427458047861973153012506595691389361443123047595975834017549312356282859235890330349

	d = gen_d(e, (p-1)*(q-1))
	n = p * q
	print("p:", p)
	print("q:", q)
	print("e:", e)
	print("d:", d)
	print("n:", n)
	_m = modular_exp(c, d, n)
	print("clear text :", _m)
	for i in range(0, 31):
		print(chr(int(_m) & 0xff), end='')
		_m //= 0x100
	print()

	m = 123456789
	c = modular_exp(m, e, n)
	_m = modular_exp(c, d, n)
	print("clear text :", m)
	print("secret text:", c)
	print("clear text :", _m)
	print()

	
	# n, e, c -> p, q, d
	print("その1,2 simple attack")
	print("解析に時間がかかる為p,qは小さい数に")
	_p = gen_prime(10)
	_q = gen_prime(10)
	_d = gen_d(e, (_p-1)*(_q-1))
	_n = _p * _q
	_c = modular_exp(m, e, _n)
	print("e:", e)
	print("n:", _n)
	print("complete!")
	_p, _q, _d = simple(_n, e, _c)
	print("prime:", _p, _q)
	print()

	# n -> p, q
	print("その3 Fermat法")
	# _n = 379557705825593928168388035830440307401877224401739990998883
	# _p, _q = fermat(_n)
	# print("prime:", _p, _q)
	# print()

	# n, n2 -> p
	print("その5 Common Factor Attacks")
	q2 = gen_prime(bits)
	n2 = p * q2
	print("prime:", gcd(n, n2))
	print()

	# c = m^e mod n
	# nが十分小さい時
	# m = c^1/e
	# c, e -> m
	print("その6 Low Public-Exponent Attack")
	_e = 3
	_d = gen_d(_e, (p-1)*(q-1))
	_m = 123456
	_c = modular_exp(_m, _e, n)
	print("clear text :", _m)
	print("secret text:", _c)
	print("clear text :", _c ** (1.0 / _e))
	print()

	# n,e -> d
	print("その7 Wiener's Attack")
	n2 = 0x00d91f0102279d099a9aa3a819faefef8e39e71075c5ed59275ae33fd16f10c6b120fbc14f2b0e85b09b7372853c22b359fb4b850e0b66da55585e1221bc23d4a84bc0cce1c1f1c080c74520c3f7cb2d041bc2c372ae96a3b9344dc00b00a75873fd339121804b39b74969ceab850a5ce8c65860fa1e7cfafb052e994a832198ece195ee8bb427a04609b69f052b1d2818741604e2d1fc95008961365f0536f1d3d12b11f3b56f55aa478b18cc5e74918869d9ef8935ce29c66ac5abdde9cc44b8a33c4a3c057624bee9bdfeb8e296798c377110e2209b68fc500d872fd847fe0a7b41c6826b4db3645133a497424b5c111fc661e320b024bccf4b8120847fc92d
	e2 = 0x470a2650f57fed98dbde75761701a2b2711c668dcaf1f58c1e87bd1ff21b19ca107bbf8ae7cfdd31e991a6900aa2e4f24ab20fa291fb014a7a7dc73df4726a057a222aa331726cf9b9ebb22e8b8812025340ed1bdf882eef353f009cbf20c1be0e6231c8021d63e82f66c94118cefb1fd3c155bede6037f822992b8e37cd6a1b011aec6dfeb63079030e1af7fabf53bb625a7c58aceaa5805b59495989965cd62440acaa326bb90ba5d315845ad295eced02a8aca56f479c7ed97cb8dbb48b89366cb0467fa77ddfccfd09d428bc4aa6f5170e68a7c219b4c8bd032dc13946e2e1ab5d18e41eddd2dad1d8cef5e7f45dcd9ada2c696dc16f7510b155d7b72c35
	print("n:", n2)
	print("e:", e2)
	print("d:", WienersAttack(e2, n2))
	print()

	# e1, e2, c1, c2, n -> m
	print("その8 Common Modulus Attack")
	e2 = gen_prime(16)
	c2 = modular_exp(m, e2, n)
	print("clear text:", CommonModulusAttack(e, e2, c, c2, n))
	print()

	print("その9 Hastad's Broadcast Attack")
	HastadsBroadcastAttack(123456789)
	print()

	# oracle, e, n, c -> m
	print("その10 LSB Leak Attack")
	oracle = lambda x: modular_exp(x, d, n) % 2
	print("clear text:", LSBLeakAttack(e, n, c, oracle))
	print()

	#print("その11・その12・その13・その14 Coppersmith's Attack")
	#print("SageMath提げます〜")
	#print()

	print("その他 Leaked Secret Key: d")
	_q, _p = LeakedSecretKey(n, e, d)
	print("p:", _p)
	print("q:", _q)
	print()
