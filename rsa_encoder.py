def modular_exp(a, b, n):
	res = 1
	while b != 0:
		if b & 1 != 0:
			res = (res * a) % n
		a = (a * a) % n
		b >>= 1
	return res

def gcd(x, y):
	if y == 0:
		return x
	return gcd(y, x % y)

# ロー法 非自明なnの素因数が返される
# n: 素因数分解したい数 x, y: 適当な値 i: 何回再帰したか
def rho_algo(n, x, y, i):
	d = 1
	while d == 1:
		x = (x * x + 1) % n
		y = (y * y + 1) % n
		y = (y * y + 1) % n
		d = gcd(abs(x - y), n)

	return d

if __name__ == '__main__':
	n = int(input(), 10)
	print("n: ", n)
	result = rho_algo(n, 2, 2, 0)
	print("p: ", result)
	n /= result
	result = rho_algo(n, 2, 2, 0)
	print("q: ", result)
