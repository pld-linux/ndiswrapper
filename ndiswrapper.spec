#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace tools
%bcond_without	smp		# don't build SMP module
%bcond_without	up		# don't build UP module
#
%if %{without kernel}
%undefine	with_smp
%undefine	with_up
%endif

%define		_snap	20040417
Summary:	Tools to "wrap around" NDIS drivers
Summary(pl):	Narzêdzia "opakowuj±ce" sterowniki NDIS
Name:		ndiswrapper
Version:	0.7
%define	_rel	0.%{_snap}.1
Release:	%{_rel}
License:	GPL
Group:		Base/Kernel
Source0:	%{name}-%{version}-%{_snap}.tar.gz
# Source0-md5:	ca388c2ae4e372c1e967b6f439d0e4ce
URL:		http://ndiswrapper.sourceforge.net/
%if %{with up} || %{with smp}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.0}
BuildRequires:	%{kgcc_package}
%endif
BuildRequires:	rpmbuild(macros) >= 1.118
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_compress_modules	1

%description
Some wireless LAN vendors refuse to release hardware specifications or
drivers for their products for operating systems other than Microsoft
Windows. The ndiswrapper project makes it possible to use such
hardware with Linux by means of a loadable kernel module that "wraps
around" NDIS (Windows network driver API) drivers.

The main package contains the userspace tools for ndiswrapper kernel
module.

%description -l pl
Niektórzy producenci bezprzewodowych kart sieciowych nie udostêpniaj±
specyfikacji lub sterowników dla swoich produktów, dla systemów innych
ni¿ Microsoft Windows. Projekt ndiswrapper umo¿liwia u¿ycie takiego
sprzêtu w systemie Linux, dostarczaj±c modu³ j±dra który "owija"
sterowniki NDIS (API sterowników sieciowych w Windows).

G³ówny pakiet zawiera narzêdzia przestrzeni u¿ytkownika dla
ndiswrappera.

%package -n kernel-net-ndiswrapper
Summary:	Loadable Linux kernel module that "wraps around" NDIS drivers
Summary(pl):	Modu³ j±dra Linuksa "owijaj±cy" sterowniki NDIS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
PreReq:		module-init-tools
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.7.7-10
Requires:	%{name} = %{version}-%{_rel}

%description -n kernel-net-ndiswrapper
Some wireless LAN vendors refuse to release hardware specifications or
drivers for their products for operating systems other than Microsoft
Windows. The ndiswrapper project makes it possible to use such
hardware with Linux by means of a loadable kernel module that "wraps
around" NDIS (Windows network driver API) drivers.

This package contains Linux kernel module.

%description -n kernel-net-ndiswrapper -l pl
Niektórzy producenci bezprzewodowych kart sieciowych nie udostêpniaj±
specyfikacji lub sterowników dla swoich produktów, dla systemów innych
ni¿ Microsoft Windows. Projekt ndiswrapper umo¿liwia u¿ycie takiego
sprzêtu w systemie Linux, dostarczaj±c modu³ j±dra który "owija"
sterowniki NDIS (API sterowników sieciowych w Windows).

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel-smp-net-ndiswrapper
Summary:	Loadable Linux SMP kernel module that "wraps around" NDIS drivers
Summary(pl):	Modu³ j±dra Linuksa SMP "owijaj±cy" sterowniki NDIS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
PreReq:		module-init-tools
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.7.7-10
Requires:	%{name} = %{version}-%{_rel}

%description -n kernel-smp-net-ndiswrapper
Some wireless LAN vendors refuse to release hardware specifications or
drivers for their products for operating systems other than Microsoft
Windows. The ndiswrapper project makes it possible to use such
hardware with Linux by means of a loadable kernel module that "wraps
around" NDIS (Windows network driver API) drivers.

This package contains Linux SMP kernel module.

%description -n kernel-smp-net-ndiswrapper -l pl
Niektórzy producenci bezprzewodowych kart sieciowych nie udostêpniaj±
specyfikacji lub sterowników dla swoich produktów, dla systemów innych
ni¿ Microsoft Windows. Projekt ndiswrapper umo¿liwia u¿ycie takiego
sprzêtu w systemie Linux, dostarczaj±c modu³ j±dra który "owija"
sterowniki NDIS (API sterowników sieciowych w Windows).

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -n %{name}-%{version}-%{_snap}

%build
%if %{with userspace}
%{__make} -C utils
%endif

cd ./driver

%if %{with up}
ln -sf %{_kernelsrcdir}/config-up .config
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/include/linux/autoconf-up.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/include/asm-%{_arch} include/asm
touch include/config/MARKER
%{__make} -C %{_kernelsrcdir} modules \
	SUBDIRS=$PWD \
	O=$PWD \
	V=1
mv ndiswrapper.ko ndiswrapper.ko-done

%{__make} -C %{_kernelsrcdir} mrproper \
	SUBDIRS=$PWD \
	O=$PWD \
	V=1
%endif

%if %{with smp}
ln -sf %{_kernelsrcdir}/config-smp .config
rm -rf include
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/include/linux/autoconf-smp.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/include/asm-%{_arch} include/asm
touch include/config/MARKER
%{__make} -C %{_kernelsrcdir} modules \
	SUBDIRS=$PWD \
	O=$PWD \
	V=1
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT{/sbin,%{_sysconfdir}/ndiswrapper}
install utils/{ndiswrapper,loadndisdriver,wlan_radio_averatec_5110hx} $RPM_BUILD_ROOT/sbin
%endif

%if %{with up}
install -D driver/ndiswrapper.ko-done $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/ndiswrapper.ko
%endif
%if %{with smp}
install -D driver/ndiswrapper.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/ndiswrapper.ko
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

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog INSTALL README
%dir %{_sysconfdir}/ndiswrapper
%attr(755,root,root) /sbin/*
%endif

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
