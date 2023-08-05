## [doc on github.io](https://walkerever.github.io/)

# xtable

print console tables.  xtable serves as both a class and a command line tool.

- [installation](#installation)
- [use the class](#use-the-class)
- [command line](#use-the-command-line) from CSV, preformatted table, JSON list to console table, JSON, markdown and more.
- [convert table data to Markdown](#markdown)

----


## Installation
    `pip install xtable`
   run it through xtable` or `python -mxtable`

----

below is a simple introduction for some basic usage.

## use the class
<pre><font color="#5FD7FF">from</font> xtable <font color="#5FD7FF">import</font> xtable

data = [
        [<font color="#C061CB">1</font>,<font color="#C061CB">2</font>,<font color="#C061CB">3</font>,<font color="#C061CB">4</font>,<font color="#C061CB">5</font>],
        [<font color="#C061CB">11</font>,<font color="#C061CB">52</font>,<font color="#C061CB">3</font>,<font color="#C061CB">4</font>,<font color="#C061CB">5</font>],
        [<font color="#C061CB">11</font>,<font color="#33C7DE"><b>None</b></font>,<font color="#C061CB">3</font>,<font color="#C061CB">4</font>,<font color="#C061CB">5</font>],
        [<font color="#C061CB">11</font>,<font color="#33C7DE"><b>None</b></font>,<font color="#C061CB">3</font>,<font color="#33C7DE"><b>None</b></font>,<font color="#C061CB">5</font>],
        ]
hdr = [<font color="#C061CB">&apos;c1&apos;</font>,<font color="#C061CB">&apos;c2&apos;</font>,<font color="#C061CB">&apos;c3&apos;</font>,<font color="#C061CB">&apos;c4&apos;</font>,<font color="#C061CB">&apos;c5&apos;</font>]

xt = xtable(data=data,header=hdr)
<font color="#33C7DE"><b>print</b></font>(xt)

</pre>

// result : 
<pre>c1 c2 c3 c4 c5
--------------
1  2  3  4  5
11 52 3  4  5
11    3  4  5
11    3     5
</pre>
-----

<pre><font color="#33C7DE"># test/t2.csv</font>
<font color="#C061CB">&apos;&apos;&apos;</font>
<font color="#C061CB">h1,h2,h3</font>
<font color="#C061CB">&quot;asd&quot;,&quot;sdfsadf&quot;,1</font>
<font color="#C061CB">&quot;c&quot;,&quot;cc&quot;,233</font>
<font color="#C061CB">&apos;&apos;&apos;</font>

xt = xtable.init_from_csv(<font color="#C061CB">&quot;test/t2.csv&quot;</font>)
<font color="#33C7DE"><b>print</b></font>(xt)
</pre>

// result :
<pre>h1  h2      h3
---------------
asd sdfsadf 1
c   cc      233
</pre>

-----
<pre>
data = [
        {<font color="#C061CB">&quot;h1&quot;</font>:<font color="#C061CB">&quot;v1&quot;</font>,<font color="#C061CB">&quot;h2&quot;</font>:<font color="#C061CB">&quot;v2&quot;</font>,<font color="#C061CB">&quot;h3&quot;</font>:<font color="#C061CB">&quot;v3&quot;</font>},
        {<font color="#C061CB">&quot;h1&quot;</font>:<font color="#C061CB">&quot;v11&quot;</font>,<font color="#C061CB">&quot;h2&quot;</font>:<font color="#C061CB">&quot;v22&quot;</font>,<font color="#C061CB">&quot;h3&quot;</font>:<font color="#C061CB">&quot;v33&quot;</font>},
        {<font color="#C061CB">&quot;h1&quot;</font>:<font color="#C061CB">&quot;v11111&quot;</font>,<font color="#C061CB">&quot;h2&quot;</font>:<font color="#C061CB">&quot;v22222&quot;</font>,<font color="#C061CB">&quot;h3&quot;</font>:<font color="#C061CB">&quot;v34444&quot;</font>},
     ]
xt = xtable.init_from_list(data)
<font color="#33C7DE"><b>print</b></font>(xt)</pre>

// result :
<pre>
h1     h2     h3
--------------------
v1     v2     v3
v11    v22    v33
v11111 v22222 v34444

</pre>

-----

// all of them support "xheader".

<pre>data = [
        {<font color="#C061CB">&quot;h1&quot;</font>:<font color="#C061CB">&quot;v1&quot;</font>,<font color="#C061CB">&quot;h2&quot;</font>:<font color="#C061CB">&quot;v2&quot;</font>,<font color="#C061CB">&quot;h3&quot;</font>:<font color="#C061CB">&quot;v3&quot;</font>},
        {<font color="#C061CB">&quot;h1&quot;</font>:<font color="#C061CB">&quot;v11&quot;</font>,<font color="#C061CB">&quot;h2&quot;</font>:<font color="#C061CB">&quot;v22&quot;</font>,<font color="#C061CB">&quot;h3&quot;</font>:<font color="#C061CB">&quot;v33&quot;</font>},
        {<font color="#C061CB">&quot;h1&quot;</font>:<font color="#C061CB">&quot;v11111&quot;</font>,<font color="#C061CB">&quot;h2&quot;</font>:<font color="#C061CB">&quot;v22222&quot;</font>,<font color="#C061CB">&quot;h3&quot;</font>:<font color="#C061CB">&quot;v34444&quot;</font>},
     ]
xt = xtable.init_from_list(data, xheader=[<font color="#C061CB">&quot;h1&quot;</font>,<font color="#C061CB">&quot;h3&quot;</font>])
<font color="#33C7DE"><b>print</b></font>(xt)

xt2 = xtable.init_from_list(data, xheader=<font color="#C061CB">&quot;h2,h3&quot;</font>)
<font color="#33C7DE"><b>print</b></font>(xt2)

</pre>

<pre>h1     h3
-------------
v1     v3
v11    v33
v11111 v34444

h2     h3
-------------
v2     v3
v22    v33
v22222 v34444
</pre>

-----

// output json/yaml/csv/html

<pre>

data = [
        {<font color="#C061CB">&quot;h1&quot;</font>:<font color="#C061CB">&quot;v1&quot;</font>,<font color="#C061CB">&quot;h2&quot;</font>:<font color="#C061CB">&quot;v2&quot;</font>,<font color="#C061CB">&quot;h3&quot;</font>:<font color="#C061CB">&quot;v3&quot;</font>},
        {<font color="#C061CB">&quot;h1&quot;</font>:<font color="#C061CB">&quot;v11&quot;</font>,<font color="#C061CB">&quot;h2&quot;</font>:<font color="#C061CB">&quot;v22&quot;</font>,<font color="#C061CB">&quot;h3&quot;</font>:<font color="#C061CB">&quot;v33&quot;</font>},
        {<font color="#C061CB">&quot;h1&quot;</font>:<font color="#C061CB">&quot;v11111&quot;</font>,<font color="#C061CB">&quot;h2&quot;</font>:<font color="#C061CB">&quot;v22222&quot;</font>,<font color="#C061CB">&quot;h3&quot;</font>:<font color="#C061CB">&quot;v34444&quot;</font>},
     ]
xt = xtable.init_from_list(data, xheader=[<font color="#C061CB">&quot;h1&quot;</font>,<font color="#C061CB">&quot;h3&quot;</font>])
<font color="#33C7DE"><b>print</b></font>(xt.csv())
<font color="#33C7DE"><b>print</b></font>(xt.yaml())
<font color="#33C7DE"><b>print</b></font>(xt.json())
<font color="#33C7DE"><b>print</b></font>(xt.html())

</pre>

// result
<pre>- h1: v1
  h3: v3
- h1: v11
  h3: v33
- h1: v11111
  h3: v34444

[
  {
    &quot;h1&quot;: &quot;v1&quot;,
    &quot;h3&quot;: &quot;v3&quot;
  },
  {
    &quot;h1&quot;: &quot;v11&quot;,
    &quot;h3&quot;: &quot;v33&quot;
  },
  {
    &quot;h1&quot;: &quot;v11111&quot;,
    &quot;h3&quot;: &quot;v34444&quot;
  }
]
&lt;table border=1 style=&quot;border-collapse:collapse;&quot;&gt;
&lt;tr&gt;
&lt;td&gt;&lt;b&gt;h1&lt;/b&gt;&lt;/td&gt;
&lt;td&gt;&lt;b&gt;h3&lt;/b&gt;&lt;/td&gt;
&lt;/tr&gt;
&lt;tr&gt;
&lt;td&gt;v1&lt;/td&gt;
&lt;td&gt;v3&lt;/td&gt;
&lt;/tr&gt;
&lt;tr&gt;
&lt;td&gt;v11&lt;/td&gt;
&lt;td&gt;v33&lt;/td&gt;
&lt;/tr&gt;
&lt;tr&gt;
&lt;td&gt;v11111&lt;/td&gt;
&lt;td&gt;v34444&lt;/td&gt;
&lt;/tr&gt;
</pre>

-----

## use the command line

<pre>[yonghang@mtp xtable]$ cat test/t1.txt  
a b c
121 1212 12
12 332  2323
[yonghang@mtp xtable]$ cat test/t1.txt  | xtable 
a   b    c
-------------
121 1212 12
12  332  2323
[yonghang@mtp xtable]$ 
[yonghang@mtp xtable]$ cat test/t2.csv 
h1,h2,h3
&quot;asd&quot;,&quot;sdfsadf&quot;,1
&quot;c&quot;,&quot;cc&quot;,233
[yonghang@mtp xtable]$ 
[yonghang@mtp xtable]$ cat test/t2.csv  | xtable -b&quot;,&quot;
h1    h2        h3
-------------------
&quot;asd&quot; &quot;sdfsadf&quot; 1
&quot;c&quot;   &quot;cc&quot;      233</pre>

-----

<pre>[yonghang@mtp xtable]$ cat test/t3.json  | qic
[
  {
    <font color="#008700"><b>&quot;userId&quot;</b></font>: <font color="#626262">1</font>,
    <font color="#008700"><b>&quot;firstName&quot;</b></font>: <font color="#AF0000">&quot;Krish&quot;</font>,
    <font color="#008700"><b>&quot;lastName&quot;</b></font>: <font color="#AF0000">&quot;Lee&quot;</font>,
    <font color="#008700"><b>&quot;phoneNumber&quot;</b></font>: <font color="#AF0000">&quot;123456&quot;</font>,
    <font color="#008700"><b>&quot;emailAddress&quot;</b></font>: <font color="#AF0000">&quot;krish.lee@learningcontainer.com&quot;</font>
  },
  {
    <font color="#008700"><b>&quot;userId&quot;</b></font>: <font color="#626262">2</font>,
    <font color="#008700"><b>&quot;firstName&quot;</b></font>: <font color="#AF0000">&quot;racks&quot;</font>,
    <font color="#008700"><b>&quot;lastName&quot;</b></font>: <font color="#AF0000">&quot;jacson&quot;</font>,
    <font color="#008700"><b>&quot;phoneNumber&quot;</b></font>: <font color="#AF0000">&quot;123456&quot;</font>,
    <font color="#008700"><b>&quot;emailAddress&quot;</b></font>: <font color="#AF0000">&quot;racks.jacson@learningcontainer.com&quot;</font>
  },
  {
    <font color="#008700"><b>&quot;userId&quot;</b></font>: <font color="#626262">3</font>,
    <font color="#008700"><b>&quot;firstName&quot;</b></font>: <font color="#AF0000">&quot;denial&quot;</font>,
    <font color="#008700"><b>&quot;lastName&quot;</b></font>: <font color="#AF0000">&quot;roast&quot;</font>,
    <font color="#008700"><b>&quot;phoneNumber&quot;</b></font>: <font color="#AF0000">&quot;33333333&quot;</font>,
    <font color="#008700"><b>&quot;emailAddress&quot;</b></font>: <font color="#AF0000">&quot;denial.roast@learningcontainer.com&quot;</font>
  },
  {
    <font color="#008700"><b>&quot;userId&quot;</b></font>: <font color="#626262">4</font>,
    <font color="#008700"><b>&quot;firstName&quot;</b></font>: <font color="#AF0000">&quot;devid&quot;</font>,
    <font color="#008700"><b>&quot;lastName&quot;</b></font>: <font color="#AF0000">&quot;neo&quot;</font>,
    <font color="#008700"><b>&quot;phoneNumber&quot;</b></font>: <font color="#AF0000">&quot;222222222&quot;</font>,
    <font color="#008700"><b>&quot;emailAddress&quot;</b></font>: <font color="#AF0000">&quot;devid.neo@learningcontainer.com&quot;</font>
  },
  {
    <font color="#008700"><b>&quot;userId&quot;</b></font>: <font color="#626262">5</font>,
    <font color="#008700"><b>&quot;firstName&quot;</b></font>: <font color="#AF0000">&quot;jone&quot;</font>,
    <font color="#008700"><b>&quot;lastName&quot;</b></font>: <font color="#AF0000">&quot;mac&quot;</font>,
    <font color="#008700"><b>&quot;phoneNumber&quot;</b></font>: <font color="#AF0000">&quot;111111111&quot;</font>,
    <font color="#008700"><b>&quot;emailAddress&quot;</b></font>: <font color="#AF0000">&quot;jone.mac@learningcontainer.com&quot;</font>
  }
]

[yonghang@mtp xtable]$ cat test/t3.json  | xtable
userId firstName lastName phoneNumber emailAddress
------------------------------------------------------------------------
1      Krish     Lee      123456      krish.lee@learningcontainer.com
2      racks     jacson   123456      racks.jacson@learningcontainer.com
3      denial    roast    33333333    denial.roast@learningcontainer.com
4      devid     neo      222222222   devid.neo@learningcontainer.com
5      jone      mac      111111111   jone.mac@learningcontainer.com
</pre>

-----
### pivot 
<pre>[yonghang@mtp xtable]$ cat test/t3.json  | xtable -v
userId       : 1
firstName    : Krish
lastName     : Lee
phoneNumber  : 123456
emailAddress : krish.lee@learningcontainer.com
--
userId       : 2
firstName    : racks
lastName     : jacson
phoneNumber  : 123456
emailAddress : racks.jacson@learningcontainer.com
--
userId       : 3
firstName    : denial
lastName     : roast
phoneNumber  : 33333333
emailAddress : denial.roast@learningcontainer.com
--
userId       : 4
firstName    : devid
lastName     : neo
phoneNumber  : 222222222
emailAddress : devid.neo@learningcontainer.com
--
userId       : 5
firstName    : jone
lastName     : mac
phoneNumber  : 111111111
emailAddress : jone.mac@learningcontainer.com
</pre>

if we look at the source code, we know class xtable support .pivot() as well,

<pre>        <font color="#E9AD0C">if</font> <font color="#33C7DE"><b>type</b></font>(js) <font color="#E9AD0C">is</font> <font color="#33C7DE"><b>list</b></font> :
            xt = xtable.init_from_json(js,args.header)
            <font color="#E9AD0C">if</font> args.pivot :
                <font color="#33C7DE"><b>print</b></font>(xt.pivot<span style="background-color:#2AA1B3">()</span>)
            <font color="#E9AD0C">else</font> :
                <font color="#33C7DE"><b>print</b></font>(xt)
</pre>


-----
### when header has space...
some command output is already a table, only not that decent, eg. as below. xtable will help a little bit.  `-c` told xtable that `container id` is together while `-t` told xtable the input stream is already in "table" format.

<pre>[yonghang@mtp xtable]$ sudo podman ps --all
CONTAINER ID  IMAGE                           COMMAND               CREATED             STATUS                         PORTS   NAMES
eeb5db3c4f9a  docker.io/library/nginx:latest  nginx -g daemon o...  About a minute ago  Exited (0) About a minute ago          romantic_hamilton
5ef267563b44  docker.io/library/httpd:latest  httpd-foreground      55 seconds ago      Exited (0) 6 seconds ago               sad_lamarr
[yonghang@mtp xtable]$ 
[yonghang@mtp xtable]$ 
[yonghang@mtp xtable]$ sudo podman ps --all | xtable -c &quot;CONTAINER ID&quot; -t
CONTAINER ID IMAGE                          COMMAND              CREATED            STATUS                        PORTS NAMES
----------------------------------------------------------------------------------------------------------------------------------------
eeb5db3c4f9a docker.io/library/nginx:latest nginx -g daemon o... About a minute ago Exited (0) About a minute ago       romantic_hamilto
5ef267563b44 docker.io/library/httpd:latest httpd-foreground     About a minute ago Exited (0) 28 seconds ago           sad_lamar
[yonghang@mtp xtable]$ 
[yonghang@mtp xtable]$ sudo podman ps --all | xtable -c &quot;CONTAINER ID&quot; -tv
CONTAINER ID : eeb5db3c4f9a
IMAGE        : docker.io/library/nginx:latest
COMMAND      : nginx -g daemon o...
CREATED      : About a minute ago
STATUS       : Exited (0) About a minute ago
PORTS        : 
NAMES        : romantic_hamilto
--
CONTAINER ID : 5ef267563b44
IMAGE        : docker.io/library/httpd:latest
COMMAND      : httpd-foreground
CREATED      : About a minute ago
STATUS       : Exited (0) 32 seconds ago
PORTS        : 
NAMES        : sad_lamar
</pre>

### xtable take care of lines

<pre>[yonghang@W5202860 test]$ cat sql.json  | qic
[
  {
    <font color="#008700"><b>&quot;name&quot;</b></font>: <font color="#AF0000">&quot;sql example 1&quot;</font>,
    <font color="#008700"><b>&quot;query&quot;</b></font>: <font color="#AF0000">&quot;SELECT QUARTER, REGION, SUM(SALES)\n FROM SALESTABLE\n GROUP BY CUBE (QUARTER, REGION)&quot;</font>
  },
  {
    <font color="#008700"><b>&quot;name&quot;</b></font>: <font color="#AF0000">&quot;sql example 2&quot;</font>,
    <font color="#008700"><b>&quot;query&quot;</b></font>: <font color="#AF0000">&quot;select name, cast(text as varchar(8000)) \nfrom SYSIBM.SYSVIEWS \n where name=&apos;your table name&apos; &quot;</font>
  },
  {
    <font color="#008700"><b>&quot;name&quot;</b></font>: <font color="#AF0000">&quot;sql example 3&quot;</font>,
    <font color="#008700"><b>&quot;query&quot;</b></font>: <font color="#AF0000">&quot;select Id, max(V1),max(V2),max(V3) from \n (\n select ID,Value V1,&apos;&apos; V2,&apos;&apos; V3 from A where Code=1 \n union all \n select ID,&apos;&apos; V1, Value V2,&apos;&apos; V3 from A where Code=2 \n union all \n select ID,&apos;&apos; V1, &apos;&apos; V2,Value V3 from A where Code=3 \n) AG\n group by ID&quot;</font>
  }
]

[yonghang@W5202860 test]$ 
[yonghang@W5202860 test]$ cat sql.json  | xtable
name          query
-------------------------------------------------------------------
sql example 1 SELECT QUARTER, REGION, SUM(SALES)
               FROM SALESTABLE
               GROUP BY CUBE (QUARTER, REGION)
sql example 2 select name, cast(text as varchar(8000))
              from SYSIBM.SYSVIEWS
               where name=&apos;your table name&apos;
sql example 3 select Id, max(V1),max(V2),max(V3) from
               (
               select ID,Value V1,&apos;&apos; V2,&apos;&apos; V3 from A where Code=1
               union all
               select ID,&apos;&apos; V1, Value V2,&apos;&apos; V3 from A where Code=2
               union all
               select ID,&apos;&apos; V1, &apos;&apos; V2,Value V3 from A where Code=3
              ) AG
               group by ID
</pre>


## markdown

```
yonghang@air xtable % cat test/t2.csv
h1,h2,h3
"asd","sdfsadf",1
"c","cc",233

yonghang@air xtable % cat test/t2.csv | xtable -F md
|  h1,h2,h3           |
|  -----------------  |
|  "asd","sdfsadf",1  |
|  "c","cc",233       |
yonghang@air xtable %
yonghang@air xtable % cat test/t1.txt
a b c
121 1212 12
12 332  2323
yonghang@air xtable % cat test/t1.txt | xtable -F md
|  a    | b    | c     |
|  ---- | ---- | ----  |
|  121  | 1212 | 12    |
|  12   | 332  | 2323  |
yonghang@air xtable %
yonghang@air xtable % cat test/t3.json | qic
[
  {
    "userId": 1,
    "firstName": "Krish",
    "lastName": "Lee",
    "phoneNumber": "123456",
    "emailAddress": "krish.lee@learningcontainer.com"
  },
  {
    "userId": 2,
    "firstName": "racks",
    "lastName": "jacson",
    "phoneNumber": "123456",
    "emailAddress": "racks.jacson@learningcontainer.com"
  },
  {
    "userId": 3,
    "firstName": "denial",
    "lastName": "roast",
    "phoneNumber": "33333333",
    "emailAddress": "denial.roast@learningcontainer.com"
  },
  {
    "userId": 4,
    "firstName": "devid",
    "lastName": "neo",
    "phoneNumber": "222222222",
    "emailAddress": "devid.neo@learningcontainer.com"
  },
  {
    "userId": 5,
    "firstName": "jone",
    "lastName": "mac",
    "phoneNumber": "111111111",
    "emailAddress": "jone.mac@learningcontainer.com"
  }
]

yonghang@air xtable %
yonghang@air xtable % cat test/t3.json | xtable -F md
|  userId | firstName | lastName | phoneNumber | emailAddress                        |
|  ------ | --------- | -------- | ----------- | ----------------------------------  |
|       1 | Krish     | Lee      | 123456      | krish.lee@learningcontainer.com     |
|       2 | racks     | jacson   | 123456      | racks.jacson@learningcontainer.com  |
|       3 | denial    | roast    | 33333333    | denial.roast@learningcontainer.com  |
|       4 | devid     | neo      | 222222222   | devid.neo@learningcontainer.com     |
|       5 | jone      | mac      | 111111111   | jone.mac@learningcontainer.com      |
yonghang@air xtable %
```
