# from __future__ import division, absolute_import, print_function

from distutils import extension
from ensurepip import version
from nturl2path import url2pathname
from unicodedata import name
# from numpy.distutils.core import Extension

# package_name = 'pyemaps' #dif module is located in pyemaps root dir

mod_name = "emaps"
ver = "1.0.0"
# mod_name = "dif"
pyf_name = ".".join([mod_name+'_dif','pyf'])
# pyf_name = ".".join([mod_name,'pyf'])
# print(pyf_name)
dif_source = [pyf_name,
            'diffract.f95',
            'diff_types.f95', 
            'scattering.f95', 
            'spgra.f95',
            'diff_memalloc.f95',
            'crystal_mem.f95', 
            'emaps_consts.f95',
            'xtal0.f95', 
            'helper.f95', 
            'asf.f95', 
            'atom.f95',
            'metric.f95', 
            'readutils.f95',
            'sfsub.f95', 
            'spgroup.f95', 
            'lafit.f95']
# dif_source = [pyf_name,'scalar.f95']               
# bloch_source = [df for df in dif_source]
# bloch_source = dif_source.extend(['bloch_mem.f95',
#             'bloch.f95'])

# dpgen_source = [df for df in dif_source]
# dpgen_source = dif_source.extend(['dp_types.f95', 
#             'dp_gen.f95'])

# print(f"adding bloch sources: {bloch_source}")
# all_source=[df for df in dif_source]

# all_source.extend(['bloch_mem.f95',
#             'bloch.f95'])
# all_source.extend(['dp_types.f95', 
#             'dp_gen.f95'])

compile_args=['-m64',         
            '-Wno-tabs', 
            '-Warray-bounds',
            '-fdefault-double-8',
            '-fdefault-real-8',
            '-fopenmp',
            '-fcheck=all,no-array-temps',
            '-cpp', 
            '-Wall',
            '-O3']

# build_args = ['--fcompiler=gnu95',    # now merged into setup.cfgs
#              '-I.', 
#              '-DWOS',
#              '-i',
#              '-tbuild_emaps',
#              '-Owrite_dpbin.o',
#              '-lgomp'
#             ]

# emaps_dif = Extension(
#                  name                   = mod_name,
#                  sources                = dif_source,
#                  extra_f90_compile_args = compile_args
#             )


# def updateManifest():
#     import os
#     import glob

#     curr_path = os.path.dirname(os.path.abspath(__file__))
    
#     pydfn = "emaps.cp37-win_amd64.pyd"
#     pydpn = os.path.join(curr_path, pydfn)
#     if not os.path.exists(pydpn):
#         print("Error building {mod_name} extension: dif! ")
#         return False

#     wildcardfl = os.path.join(curr_path, "*.dll")
#     list_of_dlls = glob. glob(wildcardfl)

#     if len(list_of_dlls) <= 0:
#         print("Error building {mod_name} extension: dif! ")
#         return False

#     dllfn = max(list_of_dlls, key=os.path.getctime)
#     # if not os.path.exist(dllfn):
#     #     print("Error building {mod_name} extension: dif! ")
#     #     return False
#     manifest = os.path.join(curr_path, "MANIFEST.in")
#     if not os.path.exists(manifest):
#         print("Error building {mod_name} extension: dif! ")
#         return False

#     try:
#         with open(manifest, 'a') as f:
#             f.write(' ')
#             f.write(pydfn)
#             f.write(' ')
#             f.write(os.path.basename(dllfn))
#     except:
#         print("Error building {mod_name} extension: dif! ")
#         return False

#     return True
# def dif_config(parent_package='', top_path=None):
#     from numpy.distutils.misc_util import Configuration
#     dif_setupconfig = Configuration("dif", package_name, top_path)
#     return dif_setupconfig
# from setuptools.command.install import install as DistutilsInstall

# class diffInstall(DistutilsInstall):
#     def run(self):
#         #call make
#         DistutilsInstall.run(self)

def configuration(parent_package='', top_path=None):
    import setuptools
    from numpy.distutils.misc_util import Configuration
    config = Configuration('diffract', parent_package, top_path)

    # config.add_data_dir('tests')

    config.add_extension(
                 name                   = mod_name,
                 sources                = dif_source,
                 extra_f90_compile_args = compile_args,
                 f2py_options           = []
            )
        
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup
    # from setuptools import setup
    setup(**configuration(top_path='').todict())
    # from numpy.distutils.core import setup
    # # setup(**configuration(top_path='').todict())
    # # pname = 'pyemaps'
    # # keys = ['kinematic', 'simulation','diffraction', 'crystallography','python']
    # # scripts = ["README.md", \
    # #            "__init__.py", 
    # #            "crystals.py",
    # #            "models.py", 
    # #            "run_diff.py", 
    # #            "emaps.cp37-win_amd64.pyd", 
    # #            "*.dll"]
    # setup(name = mod_name,
    #       description       = "Python kinematic diffraction simulation module",
    #       author            = "EMLab Solutions, Inc.",
    #       author_email      = "support@emlabsoftware.com",
    #       version           = ver,
    #       license           = 'MIT',
    #     #   package_dir       = {'': package_name},
    #     #   packages          = [package_name],
    #       keywords          = keysdef configuration(parent_package='', top_path=None):
    # from numpy.distutils.misc_util import Configuration
    # config = Configuration('testsub', parent_package, top_path)

    # # config.add_data_dir('tests')

    # config.add_extension('scalar',
    #     sources=[('scalar.f95')])
        
    # return config
    #       url               = 'https//www.emlabsolutions.com',
    #     #   ext_package       = package_name, # under pyemaps package
    #       ext_modules       = [emaps_dif]
    #     #   scripts           = scripts,
    #     #   script_args       = build_args,
    #       )
    # updateManifest()
# if __name__ == "__main__":
#     from numpy.distutils.core import setup
#     # setup(**configuration(top_path='').todict())
#     # pname = 'pyemaps'
#     keys = ['kinematic', 'simulation','diffraction', 'crystallography','python']
#     config = dif_config()

#     setup(name = package_name,
#           description       = "Python kinematic diffraction simulation module",
#           author            = "EMLab Solutions, Inc.",
#           author_email      = "support@emlabsoftware.com",
#           version           = '1.0.0',
#           license           = 'MIT',
#           package_dir       = {package_name:''},
#           packages          = [mod_name],
#           keywords          = keys,
#           url               = 'https//www.emlabsolutions.com',
#           ext_modules       = [emaps_dif]
#           )

# import os
# from sys import platform
# from setuptools import setup
# from setuptools.command.install import install
# from distutils.command.build import build
# from subprocess import call
# from multiprocessing import cpu_count

# BASEPATH = os.path.dirname(os.path.abspath(__file__))
# XCSOAR_PATH = os.path.join(BASEPATH, 'xcsoar.submodule')


# class XCSoarBuild(build):
#     def run(self):
#         # run original build code
#         build.run(self)

#         # build XCSoar
#         build_path = os.path.abspath(self.build_temp)

#         cmd = [
#             'make',
#             'OUT=' + build_path,
#             'V=' + str(self.verbose),
#         ]

#         try:
#             cmd.append('-j%d' % cpu_count())
#         except NotImplementedError:
#             print 'Unable to determine number of CPUs. Using single threaded make.'

#         options = [
#             'DEBUG=n',
#             'ENABLE_SDL=n',
#         ]
#         cmd.extend(options)

#         targets = ['python']
#         cmd.extend(targets)

#         if platform == 'darwin':
#             target_path = 'OSX64_PYTHON'
#         else:
#             target_path = 'UNIX_PYTHON'

#         target_files = [os.path.join(build_path, target_path, 'bin', 'xcsoar.so')]

#         def compile():
#             call(cmd, cwd=XCSOAR_PATH)

#         self.execute(compile, [], 'Compiling xcsoar')

#         # copy resulting tool to library build folder
#         self.mkpath(self.build_lib)

#         if not self.dry_run:
#             for target in target_files:
#                 self.copy_file(target, self.build_lib)


# class XCSoarInstall(install):
#     def initialize_options(self):
#         install.initialize_options(self)
#         self.build_scripts = None

#     def finalize_options(self):
#         install.finalize_options(self)
#         self.set_undefined_options('build', ('build_scripts', 'build_scripts'))

#     def run(self):
#         # run original install code
#         install.run(self)

#         # install XCSoar executables
#         self.copy_tree(self.build_lib, self.install_lib)


# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()


# setup(
#     name='xcsoar',
#     version='0.5',
#     description='XCSoar flight analysis tools',
#     maintainer='Tobias Bieniek',
#     maintainer_email='tobias.bieniek@gmx.de',
#     license='GPLv2',
#     url='http://www.xcsoar.org/',
#     long_description=read('README.rst'),
#     classifiers=[
#         'Development Status :: 3 - Alpha',
#         'Intended Audience :: Developers',
#         'Intended Audience :: Science/Research',
#         'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
#         'Operating System :: Unix',
#         'Programming Language :: C++',
#         'Topic :: Scientific/Engineering :: Information Analysis',
#     ],

#     cmdclass={
#         'build': XCSoarBuild,
#         'install': XCSoarInstall,
#     }
# )