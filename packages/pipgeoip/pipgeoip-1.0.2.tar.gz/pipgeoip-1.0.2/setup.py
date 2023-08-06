from setuptools import setup, find_packages

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension


libs = ['pipgeoip']
compile_args = []
module1 = Extension('pipgeoip',
                    libraries=libs,
                    sources=['./pipgeoip/GeoLite2-ASN.mmdb', './pipgeoip/GeoLite2-City.mmdb', 'CHANGELOG.txt'],
                    extra_compile_args=compile_args)

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
setup(
  zip_safe=False,
  name='pipgeoip',
  version='1.0.2',
  description='Python GeoIP',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='https://himelrana.com',  
  author='Himel',
  author_email='contact@himelrana.com',
  license='MIT', 
  ext_modules=[module1],
  classifiers=classifiers,
  keywords='geoip, ipinfo, ip2info, ip information, ip to location, ip location', 
  packages=find_packages(),
  python_requires='>=3.6',
  install_requires=['geoip2'] 
)
