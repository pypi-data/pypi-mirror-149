# Filez

### Get Started
```py
import filez
filez.ID = "MYPROJECTID" # http://magma-mc.net/projects.php/

thejson = json.loads('{"hello": "World!"}')

filez.fwrite('testfile.json', json.dumps(thejson), 'c')
content = filez.read('testfile.json')

filez.fwrite('testfile2.json', json.dumps(thejson), 'c')
content2 = filez.read('testfile.json')


folder = filez.scan('/', True) # Folder, Return file content

print(content) 
# prints {"hello": "World!"}

print(folder) 
# prints {'testfile': '{"hello": "World!"}', 'testfile2': '{"hello": "World!"}'}

```
##
![](http://magma-mc.net/FILEZ_SCREEN.png)