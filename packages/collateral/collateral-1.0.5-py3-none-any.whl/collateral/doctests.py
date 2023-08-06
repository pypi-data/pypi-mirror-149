"""
>>> import collateral as ll

Test empty Collateral:
>>> C = ll.Collateral()
>>> C
Collateral<  >
>>> C.collaterals
()
>>> C.collaterals.all_equal()
True
>>> C.collaterals.all()
True
>>> C.collaterals.any()
False

Test all-None Collateral:
>>> C = ll.Collateral(None, None, None)
>>> C
Collateral< None // None // None >
>>> C.collaterals
(None, None, None)
>>> C.collaterals.all_equal()
True
>>> C = ll.Collateral(None, None, None, notallnone=True)
>>> C
>>> C is None
True

Test sum/subtraction/division/multiplication
>>> C = ll.Collateral(1, 2, 3, 4)
>>> C
Collateral< 1 // 2 // 3 // 4 >
>>> C + 2
Collateral< 3 // 4 // 5 // 6 >
>>> C - 4
Collateral< -3 // -2 // -1 // 0 >
>>> C * 3
Collateral< 3 // 6 // 9 // 12 >
>>> C / 2
Collateral< 0.5 // 1.0 // 1.5 // 2.0 >
>>> C // 2
Collateral< 0 // 1 // 1 // 2 >
>>> (C * 0).collaterals.all_equal()
True

Test iteration on Collateral with keys
>>> C = ll.Collateral({ 0: True, 'foo': 'bar' }, { 1: False, 'bar': 'foo' })
>>> for k in C:
...     print(f"key: {k} and value: {C[k]}")
key: Collateral< 0 // 1 > and value: Collateral< True // False >
key: Collateral< 'foo' // 'bar' > and value: Collateral< 'bar' // 'foo' >
>>>
"""
