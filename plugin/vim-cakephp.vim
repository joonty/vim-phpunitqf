
function! cakephp#RunTests(arg)
    exe "caketest --no-colors ".a:arg
endfunction

command! -nargs=1 Test call cakephp#RunTests(<args>)
