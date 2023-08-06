# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cipherchecks']

package_data = \
{'': ['*']}

install_requires = \
['crayons>=0.4.0,<0.5.0', 'sslyze>=4.1.0,<5.0.0']

entry_points = \
{'console_scripts': ['cipherchk = cipherchecks.main:main']}

setup_kwargs = {
    'name': 'cipherchecks',
    'version': '0.1.4',
    'description': '',
    'long_description': "# cipherchecks\nvisually see issues with supported cipher suites\n\nTheres a few known tools out there that will check the cipher suites accepted by a system. This is my attempt in making the output of the results more readable. \n\nFor example, using [sslscan](https://github.com/rbsec/sslscan/), to only have a list of supported ciphers, you will need to grep for 'Accepted'.\n\n```bash\n$ sslscan github.com | grep Accepted\nAccepted  TLSv1.3  256 bits  TLS_CHACHA20_POLY1305_SHA256  Curve 25519 DHE 253\nAccepted  TLSv1.3  256 bits  TLS_AES_256_GCM_SHA384        Curve 25519 DHE 253\nAccepted  TLSv1.2  128 bits  ECDHE-RSA-AES128-GCM-SHA256   Curve 25519 DHE 253\nAccepted  TLSv1.2  256 bits  ECDHE-ECDSA-CHACHA20-POLY1305 Curve 25519 DHE 253\nAccepted  TLSv1.2  256 bits  ECDHE-RSA-CHACHA20-POLY1305   Curve 25519 DHE 253\nAccepted  TLSv1.2  256 bits  ECDHE-ECDSA-AES256-GCM-SHA384 Curve 25519 DHE 253\nAccepted  TLSv1.2  256 bits  ECDHE-RSA-AES256-GCM-SHA384   Curve 25519 DHE 253\nAccepted  TLSv1.2  128 bits  ECDHE-ECDSA-AES128-SHA256     Curve 25519 DHE 253\nAccepted  TLSv1.2  128 bits  ECDHE-RSA-AES128-SHA256       Curve 25519 DHE 253\nAccepted  TLSv1.2  256 bits  ECDHE-ECDSA-AES256-SHA384     Curve 25519 DHE 253\nAccepted  TLSv1.2  256 bits  ECDHE-RSA-AES256-SHA384       Curve 25519 DHE 253\nAccepted  TLSv1.2  256 bits  ECDHE-ECDSA-AES256-SHA        Curve 25519 DHE 253\nAccepted  TLSv1.2  256 bits  ECDHE-RSA-AES256-SHA          Curve 25519 DHE 253\nAccepted  TLSv1.2  128 bits  AES128-GCM-SHA256\nAccepted  TLSv1.2  256 bits  AES256-GCM-SHA384\nAccepted  TLSv1.2  128 bits  AES128-SHA256\nAccepted  TLSv1.2  256 bits  AES256-SHA256\nAccepted  TLSv1.2  128 bits  AES128-SHA\nAccepted  TLSv1.2  256 bits  AES256-SHA\n```\n\n[testssl.sh](https://github.com/drwetter/testssl.sh) does way more than just listing the accepted ciphers, however the output of that is skewed too.\n\n```bash\n$ testssl -E github.com\n\n...snip...\n\nHexcode  Cipher Suite Name (OpenSSL)       KeyExch.   Encryption  Bits     Cipher Suite Name (IANA/RFC)\n-----------------------------------------------------------------------------------------------------------------------------\nSSLv2\nSSLv3\nTLS 1\nTLS 1.1\nTLS 1.2\n xc030   ECDHE-RSA-AES256-GCM-SHA384       ECDH 253   AESGCM      256      TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384\n xc02c   ECDHE-ECDSA-AES256-GCM-SHA384     ECDH 253   AESGCM      256      TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384\n xc028   ECDHE-RSA-AES256-SHA384           ECDH 253   AES         256      TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384\n xc024   ECDHE-ECDSA-AES256-SHA384         ECDH 253   AES         256      TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384\n xc014   ECDHE-RSA-AES256-SHA              ECDH 253   AES         256      TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\n xc00a   ECDHE-ECDSA-AES256-SHA            ECDH 253   AES         256      TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA\n xcca9   ECDHE-ECDSA-CHACHA20-POLY1305     ECDH 253   ChaCha20    256      TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256\n xcca8   ECDHE-RSA-CHACHA20-POLY1305       ECDH 253   ChaCha20    256      TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256\n x9d     AES256-GCM-SHA384                 RSA        AESGCM      256      TLS_RSA_WITH_AES_256_GCM_SHA384\n x3d     AES256-SHA256                     RSA        AES         256      TLS_RSA_WITH_AES_256_CBC_SHA256\n x35     AES256-SHA                        RSA        AES         256      TLS_RSA_WITH_AES_256_CBC_SHA\n xc02f   ECDHE-RSA-AES128-GCM-SHA256       ECDH 253   AESGCM      128      TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256\n xc02b   ECDHE-ECDSA-AES128-GCM-SHA256     ECDH 253   AESGCM      128      TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256\n xc027   ECDHE-RSA-AES128-SHA256           ECDH 253   AES         128      TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256\n xc023   ECDHE-ECDSA-AES128-SHA256         ECDH 253   AES         128      TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256\n x9c     AES128-GCM-SHA256                 RSA        AESGCM      128      TLS_RSA_WITH_AES_128_GCM_SHA256\n x3c     AES128-SHA256                     RSA        AES         128      TLS_RSA_WITH_AES_128_CBC_SHA256\n x2f     AES128-SHA                        RSA        AES         128      TLS_RSA_WITH_AES_128_CBC_SHA\nTLS 1.3\n x1302   TLS_AES_256_GCM_SHA384            ECDH 253   AESGCM      256      TLS_AES_256_GCM_SHA384\n x1303   TLS_CHACHA20_POLY1305_SHA256      ECDH 253   ChaCha20    256      TLS_CHACHA20_POLY1305_SHA256\n x1301   TLS_AES_128_GCM_SHA256            ECDH 253   AESGCM      128      TLS_AES_128_GCM_SHA256\n\n Done 2021-07-14 07:37:53 [  12s] -->> 140.82.121.4:443 (github.com) <<--\n```\n\nThis _tool_ attempts to make the output of the accepted ciphers a little more copy & paste'able.\n\n[![asciicast](https://asciinema.org/a/467327.svg)](https://asciinema.org/a/467327)\n\n# installation \n\nIts highly recommended to use [pipx](https://pypa.github.io/pipx/) as it isolates all the dependencies for you.\n\n```bash\npython3 -m pip install pipx\npipx ensurepath\npipx install cipherchecks\n```\n\n## installing from source\n\n**You should only install from source if you intend on making changes to the code**\n\nYou're going to need to install [poetry](https://python-poetry.org/docs/#installation) as it is used to manage dependencies.\n\n```bash\ngit clone https://github.com/sensepost/cipherchecks\ncd cipherchecks\npoetry install\n```\n\n## license\n\n`cipherchecks` is licensed under a [GNU General Public v3 License](https://www.gnu.org/licenses/gpl-3.0.en.html). Permissions beyond the scope of this license may be available at [http://sensepost.com/contact/](http://sensepost.com/contact/).\n",
    'author': 'Joe Thorpe',
    'author_email': 'joe.thorpe@orangecyberdefense.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
