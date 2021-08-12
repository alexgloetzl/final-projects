project('meine library', 'c',
  default_options:['c_std=c99'])

#local_incdir = include_directories('include')

gsl = dependency('gsl')
obl = dependency('openblas', required:false)
cc = meson.get_compiler('c')
math = cc.find_library('m', required:false)
arp = dependency('arpack', required:true)

meinelib = library('blatt13',
  'blatt13.c',
  dependencies:[gsl, obl, math, arp],
  #include_directories:[local_incdir],
  install:true)

pkg = import('pkgconfig')
pkg.generate(meinelib)

blatt13 = executable('blatt13',
  'blatt13.c',
  dependencies:[gsl,obl, math, arp],
  #include_directories:[local_incdir],
  link_with:[meinelib],
  install:false) 

test('Ein einfacher Test', blatt13)