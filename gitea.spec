%define debug_package %{nil}

Name:           gitea
Version:        1.6.1
Release:        1%{?dist}
Summary:        Git with a cup of tea, painless self-hosted git service
ExclusiveArch:  x86_64

Group:          System Environment/Daemons
License:        MIT
URL:            https://gitea.io/
Source0:        https://github.com/go-gitea/gitea/releases/download/v%{version}/gitea-%{version}-linux-amd64
Source1:        gitea.service
Source2:        https://raw.githubusercontent.com/go-gitea/gitea/v%{version}/custom/conf/app.ini.sample
Source3:        LICENSE

BuildRequires:  systemd-units

Requires(pre):  shadow-utils
Requires:       systemd glibc

%description
Gitea is a community managed fork of Gogs, lightweight code hosting solution
written in Go and published under the MIT license.

%prep

%build

%install
install -D %{SOURCE0} %{buildroot}/%{_bindir}/gitea
install -D %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
install -D %{SOURCE2} %{buildroot}/%{_sysconfdir}/%{name}/app.ini
install -D %{SOURCE3} %{buildroot}/%{_docdir}/%{name}/LICENSE

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "%{name} user" %{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
case "$1" in
  0) # uninstall
    getent passwd %{name} >/dev/null && userdel %{name}
    getent group %{name} >/dev/null && groupdel %{name}
  ;;
  1) # upgrade
  ;;
esac
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/gitea
%dir %attr(750, root, %{name}) %{_sysconfdir}/%{name}
%attr(644, root, root) %{_unitdir}/%{name}.service
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/%{name}/app.ini

%doc %{_docdir}/%{name}/LICENSE

%changelog
* Wed Dec 12 2018 Ryan Chouinard <rchouinard@gmail.com> - 1.6.1-1
- Initial package version