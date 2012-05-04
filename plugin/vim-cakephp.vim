if filereadable($VIMRUNTIME."/plugin/cakephp.py")
  pyfile $VIMRUNTIME/plugin/cakephp.py
elseif filereadable($HOME."/.vim/plugin/cakephp.py")
  pyfile $HOME/.vim/plugin/cakephp.py
else
  " when we use pathogen for instance
  let $CUR_DIRECTORY=expand("<sfile>:p:h")

  if filereadable($CUR_DIRECTORY."/cakephp.py")
    pyfile $CUR_DIRECTORY/cakephp.py
  else
    call confirm('cakephp.vim: Unable to find cakephp.py. Place it in either your home vim directory or in the Vim runtime directory.', 'OK')
    finish
  endif
endif

command! -nargs=1 Test call s:RunCakePHPTests(<q-args>)

function! s:RunCakePHPTests(arg)
    exe "!caketest --no-colors ".a:arg." | tee /tmp/caketest_output"
    python parse_test_output()
endfunction

