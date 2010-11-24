#------------------------------------------------------------------------------
# =========                 |
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
#  \\    /   O peration     |
#   \\  /    A nd           | Copyright held by original author
#    \\/     M anipulation  |
#-------------------------------------------------------------------------------
# License
#     This file is part of OpenFOAM.
#
#     OpenFOAM is free software; you can redistribute it and/or modify it
#     under the terms of the GNU General Public License as published by the
#     Free Software Foundation; either version 2 of the License, or (at your
#     option) any later version.
#
#     OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
#     ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#     FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
#     for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with OpenFOAM; if not, write to the Free Software Foundation,
#     Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#
# Script
#     RPM spec file for metis-5.0pre2
#
# Description
#     RPM spec file for creating a relocatable RPM
#
# Author:
#     Martin Beaudoin, Hydro-Quebec, (2010)
#
#------------------------------------------------------------------------------

# We grab the value of WM_THIRD_PARTY and WM_OPTIONS from the environment variable
%{expand:%%define _WM_THIRD_PARTY_DIR %(echo $WM_THIRD_PARTY_DIR)}
%{expand:%%define _WM_OPTIONS         %(echo $WM_OPTIONS)}

# The topdir needs to point to the $WM_THIRD_PARTY/rpmbuild directory
%define _topdir	 	%{_WM_THIRD_PARTY_DIR}/rpmBuild
%define _tmppath	%{_topdir}/tmp

# Will install the package directly $WM_THIRD_PARTY_DIR
#   Some comments about package relocation:
#   By using this prefix for the Prefix:  parameter in thi file, you will make this 
#   package relocatable. 
#
#   This is fine, as long as your software is itself relocatable.
#
#   Simply take note that libraries built with libtool are not relocatable because the
#   prefix we specify will be hard-coded in the library .la files.
#   Ref: http://sourceware.org/autobook/autobook/autobook_80.html
#
#   In that case, if you ever change the value of the $WM_THIRD_PARTY_DIR, you will
#   not be able to reutilize this RPM, even though it is relocatable. You will need to 
#   regenerate the RPM.
#
%define _prefix         %{_WM_THIRD_PARTY_DIR}

%define name		metis
%define release		%{_WM_OPTIONS}
%define version 	5.0pre2

%define buildroot       %{_topdir}/BUILD/%{name}-%{version}-root

BuildRoot:	        %{buildroot}
Summary: 		metis
License: 		Unkown
Name: 			%{name}
Version: 		%{version}
Release: 		%{release}
URL:                    http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis
Source: 		%url/%{name}-%{version}.tar.gz
Prefix: 		%{_prefix}
Group: 			Development/Tools
Patch0:                 metis-5.0pre2_patch_darwin

%define _installPrefix  %{_prefix}/packages/%{name}-%{version}/platforms/%{_WM_OPTIONS}

%description
%{summary}

%prep
%setup -q

%ifos darwin
%patch0 -p1
%endif

%build
    [ -n "$WM_CC" ]         &&  export CC="$WM_CC"
    [ -n "$WM_CXX" ]        &&  export CXX="$WM_CXX"
    [ -n "$WM_CFLAGS" ]     &&  export CFLAGS="$WM_CFLAGS"
    [ -n "$WM_CXXFLAGS" ]   &&  export CXXFLAGS="$WM_CXXFLAGS"
    [ -n "$WM_LDFLAGS" ]    &&  export LDFLAGS="$WM_LDFLAGS"

%ifos darwin
    # The parameter -D_POSIX_C_SOURCE=200809 has a side effect on Mac OS X
    (cd GKlib/trunk && make OPTFLAGS="-O3 -fPIC")
    (cd libmetis    && make OPTFLAGS="-O3 -fPIC") 
%else
    (cd GKlib/trunk && make OPTFLAGS="-O3 -fPIC -D_POSIX_C_SOURCE=200809")
    (cd libmetis    && make OPTFLAGS="-O3 -fPIC -D_POSIX_C_SOURCE=200809") 
%endif

%install
    # Manual installation
    mkdir -p $RPM_BUILD_ROOT/%{_installPrefix}/include
    mkdir -p $RPM_BUILD_ROOT/%{_installPrefix}/lib
    cp GKlib/builds/*/libGKlib.* $RPM_BUILD_ROOT/%{_installPrefix}/lib
    cp build/*/libmetis.*        $RPM_BUILD_ROOT/%{_installPrefix}/lib
    cp include/metis.h           $RPM_BUILD_ROOT/%{_installPrefix}/include

    # Creation of OpenFOAM specific .csh and .sh files"

    echo ""
    echo "Generating OpenFOAM specific .csh and .sh files for the package %{name}-%{version}"
    echo ""
    #
    # Generate package specific .sh file for OpenFOAM
    #
mkdir -p $RPM_BUILD_ROOT/%{_installPrefix}/etc
cat << DOT_SH_EOF > $RPM_BUILD_ROOT/%{_installPrefix}/etc/%{name}-%{version}.sh
# Load %{name}-%{version} libraries and binaries if available
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

export METIS_DIR=\$WM_THIRD_PARTY_DIR/packages/%{name}-%{version}/platforms/\$WM_OPTIONS

[ -d \$METIS_DIR/lib ] && _foamAddLib \$METIS_DIR/lib

# Enable access to the package applications if present
[ -d \$METIS_DIR/bin ] && _foamAddPath \$METIS_DIR/bin
DOT_SH_EOF

    #
    # Generate package specific .csh file for OpenFOAM
    #
cat << DOT_CSH_EOF > $RPM_BUILD_ROOT/%{_installPrefix}/etc/%{name}-%{version}.csh
# Load %{name}-%{version} libraries and binaries if available
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
setenv METIS_DIR \$WM_THIRD_PARTY_DIR/packages/%{name}-%{version}/platforms/\$WM_OPTIONS

if ( -e \$METIS_DIR/lib ) then
    _foamAddLib \$METIS_DIR/lib
endif

if ( -e \$METIS_DIR/bin ) then
    _foamAddPath \$METIS_DIR/bin
endif
DOT_CSH_EOF

%clean
rm -rf %{buildroot}

%Files
%defattr(-,root,root)
%{_installPrefix}/*




