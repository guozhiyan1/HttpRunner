# ZHUYUAN_HUANZHE = [
#
#     ['06cf01b2af9f469bb0b5813b492acf97', 5000088, 21303],
#     ['7e583f7a1e7b426a8220f30cee8ba292', 5000089, 21304],
#     ['2525d3cc38314498b4102550f5e24b7c', 5000090, 21302],
#     ['29754572b6624e7c9c54a86f7edf8c71', 5000091, 21305],
#     ['d8142d0027bb49ad90bb98664f2bf8d4', 5000121, 21336],
#     ['8dad449c903d4f019565f3c53ea9f4d0', 5000095, 21318],
#     ['18c078c9f35f430aae1b723a3527eeec', 5000093, 21314],
#     ['003f05b6765a4c048be076dda55424bd', 5000170, None],
#     ['62870c4784a14cc2993933c074de5c4b', 5000128, 21343],
#     ['cc70e96a4f894bcfb7dee7ce9dc0cca1', None, 21435],
#     ['2253734ca6414396baf20882269b1412', None, 21434],
#     ['6e949ef7ae9643ae91004ec78c140128', None, 21436],
#     ['204d32a03d46452f9794a9bb50a9ce5a', None, 21437],
#     ['53b1e482f39c4c268c711d2cbed09353', None, 21438],
#     ['8c514951e60047dd90d9179fba9ea48b', 4033870, 17019],
#     ['ea4a37d304a54932bab1dad8df928ba3', 4037478, 17628]
#
# ]


ZHUYUAN_HUANZHE = [['550f547743614caa916ddc77c8fb6686', 196386, 13802],
['e83b9337678e435bbe00e3e31f8ab17a', 196435, 14255],
['f24dc286ba064979b3961e9a2e8497ca', 196436, 14254],
['340f6ce5bd4e494a85b8adf46778c9e5', 196437, 14253],
['f28cc17b6d5441cbb0b816cb8af7a0e9', 196438, 14252],
['57f77510aa2141e490ce7c76becea769', 196439, 14251],
['88ab0636ed234b1a8d7ff21bbe2b0f7c', 196441, 14249],
['1aa3e21017b94ceabca346856a5ea823', 196442, 14248],
['c84056075e7342df8899dc4a083ca306', 196449, 14247],
['ef16fdd04ac14704af9c471273269a5f', 196452, 14245],
['a1dfaee46dce476a8f589863b335c68d', 196454, 14243],
['8b300f807c444f3681b0dca97fda789b', 196455, 14241],
['cf16e3865b794fcb8389b960f92c61b7', 196456, 14246],
['0077020130264d5fad76cd2d23ccadc8', 196457, 14259]]
for i in ZHUYUAN_HUANZHE:
    masterPatientIndex, inhospitalPatientId, patientRegisterId = tuple(i)
    print(f'{{"masterPatientIndex":"{masterPatientIndex}","patientRegisterId":"{patientRegisterId}","inhospitalPatientId":"{inhospitalPatientId}"}},')