
Installation
============

wget https://github.com/libgit2/libgit2/archive/v0.22.0.tar.gz
tar xzf v0.22.0.tar.gz
cd libgit2-0.22.0/
cmake .
make
sudo make install
LD_LIBRARY_PATH=/usr/local/lib pip install pygit2
OR
LD_RUN_PATH=/usr/local/lib pip install pygit2 # embeds run path in pygit2 binary
