age=25
count=1_000_000
hex_value=0xFF
bin_value=0b1010

price=19.99
pi=3.14159
scientific=2.5e-3

from decimal import Decimal

total=Decimal('19.99') * Decimal('0.15')

print(total)