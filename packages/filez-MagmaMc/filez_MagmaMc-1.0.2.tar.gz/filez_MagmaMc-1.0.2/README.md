# Filez

## Get Started
```py
import filez
filez.ID = "MYPROJECTID" # http://magma-mc.net/projects.php/
filez.DEVELOPER =  False # Prints To Console

```

### Fwrite
```py

thejson = {"hello": "World!"}
thejson2 = {"hello": "there!"}

filez.fwrite('testfile.json', json.dumps(thejson))

filez.fwrite('testfile2.json', json.dumps(thejson2))

```

### Fread
```py

print(filez.fread('testfile.json')) 
# prints {"hello": "World!"}
print(filez.fread('testfile2.json')) 
# prints {"hello": "there!"}

```

### Scan
```py

print(filez.scan('/')) 
# prints ['testfile.json', 'testfile2.json']

print(filez.scan('/', True)) 
# prints {'testfile.json': '{"hello": "World!"}', 'testfile2.json': '{"hello": "there!"}'}

```

### Send
```py

thejson = {
    'HelloWorld': 'Hi!',
	'HelloThere': 'Hello!'
}

filez.fwrite('testfile3.json', json.dumps(thejson))

print(filez.fread('testfile3.json'))
# prints {'HelloWorld': 'Hi!', 'HelloThere': 'Hello!'}

filez.send('testfile3.json', 'Bonjour', 'HelloWorld')

print(filez.fread('testfile3.json'))
# prints {'HelloWorld': 'Bonjour!', 'HelloThere': 'Hello!'}

```

##