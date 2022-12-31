#! /usr/bin/python3

import atheris
import sys

with atheris.instrument_imports():
    from chardet import UniversalDetector

encodings = [
    'ascii',
    'utf-8',
    'iso8859_5',
    'iso-8859-1',
    'iso-8859-7'
]

@atheris.instrument_func
def test_input(input_bytes):
    fdp = atheris.FuzzedDataProvider(input_bytes)
    
    inputs = { k:bytearray(fdp.ConsumeUnicodeNoSurrogates(sys.maxsize), k, 'ignore') for k in encodings }

    u = UniversalDetector()

    for codec, enc in inputs.items():
        if enc == bytearray(b''):
            continue
        u.feed(enc)
        u.close()
        res = u.result['encoding']
        if res:
            if not (codec.lower() == res.lower()):
                raise Exception(f"incorrect encoding codec prediction: {enc} was {codec} but ID'd as {res}")
    

def main():
    atheris.Setup(sys.argv, test_input)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
