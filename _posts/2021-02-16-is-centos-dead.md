---
categories:
- blog
tags:
- fedora
- centos
image: assets/images/distros/centos.png
layout: post
title: Is CentOS Dead? The reports of its demise are greatly exaggerated. 
date: 2021-02-16 21:31 +0800
---
End of last year, CentOS project announced that they are [shifting their
focus to CentOS Stream](https://blog.centos.org/2020/12/future-is-centos-stream/). 

Not surprisingly, this triggered a major outlash from users worldwide, especially
from those who barely understand the change, and merely react to perception
raised by various online media, who are not even contributors to the Fedora nor
CentOS project. The general tone is, "RedHat have killed CentOS", "CentOS is dead",
and similar perception.

However, this is far from truth. The focus to CentOS Stream is primarily:

* an announcement that CentOS will no longer release point releases (8,1, 8,2, 8,3..)
* smoothen out the flow for community contributions ("community" in this sense are
  people who work on improving CentOS, such as fixing bugs, who are not Red Hat employees)
* make modularity a first class citizen, where core of the OS is well maintained with
  latest security updates and bugfixes, while ecosystem packages are maintained separately
  as AppStreams.

No more point release
----------------------

Historically, CentOS tracks RHEL, of which a new CentOS release is created, after a new 
RHEL release is launched. This make sense at the early days of CentOS, where it is primarily
a rebranded rebuild of RHEL. But take note, the point releases of RHEL recent years, are 
primarily a snapshot of a specific state of the RHEL updates repositories, akin to a 
mid-release [Fedora respin](https://fedoraproject.org/wiki/Respins-SIG). This allows 
sysadmin to create a new installation with latest set of packages with latest bugfixes
from the start, rather than installing an old point release, and `yum update` afterwards. 
A legacy from the era where internet was a fraction of the speed available today.

If you are a sysadmin that regularly run `yum update` on your server, basically nothing will
change for you. If you use containers and always ensure you containers runs `yum update` during
build, nothing will change for you too. 

Empowering the Community in C(ommunity)Ent(erprise) Linux
-----------------------------------------------------------

This is something which I believe many users would barely appreciate, but is something very
important to us who involve in Open Source OS level development, or involve in supporting 
our clients commercially. The traditional CentOS is not that open to community, because
it is trying to keep bug-to-bug compatibility to RHEL. This is a problem when:

* If you found a bug in a package coming from CentOS, and you want to contribute fixes 
  to the bug, in the traditional flow, you would have to get this bug fixed upstream in RHEL,
  as it could not be accepted in CentOS.
* If you created some packages, and want these packages to be part of the main distribution
  channels (eg: AppStreams), there are no clear way for this. 

While majority of users who involve in application deployment, or userspace application
development barely have any use case for above flow, for those who are involved with 
large enterprises and large projects that work closely with RHEL/CentOS ecosystem would face
frustrations in the processes. This is especially true for projects such as OpenStack, OKD,
oVirt, and companies such as Intel and Facebook, who uses, fix bugs and improve CentOS. The 
new change of project governance now would make it easier to the community to get involved.

Remember here, a "community" in an Open Source project are people who contributes to a project,
which can be as doing something as simple as promoting the project, supporting/helping
others in using the project in community forums, or something more complex such as fixing bugs
and building new features. A user who only consume, while some may argue is part of the community,
barely holds currency in influencing the direction of the project. One could not expect 
a consumer-first direction like what can be seen in commercial softwares, because in commercial
softwares, the consumers are contributing back in the form of payment to the organization
that produce the software, and that is a big influence. When the threshold of contributors 
drop in an Open Source project, or start to be mainly handled by a single person or organization,
a project is more likely to die, or to turn to proprietary model in order to sustain itself.

Stability
-----------

Some argue that the switch to rolling release model of CentOS Stream would imply CentOS 
would now no longer be stable. But what exactly is "stable"?. In software development,
the word "stable" can mean different things. To a consumer, "stable" is usually mean
something would not crash, nor have issues. However, to developers, "stable" means
a state of no changes nor updates. 

Being "stable" in the sense of no updates, may not translate to "stable" of no issues.
Modern software development usually applies agile methodology to develop software. 
An initial version of a software may not be issue-proof in its early releases, and
would require constant updates to be rolled out to fix issues. However, constant
updates would mean, the software is not "no-changes stable". Traditional CentOS and
RHEL is very resistant to changes due to its approach of minimizing updates, however, 
this results in an ecosystem where new bugfixes to softwares could not be easily rolled out, and
also create an environment that is difficult to work with for modern agile developers
who may require latest version of components, which carry latest bugfixes and improvements. 
Unlike the old days where software were developed in very slow waterfall model, modern
application development demands faster adoption of updates, and there is a need to
address this requirement. 

Having said that, "no change stable" is also important, however, not in the sense of 
barely having changes. There can be changes, but changes are managed to minimize service
distruption. How software developers traditionally manage this stability is 
through good release engineering which splits software releases into major and minor release. 
Within a major release, users of a software can expect no changes in the public interfaces
of the software, and that all other software that depend on it would continue working,
across all minor releases of the software. Minor releases would only be doing bugfixes,
and new feature introduction, without breaking existing functionalities. 

Circa 2013, there was an initiative in Fedora in creating a better, and more agile Fedora, 
called the [Fedora.next Initiative](https://fedoraproject.org/wiki/Fedora.next). One of 
the result of that is [Fedora Modularity](https://docs.fedoraproject.org/en-US/modularity/), 
which is a new architecture where Fedora would have a base OS layer, which are maintained 
on its own stream, and "modules" where users may choose a specific major release of a 
software component, and only receive updates related to that major release. CentOS/RHEL
AppStream repositories, introduced in RHEL8/CentOS8, was born from this initiative. 

With AppStreams, you can now choose to, for example, enable only PostgreSQL 9 and subscribe 
to its updates and bugfixes, without risking your system updating to PostgreSQL 12, which 
is also available in the modularity repos. This create a platform that would allow 
better "issue-proof stability", while keeping balance with "no-changes stability". 

With fixes landing in CentOS first before going into RHEL, it also opens up better opportunity
for the community to receives fixes early, and bugfix contributions from the community
would be easier to be accepted. Additionally, Fedora still play a role in ensuring stability
of CentOS/RHEL, because introduction of new major features and major component versions will
still land in Fedora first, instead of CentOS. Fedora still serve as the development
ground for the next major release of CentOS/RHEL, through the 
[Fedora ELN (El-nino / Enterprise Linux Next, whichever you fancy), Buildroot](https://docs.fedoraproject.org/en-US/eln/). 

One might think that with CentOS receive fixes first before RHEL, CentOS is now a beta for RHEL,
however, this is nonsense. Under that analogy, would the traditional setup where RHEL receives 
fixes first before CentOS, make RHEL a beta version of CentOS?. We all know that is false. 

What's with the EOL?
---------------------

The announcement from CentOS of EOL-ing traditional CentOS is mainly about that they are
stopping the effort to produce point-releases of CentOS 8. CentOS 8 will still continue to
be supported until RHEL 8 full-support EOL, which is until 2024. CentOS 9 will still 
be released alongside RHEL 9, and that too, will be supported until RHEL 9 full-support EOL.

Hope this clears up the FUD about CentOS Stream that have been going around for a while now. 
You may also check out [this presentation](https://www.slideshare.net/kagesenshi/centos-stream-how-will-this-impact-you) for additional information. 

Don't worry, CentOS will still continue to be a great Community-driven Enterprise Linux 
distribution. 
