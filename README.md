# Golden Sixpacks

Golden Sixpacks are yearly awards that Datascope is experimenting with
as a mechanism to recognize each others' accomplishments.

### Main guidelines

- Like the Oscars, we have multiple categories, with one award in each
- The categories represent the different avenues of value we bring
- People nominate others for awards, with a short (tweet-length)
  description of what they deserve the nomination
- For each award, we all vote anonymously (you can't vote for yourself)
- Winner of each award is announced
- We divide the performance bonus pool by the number of awards, each award comes with one such unit of bonus

### Awards
- **The Closer**  Bringer of new clients and projects
- **The Executer**  Getter-doner of shit (code / management / correspondence)
- **The Rockstar**  Contributor to Datascope’s reputation (blog posts / talks /
famous pro-bono work)
- **The Professor**  Trainer of self and colleagues (analysis / code / design
/ communication)
- **The Collaborator**  Awesome to work with (brainstorming skills / helping
right when needed / trusted to do things on their plate well / fun to
work with)
- **The Navigator**  Major contributor to our culture and business design

### Running the Vote with this Little App
You need to ask for nominations over time and record them in the
award_data.json (not tracked) and run the app to get the votes. This
award_data.json file contains both details about the awards and the
nomination information. To give you an idea on the format and
contents, an example is checked in the repo.

### Getting started
* Install [Vagrant](http://vagrantup.com),
[Fabric](http://fabric.readthedocs.org/en/latest/installation.html),
and [fabtools](http://fabtools.readthedocs.org/en/latest/).

* Change config.ini to have your project name (currently called
fab-tools-start-kit).  Only use letters, numbers, hyphens

* From the command line, run `vagrant up`. This will
create and power up a virtual machine

* Run `fab dev provision`. This will install all the necessary
packages
on the virtual machine.

* SSH to the virtual machine with `vagrant ssh FabTools_StartKit` #
project name from config.ini

* Put in any python or other unix tools you want in REQUIREMENTS or
REQUIREMENTS-DEB
