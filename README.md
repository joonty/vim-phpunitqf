# PHPUnit runner for Vim

PHPUnitQf is a plugin for Vim that allows you to run PHPUnit tests easily from the Vim window. It then reads the output and puts the errors into the [quickfix][1] list, so you can easily jump to them. It's configurable too, so if you use a PHPUnit wrapper command or have a special set of arguments, then that's no problem.

### How to use

In a Vim window, run:

```vim
:Test <args>
```

Where `<args>` are passed directly to the PHPUnit command. To set up a custom PHPUnit command see the configuration section below. You can also set default arguments which will always be passed.

### Installation

Installation is easy-peasy if you're using [Vundle][2]. Just add this to your *.vimrc* file:

```vim
Bundle 'joonty/vim-phpunitqf.git'
```
and run `vim +BundleInstall +qall` from a terminal.

If you aren't using vundle, you will have to extract the files in each folder to the correct folder in *.vim/*.

**Note:** your vim installation must be compiled with *python* for this plugin to work.

### Configuration

By default, the command used to run PHPUnit is `phpunit`, but you can change it in your vimrc file with:

```vim
let g:phpunit_cmd = "/usr/bin/mytest"
```

To pass arguments to the command, use:

```vim
let g:phpunit_args = "--configuration /path/to/config"
```

You can also specify arguments to be placed after the "dynamic" argument (the argument passed when running from within Vim):

```vim
let g:phpunit_args_append = "--repeat"
```

The output is written to a temporary file. You can change the location of this (default value is */tmp/vim_phpunit.out*) with:

```vim
let g:phpunit_tmpfile = "/my/new/tmp/file"
```

### License

This plugin is released under the [MIT License][3].

[1]: http://vimdoc.sourceforge.net/htmldoc/quickfix.html
[2]: https://github.com/gmarik/vundle
[3]: https://raw.github.com/joonty/vim-phpunitqf/master/LICENSE
