#d = {'foo': 'x', 'bar': 'y', 'zoo': 'None', 'foobar': 'None'}
#d = dict(import='x', bar='y', zoo='None', foobar='None')
d = dict(zip(['import','bar','zoo','foobar'],['x','y','None','None']))
print(dict((k, 'updated') for k, v in d.items() if v is 'None'))
print({i: 'updated' for i, j in d.items() if j != 'None'})
