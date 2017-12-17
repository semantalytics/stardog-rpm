%define __jar_repack %{nil}

Name: stardog
Version: 5.1.0
Release: 1.centos7
Summary: Stardog database
Group: Applications/Databases
License: Stardog
URL: http://docs.stardog.com
Source0: stardog-5.1.0.zip
BuildArch: noarch
Packager: Zachary Whitley <zachary.whitley@semantalytics.com>

BuildRequires: sed
Requires: bash-completion shadow-utils java-1.8.0-openjdk-headless logrotate

%description
Stardog is an enterprise data unification platform built on smart graph technology: query, search, inference, and data virtualization.

%pre
getent group stardog >/dev/null || groupadd -r stardog
getent passwd stardog >/dev/null || \
    useradd --gid stardog --shell /sbin/nologin --home-dir /opt/stardog --no-create-home \
    --comment "Stardog database system account" stardog
exit 0


%prep
%setup -q
%install
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/opt/stardog

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
cp docs/man/man1/* ${RPM_BUILD_ROOT}%{_mandir}/man1

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
cp docs/man/man8/* ${RPM_BUILD_ROOT}%{_mandir}/man8

cp -r bin client docs server webconsole ${RPM_BUILD_ROOT}/opt/stardog

mkdir -p ${RPM_BUILD_ROOT}/opt/stardog-ext

mkdir -p ${RPM_BUILD_ROOT}/etc/bash_completion.d
cp bin/stardog-completion.sh ${RPM_BUILD_ROOT}/etc/bash_completion.d

mkdir -p ${RPM_BUILD_ROOT}/usr/bin
ln -s /opt/stardog/bin/stardog ${RPM_BUILD_ROOT}/usr/bin/stardog
ln -s /opt/stardog/bin/stardog-admin ${RPM_BUILD_ROOT}/usr/bin/stardog-admin

mkdir -p ${RPM_BUILD_ROOT}/var/lib/stardog
mkdir -p ${RPM_BUILD_ROOT}/etc/profile.d

cat > ${RPM_BUILD_ROOT}/etc/profile.d/stardog.sh <<EOL
source /etc/sysconfig/stardog
export STARDOG_HOME
export STARDOG
EOL

echo '*:*:*:admin:admin' > ${RPM_BUILD_ROOT}/opt/stardog/.sdpass

mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d

mkdir -p ${RPM_BUILD_ROOT}/var/log/stardog
touch ${RPM_BUILD_ROOT}/var/log/stardog/stardog.log
touch ${RPM_BUILD_ROOT}/var/log/stardog/zookeeper.log
touch ${RPM_BUILD_ROOT}/var/log/stardog/audit.log
touch ${RPM_BUILD_ROOT}/var/log/stardog/access.log
touch ${RPM_BUILD_ROOT}/var/log/stardog/slow_query.log

cat << EOF > ${RPM_BUILD_ROOT}/etc/logrotate.d/stardog
/var/log/stardog/stardog.log {
    missingok
    notifempty
    compress
    copytruncate
    size 20k
    daily
    create 0660 stardog stardog
}

/var/log/stardog/zookeeper.log {
    missingok
    notifempty
    compress
    copytruncate
    size 20k
    daily
    create 0660 stardog stardog
}

/var/log/stardog/access.log {
    missingok
    notifempty
    compress
    copytruncate
    size 20k
    daily
    create 0660 stardog stardog
}

/var/log/stardog/audit.log {
    missingok
    notifempty
    compress
    copytruncate
    size 20k
    daily
    create 0660 stardog stardog
}

/var/log/stardog/slow_query.log {
    missingok
    notifempty
    compress
    copytruncate
    size 20k
    daily
    create 0660 stardog stardog
}
EOF

cat << EOF > ${RPM_BUILD_ROOT}/var/lib/stardog/stardog.properties
# Stardog Configuration
# -----------------------------
# This file contains example Stardog configuration properties to configure Stardog's global behavior. Stardog 
# configuration file should be named 'stardog.properties' and put into the Stardog home directory to take effect.
# Any changes to Stardog configuration requires the Stardog server to be restarted if it is already running. 
#

# Query Answering
# ---------------
# This option controls the behavior for answering queries that don't specify a dataset (FROM or FROM NAMED) in 
# the query. In such cases, the SPARQL specification says that the query should be answered only using the 
# default graph (no named graphs). However, sometimes it is desirable to answer such queries using all
# the information in the database, including the default graph and all named graphs. Setting this option to true
# changes the behavior of Stardog to do this. Queries that specify a dataset are not affected by this option.
# 
# query.all.graphs = true

# Default query timeout duration for all databases in this server. Once a query execution time exceeds this limit
# the query will be automatically killed by Stardog and the client will receive an error message. This value can be
# overridden by a database-specific timeout value in database options. If this value is set to 0 then no query will 
# timeout unless overridden by the database option. The default value for this option is 5 minutes.
# <p>
# The timeout values specified in the property file should be a positive integer followed by either letter 'h' (for
# hours), letter 'm' (for minutes), letter 's' (for seconds), or letters 'ms' (for milliseconds). 
# Examples: '1h' for 1 hour, '5m' for 5 minutes, '90s' for 90 seconds, '500ms' for 500 milliseconds.
# 
# query.timeout = 500ms


# Access Log
# ----------
# Logs all connection-based events, such as queries and transactional changes, and authentication events. Connection
# boundary events, that is open and closing of the actual connection, are not logged. 
#
# Access log is disabled by default and should be enabled explicitly in the configuration file by uncommenting the next 
# two lines. The type of the log is required and there are two allowed values 'text' and 'binary', both based on Protobuf. 
# In text logs, entries are serialized as key-value pairs in plain text and log entries are delimited by the ASCII Start 
# of Text and ASCII End of Text bytes. In binary logs, entries are written as size delimited protobuf binary messages.
# 

logging.access.enabled = false
logging.access.type = text

#
# [Optional] File name. By default, access log is saved as a file named 'access.log' inside the ${STARDOG_HOME}
# directory. Optionally a different file name can be provided as follows. An absolute path can be provided to save the 
# file in a different directory.
#

logging.access.file = /var/log/stardog/access.log

#
# [Optional] File rotation. It is possible to define a file rotation strategy so that log entries will be split into multiple
# files. One possibility is to define a limit on file size and start a new file when the size limit is reached. The file
# that exceeds the limit will be renamed with a unique suffix and all the subsequent entries will be added to the newly
# created file. The size limit is defined in bytes as follows. See audit log example for defining an alternative way of
# rotating files based on fixed-time intervals. 
#
# logging.access.rotation.type = size
# logging.access.rotation.limit = 1000000


# Audit Log
# ----------
# Logs all events and is a superset of the access log. 
#
# Audit log is disabled by default and should be enabled explicitly in the configuration file by uncommenting the next
# two lines.

logging.audit.enabled = false
logging.audit.type = binary

# [Optional] File name. By default, audit log is saved as a file named 'audit.log' inside the ${STARDOG_HOME} 
# directory. Optionally a different file name can be provided as follows. An absolute path can be provided to save the 
# file in a different directory.

logging.audit.file = /var/log/stardog/audit.log

# [Optional] File rotation. Audit logs can be rotated similar to access logs. Size limit can be used as described above. 
# Alternately, log files can be rotated at fixed time intervals. The interval value should be a positive integer 
# followed by either letter 'd' (for days) or letter 'h' (for hours). Examples intervals are '7d' for weekly logs, '1d' 
# for daily logs, '12h' for two log files per day, and '1h' for hourly logs. 
#
# logging.audit.rotation.type = time
# logging.audit.rotation.interval = 1d
#
# Note, while it is unlikely that both access and audit logging should be enabled, Stardog will not prevent you from 
# doing that. But it's strictly superfluous since audit logging is a strict superset of access logging; i.e., the former 
# can be created from the latter offline.


# Slow Query Log
# --------------
# Logs all slow queries. A query is considered to be slow if its execution time exceeds the slow_query.time value
# defined below. 
#
# Slow log query should be enabled similar to other logs 
#

logging.slow_query.enabled = false

#
# Slow query time is specified as follows. Any query whose execution time exceed this limit will be logged in the slow
# query log. The time value should be a positive integer followed by either letter 'h' (for hours), letter 'm' (for minutes), 
# letter 's' (for seconds), or letters 'ms' (for milliseconds). Examples intervals are '1h' for 1 hour, '5m' for 5 minutes, 
# '90s' for 90 seconds, and '500ms' for 500 milliseconds. If no time is specified in the configuration, the default value
# of 1 minute will be used. 
# 
# logging.slow_query.time = 10s
#
# [Optional] Log type. Unlike access or audit logs, slow query log has a default type for formatting the slow query events
# which is intended to be human-readable. If no log type is specified, this default type will be used. This default format
# is not suitable for machine-processing and meant to be only for developers to read. For a machine-processable format,
# the type of the slow query log can be set similar to other logs.  
#
# logging.slow_query.type = text | binary
#
# [Optional] File name and rotation. By default, slow query log is saved as a file named 'slow_query.log' inside the 
# ${STARDOG_HOME} directory. Optionally a different file name and a file rotation can be provided similar to other
# logs. See the instructions above.

logging.slow_query.file = /var/log/stardog/slow_query.log

# Log Failure
# ----------- 
# There is an additional flag for controlling how failure to create a log is interpreted.  By default, a warning message 
# is printed to the system logs. But, for example, if you are using the audit logs you may not want to start the server 
# *without* audit logging and want any failure to be interpreted as a fatal error. You can use the following setting
# for this purpose.
#
# logging.create.failure.fatal = true 


# Connection configuration
# ------------------------
# Connections that have been idle for a specified amount of time are automatically closed by the server. The following
# option specifies this limit in milliseconds. The default limit is 3600000 (1 hour).
#
# database.connection.timeout.ms = 30000


# HTTP Configuration
# ------------------
# The maximum number of simultaneous http connections for a client is configured by the following two options. 
# See http://hc.apache.org/httpcomponents-client-ga/tutorial/html/connmgmt.html
#
# http.max.connections = 200
#
# The length in characters of the longest query that can be sent over HTTP GET to the Stardog server. This is to avoid 
# URL overflow in some web servers.  When the query is longer than this threshold, Stardog will automatically switch 
# over to using HTTP POST. 
#
# http.max.get.query.length = 2000


# Waldo Configuration
# ------------------
# Configure whether or not an additional step of performing a describe over the literal being index should be performed
# while building search indexes.  false by default, setting this value to true can allow for more accurate searches by
# including information about the triples referencing the literal to its search index.  However, this also slows down
# search indexing and increases the size of the search index.
#
# waldo.describe.during.indexing = true
#
# Use of wildcards as the leading character in a search string is not enabled by default as this tends to be an expensive
# operation, this is mentioned in the Lucene FAQ (http://wiki.apache.org/lucene-java/LuceneFAQ).  However, if your use
# case requires leading wild card searches, they can be enabled by setting this property to true.
#
# leading.wildcard.search.enabled = true


# Watchdog JMX Configuration
# --------------------------
# Explicitly enable or disable the Watchdog JMX module.  Has no effect if Watchdog is not available or disabled directly
# due to license restrictions.  The default is true.
#
# watchdog.enabled = true
#
# Specify whether or not Watchdog should be accessible remotely.  When true, you will be able to access the Watchdog JMX
# server remotely at the default port (5833) or the specified 'watchdog.jmx.port'.  If false, the Watchdog JMX server
# will only be accessible via the process running the JVM.  The default value is 'true'
#
# watchdog.remote.access = true
#
# If the Watchdog JMX server is configured for remote access, by default, it will bind to port 5833.  You can provide a
# different port for the server by setting this property
#
# watchdog.port = 5833


# SSL
# ---
# If you would like to set any of the standard system properties for SSL support, you can provide them here rather than
# via the standard JVM arguments.  Note that these specify the global defaults, they can be overridden on a case by
# case basis using the appropriate ServerOptions.
#
# Specify the password for the keystore.
#
# javax.net.ssl.keyStorePassword = myKeyStorePassword
#
# Specify the location of the keystore.  If this is not specified, $STARDOG_home/keystore is checked, and then, the
# standard JVM locations within $JAVA_HOME.
#
# javax.net.ssl.keyStore = /path/to/the/keystore
#
# Finally, if the keystore is of a different type than the default (JKS), you can specify its type:
#
# javax.net.ssl.keyStoreType = FOO

# Backups
# ---
# Specify the top level directory which is to be used by Stardog for storing backups.  By default, this is the
# '.backup' directory in your Stardog home, but you can use this property to specify a different location for
# backups.  Within this directory, backups are stored by database, and for each database, in date-versioned
# directories.
#
# Your typical backup directory would have a layout similar to this:
# .backup/myDb/2013-10-02
# .backup/myDb/2013-10-11
# .backup/myOtherDb/2013-06-21
#
# Within each of those directories are the actual backups themselves.  If you want to restore a database from
# one of those backups, you will have to use the complete path to the backup, not just the path to the top
# level directory as specified by this property, ie, `db restore $STARDOG_HOME/.backup/myDb/2013-10-02`
#
# backup.dir = /path/to/backup/directory

# Exports
# ---
# Specify the top-level directory for storing files which are exported by the server.  The default value is '.exports'
# in your $STARDOG_HOME directory.
#
# export.dir = /path/to/export/directory
EOF


mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig

cat << EOF > ${RPM_BUILD_ROOT}/etc/sysconfig/stardog
STARDOG_HOME="/var/lib/stardog"
STARDOG="/opt/stardog"
STARDOG_JAVA_ARGS="-Xmx2g -Xms2g -XX:MaxDirectMemorySize=1g"
STARDOG_SERVER_JAVA_ARGS="-Xmx2g -Xms2g -XX:MaxDirectMemorySize=1g"
STARDOG_EXT="/opt/stardog-ext"
EOF

mkdir -p ${RPM_BUILD_ROOT}/usr/lib/systemd/system

cat << EOF > ${RPM_BUILD_ROOT}/usr/lib/systemd/system/stardog.service
[Unit]
Description=Stardog database
After=syslog.target network.target

[Service]
Type=simple
EnvironmentFile=-/etc/sysconfig/stardog
ExecStart=/usr/bin/stardog-admin server start $STARDOG_OPTS --foreground
ExecStop=/urs/bin/stardog-admin server stop
User=stardog
Group=stardog

[Install]
WantedBy=multi-user.target
EOF

sed -i -e 's#${sys:stardog.home}#/var/log/stardog#' ${RPM_BUILD_ROOT}/opt/stardog/server/dbms/log4j2.xml

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(0755,stardog,stardog)
%doc docs/COMMUNITY_LICENSE.txt docs/EVALUATION_LICENSE.txt docs/README.txt docs/COPYRIGHT.txt
%attr(644,root,root) %{_mandir}/man1/*
%attr(644,root,root) %{_mandir}/man8/*
%{_bindir}/stardog
%{_bindir}/stardog-admin
%attr(554,stardog,stardog)/opt/stardog/bin/stardog
%attr(554,stardog,stardog)/opt/stardog/bin/stardog-admin
%dir%attr(750,stardog,stardog)/opt/stardog-ext
%dir%attr(750,stardog,stardog)/opt/stardog
%dir%attr(750,stardog,stardog)/opt/stardog/bin
%dir%attr(750,stardog,stardog)/opt/stardog/client
%dir%attr(750,stardog,stardog)/opt/stardog/docs
%dir%attr(750,stardog,stardog)/opt/stardog/server
%dir%attr(750,stardog,stardog)/opt/stardog/webconsole
%attr(600,stardog,stardog)/opt/stardog/.sdpass
%attr(-,stardog,stardog)/opt/stardog/bin/helpers.bat
%attr(-,stardog,stardog)/opt/stardog/bin/helpers.sh
%attr(-,stardog,stardog)/opt/stardog/bin/install-service.bat
%attr(-,stardog,stardog)/opt/stardog/bin/stardog-admin.bat
%attr(-,stardog,stardog)/opt/stardog/bin/stardog-admin.fish
%attr(-,stardog,stardog)/opt/stardog/bin/stardog-completion.sh
%attr(-,stardog,stardog)/opt/stardog/bin/stardog-server
%attr(-,stardog,stardog)/opt/stardog/bin/stardog-serverw.exe
%attr(-,stardog,stardog)/opt/stardog/bin/stardog.bat
%attr(-,stardog,stardog)/opt/stardog/bin/stardog.fish
%attr(-,stardog,stardog)/opt/stardog/bin/stop-service.bat
%attr(-,stardog,stardog)/opt/stardog/bin/uninstall-service.bat
%attr(-,stardog,stardog)/opt/stardog/bin/windows/amd64/stardog-server.exe
%attr(-,stardog,stardog)/opt/stardog/bin/windows/ia64/stardog-server.exe
%attr(-,stardog,stardog)/opt/stardog/client/*
%attr(-,stardog,stardog)/opt/stardog/docs/*
%attr(-,stardog,stardog)/opt/stardog/server/*
%attr(-,stardog,stardog)/opt/stardog/webconsole/*
%dir%attr(700,stardog,stardog)/var/lib/stardog
%dir%attr(755,root,stardog)/var/log/stardog
%attr(664,root,stardog)/var/log/stardog/zookeeper.log
%attr(664,root,stardog)/var/log/stardog/stardog.log
%attr(664,root,stardog)/var/log/stardog/audit.log
%attr(664,root,stardog)/var/log/stardog/access.log
%attr(664,root,stardog)/var/log/stardog/slow_query.log
%attr(640,stardog,stardog)/var/lib/stardog/stardog.properties
%attr(644,root,root)/etc/bash_completion.d/stardog-completion.sh
%attr(644,root,root)/etc/logrotate.d/stardog
%attr(644,root,root)/etc/profile.d/stardog.sh
%attr(644,root,root)/etc/sysconfig/stardog
%attr(644,root,root)/usr/lib/systemd/system/stardog.service

%changelog
* Sun Dec 17 2017 Zachary Whitley <zachary.whitley@semantalytics.com>
- Update verstion to 5.1.0
- Fix ext directory
* Sat Nov 18 2017 Zachary Whitley <zachary.whitley@semantalytics.com>
- Bump version to 5.0.5.1
- Surpress creating home directory for stardog user
- Add env variable for extensions and server java args
* Sat Jan 14 2017 Zachary Whitley <zachary.whitley@semantalytics.com>
- Update to Stardog 4.2.2
* Sun Oct 02 2016 Zachary Whitley <zachary.whitley@semantalytics.com>
- Initial spec

# TODO
#separate rpm for javadoc? client? server?
