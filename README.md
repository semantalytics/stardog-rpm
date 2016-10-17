# Stardog RPM for CentOS 7

## Building the RPM

```
[userid@hostname ~]$ sudo yum install rpm-build
```

Create directories for RPM building using your home 

```
[userid@hostname ~]$ echo '%_topdir %(echo $home)/rpmbuild' > ~/.rpmmacros
```

download stardog using link in email sent after requesting download at http://stardog.com

```
[userid@hostname ~]$ wget --content-disposition --directory-prefix ~/rpmbuild/SOURCES/ 'http://mandrillapp.com/track/click/30526154/stardog.s3-website-us-east-1.amazonaws.com?p=eyJzIjoid1dnQ3FLY...'
```

download rpm spec file

```
[userid@hostname ~]$ wget --directory-prefix ~/rpmbuild/SPECS/ 'https://raw.githubusercontent.com/semantalytics/stardog-rpm/master/stardog.spec'
```

Build rpm

```
[userid@hostname ~]$ rpmbuild -bb ~/rpmbuild/SPECS/stardog.spec
```

## Installation

```
[userid@hostname ~]$ sudo yum install ~/rpmbuild/PRMS/stardog-4.2-1.centos7.noarch.rpm
```

## Post installation

Log out and log back in to pick up environment variables 

download license key

```
[userid@hostname ~]$ wget --content-disposition --directory-prefix $STARDOG_HOME 'http://mandrillapp.com/track/click/30526154/stardog.s3-website-us-east-1.amazonaws.com?p=eyJzIjoid1dnQ3FLY...'
```

```
[userid@hostname ~]$ sudo usermod -a -G stardog userid
```

```
[userid@hostname ~]$ sudo systemctl enable stardog
```

```
[userid@hostname ~]$ sudo systemctl start stardog
```

admin password must be updated in /opt/stardog/.sdpass if changed
