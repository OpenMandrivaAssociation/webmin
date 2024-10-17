# zero out some useless deps.
# (tv) we'd better had a link in minicom & package Encode::HanConvert:
%define __noautoreq '/sbin/runscript|perl\\(Encode::HanConvert\\)|perl\\(Win32::Daemon\\)|perl\\(\\)'
%define __noautoprov 'perl\\(File::BaseDir\\)|perl\\(File::Basename\\)|perl\\(File::MimeInfo\\)|perl\\(JSON\\)|perl\\(JSON::Backend::PP\\)|perl\\(JSON::Boolean\\)'

# don't spend time with this either
%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

%define i18n_date 20080131
%define with_i18n_tarball 1
%define with_i18n_patch 1


Summary:	An SSL web-based administration interface for Unix systems
Name:		webmin
Version:	1.996
Release:	2
License:	BSD
Group:		System/Configuration/Other
URL:		https://www.webmin.com/webmin/
Source0:	http://prdownloads.sourceforge.net/webadmin/%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Source2:	other.modules.tar.bz2
Source30:	webmin-mandriva-theme.tar.bz2
# some images were missing
Source33:	advanced.png
Source34:	descs.png
Source4:	webmin-postinstallscript.sh
Source5:	webmin
Source6:	webmin.service
Source9:	http://www.openit.it/index.php/openit_en/content/download/2474/10171/file/openvpn-2.0.wbm.gz
Source10:	webmin.pam
Source11:	webmin-16.png
Source12:	webmin-32.png
Source13:	webmin-48.png
# uses include instead of pam_stack
Source14:	webmin.pam-new
Source15:	webmin.logrotate
# (gc) have the updates; this needs to change for each version and/or release, see
#      http://www.webmin.com/webmin/updates.html
# Other Themes
Source51:	http://www.gehrigal.net/download/webmin_theme/webmin-theme_gehrigal_0.41.wbt
# the configurator for this theme
Source52:	http://www.gehrigal.net/download/webmin_themeconfig/webmin_gehrigal-themeconfigurator_0.21a.wbm
#  Webmin Module Usermonitor
Source53:	http://www.gehrigal.net/download/webmin_usermonitor/webmin-module_usermonitor_0.12a.wbm
# Other modules
Source54:	http://gaia.anet.fr/webmin/openldap/openldap-0_6.wbm
Source541:	http://gaia.anet.fr/webmin/openldap/openldap2-0_1.wbm
Source55:	http://www.bvan.f2s.com/ldap_groups_LDAPapi.wbm
Source56:	http://www.bvan.f2s.com/ldap_browser_LDAPapi.wbm
Source57:	http://prdownloads.sourceforge.net/netatalk/netatalk.wbm
Source99:	webmin-scripts-i18n.tar.bz2
Source100:	webmin-i18n-%{i18n_date}.tar.bz2
Source101:	awstats-1.9.wbm
Source102:	dgwebmin-0.7.1.wbm
Patch0:		webmin-fix-configs.diff
Patch1:		webmin-1.100-remove-atboot-problem
Patch5:		webmin-fix-newmods.patch
Patch7:		webmin-0.85-never-fail-detect-os.patch
Patch8:		webmin-0.85-enable-changed-theme-at-installation.patch
Patch9:		webmin-1.550-fix-status-in-init.patch
Patch10:	webmin-1.510-fix-os-list.patch

Patch13:	webmin-openldap.patch
Patch15:	webmin-fix-netatalk-paths.patch
Patch17:	webmin-1.220-remove-mandrakestuff-from-init.patch
Patch19:	webmin-0.92-add-default-configs-logviewer-fp2k.patch
Patch21:	webmin-0.950-add-netsaint-mandrake-config.patch
Patch23:	webmin-1.020-ssl-location.patch
Patch24:	webmin-1.020-suppress-missing-netatalk-interfaces.patch
Patch26:	webmin-1.060-mysql-fix-installing-missing-packages.patch
Patch29:	webmin-1.100-let-localauth-config.patch
Patch32:	webmin-1.310-usermin-fix-installing-missing-package.diff
Patch33:	webmin-1.130-postgresql-fix-installing-missing-packages.patch
Patch35:	webmin-1.220-usermin-fix-index.patch
Patch36:	webmin-1.350-mandriva_theme.diff
Patch37:	webmin-temp-permission-fix.diff
Patch38:	webmin-ssldir-cosmetic.diff
Patch39:	webmin-fix-bandwith.diff
Patch40:	webmin-fix-sarg.diff
Patch41:	webmin-1.680-omv_detect.patch
Requires(pre): rpm-helper openssl
Requires:	perl
Requires:	perl-CGI
Requires:	perl(JSON::PP)
Requires:	perl(Encode::Detect)
Requires:	lsof
Requires(pre): sed chkconfig findutils coreutils initscripts grep perl-Net-SSLeay perl-Authen-PAM
Provides:	%{name}-%{version}
Provides:	%{name}-theme-mandriva
BuildArch:	noarch

%description
A web-based administration interface for Unix systems. Using Webmin you can
configure DNS, Samba, NFS, local/remote filesystems, Apache, Sendmail/Postfix,
and more using your web browser.

After installation, enter the URL https://localhost:10000/ into your browser
and login as root with your root password. Please consider logging in and
modify your password for security issue.

PLEASE NOTE THAT THIS VERSION NOW USES SECURE WEB TRANSACTIONS: YOU HAVE TO
LOGIN TO "https://localhost:10000/" AND NOT "http://localhost:10000/".

%prep

%setup -q -a2 -a30 -a51 -a52 -a53 -a55 -a56
# Unknow extension, rpm won't unpack it.
tar xf %{SOURCE54}
tar xf %{SOURCE541}
tar xf %{SOURCE57}
tar xf %{SOURCE101}
tar xf %{SOURCE102}

install -m 0644 %{SOURCE33} mandriva/webmin/images
install -m 0644 %{SOURCE34} mandriva/webmin/images
rm -fr %{name}-%{version}/dhcpd
rm -fr %{name}-%{version}/useradmin

%setup -q -D -T -c -a 9 -n %{name}-%{version}

%patch41 -p1 
for i in */config-mandrake-linux-8.2; do n=`echo $i | perl -pe 's/...$/9.0/'`; [ -e $n ] || cp $i $n; done
for i in */config-mandrake-linux-9.0; do n=`echo $i | perl -pe 's/...$/9.1/'`; [ -e $n ] || cp $i $n; done
for i in */config-mandrake-linux-9.1; do n=`echo $i | perl -pe 's/...$/9.2/'`; [ -e $n ] || cp $i $n; done
for i in */config-mandrake-linux-9.2; do n=`echo $i | perl -pe 's/...$/10.0/'`; [ -e $n ] || cp $i $n; done
for i in */config-mandrake-linux-10.0; do n=`echo $i | perl -pe 's/....$/10.1/'`; [ -e $n ] || cp $i $n; done
for i in */config-mandrake-linux-10.1; do n=`echo $i | perl -pe 's/....$/10.2/'`; [ -e $n ] || cp $i $n; done
for i in */config-mandrake-linux-10.2; do n=`echo $i | perl -pe 's/....$/2006.0/'`; [ -e $n ] || cp $i $n; done

rm -rf JSON
find bind8 -type f -maxdepth 1 | xargs perl -pi -e 's|/var/run/named\.pid|/var/run/named/named.pid|'

# daouda: added mandriva-linux to known OS
cp config-mandrake-linux config-mandriva-linux

# force theme to blue
pushd theme_gehrigal/skins
  ./change_skin.pl s blueedition.skininfo
popd

perl -pi -e 's|redhat-linux(?! mandriva-linux)|redhat-linux mandriva-linux| if $_ =~ /^os_support.*redhat-linux/ && $_ !~ /mandriva-linux/' */module.info
#'
perl -pi -e 's|/etc/smb\.conf|/etc/samba/smb\.conf|' samba/config-mandrake-linux

(find . -name '*.cgi' ; find . -name '*.pl') | perl perlpath.pl /usr/bin/perl -
rm -f mount/freebsd-mounts-*
rm -f mount/openbsd-mounts-*

find -name ".xvpics" -o -name ".*.swp" | xargs rm -rf

%build

%install

# IMPORTANT: there is no %{_datadir} and so on, since the directories are decided by the post install script.
mkdir -p %{buildroot}/usr/share/webmin
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/usr/bin

find -type f -print0 | xargs -0 chmod a+r
find -type d -print0 | xargs -0 chmod a+rx

# (gc) remove ldap module, we don't have perl modules to make it work
rm -rf ldap

cp -a * %{buildroot}/usr/share/webmin
install -m755 %{SOURCE6} %{buildroot}/%{_unitdir}
install -m755 %{SOURCE4} %{buildroot}/usr/share/webmin/postinstall.sh
install -m755 %{SOURCE5} %{buildroot}/usr/bin

mkdir -p %{buildroot}/%{_sysconfdir}/pam.d
install -m755 %{SOURCE14} %{buildroot}/%{_sysconfdir}/pam.d/webmin

rm -rf %{buildroot}/usr/share/webmin/*/{CVS,*/CVS}
rm -f `find %{buildroot} -type f -name .cvsignore`

# (gc) remove zero-length files (to check sometimes if they are still zero-length'ed)
for i in /usr/share/webmin/caldera/images/letters/254.gif /usr/share/webmin/i4lctrl-0.6.7/lang/de /usr/share/webmin/caldera/images/letters/255.gif; do
    if [ -f $i ]; then rm -f %{buildroot}$i; fi
done

echo "rpm" > %{buildroot}/usr/share/webmin/install-type

# (sb) remove development file
rm -f %{buildroot}/usr/share/webmin/mount/macos-mounts.c

echo 'blue-theme' > %{buildroot}%{_datadir}/webmin/defaulttheme

# (oe) remove invalid file that breaks webmin
rm -f %{buildroot}%{_datadir}/webmin/mandriva/config.cgi

# Install icons
install -d -m 0755 %{buildroot}%{_liconsdir}
install -d -m 0755 %{buildroot}%{_miconsdir}
install -m 0644 %{SOURCE11} %{buildroot}%{_miconsdir}/webmin.png
install -m 0644 %{SOURCE12} %{buildroot}%{_iconsdir}/webmin.png
install -m 0644 %{SOURCE11} %{buildroot}%{_liconsdir}/webmin.png

# Menu entry

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=%{summary}
Exec=%{_bindir}/www-browser https://localhost:10000/
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Configuration-Other;Settings;
EOF

rm -fr %{buildroot}/usr/share/webmin/acl/Authen-SolarisRBAC-0.1

#logrotate
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE15} %{buildroot}%{_sysconfdir}/logrotate.d/webmin

# Drop SVN internal files
rm -rf %{buildroot}%{_datadir}/%{name}/dansguardian/*/.svn

%post
%_create_ssl_certificate -b miniserv

if [ "$1" != 0 ]; then
    service webmin status >/dev/null 2>/dev/null && need_restart=1
    service webmin stop >/dev/null 2>/dev/null || :
else
    [[ -e /etc/cron.allow ]] && if [ "x`grep root /etc/cron.allow`" == "x" ] ; then
	echo root >> /etc/cron.allow
    fi
fi
/usr/share/webmin/postinstall.sh
%_post_service webmin
[[ -n $need_restart ]] && service webmin start >/dev/null 2>/dev/null || :

%preun
%_preun_service webmin

%postun
if [ "$1" = 0 ]; then
    rm -rf /etc/webmin /var/webmin /var/lib/webmin /var/run/webmin /var/log/webmin
fi

%files
%defattr(-, root, root, 0755)
%doc LICENCE
%{_unitdir}/webmin.service
%config(noreplace) %{_sysconfdir}/pam.d/webmin
%config(noreplace) %{_sysconfdir}/logrotate.d/webmin
%{_datadir}/%{name}
%{_bindir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/*.desktop
