" ------------------------------------------------------------------------------
" Vim PHPUnitQf                                                {{{
"
" Author: Jon Cairns <jon@joncairnsMaintainer.com>
"
" Description:
" Run PHPUnit from within Vim and parse the output into the quickfix list, to
" allow for easy navigation to failed test methods.
"
" Requires: Vim 6.0 or newer, compiled with Python.
"
" Install:
" Put this file and the python file in the vim plugins directory (~/.vim/plugin)
" to load it automatically, or load it manually with :so sauce.vim.
"
" License: MIT
"                
" }}}
" ------------------------------------------------------------------------------

if filereadable($VIMRUNTIME."/plugin/phpunit.py")
    pyfile $VIMRUNTIME/plugin/phpunit.py
elseif filereadable($HOME."/.vim/plugin/phpunit.py")
    pyfile $HOME/.vim/plugin/phpunit.py
else
    " when we use pathogen for instance
    let $CUR_DIRECTORY=expand("<sfile>:p:h")

    if filereadable($CUR_DIRECTORY."/phpunit.py")
        pyfile $CUR_DIRECTORY/phpunit.py
    else
        call confirm('phpunitqf.vim: Unable to find phpunit.py. Place it in either your home vim directory or in the Vim runtime directory.', 'OK')
        finish
    endif
endif

" PHPUnit command
if !exists("g:phpunit_cmd")
    let g:phpunit_cmd='phpunit'
endif

" Static arguments passed to the PHPUnit command
if !exists("g:phpunit_args")
    let g:phpunit_args=''
endif

" Static arguments passed to the PHPUnit command after the dynamic argument
if !exists("g:phpunit_args_append")
    let g:phpunit_args_append=''
endif

" Location of temporary error log
if !exists("g:phpunit_tmpfile")
    let g:phpunit_tmpfile="/tmp/vim_phpunit.out"
endif

" Debug enabled
if !exists("g:phpunit_debug")
    let g:phpunit_debug=0
endif

if !exists("g:phpunit_callback")
    let g:phpunit_callback = ""
endif

command! -nargs=* Test call s:RunPHPUnitTests(<q-args>)
command! TestOutput call s:OpenPHPUnitOutput()

" Run PHPUnit command and python parser
function! s:RunPHPUnitTests(arg)
    let s:args = a:arg
    if len(g:phpunit_callback) > 0
        exe "let s:args = ".g:phpunit_callback."('".s:args."')"
    endif
    " Truncate current log file
    call system("> ".g:phpunit_tmpfile)
    exe "!".g:phpunit_cmd." ".g:phpunit_args." ".s:args." ".g:phpunit_args_append." 2>&1 | tee ".g:phpunit_tmpfile
    python parse_test_output()
endfunction

" Open the test output
function! s:OpenPHPUnitOutput()
    exe "sp ".g:phpunit_tmpfile
endfunction
