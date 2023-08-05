class JuceRSA(object):

    def __init__(self, key):
        self._part1, self._part2 = self._build_rsa_key(key)

    def _build_rsa_key(self, key):
        if key.count(',') == 1:
            part1, part2 = key.split(',')
            part1 = int(part1, 16)
            part2 = int(part2, 16)
        else:
            raise ValueError("The string needs to be two hex numbers, comma-separated")
        return part1, part2

    def apply_to_value(self, value):
        result = 0
        while value:
            result *= self._part2
            div = divmod(value, self._part2)
            value = div[0]
            remainder = div[1]

            remainder = pow(remainder, self._part1, self._part2)
            result += remainder
        return result

    def encrypt(self, value: str):
        return hex(self.apply_to_value(int.from_bytes(value.encode('utf-8'), byteorder='little')))[2:]

    def decrypt(self, value: hex):
        decrypted = self.apply_to_value(int(value, 16))
        decrypted = bytes.fromhex(hex(decrypted)[2:])
        decrypted = bytearray(decrypted)
        decrypted.reverse()

        return decrypted.decode('utf-8')
