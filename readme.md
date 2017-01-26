# Vulnerable flask app

### Install python2.7.x

https://www.python.org/downloads/

- Instructions for multiple platforms:

https://wiki.python.org/moin/BeginnersGuide/Download

- If you are using *nix based OS there's good chance python is already installed.

- On Windows in installation setup you can choose to add python's folder to your "PATH" so you can run it anywhere without absolute path.


- If you have multiple python versions installed and python2 is not default use `python2` and `pip2` in commands below.

### Install other depencies

- pip how to: https://pip.pypa.io/en/stable/

- Open terminal and run command:

`pip install flask`

### Launch app

- Clone this repo with git or download zip and extract.

- Open cmd/terminal

- Navigate to code folder where you cloned or extracted this repository and run:

`python app.py`

Open web browser and go to `http://127.0.0.1:5000`

## Report

1. SQL-injection
Applications login form has SQL-injection vulnerability which allows attacker to login without knowing credentials. Also search function has injection vulnerability which allows attacker to view private notes of  all users.

- Steps to identify:
Login:
Simple way to notice injection flaw is to give input like " 'anything "(without " ") to username input and any string to password and then submit. That will cause "sqlite3.OperationalError" exception.
To actually exploit this flaw insert string like "'OR '1'='1"(without "") in username and password inputs. Then press login and you will be logged in as first user in database.
Search:
With using string like "'OR '1'='1" the application will list all comments and all users private notes from database because they are stored in same table.

- How to fix:
Passwords are stored as plaintext in database so hashing+salt should of course be used. Plaintext stored passwords are obviously bad in general but also with this issue if hashing would be used it mostly prevents the attack described above. When attacker gives malicious input for password like "'OR '1'='1" then hash+salt will turn it in somehting like "a4fe1eb5a3cfbdf28a32abb24095eefa" and of course then it doesn't have same kind of affect in SQL select statement. Also prepared statements should be used in every SQL-statement of the application so SQL injection flaws could be prevented in general like the one in search function.


2. Reflected Cross site scripting:
Application has reflected xss vulnerability in its search function. If search doesn't come up with any results users input is reflected back. This allows attacker to craft malicious url for the search.

- Steps to identify:
When search function of the app is being used it can be noticed that it takes one parameter "term". So testing with some malicious input will help to learn that application is vulnerable to xss attack. Full example:
http://<theapp>:<port>/search?term=<script>alert(1)</script>

Note: Some browsers like latest version of Google Chrome seems to block this attack. Chrome actually tels in console of developers tool that it has blocked javascript from running to prevent xss attack. But this has tested to work with Firefox 50.1.0 and Internet Explorer 11.

- How to fix:
Every input should be considered as unsafe and be escaped. With Jinja templates that flask uses this flaw would be actually fixed by default so just removing "| safe" from displayed variables in templates should fix this issue.

3. Stored Cross site scripting
Application also has stored xss vulnerability. When comments are send and displayed to user the data isn't escaped.

- Steps to identify:

Post comment to site with string like "<script>alert(1);</script>". Now javascript is being executed when index or users home page is loaded.

- How to fix:

Same fix as in reflected xss. In short, escape all input given by users.

4.Insecure Direct Object References
When user accesses to his private notes it's being checked that user is authenticated but not that current user is the user which data is being requested.

- Steps to identify:
Launch the app and when logged in select "My notes" from navbar. Now applications path is "/home/id/<users_id>". Now by changing id number in url user can access other users private notes.

- How to fix:
Now app only checks that user accessing '/home/id/<id>' is authenticated. It should also check that user id in session matches to id which notes are being requested.

5. Cross-Site Request Forgery (CSRF)
App doesn't send csrf token in forms.

- Steps to identify:

Launch app and login then open new browser window and run similar url in browser: http://<theapp:port>/sendata?note=nocsrftoken
This url will make logged in user to send public comment "nocsrftoken" to site without being prompted.

- How to fix:
First allowing GET requests to “/sendata” which is route for posting comments/notes is useless and allowing POST would be enough. Though this alone isn’t enough, instead also csrf tokens should be used. With flask it is possible to use CSRFProtect extension and initialize app with it. Then "{{ csrf_token() }}" just needs to be added to forms in hidden input and Flask will basically take care of less. If done manually csrf tokens should be generated and return with  requests, then tokens needs  to be send to templates on requests and add it in forms input and check for the token on server side when form is submitted.

Using OWASP ZAP to identify some of these vulnerabilities:

Launch ZAP and set your web browser to use ZAPs proxy server. Launch the vulnerable app and just use quick attack option in main screen and pass http://localhost:5000 as url and press "Attack".
ZAP will identify SQL injection vulnerability in login form. Also XSS vulnerabilitie in search function will be instantly detected. To test for stored XSS(ZAP flagged this as reflected) post one comment on site and then select that request from "sites" in zap and select "attack".
This of course will also make ZAP post every string that it tests as comment.

## Report

1.SQL-injection

Applications login form has SQL-injection vulnerability which allows attacker to login without knowing credentials. Also search function has injection vulnerability which allows attacker to view private notes of  all users.

- Steps to identify:

Login:
Simple way to notice injection flaw is to give input like " 'anything "(without " ") to username input and any string to password and then submit. That will cause "sqlite3.OperationalError" exception.
To actually exploit this flaw insert string like "'OR '1'='1"(without "") in username and password inputs. Then press login and you will be logged in as first user in database.
Search:
With using string like "'OR '1'='1" the application will list all comments and all users private notes from database because they are stored in same table.

- How to fix:

Passwords are stored as plaintext in database so hashing+salt should of course be used. Plaintext stored passwords are obviously bad in general but also with this issue if hashing would be used it mostly prevents the attack described above. When attacker gives malicious input for password like "'OR '1'='1" then hash+salt will turn it in somehting like "a4fe1eb5a3cfbdf28a32abb24095eefa" and of course then it doesn't have same kind of affect in SQL select statement. Also prepared statements should be used in every SQL-statement of the application so SQL injection flaws could be prevented in general like the one in search function.


2.Cross site scripting:

Application has reflected xss vulnerability in its search function. If search doesn't come up with any results users input is reflected back. This allows attacker to craft malicious url for the search.

- Steps to identify:
When search function of the app is being used it can be noticed that it takes one parameter "term". So testing with some malicious input will help to learn that application is vulnerable to xss attack. Full example:
http://<theapp>:<port>/search?term=<script>alert(1)</script>

Note: Some browsers like latest version of Google Chrome seems to block this attack. Chrome actually tels in console of developers tool that it has blocked javascript from running to prevent xss attack. But this has tested to work with Firefox 50.1.0 and Internet Explorer 11.

- How to fix:

Every input should be considered as unsafe and be escaped. With Jinja templates that flask uses this flaw would be actually fixed by default so just removing "| safe" from displayed variables in templates should fix this issue.

Application also has stored xss vulnerability. When comments are send and displayed to user the data isn't escaped.

- Steps to identify:

Post comment to site with string like "<script>alert(1);</script>". Now javascript is being executed when index or users home page is loaded.

- How to fix:

Same fix as in reflected xss. In short, escape all input given by users.


3.Insecure Direct Object References

When user accesses to his private notes it's being checked that user is authenticated but not that current user is the user which data is being requested.

- Steps to identify:

Launch the app and when logged in select "My notes" from navbar. Now applications path is "/home/id/<users_id>". Now by changing id number in url user can access other users private notes.

- How to fix:

Now app only checks that user accessing '/home/id/<id>' is authenticated. It should also check that user id in session matches to id which notes are being requested.

4.Cross-Site Request Forgery (CSRF)

App doesn't send csrf token in forms.

- Steps to identify:

Launch app and login then open new browser window and run similar url in browser: http://<theapp:port>/sendata?note=nocsrftoken
This url will make logged in user to send public comment "nocsrftoken" to site without being prompted.

- How to fix:
First allowing GET requests to “/sendata” which is route for posting comments/notes is useless and allowing POST would be enough. Though this alone isn’t enough, instead also csrf tokens should be used. With flask it is possible to use CSRFProtect extension and initialize app with it. Then "{{ csrf_token() }}" just needs to be added to forms in hidden input and Flask will basically take care of less. If done manually csrf tokens should be generated and return with  requests, then tokens needs  to be send to templates on requests and add it in forms input and check for the token on server side when form is submitted.

5. Security Misconfiguration

This vulnerability exists because to make some above vulnerabilities to work I had to disable or bypass some default security configurations of Flask and Jinja2.

Using OWASP ZAP to identify some of these vulnerabilities:

Launch ZAP and set your web browser to use ZAPs proxy server. Launch the vulnerable app and just use quick attack option in main screen and pass http://localhost:5000 as url and press "Attack".
ZAP will identify SQL injection vulnerability in login form. Also XSS vulnerabilitie in search function will be instantly detected. To test for stored XSS(ZAP flagged this as reflected) post one comment on site and then select that request from "sites" in zap and select "attack".
This of course will also make ZAP post every string that it tests as comment.
