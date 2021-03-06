# plugingen.py -- Tools to generate plugins as luigi modules.

import plugin
import tools
import os
import sys
import datetime


def genheader(f):
    """Writes all required boilerplate stuff for each luigi module."""
    f.write("# Generated by ariadne on %s.\n" % datetime.date.today())
    f.write("import luigi\nimport os\n")


def gen_deps_inline(deplist, f, plugindir):
    """Generates all specified inline dependencies."""
    if deplist==None:
        return

    for d in deplist:
        f.write("        os.system('ariadne.py runplugin %s %s " % (d[2], plugindir))
        for a in d[1]:
            f.write("%s=%s " % (a, str(d[1][a])))
        f.write("')\n")


def write_dep_def(f, plugin, depnum, argdict, plugindir):
    """Implements a limited subset of gen() intended to wrap individual dependencies."""
    namestr="%s_l%d" % (plugin.name, depnum)

    f.write("class %s(luigi.Task):\n\n\n" % namestr)
    f.write("   def output(self):\n")
    f.write("       return")
    modlist=plugin.files_modified()
    first=None

    for f in modlist:   
        if first==None:
            first=f
        else:
            f.write(", ")
        f.write("luigi.LocalTarget('%s')" % f)

    f.write("\n\n\n")

    f.write("   def run(self):\n")
    f.write("       os.system('ariadne.py %splugin %s %s" % (exectype, wrappername, plugindir))

    for a in argdict:
        f.write(" %s=%s" % (a, argdict[a]))
    f.write("')\n\n\n")

    return namestr


def parse_deps(pl, f, plugindir, args, depnum):
    """Iterates through all dependencies and either generates them or 
       pushes them into a list for furture generation.
    """
    deplist=pl.depends()
    classlist=[]
    inlinelist=[]

    try:
        deplist.extend(pl.train_depends())
    except:
        pass

    print("Recursing on: %s" % pl.name)

    if deplist!=None:
        for d in deplist:
            depnum+=1
            dclass=plugin.search_plugins(d.dependency_name)
            if dclass==None:
                print("Couldn't find plugin for dependency: %s" % d.dependency_name)
                raise Exception
            else:
                # Determine if this dependency would be best suited
                # for inline execution:
                dep=dclass()

                (a, b, c)=parse_deps(ddep, f, plugindir, d.arg_dict, depnum)
                classlist.extend(a)
                inlinelist.extend(b)

    depnum+=1

    if pl.files_modified() == []:
        inlinelist.append((pl, args, pl.name))
    else:
        gen_name=write_dep_def(f, pl, depnum, args, plugindir)
        classlist.append((pl, args, gen_name))

    # Return depnum so that it can be used to generate unique-ish dependency names.
    return (classlist, inlinelist, depnum)


def gen(pl, f, wrappername, plugindir, exectype, existingargs):
    """Generates a luigi wrapper for the specified plugin."""
    argnames=[]
    deps=[]

    classdeplist=[]
    inlinedeplist=[]
    
    try:
        argnames=pl.get_arg_names()
    except:
        pass

    deplist=pl.depends()

    if exectype=="train":
        try:
            deplist=pl.train_depends()
        except:
            pass


    print("Number of dependencies: %d" % len(deplist))
    depnum=0

    for d in deplist:
        dclass=plugin.search_plugins(d.dependency_name)
        if dclass==None:
            print("Couldn't find plugin for dependency: %s" % d.dependency_name)
            raise Exception
        else:
            (a, b, depnum)=parse_deps(dclass(), f, plugindir, d.arg_dict, depnum)
            classdeplist.extend(a)
            inlinedeplist.extend(b)
            depnum+=1

    print("Number of class dependencies: %d" % len(classdeplist))
    print("Number of inline dependencies: %d" % len(inlinedeplist))
    
    f.write("class %s_l(luigi.Task):\n" % wrappername)
    # Temporarily disabled for existingargs support:
    #for a in argnames:
    #    f.write("    %s=luigi.Parameter()\n" % a)

    if len(classdeplist):
        f.write("   def requires(self):\n")
        f.write("       return")
        for c in classdeplist:
            f.write(" %s(" % c[2])
            frst=None

            for a in c[1]:
                if frst==None:
                    frst=a
                else:
                    f.write(",")

                f.write("'%s'" % str(c[1][a]))
            f.write(")")

        f.write("\n\n\n")
    else:
        print("No luigi-able dependencies found")

    f.write("    def run(self):\n")
    gen_deps_inline(inlinedeplist, f, plugindir)
    f.write("        os.system('ariadne.py %splugin %s %s" % (exectype, wrappername, plugindir))

    for e in existingargs:
        f.write(" %s" % e)

    f.write("')\n")

    try:
        fmod=pl.files_modified()
        if len(fmod)!=0:
            f.write("   output(self):\n")
            f.write("       return ")
            for mod in fmod:
                if mod!=fmod[0]:
                    f.write(",")
                f.write("luigi.LocalTarget('%s') " % mod)
            f.write("\n")
    except:
        pass
        
    f.flush()


def gentest(pl, f, wrappername, plugindir, exectype, existingargs):
    """Generates a luigi wrapper that can do internal testing."""

    # This will be the same as gen, but with a custom complete() method.
    gen(pl, f, wrappername, plugindir, exectype, existingargs)

    # Now write the complete() method:
    f.write("   def complete(self):\n")
    f.write("       return not 0xFF00 & os.system('ariadne.py testplugin %s " % (wrappername)) 
    for e in existingargs:
        f.write(" %s" % e)

    f.write("')\n")
