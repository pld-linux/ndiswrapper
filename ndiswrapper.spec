# TODO:
#    fix summary/desc for src.rpm
#
# Conditional build:
%bcond_without dist_kernel	# without distribution kernel
%bcond_without smp		# without smp packages
%bcond_without up		# without uniprocesor packages
#

Summary:	Userspace tools for ndiswrapper kernel module
Summary(pl):	Narzêdzia przestrzeni u¿ytkownika dla ndiswrappera
Name:		ndiswrapper
Version:	0.6
%define	_rel	1
Release:	%{_rel}
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	7eee09ad2a869efcff570ef064063654
URL:		http://ndiswrapper.sourceforge.net
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.0 }
%if %{with up} || %{with smp}
BuildRequires:	%{kgcc_package}
%endif
BuildRequires:	rpmbuild(macros) >= 1.118
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_modext					ko
%define 	target					module
%define		no_install_post_compress_modules	1

%description
Userspace tools for ndiswrapper kernel module.

%description -l pl
Narzêdzia przestrzeni u¿ytkownika dla ndiswrappera.

%package -n kernel-net-ndiswrapper
Summary:	Loadable kernel module that "wraps around" NDIS drivers
Summary:	Modu³ j±dra "owijaj±cy" sterowniki NDIS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.3.18-2
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.7.7-10
Requires:	%{name} = %{version}

%description -n kernel-net-ndiswrapper
Some wireless LAN vendors refuse to release hardware specifications or
drivers for their products for operating systems other than Microsoft
Windows. The ndiswrapper project makes it possible to use such
hardware with Linux by means of a loadable kernel module that "wraps
around" NDIS (Windows network driver API) drivers.

%description -n kernel-net-ndiswrapper -l pl
Niektórzy producenci bezprzewodowych kart sieciowych nie udostêpniaj±
specyfikacji lub sterowników dla swoich produktów, dla systemów innych
ni¿ Microsoft Windows. Projekt ndiswrapper umo¿liwia u¿ycie takiego
sprzêtu w systemie Linux, dostarczaj±c modu³ j±dra który "owija"
sterowniki NDIS (API sterowników sieciowych w Windows).

%package -n kernel-smp-net-ndiswrapper
Summary:	Loadable SMP kernel module that "wraps around" NDIS drivers
Summary:	Modu³ j±dra SMP "owijaj±cy" sterowniki NDIS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.3.18-2
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.7.7-10
Requires:	%{name} = %{version}

%description -n kernel-smp-net-ndiswrapper
Some wireless LAN vendors refuse to release hardware specifications or
drivers for their products for operating systems other than Microsoft
Windows. The ndiswrapper project makes it possible to use such
hardware with Linux by means of a loadable kernel module that "wraps
around" NDIS (Windows network driver API) drivers. This package
contains SMP kernel module.

%description -n kernel-smp-net-ndiswrapper -l pl
Niektórzy producenci bezprzewodowych kart sieciowych nie udostêpniaj±
specyfikacji lub sterowników dla swoich produktów, dla systemów innych
ni¿ Microsoft Windows. Projekt ndiswrapper umo¿liwia u¿ycie takiego
sprzêtu w systemie Linux, dostarczaj±c modu³ j±dra który "owija"
sterowniki NDIS (API sterowników sieciowych w Windows). Ten pakiet
zawiera modu³ dla j±dra SMP.

%prep
%setup -q

%build
%{__make} -C utils

cd ./driver

%if %{with up}
ln -sf %{_kernelsrcdir}/config-up .config
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/include/linux/autoconf-up.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/include/asm-%{_arch} include/asm
touch include/config/MARKER
%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 modules
mv ndiswrapper.ko ndiswrapper.ko-done

%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 mrproper
%endif

%if %{with smp}
ln -sf %{_kernelsrcdir}/config-smp .config
rm -rf include
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/include/linux/autoconf-smp.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/include/asm-%{_arch} include/asm
touch include/config/MARKER
%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 modules
%endif

cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{sbin,%{_sysconfdir}/ndiswrapper}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc/
install utils/{ndiswrapper,loadndisdriver,wlan_radio_averatec_5110hx} $RPM_BUILD_ROOT/sbin
%if %{with up}
install driver/ndiswrapper.ko-done $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/ndiswrapper.ko
%endif
%if %{with smp}
install driver/ndiswrapper.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/ndiswrapper.ko
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-net-ndiswrapper
%depmod %{_kernel_ver}

%postun	-n kernel-net-ndiswrapper
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-ndiswrapper
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-ndiswrapper
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog INSTALL README
%dir %{_sysconfdir}/ndiswrapper
%attr(755, root, root) /sbin/*

%if %{with up}
%files -n kernel-net-ndiswrapper
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*
%endif

%if %{with smp}
%files -n kernel-smp-net-ndiswrapper
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*
%endif
