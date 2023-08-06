# Inspect requirements

Inspect requirements is tool indendend to make it easier to compare requirements.txt files between multiple projects/applications.

Basic usage:

```sh

# e.g. in a directory structure as follows:

$ find .
./project1
./project1/requirements.txt
./project3
./project3/requirements-prod.txt
./project2
./project2/requirements
./project2/requirements/dev.txt


# ..output would be like this:

$ inspect-requirements

Type a number or "q" to continue >a

Select repositories (or "a" for all)
* 1: project1
* 2: project3
* 3: project2

--- Summary ---
fastapi, 2 different versions
  * project1/requirements.txt: "==0.75.0"
  * project3/requirements-prod.txt: "==0.74.0"
  * project2/requirements/dev.txt: "==0.74.0"
starlette, 1 different versions
  * project1/requirements.txt: "==0.19.1"
  * project3/requirements-prod.txt: "==0.19.1"
  * project2/requirements/dev.txt: "==0.19.1"
psycopg2, 2 different versions
  * project1/requirements.txt: "==2.9.3"
  * project3/requirements-prod.txt:
  * project2/requirements/dev.txt: "==2.9.3"
pytz, 1 different versions
  * project2/requirements/dev.txt: "==2022.1"

```
