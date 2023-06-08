STANDARD_CHOICES = [
    ('C89', 'C89'),
    ('C99', 'C99'),
    ('C11', 'C11')
]

PROCESOR_CHOICES = [
    ('MCS51', 'MCS51'),
    ('Z80', 'Z80'),
    ('STM8', 'STM8')
]

OPTYMALIZACJE_CHOICES = [
    ('--nogcse', '--nogcse'),
    ('--noinvariant', '--noinvariant'),
    ('--noinduction', '--noinduction'),
    ('--noloopreverse', '--noloopreverse')
]

MCS51_CHOICES = [
    ('--model-small', '--model-small'),
    ('--model-medium', '--model-medium'),
    ('--model-large', '--model-large'),
    ('--model-huge', '--model-huge')
]

Z80_CHOICES = [
    ('--asm=z80asm', '--asm=z80asm'),
    ('--fno-omit-frame-pointer', '--fno-omit-frame-pointer'),
    ('--reserve-regs-iy', '--reserve-regs-iy')
]

STM8_CHOICES = [
    ('--opt-code-size', '--opt-code-size'),
    ('--model-medium', '--model-medium'),
    ('--model-large', '--model-large')
]

Optymalizacje = {'--nogcse', '--noinvariant', '--noinduction', '--noloopreverse'}
OptymalizacjeList = list(Optymalizacje)


SESSION_DEFAULTS = {
    'standard': 'C11',
    'procesor': 'MCS51',
    'optymalizacje': OptymalizacjeList,
    'mcs51': '--model-small',
    'z80': '--asm=z80asm',
    'stm8': '--opt-code-size'
}

STANDARD = {
    'C89': '--std-c89',
    'C99': '--std-c99',
    'C11': '--std-c11'
}

PROCESOR = {
    'MCS51': '',
    'Z80': '--portmode=z80',
    'STM8': '-mstm8'
}