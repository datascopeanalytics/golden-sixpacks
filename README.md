# Golden Sixpacks

Golden Sixpacks are yearly awards that Datascope is experimenting with
as a mechanism to recognize each others' accomplishments.

### Main guidelines

- Like the Oscars, we have multiple categories, with one award in each
- The categories represent the different avenues of value we bring
- People nominate others for awards, with a short (tweet-length)
  description of why they deserve the nomination
- Instead of natural gifts and character traits, the idea is to focus on the amount of effort and improvement
- For each award, we all vote anonymously (you can't nominate yourself but you can vote for yourself if nominated)
- Winner of each award is announced
- We divide the performance bonus pool by the number of awards, each award comes with one such unit of bonus

### Awards
- **The Closer**  Bringer of new clients and projects
- **The Executer**  Getter-doner of shit (code / reports / prep)
- **The Navigator**  Major contributor to our culture and business design
- **The Corresponder** Keeper-happy of clients, communicator, keeper-on-tracker
- **The Professor**  Trainer of self and colleagues (analysis / code / design
/ communication)
- **The Collaborator**  Awesome to work with (helping
right when needed / trying to give good feedback / trusted to do things on their plate well / effort into being easy and fun to
work with )


Potentially also:
- **The Rockstar**  Contributor to Datascope’s reputation (blog posts / talks /
famous pro-bono work)
- **The Networker**  Builder of relationships
- **The Maker**  Builder of useful internal or public (non-client) tools


### Getting started
* Install [Vagrant](http://vagrantup.com),
[Fabric](http://fabric.readthedocs.org/en/latest/installation.html),
and [fabtools](http://fabtools.readthedocs.org/en/latest/).

* From the command line, run `vagrant up`. This will
create and power up a virtual machine.

* Run `fab dev provision`. This will install all the necessary
packages on the virtual machine.

* Run `fab dev serve`. This will start the flask development server on the
virtual machine.

* You can interact with the server on your browser at `http://localhost:5000` 
(of course, for others to vote, we need to run the server on a machine with a 
static IP, but for now the instructions will use localhost).

* Go to `http://localhost:5000/admin`
 
* Log in as the initial superuser as listed (dumbledore:hogwarts4eva).
 
* Use the admin interface to create a new superuser, delete dumbledore and log back in.
 
* Create the other users (voters), change the categories if need be, and add nominations.

* Ask participants to give their own nominations, create those as well.
 
* Send paricipants their username and password combinations, give them a deadline, and 
check the admin interface to keep track of the situation as they vote.

* Once everybody votes, share the results with everyone.


