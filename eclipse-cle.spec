%define eclipse_base    %{_libdir}/eclipse
%define install_dir	%{_datadir}/eclipse/dropins/cle
%define eclipse_ver     3.4
%define gcj_support     0

Name:           eclipse-cle
Version:        0.1.6
Release:        %mkrel 0.0.3
Epoch:          0
Summary:        Provides editing of grammar and scanner specification files
License:        EPL
Group:          Development/Java
URL:            https://cup-lex-eclipse.sourceforge.net/
Source0:        http://internap.dl.sourceforge.net/sourceforge/cup-lex-eclipse/pi.eclipse.cle-src-%{version}.tar.bz2
Requires:       eclipse-platform >= 1:%{eclipse_ver}
Requires:       jakarta-commons-collections
Requires:       java-cup
Requires:       jflex
Requires:       log4j
Requires:       velocity
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  ant >= 0:1.6
BuildRequires:  eclipse-pde >= 1:%{eclipse_ver}
BuildRequires:  jakarta-commons-collections
BuildRequires:  java-cup
BuildRequires:  jflex
BuildRequires:  log4j
BuildRequires:  velocity
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
#BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
CLE is an Eclipse plugin providing editing of grammar specification
files used by CUP and scanner specification files used by JFlex.

The plugin also includes the necessary builders needed for Java
sources generation. 

%prep
%setup -q -n src
%{__perl} -pi -e 's/<javac/<javac nowarn="true"/g' build.xml
%{_bindir}/find . -name '*.jar' -o -name '*.zip' -o -name '*.class' | %{_bindir}/xargs -t %{__rm}

%build
for jar in \
/usr/lib/java/swt.jar \
%{eclipse_base}/plugins/org.eclipse.core.commands_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.core.filebuffers_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.core.resources_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.core.runtime_%{eclipse_ver}*.*.jar \
%{eclipse_base}/dropins/jdt/plugins/org.eclipse.jdt.core_%{eclipse_ver}*.*.jar \
%{eclipse_base}/dropins/jdt/plugins/org.eclipse.jdt.ui_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.jface_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.jface.text_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.osgi_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.swt_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.team.core_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.text_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.ui_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.ui.editors_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.ui.ide_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.ui.workbench_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.ui.workbench.texteditor_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.equinox.common_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.equinox.registry_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.core.jobs_%{eclipse_ver}*.*.jar \
%{eclipse_base}/dropins/jdt/plugins/org.eclipse.jdt.launching_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.debug.core_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.ui.views_*.*.jar \
%{eclipse_base}/plugins/org.eclipse.equinox.preferences_*.*.jar
do
    test -f  ${jar} || exit 1
    export CLASSPATH=$CLASSPATH:${jar}
done

export CLASSPATH=$(build-classpath commons-collections java-cup jflex log4j velocity):${CLASSPATH}
export OPT_JAR_LIST=:
%{ant} -Dbuild.sysclasspath=only \
    -Declipse.plugin.dir=%{install_dir}/plugins \
    -Dworkspace=.. \
    -Declipse.version=%{eclipse_ver} \
    -Dproject.name="CUP/LEX Editor Plugin"

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{install_dir}
%{__tar} -C %{buildroot}%{install_dir} -xvf output/pi.eclipse.cle_%{version}.tar.bz2

%{__mkdir_p} %{buildroot}%{install_dir}/plugins/pi.eclipse.cle_%{version}
(cd %{buildroot}%{install_dir}/plugins/pi.eclipse.cle_%{version} && %{jar} xf %{buildroot}%{install_dir}/plugins/pi.eclipse.cle_%{version}.jar)
%{__rm} %{buildroot}%{install_dir}/plugins/pi.eclipse.cle_%{version}.jar

%{__mkdir_p} %{buildroot}%{install_dir}/plugins/pi.eclipse.cle_%{version}/lib
pushd %{buildroot}%{install_dir}/plugins/pi.eclipse.cle_%{version}/lib
%{__ln_s} %{_javadir}/java-cup-runtime.jar java-cup-11-runtime.jar
%{__ln_s} %{_javadir}/java-cup.jar java-cup-11.jar
%{__ln_s} %{_javadir}/jflex.jar jflex-1.4.1.jar
%{__ln_s} %{_javadir}/log4j.jar log4j-1.2.12.jar
%{__ln_s} %{_javadir}/velocity.jar velocity-1.4.jar
%{__ln_s} %{_javadir}/velocity.jar velocity-dep-1.4.jar
popd

%{gcj_compile}

%clean 
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc web/*.html
%{install_dir}
%{gcj_files}
