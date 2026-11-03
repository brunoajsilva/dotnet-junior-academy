# assemble mod4_bank.py = m4_head + m4_tail with the VD block after FEATURES
old=open('mod4_bank.py',encoding='utf-8').read().split('\n')
i=[k for k,l in enumerate(old) if l.startswith('VD = {')][0]
j=[k for k,l in enumerate(old) if l.startswith('FEATURES.sort')][0]
blk=old[i:j+2]
lines=(open('m4_head.py',encoding='utf-8').read()+open('m4_tail.py',encoding='utf-8').read()).split('\n')
idx=[k for k,l in enumerate(lines) if l.startswith('    ["auth-7", "dotnet-2"], "Se só contares falhas')]
assert len(idx)==1
k=idx[0]+2; assert lines[k-1]==']' and lines[k]==''
lines[k+1:k+1]=blk
open('mod4_bank.py','w',encoding='utf-8').write('\n'.join(lines))
