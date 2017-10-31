import hashlib

class Simhash(object):
    """ A locality sensitive hashing (LSH) implemetation.
    It is a particular case of Charikar's hash (simhash).

    1. Document is splitted into tokens (words for example) or super-tokens (word tuples)
    2. Each token is represented by its hash value; a traditonal hash function is used
    3. Weights are associated with tokens
    4. A vector V of integers is initialized to 0, length of the vector corresponds to the desired hash size in bits
    5. In a cycle for all token's hash values (h), vector V is updated:
        * ith element is decreased by token's weight if the ith bit of the hash h is 0, otherwise
        * ith element is increased by token's weight if the ith bit of the hash h is 1
    6. Foinally, signs of elements of V corresponds to the bits of the final fingerprint
   """
   # The more bits the more sensitive, but beats the cpu.
    def __init__(self, argin=None, bits=64, algo='sha1'):
        self.hashbits = bits
        self.hashalgo = getattr(hashlib, algo)
        self.n_token = None

        self.fingerprint = None

        if argin is None:
            pass
        elif isinstance(argin, list):
            self.simhash(argin)
        elif isinstance(argin, int):
            self.fingerprint = argin
        elif isinstance(argin, Simhash):
            self.fingerprint = argin.fingerprint
        else: # String
            self.fingerprint = self.simhash(argin.encode('utf8').split())

    def __str__(self):
        return str(self.fingerprint)

    def __int__(self):
        return int(self.fingerprint)

    def __float__(self):
        return float(self.fingerprint)

    def simhash(self, tokens):
        self.n_token = len(tokens)
        v = [0]*self.hashbits
        hashs = [int(self.hashalgo(w).hexdigest(), 16) for w in tokens]
        for h in hashs:
            bitmask = 0
            for i in range(self.hashbits):
                bitmask = 1 << i
                if h & bitmask:
                    v[i] += 1
                else:
                    v[i] -= 1

        fingerprint = 0

        for i in range(self.hashbits):
            if v[i] >= 0:
                fingerprint |= 1<<i

        return fingerprint

    # Hamming Distance
    def distance(self, fp1, fp2=None):
        distance = 0
        fp2 = fp2 or self.fingerprint
        x = (fp1 ^ fp2) & ((1 << self.hashbits) - 1)
        while x:
            distance += 1
            x &= x-1
        return distance

    def distsim(self, fgp1, fgp2=None):
        fp1 = self._get_fingerprint(fgp1)
        fp2 = self._get_fingerprint(fgp2)
        distance = self.distance(fp1, fp2)
        return 100 - distance / self.hashbits * 100

    # Not mature, but the idea is to try to normalize with the size of the text
    # to get a interpretable percentage ??? New mesure ?
    # Take a Simhash in entry for further parameter
    def _distsim(self, fgp):
        fp = self._get_fingerprint(fgp)
        nt = self._get_n_token(fgp)
        norm = self.hashbits
        if nt:
            norm = max(nt, self.n_token)
            norm = norm if norm < self.hashbits else self.hashbits
        distance = self.distance(fp)
        sim =  100 - distance / norm * 100
        return  sim

    def similarity(self, fgp):
        fp = self._get_fingerprint(fgp)
        fp1 = self.fingerprint
        fp2 = fp

        if fp1 > fp2:
            return fp2/fp1*100
        else:
            return fp1/fp2*100

    def _get_fingerprint(self, fgp):
        if not fgp:
            return None
        elif isinstance(fgp, type(self)):
            return fgp.fingerprint
        else:
            return int(fgp)

    def _get_n_token(self, fgp):
        if isinstance(fgp, type(self)):
            return fgp.n_token
        else:
            return None

