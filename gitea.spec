%global   gitea_user  gitea

Name:           gitea
Version:        1.6.1
Release:        2%{?dist}
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
install -p -D -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/gitea
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/gitea.service
install -p -D -m 0664 %{SOURCE2} %{buildroot}%{_sysconfdir}/gitea/app.ini.sample
install -p -D -m 0664 /dev/null  %{buildroot}%{_sysconfdir}/gitea/app.ini
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_docdir}/gitea/LICENSE
install -p -d -m 0700 %{buildroot}%{_sharedstatedir}/gitea

%pre
getent group %{gitea_user} >/dev/null || groupadd -r %{gitea_user}
getent passwd gitea >/dev/null || \
    useradd -r -g %{gitea_user} -d %{_sharedstatedir}/gitea -s /sbin/nologin \
    -c "gitea user" %{gitea_user}
exit 0

%post
%systemd_post gitea.service

%preun
%systemd_preun gitea.service

%postun
case "$1" in
  0) # uninstall
    getent passwd %{gitea_user} >/dev/null && userdel %{gitea_user}
    getent group %{gitea_user} >/dev/null && groupdel %{gitea_user}
  ;;
  1) # upgrade
  ;;
esac
%systemd_postun_with_restart gitea.service

%files
%{_bindir}/gitea
%{_unitdir}/gitea.service
%config(noreplace) %attr(664, root, %{gitea_user}) %{_sysconfdir}/gitea/app.ini.sample
%config(noreplace) %attr(664, root, %{gitea_user}) %{_sysconfdir}/gitea/app.ini
%dir %attr(770, %{gitea_user}, root) %{_sharedstatedir}/gitea
%doc %{_docdir}/gitea/LICENSE

%changelog
* Thu Dec 13 2018 Ryan Chouinard <rchouinard@gmail.com> - 1.6.1-2
- Fix crash on start caused by default configuration
- Cleanup spec file

* Wed Dec 12 2018 Ryan Chouinard <rchouinard@gmail.com> - 1.6.1-1
- Initial package version