from abc import ABC
from enum import Enum
import random
import matplotlib.pyplot as plt

counter = 0

class Dict(ABC):

    def __init__(self, iterable=None):
        self.data = []
        self.size = 0
        if iterable is not None:
            for (k, v) in iterable:
                self[k] = v


    def _find_index(self, key):
        global counter
        for (i, (k, _)) in enumerate(self.data):
            counter += 1
            if k == key: return i
        #return None

    def get(self, key, default=None):
        i = self._find_index(key)
        if i is None: return default
        return self.data[i][1]

    def _key(selfself, element):
        return element

    def _h(self, key): #
        return hash(key) % len(self.data)

    def __getitem__(self, key):
        i = self._find_index(key)
        if i is None: raise KeyError(key)
        return self.data[i][1]

    def __setitem__(self, key, value):
        i = self._find_index(key)
        if i is None:
            self.data.append((key, value))
        else:
            self.data[i][1] = value

    def __delitem__(self, key):
        i = self._find_index(key)
        if i is not None:
            self.data[i] = self.data[-1]
            self.data.pop()

    def __len__(self):
        return self.size

    def __contains__(self, key):
        return self._find_index(key) is not None

    def __str__(self):
        result = '{'
        first = True
        for (k, v) in self.data:
            if not first:
                result += ', '
            first = False
            result += str(k)
            result += ': '
            result += str(v)
        result += '}'
        return result

    def __repr__(self):
        result = 'SimpleDict(['
        first = True
        for (k, v) in self.data:
            if not first:
                result += ', '
            first = False
            result += '('
            result += repr(k)
            result += ', '
            result += repr(v)
            result += ')'
        result += '])'
        return result

    def __eq__(self, other):
        return self.data == other.data

    def __iter__(self):
        for (k, _) in self.data:
            yield k


class ChainHash(Dict):

    def __init__(self):
        super().__init__()
        self.data = [[] for i in range(20)]


    def _find_index(self, key):


        global counter
        h = hash(key) % len(self.data)
        for i, value in enumerate(self.data[h]):
            counter += 1
            if (self._key(value)) == key:
                return h, i
        return h, -1

    def find(self, key):
        global counter
        counter = 0
        h, i = self._find_index(key)
        if i == -1:
            return None
        return self.data[h][i]

    def insert(self, element):
        h, i = self._find_index(self._key(element))
        if i == -1:
            self.data[h].append(element)
            self.size += 1
        else:
            self.data[h][i] = element

    def delete(self, key):
        h, i = self._find_index(key)
        if i != -1:
            self.data[h][i] = self.data[h][- 1]
            self.data[h].pop()
            self.size -= 1

class LinearDict(Dict):

    def __init__(self):
        super().__init__()
        self.data = [LinearDict.Helper.EMPTY] * 1010

    def _empty(self, i):
        return self.data[i] == LinearDict.Helper.EMPTY

    def _deleted(self, i):
        return self.data[i] == LinearDict.Helper.DELETED

    def scan_for(self, key):
        global counter
        first_index = self._h(key)
        step = 1
        first_deleted_index = -1
        i = first_index
        counter += 1
        while not self._empty(i):
            counter += 1
            if self._deleted(i):
                if first_deleted_index == -1:
                    first_deleted_index = i
            elif self._key(self.data[i]) == key:
                return i
            i = (i + step) % len(self.data)
            if i == first_index:
                return first_deleted_index
        if first_deleted_index != -1:
            return first_deleted_index
        return i

    def find(self, key):
        global counter
        counter = 0
        i = self.scan_for(key)
        if i == -1 or self._empty(i) or self._deleted(i):
            return None
        return self.data[i]

    def insert(self, element):
        i = self.scan_for(self._key(element))
        if i== -1:
            return
        self.data[i] = element
        self.size += 1


    def delete(self, key):
        i = self.scan_for(key)
        if not self._empty(i) and i!= -1:
            self.data[i] = LinearDict.Helper.DELETED
            self.size -= 1


    class Helper(Enum):
        EMPTY = -1
        DELETED = -2


chain = ChainHash()
linear = LinearDict()

X = [[], []]
Y = [[], []]
rang = 1000
data = random.sample(range(rang), rang)

for i, value in enumerate(data):
    ran = random.randrange(0, rang)
    chain.insert(value)
    linear.insert(value)
    chain.find(-1)
    X[0].append(len(chain))
    X[1].append(counter)
    linear.find(ran)
    Y[0].append(len(linear))
    Y[1].append(counter)

plt.plot(X[0], X[1], label="Lancuchowy")
plt.plot(Y[0], Y[1], label="Liniowy")
plt.xlabel = "Wielkosc slownika"
plt.ylabel('Liczba porownan')
plt.title('Porownanie lancuchowego i liniowego')
plt.legend()
plt.show()