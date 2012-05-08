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
        call confirm('phpunit.vim: Unable to find phpunit.py. Place it in either your home vim directory or in the Vim runtime directory.', 'OK')
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

command! -nargs=1 Test call s:RunPHPUnitTests(<q-args>)

function! s:RunPHPUnitTests(arg)
    exe "!".g:phpunit_cmd." ".g:phpunit_args." ".a:arg." ".g:phpunit_args_append." | tee ".g:phpunit_tmpfile
    python parse_test_output()
endfunction

