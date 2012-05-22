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

#### Callback for modifying arguments

You can do some more in-depth argument handling when running tests, with callback functions. You can define a callback function and tell PHPUnitQf to use that function to parse and potentially modify the arguments passed to PHPUnit when running `:Test`. The callback function takes the arguments as it's parameter, and returns the modified arguments. Think of it as a filter for your test arguments. You can tell PHPUnitQf to use the callback with:

```vim
let g:phpunit_callback = "MyCallbackFunction"
```

A callback function looks like this:

```vim
function! MyCallbackFunction(args)
    let l:args = a:args
    " Do something with the arguments
    return l:args
endfunction
```

For example, let's say I want `:Test` on it's own (no arguments) to try and find and run a test case for the current file. I would write a callback that accepts the arguments to PHPUnit, and tries to work out a test case from the current filename if the arguments are empty. Here's one that I use that works for CakePHP (I won't explain it, see if you can understand it :D):

```vim
" Let PHPUnitQf use the callback function
let g:phpunit_callback = "CakePHPTestCallback"

function! CakePHPTestCallback(args)
    " Trim white space
    let l:args = substitute(a:args, '^\s*\(.\{-}\)\s*$', '\1', '')

    " If no arguments are passed to :Test
    if len(l:args) is 0
        let l:file = expand('%')
        if l:file =~ "^app/Test/Case.*"
            " If the current file is a unit test
            let l:args = substitute(l:file,'^app/Test/Case/\(.\{-}\)Test\.php$','\1','')
        else
            " Otherwise try and run the test for this file
            let l:args = substitute(l:file,'^app/\(.\{-}\)\.php$','\1','')
        endif
    endif
    return l:args
endfunction
```

### License

This plugin is released under the [MIT License][3].

[1]: http://vimdoc.sourceforge.net/htmldoc/quickfix.html
[2]: https://github.com/gmarik/vundle
[3]: https://raw.github.com/joonty/vim-phpunitqf/master/LICENSE
