"""Streamlit Community Cloud version of the educational MODFLOW-NWT + MODPATH 7 app.

CODE MAP (search for the named function/class to navigate):
    1. Reference data   - REFERENCE_B85, reference(), geographic constants
    2. User parameters  - Well, Options, SolverSettings, ParticleOptions
    3. Flow model       - make_stress_data(), make_flow_model(), run_flow()
    4. Budgets          - listing_budget(), read_budget(), assemble_budget()
                         LIST-authoritative package totals; CBC spatial diagnostics
                         BudgetDiscrepancyError, listing_budget_text()
    5. MODPATH          - particle_release_groups(), run_modpath(), path_xy()
    6. Plotting         - draw_map(), _draw_active_grid(), _budget_figure()
    7. State/results    - particle_count_slider(), _store_particle_control(),
                         restore_postprocessing_preferences(), _render_results(),
                         _run_modpath_for_result()
    8. Streamlit UI     - main() (expanders, preview, separate Run buttons)
    9. UI styling      - inject_expander_styles() (expander and MP-only CSS)
    10. Deployment     - resolve_executable() (Linux bin/ or USGS download)
    11. Checks         - self_test() and separate regression test scripts

Maintenance: model inputs and postprocessing controls must remain separate.
Never accept a nonconverged solver run or a run with a listing-file
percentage budget discrepancy exceeding MAX_BUDGET_DISCREPANCY_PERCENT.

Run alongside the other apps: streamlit run NWT_Fieldcase_Streamlit_web.py
Place Hintergrund.png beside the script or in ./FIGS/Hintergrund.png.

On Linux, executables are resolved from a repository-local bin/ folder,
otherwise downloaded from the official USGS/MODFLOW-ORG releases to a
writable temporary cache. Windows retains its local executable support.
Reference arrays are embedded below so no auxiliary Python module or input
archive is required.  Flow time units are seconds; lengths are metres.

Source: user's mm01 MODFLOW-2005 model (one layer, 100 rows x 70 columns).
The archived CHD was NOT active in the supplied model; this app replaces its
47 eastern positive WEL inflows with CHD cells.  This is a conceptual model
change, and is not claimed to reproduce the original head solution.
"""
from __future__ import annotations

import base64
import io
import json
import math
import os
import stat
import shutil
import tempfile
import zipfile
from dataclasses import asdict, dataclass, replace
from functools import lru_cache
from pathlib import Path

from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# --- Authors, institutions, and year
year = 2026
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
}
institutions = {
    1: "TU Dresden"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)  # Institutions in one line

ROOT = Path(__file__).resolve().parent
# Separate from the repository to avoid writing simulation outputs to Git.
EXECUTABLE_CACHE = Path(tempfile.gettempdir()) / 'gwp_fieldcase_usgs_bin'

SEC_DAY = 86400.0
MAX_BUDGET_DISCREPANCY_PERCENT = 5.0  # absolute MODFLOW LIST percentage
SEC_YEAR = 365.25 * SEC_DAY
BASE_K = 5.2e-4  # m/s; excludes original lake/high-K cells
BASE_RECHARGE = 5.323598752757e-9 * SEC_YEAR * 1000.0  # mm/year
BASE_C_PER_M = 1.277053869525e-4  # m/s, effective/INFERRED reach-length reference
ARCHIVED_CHD_HEAD = 372.6  # m; archived but not present in original .nam
DEFAULT_EAST_CHD_HEAD = 375.6  # m; provisional inflow value; NOT calibrated
WELL_CENTRES = ((4.65, 4.45), (5.05, 4.55), (5.55, 4.65))
WIDTH, HEIGHT, DX = 10000.0, 7000.0, 100.0

# Compressed, embedded arrays extracted from user-supplied mm01 files.
# Model data include IBOUND, elevations, K fields, RIV, CHD, original WELs,
# and the original unpumped head solution for initial heads (not a validation
# target for the revised CHD conceptual model).
REFERENCE_B85 = (
    'P)h>@EdT%j2mk;8Apks^_vrus|NsC0|NjaA6aZ;rZ*^{DE^csn0RRvH;B5c^000005di=I00000?b5MI#6T2=(QNBeOg9QCA_#(5+bK2{RubHZ'
    'g1C~1jrbJ4u<IL`WtV#cXW%O`)t|%s+}vH?-'
    'mjX^=BuuU>2a(VrCz?A)wa~9&G<3)Zx5SsJ^bBY^{>;gy`P@@_hI{eeA;zwIqy!|@?Ca2N2{i3mfj&w^gnUok|8c!xNzaJESu=<T$W`My*sN-'
    '^ky#0vWecC)h2o?m-x7FnPW1?D0*+!w-'
    'ddOORl)gH{rsC3zvOcaN)v*3zs;X=&fAh<HCgtmuM3%T)1%I!X=AM^j0o8;=<(+Hqjfi+C=Z;k}ob?_GJ^jD??oVZxg*ITU@y8ViUa~V_YOjk|'
    'arzBuSDaNs=T<k|bs57f?$B1T6pn00;m803iTF<R_8;|NsC0|Ns9702BapZ*VSdaCrd$5CA~i00000001@u00000008aMOHNZ^9LC`?bp_%D4='
    '5bK0tJ*y1w5iwE>fL1aAX>3<G_Gv2^|<$;Yin{d-'
    'Bx0D{yF@ck<=?=Qn)5ci)}8eLvN>ZhS4z`=gJ;vR#yWgPpQjl!MFR)v$N*;c|H1pWHjW&!c{QAARb5>DT|o^;WA{Y`2!0#kb<$c4IKv&2hCk+4'
    'Q(-Om=Hr{r*+2et-U`cY9p@?e3(zn{FoEOuBpNigdH-=F-'
    'ijyPxhsy7_bq=@!zJ=@!#1rCUz7obF+|X1bMhtLawLt)*+FTTi!<ZX?}hx<~0Ar`t-'
    'mm2NxTPP*N6?R4#QPtxtB+fR3p?jYUMbXB@%=?>E!rhA_5MY@;iI_Wy;UZp!qcbx7d-'
    'ATIBbg$E$rR%2arhAi)7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc'
    ';ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7'
    'hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;'
    'e{7oc;ST?UU=b!7hZVbg%@7_b1#1YP)h>@EdT%j2mk;8ApqDSM56!y|NsC0|NjaA6aZpxbaZcRE^csn0RRvHK-'
    '&NS00000Mgjl;00000?b5w+jA0zc;f;@A5fKDIyxki!TdYwqMzNKS(I`}AM|MYH#O!9@CX=I3aZH?t&mahb@NV`#0;Rd`=9%X|zw&x|`|hnf_o'
    'f<EW36274Id23>qU8^f30j4Wq)O`I_N&WzcN_vjqf+RkA}VaK781H(yRYVm)q@DakYJ^Rje2Pwq}34SEJ6A@m`NQjq%=$Ixk<;tKa9(>b)IxcD'
    'r}!-lyA0w~_8cx{v8TrQ1xmneKDCFX_If+e){U?pwO=>3*c!PPd)zXS!eMey7_>x0CKqx<)nWrm9J|r<!#2yW8!pCf&Yt`_oOQn@)Ei-NAH+(l'
    'ygH(;ZHCB;C<;GwEj19ZNTx?s&SnbaUxWq&u1JRJ!?e^XX2fJCp8gx`lKL>CUA)pYB4s#dM45E~ev!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%'
    '@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;'
    'ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7h'
    'ZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg%@6U;e{7oc;ST?UU=b!7hZVbg_r-_%U@7S0|YGq000O8001EX-'
    '%u|Z|NsC0|NsC02mllSb98caE^csn0RRvHK-&NS00000yZ`_I00000?Z~kX!B7B&;aWY#-'
    '7ZOonur)oHqymll1AGYM5Pr5@f2QI8*gC#&hq8_pWS|&A4bU|dBw8oPHkL<xT+U14Y6+8ds|$OO<Pt&-'
    'xQaw>U(!CZdLy$vn)%)Je#KB9sb)m8J0iSBuSDaNs=T<k|arzBuSDaNs=T<k|arzBuSDaNs=T<k|arzBuSDaNs=T<k|arzBuSDaNs=T<k|arzB'
    'uSDaNs=T<k|arzBuSDaNs=T<lKlAvP)h>@EdT%j2mk;8AprFE^A`XA|NsC0|NjO66aZ*zE^csn0RRvHK-'
    '&NS00000>Hq)$00000?b5w!!eA7D;kdf?2EOgHkReVL5n3s@Ra`naNzh1#(nwOeh<FjbChyCiu~398iauv~IA=P;`#XMrn@n5DPqL1SqMlc=AL'
    '3xyi)o0<vih#_uUT0wisOBhf7Zp}UVr4P;;?tRS(b*U>@f|S&}`bTyWaMpJ$xofk|arzJZEy6>C0a){THvx|2okPn{=X^`?hH(y17sF!b|j`8<'
    'HeRk|arzBuSDaNs=T<k|arzBuSDaNs=T<k|arzBuSDaNs=T<k|arzBuSDaNs=T<k|arzBuSDaNs=T<k|arzBuSFIZTC=10|YGq000O8001EX+M'
    'PC2|NsC0|NsC02LKcRc57iSZg6=401yB`+W-'
    'In0002%000000002((lKfRQ4oOPO<`j$@e1K7Y_V36ASeiS2_cZeDlGaWg{bUGn&2tCK~5TDDTKf_hWJhMF;h+PA0A&Go@O`Md-'
    'f3*sh(HyKE&a25c3e1n`&2;>(@=SNZ<EqxvJCgUcZ&wblkiBqR7Kt(aXa=G@EwoGp6Us?T92vk|as;H?z}p#^+x8Fa9lm>O?ne(ur=a+oql9<~'
    'r32FVTx`NRlK;k|arzBuSDaNs=T<k|arzBuSDaNs=T<k|arzBuSDaNs=T<k|arzBuSDaNs=T<k|arzBuSDaNs=T<k|arzBuVmr`vp)-'
    '0|YGq000O8001EX#X&}h|NsC0|NsC05C9YacV%pBUvqDDa${w4E^csn0RRvHfD!-'
    'z00000oCN>?00000o!5IzQ&$`Z@T+v7_@E$)kxr|i1?@Uo3JPL5QXjOGw&2(_PASU6*Ptn=7-hNhxv5b>YJ5eVh@!%RqT*Cs@qx-'
    '%&^bX##MFp!%m;Of3KDmhlyl;5r`%-yulJMlJ->6$J-^#-'
    '*C)jrXZ2#1F)JmhY1#8Fl1Q;6Dt&@PDwd>YS#m5XnaNp})U<!EPfJ;noyJ|yUXWr=<Gu&Ul}f2t87vj&iT~%vlc9cM(caq)MK#xgqCdXg7TxW;'
    'f;1xQASrML_3VAHd)%&ll^GaFcQzLJPA-i)KG@ZGP0!BqIHN_(H<~(Azt3EZ*P{1cqHCLqWWa^kt7?ihc`BIi%i}|NT!ekc-'
    'G$nn3qJ=g#y<Rc%dtVP#B^ukP|S*^vIOBs;G?i#PU)1r)rHWVjYIXjc9$BCJXU?|f!NDKO{I$7axi`jcJcfz=K5tKx-'
    '&Xtz9;u=`Z@r35cY_<k9@q>!TQExFMZ=vT<7(xit4NmsV44T;n2hJQtTCILxHvy?yn5HY`>3o?b%UuXX4Sk{LENOl@IU`?EVimnUnnB{>rhxZ('
    '~YM_8LxiZvJ79f2y;J;Qn`y*P*25wznr2zXa=7U>`YpM)3*(oL_<Sk<8uxG#{=%6xWwm{cvAHvnPE#=bed*4=)`s)<u3iiW}lp5grWhfA@Gjx^'
    '?RB+@0R8>eHi)tS#T3>N}oZALsr@G`<0%FyKn;7OQf$Jrw4LVYkk7D|r<T_b&|BxAK|7BV#ChKEtuo^T+e}1nh5w#r`j@K##zFsiMk0V-'
    'DOOr*rqW-'
    '=f!RP77U)=W%ZT#fd{sm)(Z_JretQ@9Pm4{xg0ek4N$NBpz4scr<qPyws+H6Jh^$I=BAx6XT+5_bY%S?2dEO4wxcAKFj0GWS;Rn&cyJHCw^7XS'
    'T21araQO(LwOIHGtLYF`D*O+d>&_}@QmkiW-4~}!OeH;HK2d7#8Z>^dLGT{Qc;~-'
    'Kg##}aAOtBpN75uoc*Ttr3>fI$97%ZDsA;UkWc*2g0OALgJFM~jy>|cz_h&o7`k)kQ&3&UZjJH<>myFjkHzj^XlOp6gZ<y>Tz|ScTP;r)fcG~`'
    'oSv`2&Xii;=deP$GX~_)i4U%Am4JNW^n5M$-j4eXwjWzmRA&w7Q&pEw(M{05SmG~Ms@>Mz38Xt?MAFsn`)k&~{uGD3v&(Sf^-'
    '{P#rz0a;u5PS0CByoi&KgmKZcB`c@dxu0zh%mpcTg2TcbgH7@ciR>U-xk!Uxz(gc~Z1pDWN-)faD{j_b%-i2=a-'
    '$#dQ6yZi4+k9{WN^XQj#;_CKei1ho03Z+XJDr{MV~PS4k4Uz^ia(klg=Pj274=hqiE+&AZTfPCU-lH{Y0w!{8w?AZ~IvpjC&aqfE0^Yb{%<2D{'
    '=5_#q)UNu0FnBON9%ujrEf9b;ykz?r2-G@WgcaN3?gZGDxc<kMR`QZwX&&<GHljVM^UIQEvUp(vCxnaj(eLQX>Zr)sO-'
    '`eR(cW$56Qz|c(XyN(&0{buF$950C4(lUcoBQ3sj=Qiv;z9a87rJsr)17+`mlSoF+M~ele;aXXK9kh5BjWms_4+3bGP-l;#IXA9UcWQmpg!V-'
    '!3C2qexd~R5s$gtdhGxL&U}e|!M!V!D)+$t<aF*Fi^_zF8(YBhgNWPfriUaIf_#>E%iKK^+E2mz-#xzp{qVD`y1%{c<NjeI-eIm3cwC0{e}#Qh'
    '$!`}dD)9Rs5f8|gZF<t~P*I(GKNgNVtgywx`iUP;ypy}g>cY7`8Fq2G@%x#rpnl@!HsKDBM)?0^CicJlvYuaRg#Fj)T%W!=HRQ=0uVG+)#7FE?'
    'JI=lU`7CimYuRzPjicz!y(fB~NZmYEFNyvKP)h>@EdT%j2mk;8ApkbYAVL5C|NsC0|NjX96aaE*c4cxdZg6=401yBW8~^|S0001R2mk;80001;'
    '*LzS@*BuA&wZ3o@lvt7>jgJK#7I6#e@=_P?RU%@HMhuVCk`m-'
    'mqegkIJX9_s?}t(q)Fd@k;>0|tX=|g6n5~H!6$N}EqgF)3pokcyTC0<u{T=c<H+$}x%=G@Vewokw=ImkpeV5G(BIhss%>bQMmt#ywOp8x7PBR!'
    'SNkK-F!I-ovH9a+MW$dcdghcz#L*rJYC6b?~EsaY~B-v}SU!chlFu`P4YxqAOy-xku-jL}(eB`=0*RoyPtn!C#POFbk%#|P?v&uj53iJAw-'
    'O0hkn+@^%l8vPjWJfPEpJacCpLck)Pj^t91X<`!=yx5wRO{bbpzU?cf8FO5vr%;($d29?jecyw?eGIC51D(v%;&h08zKIc6Z)jaCCeqqLhp^<B'
    'em^?`UUygUS{5Yefn$cJdlq&zF+3e_J?@op7cpaU5Nx)=)KTKM121IVefElZ;L{|@d&v<;<KhlY}JpgkRUsHh57FA17iw^e`n{d&$>TRB*;SVi'
    'GG{qY~%FKOl>bSA4Wcob*l3~=H4&!wdDF*i2wA%%j0)szAZr(`tj(S+(tj!VJp=3wn+5w(r%UG@3;JCnQw^%`Gm-Opg)+<e(A}YSZ%K`A7j68;'
    '+>vejdicCkRS`a0ew>VzlJ?{IYZma%#+)`9Zq~}hi7`}+6@w9p&y0b*jv*O(kJjb=ItN%Y~tqyJXxF<nJz&VdN=e9Lte-'
    'lWZ3vK-W7d~OZ3+AL9W`~7J)v6{5p3NKX&k}!M;1IB*@%-GJonMd5BLrU3n^Tu`EFrdKdHutGA7--'
    'e0cmW#%W?e?i2XZmtY{<AfqX7J4W2*Jlq-'
    'KXxrk+v}LOud^}Nt@5P4S%+G^OC`t+j`#CAdi#H;ImCaY+#4R%Q!GJt^a}I#>q}O7$c|oSe#dt5s61pxuVen-WPKkYepQw4fVy$3CCEbWg8oij'
    'Zbn1Q25oO!gnp6z15A8t$daO(<9QNfp?5|9^qV)OK`*V-'
    '_6qaRpB+}YaG3c@n_Cg>(~~0ahW<~J4sA|Zlcw!u=Amzi_rEyM?7g&{_OH;7LSN+T-'
    '(3G?oVM374}DAgt6PfCmM`B#``6Li!qG$D5+8MBRgmQw3+-Q_H=wt*No&gMDz&}BJoGd1zdw{-'
    'pOUW7z7~29^mS=r?H5cL+FoWJ`k8q7hiyJr^kuZKx%*)r`uT=cURM!o+%vGhuTP2mc=RF1tJ9LxWNmL-'
    'h#va+20IUAN3Sps{jBnk9lgvv^eyopA6|0w@rV@Kze4YcKKqLUdp(vGYI_~?(9gu@ANASu;OaWs*Fx`wUYXsw@b2^Z+Fp4LJ@hm2ga2q!e9tMg'
    'uZ7+ly+wa|+&@0g)Al;%;ic0m&uyLgSwhfy+SiRDZ$jVZ88$k*F<09w3(!M96TkO|{mnZw3u#{qy$||J+Zx)-'
    'L(;Upj(O;3;_okuIdT1H1?_90pM>6H*njJPS-VKvEA!Dq-'
    'x9x~%h}!RyovTNH=lXvTjIBPy*G5o^?2I9LO&UO?*Ttst$UfaS6)RAeM|h6Tfcg!FVCd?EA&&)FO8`D_N{aI+Fr*z^eyp^+RYhrH|Nv-'
    '6?!xJ;4@9zrw-53_R2i;(9buma^vn1@eRRcw6B{)-'
    'VgnaJw10zD}JZ#b<9Jb6MxlwD*p1wQrhp_{8!LJpQ}7%Za(wS=PD1Gn?Dyl^fU3%E1MsA)XbrME%g5AZ~Dr9%eEJ5dmZ!8&#Lo4=H`c?hra!ed'
    'C1L<^O=YKBtEbp_CeIh<+M+QJ^+2yqWyb9$=`#TUYUa)`c`!w$lQG9p+AZ5ZTQ>M8O9RYr`-'
    'Hd^w5XIw?`^@7DEZ`M{Yjz(1$7ynVUZwJ@i`_`M&hN`?`+J%V^)77WqK*9p68U3&~lp?RCsUA9k_xK<4JZj2`-s_`KZw*E}8-'
    '(|+XUGY|bn{2wf38^7!*rhUiF4?z!orSg!u`OHKAs61qD{w(zHa*KJ$XB_7<5B;F>kR81;6FuyEm50pDXCC&w%0uSn%jjW$t2|_GKJ&1TRUR_u'
    'CG@agRUR_uXP}3Dd7F92XB~Yodf1o54=Ve0O2Nk~>HZY@0Q64#UaW1itQU9-'
    'df2bTulP%8W$}>yeardj=wZLAJY>#KLl66s_`kjx`sdCs*3$hc^#15QU7FtUj<gE=RP?Z4Rp)`s`5^SLU%Q!ye9qAaqKAD+d}YM>Z)Wrq(ETa&'
    'e(1B5^Pa}Iw*)=_J?vN2c_4G%A3f|>m50oEKlHF)RUR_u&FEpj62H&X`I2*UG~KsCZ$@8p-'
    '}!dovqb_w1wHK7JM27=&pZ0b=wZJS|6=aLcbks%?_17KLJ#|u_|x(CM&^G|Lia7_ebB>xRe8vqH=&39N_@Q6M9YYnNV;!@-'
    'Vc4q<K+_v^c4!cH+tB|s`EhRycc?S>0uu71xN3R9`>=yL+1Q=^stYKuikPjtYY;Nx}SyKAH6B$E8EUr6bQTrdf4Bp^FZdj0X^(*;)h5TG4lKU`'
    '&{S)&_|WWG;jT9iolOT5Br|@bouhG9nbaef1wXVe`o%^eczwU5qLNB&=17lyjV4*duadnd7%$NKT!YmG2?^v0`H0*`s6P8e%M>NA?HaB?Uxpjp'
    'Nif&!FlS1r$qwqf*$&W_z!#@?;g{YLi<JNr=kDtndrS6hE@o?6ME<$;@x*`bsicWOZ!OZr=wpOQgC!i)~28F7W5z0XLnufo+<D;^w4j__qF()_'
    'kF#J_8sSYr5`=?74gHrT5SF<b2jZSp$|r%*yC07>9?f<|Kk%(`;PdN9kp-Y`g?!h3H=Q86VAT-'
    'j6Ne2{r><^O9KQg000080000X06~(VaR2}R|NsC0{|o>W0A*owbYEj=WG-%Sc>w?r0N4ir000000ObGx000000G-'
    'so3c@fD2JmzBDY8YOqoRmICc#0i|8<gLTO7nnD>{g9@8G0QlSeZm2qKv8yyeK{H{6#Y*Z#B@E=zQzvyPKuo$Hp;?X;-'
    '_rPC}w<k4=G<#F<yccN{PxOuUO_K7=JYK=hEtAV<xf2&L%H88I}H20gU?&;k>7=w;N%o)%z=q%{mJ+>d{7<3kNGy?Yn9Sfa%$KN?XM`O$x&@t$'
    '&(6KMa1ak&-EOf?~19UXSoDn+m<p7-p9nECU{ae3tfR2TZJkElS=9n`=$9+!@p(Bs8preJ%anF+%bS!lA?H*7|0|YGq000O8001EXLnX-'
    'x|NsC0|NsC03;+}WXk}q!Uvgz;E^csn0RRvHK-'
    '&NS00000z(xQ700000)tz~4o!wU6J;l!G%=6?pgEKjHVkeHBI61KsXLja!p6AI<&aq3OLI_oeq6#5OXG$kZRZ)Z}LI@$+(w5FGr9u@#RmDv_#*'
    'XLN>GpGf%WL<$mrLP(;X?j7%JF;NcfWf->silQd+oh{qV~ec(^t~dl4;*paQ{L5y}E*myn?+CcNc8UD|q;-?rq(jm$zQk-'
    'G4Cgea)Tc^$)`L^^fnoeh~h@aeHy`*1WRfO<VK6KkrZWZ+h+BIhV_)rV`ix>c8sS7(UY`{)Nw9{5zdL`)_kniC^v+`<;gHIWuF+UtSbGf9bc9z'
    'y8zNsl?M?d;1eh!e{;CAOH9lr=$`;a^Uv+|CW_X{QTkn^A{F`&-K|q_><L{sl>yHe;M2-'
    'J(c+H`M)>x18MyKb270u{P*d2GVwo7hK7tK6F>AD|KVp2jV2SRU;pW4MI*_?-'
    '&<Dn`|F02iK=k>{Gnvxe>Svi*gnYh1Ifgm|9$GmeyTs2_>Vtx=$Cu?l8MUczxxkfhtHo_l65gRe4hV<fAqJ0vp1Re+rOFj3w7ah@Lc#J-'
    '0$BVFZ+=Lp&c)pMt-'
    'g<i_h@hx^8AF@i+fQ_&1yO&PydqCjKo<CCVo{U@`r*jO$m>FRN0C(7LJrEHCxVcIBrM;eRWxu1h6y3qy~tPbIG24}U30ee=CHrV_t;H1zDIR3h'
    '<L{zb#ef4=@V|Ezz8(cZr^^pnOVd>;JK=S?F47yTPUkA%<R9|*_@pQnH9r(VtrpX%>yaFNZp2fPH-'
    '{nBrRe&2aB^g#Fwy>x$1CjAxg643Lb&jVg2y76Tgr+*W=`EkI@yNQ7fc$t9R{xR?|%6JF7s67EEn<fS*;6!*H1U~^U9ijO*177}RfY~nxd}v(5'
    '=LEd}SHOqHub2CW@AY2cz5!L0)6>2Ee>a%N@o9|rOmGqK@|PwIV;=9bkbVhxSsI#G81ORj+R1>IHxob&c$qN2U&`bE`MhtyOZRUFfN#LQ0$wKI'
    '^Rodj;cc^j@Xrxm^xgp{1rq}sK4qr?7vCR-;a77Q*YLS~;>E(}zwQei7I4xy(XrX!AoTZyx%^rdcndfg|D8Yt;ZuB(fnA01`IS{a+;%1n{t0-'
    '|^T)wQz{}Z*3&MB`e}M;%1X%w35WEm@a&f{?15Pw90VjVgJiaO5K;zlR_W>XOv?~ly_!JL@&)xuwmhgMod3cV-IRk#k=DnxEqqBIAfS1*wxxX?'
    'GJO#YGnit+E!pnjQ!&w2&0$#*tdGtp<cw0w51iVbZ_`ej;KLID=_sxHP@M63o{D)8Vf53&tDSS@Q?)C5)toiqbLcdPX%nyaniPs(oIFVnNf;|P'
    'itegNwz=`ZPe5(60;N5ioAMhf4d<Gw5_>I6T6Xy1lBaC;z%cn3*WdSeZvoPMmZNQ7#+wXj$aqH!NJ@ANq4mfYgKZfT|n8VR5cq9jZIz5$`fWyx'
    'Oyo~-'
    '_XuzCQV!|!{{yh5O+u%k1Y6Z9ocoDDV@w<HR6Yw%&9zVJPd<0&ZaDTrY@bXW>>;1@<RAS<GzgU<`EDqgzt_Zs<PJPqAZU@iXzxTM(I7GVTABJK'
    '6-Ozus;~eZNe3nggXg2(s4K4ys#Pi|v*o0wP|7UW22Dl11kv~ZTkDuX>z$?-'
    'TW8h;HKNIkBTL49$1e~0hxM3LgiSDcHN8j|JcLGl2R{}mJXyNC=r^X>%FMbU76Tf{1Z=rp9UN$^8jq#hoc;><jb7*&j7xPELU&JqeJ($sN1iXZ'
    '&{rJa#mkGC=u@*a92aY!2&o{!efmbHzFKa9JEu=q-'
    ';Jsq(@y`%m)ZVG+u^iXA>hJI=`!@T_<~_4{zkm~&)f9AX7CJE#d&}Uuboe<9`~8eR7>7T`@Dn58BjOc};{g28&-'
    'Z=sO~8r#N5F^f8$M;91AHIur*@CK{}B#Dd;jx)3jd}ut~20+nY25X_ReAaBmJW1EXE%%!+uu4BdfUI8vM;#bn<%osQ~<KMCWV<w_CBRfEU?C5q'
    'wmPzS@pn*zvu`i}*XodByyYcrb_e%;Eh4PNa{+=YJgth7$Vy?+4hA1)Rw4v(Ph{_^k|ZmyRw>OHJCjbj3J4GwM8`ej8$Z2hkn<@Jk<m54g~HcE'
    'e9S;A4RAhlz*A@k1H#{S@qdDt=`K<2RH4&mvCBCEl5XE}aK%7Qi!$!QIl-H}!hNFKWjc-'
    'g7Peu^t^5@G{Z8hd1Gmw}8*B=$mcyYZ3NYjJ<7#Z~hG6#c*PNT>2pg9?ZdBa)=M3I9j?s^ncBS0Yq`M#YNHw8T3y&@n;(2HI9xAydu6DC7uc6E'
    'dMtIUku=v`iP5qiN6C*+5?P#IN;<T2RZZ${pjZKd-=&R?w=0sr|=%r;K7;bwcKz0ly1l+&YJ^|1iUB?TL5krr4kcx__3wvm`J}!r>%h()-'
    'wL<!D|8hv<Vz-0bhmazis%ZVt9Q!cDRG~mwfN>VsVh(D~EV5hjEW|i|pOvh$-'
    '0F6ykz_lL<HQ2brl!eW3o&;62l^$Irw$0WZ=GWB8j9bjYyl74c5Mf$TQmM7p9I9n#}^*YNdy6Ao)MIqCQGyDY|WDslaHz{yuX_1?Mg%^b#mK6b'
    'DOTr4GyTAunQZdaj)0$!w}0$#-5>%rYduHQtQv<15>gl~%I=VId1?dYBz^j`^nuk?F|8`HI>S1ca-_koU=<<P!tcsHB(oPuATLVS>g{bZsGGPo'
    '|C@k-'
    '<VpV6xUFXE+9#(%`)X7z9274>gFpS|Ft8(j2~mkHNRz~FxPz4XH8<Yb;u`IsEyu|Eb*zWOQs8RBZ?3FncIT8MvMf*)JX|5xF6)}ZUxqMtXQQ#S'
    'Is8QzF=i~6Ss{w)TVJ9u6R{aniU?EK#0MflEvA9LuRD1H`CX47BU*v%B;<tgajEbJtcxFX<X%>;2r`8o0HXZIKK3!~`Kz$?P%5aT_-XCLuW;1l'
    'V;fEW3RfFrdxTrd3;?jt@(Bc3xHPydtS<g1_3+jG!m!7nL4yac_s96MQszgYuL*5SuD@b``Q@6E1Tq)WE(oPZPg*}yBZiyip?Quux+asDp&uIx'
    '`AH`0+&+-&+*JeW<tXXDQ!-J*CR3;WID_fbCA@^hwJ^!|ZY^!qXRVTAl{z>9Q4@I%s>{hm)z+|-'
    'r)=5u<<w*)*Xeh<G>+%V4l(&^7^`gg|HhZo^<Hat3?{KFFT=yLqYYW&R_^zu5sk94l$w=J}<ka%GmadxrCLDB^!_|;P4*PYmD8U4PS-'
    '|zm@!;S1X2Y;Ny^RvN!HshZSzec)6{F{ZI$;5wUrY7SN%^#$rYXYx`cgEq1G0)41Z-($YgRV<-U(2U-p-T)u#y=zE`NDmL>kQ)1Y;gZI;>A8K-'
    '>dgr;(Ay5cQy8vPdvSz_@Th_bLx*R__0EGxCsBgo%`<qH>LQuo#1H~ezuJ3cH_s&|Mc*p@yh|XIq*id$3x=PDBohbMdOl1z9!&Aac>58kPh#rk'
    '@pLDkv|UODqfD}6V0z!eocJb=lM7FcfgDA*GFD2;7WEr!uOx?R~bI9rSY4FKb#3a%tC+8LO<k^XUxT4<PxvUMmNm%I7vJ_*Y%6q8}zRFZzX;?k'
    'N#PUep^reVI%F>j9=SIoVE@AE#~^|#HA6h2&cQy(PikL-QcL4xUC}fO&z!A%j3r4WsP?>d8%xmSF!%rxKDv!r_k;!zR%=$8R+_S_&AMz4&$jf('
    'Rg4Ky&L?Ao<GFrfa_WDS2yuf7r3(dp+TQ#GM%e_vwY7K#$_t;?{wninfQ}g*h4Pun+;!BK6ehdn#=gl2S*EucbDK#mNQ<f@V{$_gVyo94fN|q_'
    ';(BVD#SjEz-h7PSLDx1oL9snyRgGD`oElUsURNRLwolyE_=TmZZtmG%r8g0VtHJPpKTsjx-tvi$-'
    '>?;>7NYjI?}oFb74HiLu16n0WZ>x!|0Vk^hiJXwO-<;F7VLf^$Ipmt#KPgCx1>(&QpnRroi_(*stl{nczFh%jxfPu<N-'
    '#AFb!j$Db_ZcZ<;t%jky{=-'
    't(fQ$BcGhrJi@_b7fA{tLlv5&gFvJe3e%M7*N=l;MwdV~^$VPX+pV4}7(k@4p~kj8BxujPfiN4_W+d^NP|7QGU*JuGP8d{nAsD^(E3nfmh_G$H'
    '=>ldcH+^caVHrz>E4L;6vm230~;|NBzwI47py`b>rxubk|juZ`A#w`620{S?JE$=<qqTKf;Odv5@gx?EXjkV>#Ea0v~zk(<tAf_uoi=ZpNOr;>'
    'Wk~`(k))2Y$T-p4tgt?*ccw>F09nu!20~9`yZQ@V^(oRr%%cV)ZPt?<mirc4lKAk!}$mL^@ae5!Edy9#2QFrJ-'
    'ZS8TWt}<&#I44;TgqgXH=9h@X1M(|uw-sK?`Ijc>SK{1NUWzP5SGboY~1f1z=l25x3}-e2}ToA`Au<1`;TUr0V-'
    '5qMaFKU$97Ur9cEHT;wh4%UIc4e0Gn#6?@cXCdQR#B;XOKRduxDgJ0D{-'
    '_MT*iAfEfj`@WJ@4f{m9(c4zWIW9k)O{7@6r5_{N)t<%M|B%%g@PPqq+r)i_}l)y!U4xPmM>wi{5Jlo*5<{8uU6A*-'
    'a0AD&R%q)=fUI4_zCs7Y;_eK2P>%IL&hZs&Se|TrmTj&%z$&aQ!^;91Hkd#P>_+k7eL6s-'
    'v@cXxYbF`f0t_w^$xm_uI<nHpV^Dx58@)IM@l#@8bI1@JKoN;|l5m_JHTT=<$8L?>@(gc;_H|dl0-I`tEUL@v`_K(zoV^tR6~smgV-'
    'V{?DY}GSGP$*mb(sEyy27^>Y^2SlyiZ#p>qzsfX$zPW}Y{bmNEmJnj}wM_fl+y@cUdIwYGsVZ<-OK`!-'
    '>a~S`5^mjBrr2btBA1p_|t>iwd8TWkpZ5?^M4UA8emy^!fO5C{(KT`~!??4BZ((ax3(K7u0ZrWRcF5km@?WG-'
    '+@Yz1_m7w1bFmBcO#e>XW9{ld{V)3%ZCDOO%hr|ofyrTLis$0<aQ5-'
    'ElYUB2q`Jkw7!SJGSA4dNUdR>e9rx*NmJI|O7wz^&MV)(u6dW`%|8upq=+>#AnPlK;#(0<FK%z-'
    '!Oqq`QOZx*9NqWMJWhN#|B_{{fu1)G1CPTRzNw$P7-'
    '=%FI7PmukT5I>cIw_U_vyBY6ta8rRj?j<g(#2@TKSMBG068yf3{7*IW4b|NLYru=mH|sgsjC16NlqZ=&d$RD?QU2fJXw8SEgZDJ_+h_8&5njw6'
    'Db5)7e2Ue#SYB7(cY~uy_gel}I%o*qvAW+h+MDV4m)@RA{%8iglFRpV&^PnJ$3pbu68yq4cz*>tWHoqLLqDzcx?Ht0njcbp9Oe6k-'
    '(qyf4(zf7yW2^-'
    '%b362?eVhZRn(rn)SXn)u6<mW03QeNpH=v`YW!C<^HE;|UaYQCx_=6OW{TGVm~N3Sj_SGf9+|{{8R*D#crOimwmjN6^|fJK<>yAgK{O8_-'
    '1Rdr9q^+5>1I8^C*tjH>MQ$vzDeUB;w{aue`Y=^!{0}KV5;+r<>!Rox%B^h#&Z$ZFCiXT4nM5KzVpa;=X<_i*Ka__ZDQQEaQ{MZP=tTm4xjAsx'
    'LM=4i*}U3=jHHN1$Mj_KB@%o`>@yj=<Ec%dVs%I@!V?0rTXjBziQ_c&)+KF5cwfnZ(%yu;v)S$%DV_>>F{S7|Bv`Z_8IV^aU3DPHcT8e==nO?M'
    'ZkmNt{(C)UFe`s@Jlav8zlY?_mj@H^(h&iU$lA#)4RgG%?HhehZdk;77_m}#V(hVhg!vb^01$^T(=&6C}3PRp&z#3p9}ea5r5y#^(E-'
    '=o%pp~^zUx`M>&7r11|T%XO&#P5B-#YXA-pc0Q^+N@2lbcuMscCC)U5lE9Qqxx0ucqzA~|&O!BB1)Xzlq3(_eOUMxORe~fs(PIw&jd1?9gKChc'
    'o`?|>2b@Kln>KF#V*$DhIo}8=~HoWWmspyFr^k**PHWzzb052>?=P&hmNP2Y@I&=*>b1gi(0spm;@!kv`x8gsdc|`qv2Ygb>c<-'
    'X$%Xoe{`O*sPau59+=@t3U{oF5sZaRRjtpZO~=$dNcw675_^2bwr-'
    'I?{X<^3)HrS@deUzx<sQJzk`luq2229HPcjIzfu@+hP5#W1`uMBZh9JaC`SH|l-6@I#&OQ8)FL!GFnL4-'
    '=1%ai4VTE{lB9RN6Pg>vQFw<}$7ec>l%3E6eaRE3lu{@WmQmf2Mxfz;iZYUt92Fh2X1*|8FNxRl<0dg4<o_@7?fEIeK;vyuBCvM!X{b6!D7e_W'
    '<uvh0conkaXhLpj+(I;$_R<>b<7mXS0akvf%A#zDRbR314U6KhyEcX{kv)VR#WAjG=Q!8TY9EQaFs(iO6nysgvoZZu1lMyr1xIeZ)&cu8*W+(>'
    '$-J=S>9<GtlR`@b_Hw`2t@jB0gA#-K@mUSHq+E_~&)-'
    'eF6Qk34gK0>z}NyQvcu1xR#Jl+sW_Ch~Iaki!1OSd%)kfiGxh9DDQj#on6IyRDJpRM)`rr|0v#w^8Sh=vv~g~F0%P(*<%KFn4X%9Yi(ZI@M8I0'
    '>DPc4+3zs<xgoDp5FhlzKfTmJb-RwyxODnD5{=^^es7fjr+M6O>#4-'
    'sGsu_b!qano9#L_|66|;x{IinxkJg9i{nryu6);|#$<J;DZ`<IHV(e!J@ocHrJL&ml@LoCX*n^*mcty|MPaY;ge&7JVKLF1~yz-^-'
    'qUT3Au{tP=hiqM!twU4ZC=-'
    '2{!Fyz&|I+D~H2NXZFT%wbI&~D?GR(Zv5P6qD@YT=XZ5?ayOR}df{7t9V@k)nSUAW}|Z5>=DIw}Xgm_fU9$!|sL7Nx(JaNTn92CJ~!Joq!xEgI'
    'J-FK2bzwth(W+0Ok-;O$7?%75$zZx!Hk4{>lMINb*yMfnxI&jEO*ihN=<`1(`8i})~$db%w1M;81T)z6u3vHE|#Zw9(8gLX&r((2#O=-'
    'LP`ww~T}s@3gE9}SY%jn*wH57fhaQ5X4}PW)Gw<4gQA!aTv}<YYe4>P<C{Gl=(d;l+9UeIY!s1YNuw{SfI~@oQ9HDSa2!`P=$L*;SFRFB5N;c>'
    'dP(t;Nma=?b4;)_Ychzy0uJf_5Ch|5t&(YVrovjMvwwQ~t0|tE0C%e~oXH$F=xb<CaN08Lcm}d0~xLI{GpV{}ioDlRt>?V(aNO{zIO(6Mp->-'
    'bK98L%mfubu*usNBG42L7&%W+B#e5gG{eq7yfKrS}uGtk2rfFI${a<UjYxSV*J+dzUzG5nduf=pC~`Gjq8fR)eb&O;iFyf^=|x0Ir+am^lK%4Z'
    '6AEIpLQi^R~0(93j9^${}1whU&H*+AN6T<a`O9GUcYVi3RXX7e#mr-)#+M&l&u?)-'
    'KJp=pV6yPd}RK}@S^b;BHpoip#l6<ANse~>%H~6E_kVvb!xWWahSZ{cycm+vwBm*i`BgdUsk`ckhpaz@3jJ)t;S#E^M32m@deBiMDerwWgGrvJ'
    '3L$hukFO1%D~}n__>0(bFa@Y>-'
    'YPK^Ap7VQC>y<Da!B5E)L;8Yrs>@m&1+tAc~i5e%JJh#x2wH?6%HT{S~bPklm(%vo!iEs>8H=o#|car4i!iXg#B?Q`EQw9H<|9(ZAi)Uv`nF>7'
    '>51m%Q<i=V25lW%znttN#|>qJ0-'
    'MoQu4^Mc=Q$PFABQ^Ihlay*CnPZKhue@xMjB9#MXx1iifzJ}6_n%dw|DUbkX;Mc3_jU90}90>9PR^Ff|_2)rKxe>K?0;V*|5!-'
    'w+S(YiB@m+^TfxXr*WGg6cF_~M-'
    '??;?NwnQ@Qy>yW=4!;g$IpFHgT$oR$ZA|27k?<2ejXI=Q4PS(HmvL15C`ON0cZQY%&p8<Ym`?_fH>LTo8DdV&f9Oa=C*5VH~fTxY<k1gP;kbFZ'
    'iI%Eg^REocd^0ylAX#P<BTnYa~@v?ApfO)Pe=BW<CbBBn}4{`q*`13G2>I>pU`XJN&j`}^5_%q7ON#|tXr!%-d-S_FReWPsNNaHc?^#<}Y(K-'
    '@~r-h41znDK#JNkTHS~{TH>+WP<ojyM)ehBxGKN;t`3|}Xs_-'
    'cl)3(@cAQ$M@N^K{~gmDp<@<GGgc-+=u_b^dDiHu4X}%p;XBemn6;WjwFk>us%WQaWlMc-_za51_ZJ@b}fkbqD$XA=*;|{tv@zhndej^5yWNxH'
    'r@508FRYem@%5jMU_M4aJkuI(n;L5N}577_Cl9b}$A$M!mjHe;@X7mJS|docsAc(l2^`q<7_)I^mOE;-VqurN)z!`9xcXr*XG>%-'
    'KFKExoXq{N6J7eI<6X23-)XBeHcNmT$53L&`^P$G%G#|D9f^Eqs+T-'
    'g~HPsD#h<^ZW$76V3nVy$=#^9D)xczoYve26so``7ekUtG~54S^glxiLF<(yqwKL+d6vlLwe6>{{_A0I6N`NzF;<wJc525X5WP&^1g%2FGul_`'
    'n$*L8-%k@;HrcCUN3o>a3ARaTj!MN``BpwW-xxU8Ta|v$zpgRs>{{y*6@Do_<sR^-'
    '%LCc)wRfucA%F_@hiK)!ESVM1vuM_zuQMXcRzSLK)hdtjywoI9s&<F^!s6+cZ58^5qRq;?K=A9@M5~q{JrJjY~I=SSy28f9lK0VP3GOD<D+^P_'
    '4{Y?DbYND^vNhVh}JcVr-zs?8bGJ?`+8X6vxm5<8^81kp6T#;1LG;HpRoCJ+kZklF_S#O9C&*H_*u+*E%*6F;Wr;Uigd1cE6TU%J&V!BJHTD!h'
    'oozx`DXd4sD4H7o1i^W{3Clfh%So!j{bjy@j3#ZALTv1AWrPl@@^Uj+s`e7I5Go%PESqNQ)_%9Ua`7v+wW3-+2)DIh-'
    '=5tt<gF)tM|6~X`4S1KlJ<lmR6ssxT~8u>JvN@;l=c>`9bw#rq3UV?`EP)tPXPl`eTXjvmo8Jn)o%}*PY3ZHo_-'
    'c$TMvtjxNTJm*8)9(r;zx)C%Ipz04<7qBr)Fr#b)*tMNAn;lD%R?=bIi1pYsYA36$;9pm@MzdT+{zZyO?j#h6J;l%Q{wr)|p8}W**8#8|(oiK)'
    'f8TGms+3zs(Ktt@`GDv(p;Ok2CyI%OIhu?RB537TT{E_8xY<-E<T?i*r;f<N-'
    'g=pSL`Tiy3GgdI3t9jqG_@52<i%sxJq+8TK+rdLAaq%wfX*d3*f_}60LHpqE1bkQJb#UUNL&RY<wC6DGKFatUgI|t;-'
    '{bJki7$^A^D|aYX?0Il7a%^4>MU)aD4VB|fB8%vWZd_SvU(TU%P4vM5%TxLt~cbD2Z^@_z=f>?==J>>Y#p`w<r9DJ@O^a^hYcqu_uaJhbh7`c<'
    'OOCiuQiu(UWguEir-&}z2?y$YtaP-'
    '=!MOU(^hnIk?*@9{wXD1Ec5zX%in5TE77fyUJ?IRlg~K_9&5P&Vf@k&c>EY~$Z^_pg6Ez9XD7crUaSs5@n*X3s~|i_d}8yymXEXfMAIv_u0wbm'
    '!_G&UM;v87XvFJP^xn}rdp)NgT=j8XFFezYF787AcA}>{sN3xIdOfStvbr6O+cffKv#`T?=#fR_^Ot$urR@);`>*5s0^e^=I4kseT=C2f>}w~_'
    'DdYYX@bF%*qtx#b#1B<o&m@0(2!DSVe|ZGIc9eD<hmTHR$0xx}E&j9i%i~47obKyDj7RkRwAAGOqw>R1U5l-'
    'A)q9Oo&mZxM>~s|TjKDvUA5y+zka%gp>z{PrKCbKW`WNN*KC%AZ@^l@(4qxq#_U%?2F$FwKXZ&-'
    '?lgz_UEb_W;`L$K(<28)Wdd7Dnx@L>d6Ing3^hyc55Y0QwUMhUPS$cIpdiMaouO<#Xh<~baJu5ys3LcL+PNa8EV!yT6!zu82`pe_R*2Sy6X+FP'
    'f^FYG)=j3EPi{3ZNuUP)p)^%8(#dt;I7S-#Dhb^x*NS#x(pOo!CCO+w*E}@IxM><#WOsB7NlYNf(IwY%OmyVc@-'
    'Oi@J=X*V!czikbvYI?tK6+w3ergkXbE~hD7oN8>Zl&nW$PZbbMSNHZ4<z`kqF<}ge}`yKq*F95$K3CzKTh&}Ex$Vj-cG|)XYh09z8r3B9ftWC%'
    'ja93*5V$kr#76}zGCA4G3-'
    '3rH_FD(_K(uI4tYEzoigC{3pT$fJz)EBcQdcuMf}tWAALm6b`fvcIRc}}$^4LTm+g67;chl|xBz=t!h5eEUWs(B_{;X=-'
    'o&_UCI3`JUTTN$`=s$JBd<~c?jn6F{!5^zs;D112%c-'
    'O(<8L!7(9L)eRC3itff7t!0j2{<1Dy8N4$6b%i+cL!_|02`qkzOWv}Dzchn!_jNcgJW$VSFILP*07Jm;j?$JDv{yzXd`hA{R{n5j9ksnfjbh1C'
    'pN7psB-'
    'p%+;{hxu($U%?J^!;>|_gDZQEcH5Fjc=as$02(z02iCl7lpp>w(Zj*f47V8cXQu8{Jj#Lw;#Sa0IsS%udj9<=6OfSBOk}FodDmp_@`5}|1|#TE'
    'cwQByx)23{Q}Rw^!4M$<^{#apOcgOhN<7jUB?RdQJgHlG)8`H6n`?xxJLUf+x)Ywlehg0_5Xga@7B2VdflA-Nf$aO%Kr-'
    '&AMr;$UN3HSSvLP=>jI=hX8C#m`H_X_l%=k7tu9Ksd!6U!G>%))tJ{3PZSis`I%pU1S2_3J!|(UO8wv7TRp8(tdAb_fd4ze$$p5HaC*iMC#Mh_'
    'si)YDqog+Rv56&;5lP-a$%U?fUZ2sT&H&(mHeP1}6|FM1N<X^|&n^AByO1)%sPK2#@wSBsE-'
    '$CkN2KaxpU$^apDgV?>Jzf{<2|f|;bfBL<!Yj6K=5TVdp3lxPP<yA*zfrx5`h5|f%lLj3<C{+$yB?jnk?*%MZbiQThWu)&*UMQvr04JTx?7t+R'
    'R2_yk3GcaVf55dt~-v7I*FgEW!z8W2hWf<KF4#;GjD#8d4o&v;brvK74+1#uManN-h=WDWA10v|6{&RUiq$3-yh2M>k-'
    'aJe7|MeH`(?XvvWl>&I9OK+vlav*Pp3Bd#I1;=6;{>Tb=Ch^3nCKaMuUkMv{~35_I1w_=oAlC$quNd|w|e9$N0}MdSyfd1%?mCdRMO_pg*c*n!'
    '^J34hqWgB3oHsNe4guT@^RBA$x$igf%jbk7NN>q+?K6gW78-Z@KrejdMe0sg#1zVR~rc7^x8h91Ap``-'
    'BOaijK(`FafbrwAV!?@_O#w7P2X^oZ{(W_cBx#}UsA`n-'
    '_*$pF074^Kt=cI!UfzF(cKo0ebhAns}hhh1LxU^>_G(YC*|`g;cBFb5ngz#lBZKdfN9@`$I_`nq}Hax-'
    '>X=y`wXs}g>1`^rUrNP2A_{E+baNvm&Ce;;N(=_qmkaq@5{;jLQQc^aIZCEtFI_FX_fUqqi>#tyFVysPlib>glY;O6Fcj~CM)rdNggQLmfSc#j'
    'ZIk9giq{$ZH<w+JV)gF)Y?L;W$p{Bpmae<nM#{T3o#F@3A|??f+m@O?YD>GpNkmiJM+GX2~ywPU95GiLimDV|%3o>|GbtpR827@v*&eGBo;Hm{'
    'r0IF`cmW#s28$XD(4x+nF=0eGewT~dSJIzn7?jCsZr#6`8>;uL&v27H|ZujiTHyNIs6guc2$JFn87>%`SJ@LM;*^DXiNcmCwKvGu8ncSrpEG0W'
    'fEzNKpKF#c%R_xq6_86sX8^tuE)e@1$>-|OXMx4piu)#~PC2VKNVpQvByq&**r??3wdqSfo#dH~tG?WZ@5e#?cY=Mg_FB44-'
    '6_x%w*^2z_N_j)M(ZY$$f<m-s!r+0eYw&msYeWkB!R$igX_v_I-LJfZJC~@*}@+~LvXSL|<)98@1@Wgp=bb<G~L>=&D{M%LVa19=d_(c77i|5}'
    'a@AF;Y#qePB#<mZS`5CKIksS;(ezp(ykndM%`$QQ|<j11;NA}z6^(^Y=ZgfeP??0xvz7zk}K|ZJ5|E~VC`$p&L*?!V$_jKR)QhH`S{k_=N(c3<'
    'S;-'
    '9sCK9Qcg8C_H8=gQbVP~yp5=!0_n(;lyr(|r=?(rV_94xv{Md)<L>73me(>nX<fjK|5+XBUY3FQR)c<3A%ktLI*aw{9{|b&LMEjs4suj=RV8_y'
    '72~v2_^Yxna+jSiOPG``S80+y7KN6UE2ocWgb7erNkx_IjP1?5YPH6V-34-'
    '#Ur2JDg86zuE5fQie<MipBF*cb>yM`%K>tNOrrx_lr{dSNgemy6-ytMgjV93**1d_pcOgOTDhe_LH-HS)~8=Ghcha>zz#B>bfJ;e;z}BoB#*4e'
    '194qI}0w(<6kd=w@dh$EAYit+I1a%xdFazq4#fNA9r}Kd+^SEzJCC}J^KI0jq!#2`jG1o<w1sgKT5stAa-'
    'y2B@dumqxm0;du)B8ou4TF>hW_%^j=-WQ=h<5CphZh`5(FNBk@?T?+31N`<$Fy|Dxa9K6SIu1M~bm5!t~qU$?0Htnu@SWN#Z8pRLTh7J-'
    '``=!l)Z54*-W@<X<7kJa7EP7ZqAq~f!q=+fix$Vom=@%<Te&pC9}1@gF;@N1WOkE{64Yw+U@@-'
    'R1fzuUCy4*YVLcHc)YKj3~3@lTJ?T~GdK+(=Ik`gxePAB%Wr(DSFVzXA6*>fe6m_xg!zqH|g0A0nLSx^8$VihqRrPV`6z`1}aY+P&UIab&;m(='
    '2}w`620(>CERv^|{imwjb(p`gb+FlTV&~1NhnG`zg!s6%)Udpi6hbPvyRTRs6IM9b@}z*!t8%@XQh7;A7~b6U0}we4ZwLI}2Z&=Xn>I$GF6MT;'
    'ct$p>MClr#JDhk)9Q=-'
    'Nhf@qumdf7kx<oJVK{G27gbmyJzs(vv0+Z>^q8QY~8!%OKhJN^>4rLt1SP~=Xnr2x7W_wv~%*rN8RY1E^zaSc%~Eo(t#gpXB}D_@$pB`%NU+zC'
    '*#S<^9roqQsWlo{dN5UU$-c}kMjN+$94Fz0^+01e80`lt5W+*@n=!pw)9!#ht$6Ze1Ad9--'
    '>6BphJ&)or=vX%g>)dZ=J*6MZ6;3xJ=#ARq{aBiT7^cPi~>JZljOxfb)Ck=KJ`o2i*4&@AViSdjd|M(vD}?;q!0Bi|rq1`}LTA5#RQEe4}yd_j'
    'P1eM<74j`;~o`yTM;K{L%$(qIDqpdj~qW9e!#<7qxqS*Y>p&pWC^yX?|{`czhb~mkTe<qds8~|6j)6SK+VLcwMf>btC<}h5j#s*LU!ooxY!f?L'
    'TOFIop>~@m7`ZTdKbwCa-psd8TMSNVq!9=UK+@JbvvWxV!`|uHX-^VF%a2&rSTvEp*Kt+IN?B-'
    'DmtCfbWO2=MnbtnBPBvAD?1>&$#|MzklJl5kK~m4~hJX?Qd#vu$}L0=Y-h0AUhYr&QrAd1L3#}Jrd~?;}grL2xo1??``OmXx}m6f5`JJ`aZ+Y-'
    'LZXLgoD}mf%){yVt9NxdSo^Il#hSd!0$HEUt1ZkV&9)#^Ax+#r@NUq-UA*ZKcs%B#(x|_XB?s5kD((@kWZ^6u0DhRIETN8@^H%cT}Jm_h4-%0-'
    'W%wmTll5h_^-S0<vs3mA3gREUVDVzeav-'
    'F;Gd`Ht7p8|bK3O+KNsP}_`>Si>|9NaM<4S!z39qbuh%zSqUU$}zG0Tfw>miWPX~FwkIpB;aT|W7mCp`8FTl<#vHXzLZP~swdY@_Z+brV5x$x^'
    'k_<t$>Xazbn4?bVV_!e-'
    '#&A!i%#&J7*R0<w;fxmL}$6oHgpYIQVkAwKb8n0uKo;gk)=cL!INH3g0H=P6L7Z{&Q*ufS2;x%x7o#)@AeYeqNckp|6$tT_Cc@NO#54rv^ancj'
    '`>?!Z@jDC5}_0NgNU%<03=_mW_Wj@;0h4uP;p6!odb=Sf}x94MRUl!Ys(DvJq-|g^xoAh`)`)ss<vsU!VN9q{5To+ls$L7av9fRyNoBo-OUCzd'
    'C=kfPN*v&HZ;3~!`@<aOjMn4Ba_p|dhclf?xwr{20&-P8Ogm)6~M-_Z`h<-'
    'jyKIN$AZ}lFv;5LezZQfArxk&!@GJfhRar<@rZp16fkKQK!y9@8!1Md&u&xh1gJOam$d7mf5gHK)8svXbqYcIgpOWOMqKll<q+2g!n`wZH?{ia'
    '8(9>wx&rc2ZhpWuT|@-H1;cOYD}!&`0OuoXSi4sU#Noc=%Otc`-Rh*#{~XyI`tydBLCNv|wHk1U60SA(Z~;^PhYl}+^9R<19CPj>kFMD_D-'
    '?z4w{*gotq;rnQt9}=J2I>Tc;_XKu)3jR9-'
    '??m%KR<EKs;0ktdjpttnZ#Tj7ZE$&q`Otg#t^3%;190<*{&>uDo)8Z{g}<JmbDv{JFVHhD94ET}EA;a#+STLrY<BLDo!hJSb)z@C@F$-'
    '<Z(?;!dTs}}_(&eM9lzFwUuhu@ZX<r`WSvou@26_(@b#Q=_$<TE9Tm?^hnI8l1M{%=Mew=p<GvFAp6BaY%@0}qw(PACzApwRb`I+<^iR3hZL7W'
    'edCmdwWBc^iz%xgAPLyZSIGjQsokdqf`8a)l8Qfmsch|Vj4dVP;;O90th~j1a{Q)}oA-'
    '{hF{vUJyr(E|8J@lOMe?k28f;j6X`IuMe?N{*dtJGwk)o@{c!SJDR?ZWOqp=UeM8McpH2l=y)=-'
    'YP2yA{3M0)MoUmoY!p<+@4wW610EY(E*>&sBUm6+4^h=N8$1%j(x?U8~i#Xq?s%U#zD;Hqy^q;Pq|XXS<)*EB-0-'
    'eF$y;L0iA7ajEkC60H8#){zNEC%i6Od~=%TokfqH_dLIN^D_2umFHe3p1Mi<Zoy}fUQvJCXFMM;&X3@Y$Kd@5`R=F8n?3_~&(S$Ac-'
    '~9&O@t5e@oWD6IyISRm0fiC{*$)uRO4d%ICWzG9em&6`B%%Y>AhR2TWLY(wvcc6=;r~*ulIT$Q2uPh^R{|U2Kl6H@+;AKugWja_5J6>Lrc(mEB'
    'w3}>CUzMegpn|lb_Ej{w{)tc7T(ezW;`Jcn>;aALAL#4_UpobkY&8(^mUW(7&hf2T}f3?YO|_CH&nLbo(`U;0AcQ3I1<m-'
    '**}3d&KV#z~w{q$Rl|03GI4{zk5bMJm)zt`1?z)f5rQ}!oR)7AHCr@Z&H){l*%4H5x0Kw{hQP;onGH29_sM%Hyt87Ya_mH!B4fY{;=KkjqP`7^'
    '$mjIkk@Bf-'
    'q!Sr>|`qAH4}T8jUCMgPmAF7W%%`#=(9ZHfOXhq0r}L;=*L3rz8Kyu@qNRjGs?+h?8W}~`TAA$!$IFyLptRM<8Yk&pG4Q3Vw}&yJLmBy7tyts;'
    'gPHO)o4CQ{dNm}i}EYdx%aV)2l&B9jPqms<rDDsl=$x%dF|(}Q)Fi^v6ENe={5Ly!}o8{({FhHPTzmW@+21D$ZvO`hd+|f`$*kEJM%nk<YQWil'
    'bXr@wGoGRFz;;q)$8Y~+4=Uif0=kXgZIuRPc{wvn+4wI`Z>^g@5PK$bZ)rDGanvU&;2&i|67Phwt=theqNRBi>v%(1%6|%uS?XpR>4OHx&L9t='
    'P3Ml0v@j=emadlKZ{N}kFK~#ynmT-y9$1ze4L(l8~ogXr|$8)`#dMoE5<9*bx-lr&(N>WvA0O4X#8KnGq1t@YsZPcuY*_WxR0$X?SN-'
    'GsE4t9{71&QoxfY1Tbt_=`R^94YsT-iJ6~D6rT*ym`EQM1w9m5o$@W>y;eBS%&$;N%dGO{!cxEZQumV0_jgDE%`)(i(-'
    'sI<o=)H=3KPdT~o$$bJo>$@Lm8t)u^&tAa?FV)kyF7+2IKlHzao;mse-'
    '7MTVB9W|H@kxVxdvXNJio=w>X*Cl&wX(Jfbo4uzdVN5p3wfMo>x&ny#RkN@prGVtJgf|HSK!?57wa{>$qQCYBK+!c7MdqKl;3%?694B>?khQ_p'
    'Ruf7Ul(;shesgezLf_i~Xj0;iW-zaC9E9okJl0w*AJZ!M`(k&pGt(eC#vI_v`zWymy}Oe=7Y}z;&C+^G5TD@~b6&zUEi+xEhCj=-'
    'LDLt!m$A!`7_|AIGu(ljy5cyw4f@S~QQS@wkk?jPkd_-wpUb(zoJ`d+7csZ)^D#i-'
    'SzB7_V4fMf&~)y!ev#y@F?7V^42rM;&}vM?R(=yw~HG+p+t0uQyS9+NoP;V;;GU`NmfKQw#aqX8cPt`TlmVdlGMSvp&)49frJ4SoWUwm2)g|&>'
    '7S5N3*=HQte#e=la^YGqzu@^#2<8dL4PE=saJWPqaL)okOI4_zv;2?UQWh2nm<Af6r0=e%#kH3nr)G{j=!n^Zf22c6*uUUd4}I=lYxQ*=^qQF8'
    'IAi|2*J+4~Y{WQ@`+p`#<&hLYc!0+WnILdWCL!jqZ6v9RCJAUkA_CgZFyIp`Pp7&=GAu?`QhM_(IRKd~6HxOEd9tGk&GT^Dh=>**t=NH{knX+C'
    'FpY=XC7T&b6NE=jVxkX8ZZAx_%+LZ3*_Y0{pMWp7QZm>(P4~eZM*J$2LD-'
    'MtZpveN;xj+PTh^*!h0&Qw0tW;wPg#uHN$m{awp-r||>l;I#|z&n0-{3if-AalFC!-'
    'J+ehv75W_QIwApP9K4@D8C{d_l(~?N7uXnpD(e?SMbMc{MQ@&T^+i*p1eUl{`)Qd{w?Ft#`w2VU)u^Fw32UWVLqS*{4^66HIwgc!jBogI=n8*@'
    '+-Dp&Grqlx?9<o?JJ+{`zc5V%=Gi+b^rPB|F_xCQsbP*IIhJ`H~7BF`rTIeyNLL62lw5Hzl-'
    'W|)sL0nB&zeb^+UEFm~{6sbj=C$?<ws447fk%^|y*sE)nlth2O3*J~zCMMelJ3opBGpe4qUBL-g+>p7#V@{S^E@19va*yDz~}lur?U-'
    '|*gbyk8ymSkHUEr9a+cpKr0xR`h2p`H&Wmi{-al@Egs{CpE!8O^zqsuiei>vvXce->P4Rd|jmN4<i3z=gj8NAJhF@agD<qU-zv0E`}GDft!{5e'
    'ht^HBfnb!uW$BqX7s+r^k<2m-'
    'z(hiM(^#RpQHI_`Byt1rpEV;lV3fKUO4INn=Owk9G@pXyGZ<f89ZObZm+|uH_<b<!POmbdyn=<^M|Hy#WznpZ>#)Wl!p_KyriFA!CS9s=NtO5j'
    '`r81uinB(Z{fpt@b^3HxrMs7NRLPlME*wO)C3=Vpq{(g<0Ol_ZGF7@CGtbI--hicB>$N1=jB-4lg4od{g+FB&Gq^x`RgU<vq-'
    'mCU5l+}m7Nvf7dG?%LjGRt`*7I)xVm3Cc-TvPYv<k_@N<OJzcujoQO4ysI-{0xJdM4dMNgb3e|HgFUxC-'
    'J;rDLvem6beFC5(k|55%{Jn@M3JqFiLX~#3}^PKj+^m!k(>ovcBgB{fo57dLtdi3F2_~#wt@(#Sc!{0Vz@6G7kX6mAvnBQq4zxIK7f+phRR_f~'
    '7eZOtnuf_Ja6kiYezL@I2@#N(B!*-sIuA7Rz%%ERqW1sWz0}J8hXumn>gVnr$KK8I4f3uPC-hzLQ_B~ZUmx9kSbX~cxBNBf0`~IfllY?K`7x}2'
    '~119^Z_5C$;->42({c{Qax&mKa!*AW7-'
    'M5(cy958<r9Jm~zlZp(NBGev^v6@553>1X;q@i_{R%sI&G^6Z_($VX5C6RdKkx8&@8Fvx`Z$UIY@!aK3A=Bi{^<kbYJBp6@0*El+I)Wv;rEl*#'
    'aKO_?IWe<jiQ5Wy-<dqb1hs>qhDsypR=*gdBnSm;N>XaV(UV5T|VO;t$!A-x8k3-p(CPsB3u6~9<QLkDt-TC;lR#YJ>>gms~?YnqZ9DNDaP>(_'
    'l@dW)X$f|-'
    '&OR_b=r56cHM#}@4)}}u!je<_aVCaG537}zMjF8&uRAy`0Euq`8E9(@rr&|Pn`dj{K{K+>K)HXV#i7Fm*oAL$lErNXZt|B{2o2~o;rsn&$sCNH'
    'sa_GUzccgnRf24emCU%@9I52`~Lp&*V*WjY3Ti#@Z)UWYrgN>uKP!IP_nB$-?zo;6?DHSKPUSwLLcoQF5L+Zqk4bK&*{2^@5iq9uyY-bz{|(bF'
    'DK!TQ;g#o?i=O(g~!X_{3_#co%Y@2dAGU$U2uPo=RTmlkKl#K56NDh!N)Hc=a=x-'
    'EBNU(anc*|FP3+!M@PK{2k&Ti62F*4?<CQ2_Wuu#6ZQWG^vrv7$Om+6v*-'
    'P7UdYxr3%^~y&w}mOA^sd9zP5co()_$o^;b4_H4Pq^3IEN(4@LX7%PyDUmsjFv@)+l}yl1q}k9c@1|1aY2JN#Tc;V_z4)cyC-uTg!A+Fe7O8tG'
    'iMFPbNko<0jM&V&Dp=#9(1Zb<!q9lO2>4x;#3e0`tiK19boqTily-'
    '^dRMuTefueD;d?F^YpsujqGg(N%BpTkq)4B)?1XycGSDLN9(GKl=gue^1`^J@Y{yh_9Q;r?h$<l<k{r`w=QGu>GO>sq-'
    'K5{SR#)E8ACG__lM>r{VW!;ZNuI`b6>lV)V>1#wn_A(Ri)(ecR;^H`71Sc@P@sC@#`C?q)pp_&FhV{<oc5rtfRun<M1!kCVST>G?UUo3r)KdY?'
    '=1-xcim8oKiax-yziR6H8R&$6e7#9NQS`4h(T8U8ZzLsqw9akKQ>8~jxr`Gk7-'
    '?JYX(9lVx=XOq}T3Z6>wyHsjY$ErU+u;0#m#`_!04}D<0P&4_HR`Asho;t|?c6t4#@Zaz2;Pn2se*bfF@_ZcOE}Q(>G<3o&zMtdu+qTcY#%&pV'
    'v=Teb0}t!KVYF|%t!vfqiqV55evYErU5<{}%Q!`Gk>2+p_Fuy|A4PW_=RURA`)P1}j&@w&K9|sySHS-'
    '@{KF0O&@ILznom@_9)RbE*!^STu&6#;eD&P(EYj1jc#qe_g>O8+VtHDP?_1)Fci<@rep9qJ#kiz+-'
    'xRzT`60FYJ>&Zg_`vi`6LsA!o)6YI*}kTqsC%;g+xvZ;we4$X`zG4CTk<>E*v&NTYZl`@hxX3*^Pz>`W#DKfx^4};6V=aswQj-A-&8+DakO-'
    '0Ilte_{q}SJ1Ag9vcp{36Y`+%E=UTnL?Ki0BUcl}zG0xHc3F_~g=!Iw<yvFaI&nHU1Me(z(6B2JfV|-'
    'uGj+gM=EBfmV?^OrRqdc7O{0=*d^oev$3Y?|zhYhs10XsJS_&}WWp83IVz#H$$<2Uhrv)8-'
    'Wx>dz#oqq0&c&v~A4}!N5KNm^%V(0nUx!2MBqICTn`h7m*xEMQ&@M7nP*g9z8y}-}260Qs3*<$P@nlIA$m-'
    '~6o>eu~@Yn7iPBYr*%4;{k~obY`Wgp(+rYx_P4SC{b*QQe%?D@X_5hNq%+tHQ$rpHEaAAH~nIv*+~B3$L@)eIh?(^FeA?J@Za)v72`u{|G-'
    'R;*1nHYJj&I(BlpK{sVcEh-c)V-=k+Ep0WJD`n`p?+2$)dd|wW$-`4vKkOv(0^JX-T>EtKuT-vF=PSN(W)HuzDKNn#i%g|>l@#AZ-yLEnEo}Jq'
    '&yDfybwqq})jPowfy9gJ1iASROBJoBPN6TK15x<{62cF{ZXSn})^h}h`RsURNysv}To4$TXe*G>ux{tj)q<xR@Gm&nw`62OEl<(JlUSk(;c+Wa'
    '`%;taIf#*oCXq-~$m<I6O0KYb1PYwLO3IFgRIjMhj{}0r^yr+KZ8_7vNQol8`{;`!j%SV0}<ze(ZTlYNV=fv9n(6-'
    ';4>}4u;H3R#YjXs@^oh;&gmXY6BiCwMX{UW?5KHJRrZG(rl^ZQaiPf>PIfq%DipZDXhs{A||t8=mQ9W0L4IG(~T&w!Kj<SU|iXxsNm{T<b}2#-'
    '-cuKM{t&v{6^^%x$0g8f8!T-kk8pJ4S)if5yFX4zAe-`DSw@Ky@^L_DJBH-Pg7aNUra%-'
    '0H^P0308XnZ0aEPwi*b+X^^?=3H^=eCiTi|SsK7wAJ54-'
    '#KRakczZCjL4Hd!2z@<f1#~!Ly6N(^C3vrJoON`o+#EGQ0@C+lW85gUeFll``x&+J{?ua6ddyMgJV~eW5g-'
    '#~6obzR32$70%B4Iz{2)3eSt;BKfad{QnN~hEYAP>0FK5W1jyMzw*r2f2dzyGTyK0zc=tgl)p7UB>nl0-'
    'z9m!6#dcwA2#668{nS?bajL0ccnj?JTIsAH<7<LKKX#&jpA*~=c#{fzRA|5MdymkzHQxpv|hyKr-kEe-'
    '>1;#kHiP_z{x`Fc`5v`lHWz~k#tk!j|?xieqMMjWt_^erwYci68(@s|5c&?4*B_IvfpE#cM<MS<42<TB8#K-oGY~Jny-@=|KCFA-'
    '{J4~xIU`K)q6bV{!j5g&$<2u?R<&7yhiW5!Qa)Pf9vtb@A!SBZ!P{&{21|x#-'
    '{=PZUo1TTo=_lslS@h7fn9TsB!+_@wNE(J@ZEIJ#S<4m$E;r*Xv>)vd_=W(|e7fZ|q!@DcH|6#wj{aM8981oVgVHTY-Lz_A8X#7QmmI>7NKMde'
    '2hs7tI6Mx<%Pp!uR*Lb2Vk>NBrCeweuwY;xs&XmON{;{!Hz^g5J7@U%5g2am)AfvA9Thdcb=;q8-'
    'tC5aHrE<NSj6it6M{x5%FB;k_sx5>F@Lr<BJ%#w)^mgcH4QBiA>kChKjjuEpxLW#7^Kw9P-'
    't??m%U#yf@|%lnD9TYa69?XN5x4uH$i<mCBmreoBOskCb*JU9nlTtL4qA+B2i|KyR+Sj&4AaKA|Jnm@Ah@?-~P+^2%LI;wZkdsgG04*9u=vV-'
    'G{_et<}n)aRb{W!#fml)S8+~*p4=_WiDtq&2d?=#*H;GJk*QM~pP+&=g9s<PK;K2i6r<9GF5=cM_#D9>VkNPOD>-'
    'W%YZ2Kc)XoHfFGjo4KS`FvY{*n+=kCLV64{;3%riS&;8=>xjN=C9wgKB+l5S?_6e4z}-'
    'u?TcsU;pn|H(E~a7ktnWKT=#AE{g?f(Cf~Xi`!1lLHq-xwu6NBJ2_I#|lhHm=;;RJxR83r61CEdQx<$3Gmi|A@bI+lxE`Z;tE=v02I{XmL7pXm'
    'W;i>z)S2Pc8`zQ#%&(KfLy}nYs{L0q{$<FJD^XlQ*w?5x2TqWVN$PY<RG@!p5@z0I$a3k;C$bDMKyR@J?tgf<!d`S!YPBk+R-'
    'OT!dCgz))m>2j!-'
    'CZ<aX?2{&Gd90u`>vW_vhzgkoCxvY490afx@|uFvl#!s9Gt9%m)FuC8yJtxj9awtg4z@Di*Q>3A5?;$1a?$SoKfTFC8~dp^L;J4@HG4ttwU4)T'
    '!R0u!dusU-%4A5rsv)D_0MYGL+}{YLs?v8>xcBaXr9RG<rJ6IVMp~|7bhGh@lz@IEQ*&k9u4UJh)>kNjo`M?>+3Afukmb6PU1-'
    'Y*uwrVE#M;ZSC)^FJvMpWgXv=RW0TjDOMi7yS2KXW8zr7kgNLWUBh%r@T;6*gI9d!omh*nA8P9w_S488q89h))yjslrM*HU)UNp{?eqOlnR1L4'
    'y`1z}PujBASE&Y5NKXndWbAj=`%yrRxwC#th`Gec|xx2LczOR3lj(UtPd%}A>^ZIT1<(ItYYxMUUU;knG7WGr4TP!bUc^1p7Sp1{w8|j}2C$iT'
    '@>RMaLyR@=jRIBf!VC&>{eGB>h2si4FX4XSTbrFguKJdHutg~+Q{XT@FKHrzq&PNg6v*5#N=)qa^`#kz}5j?bv&sDrfwEu$i!Y1q^%J0f9O3{;'
    'L*m(uKQAr*wfq$=tr=tB_#GA)`e-7dBH26A)AGrYkMEi&-KN02WgtOax-u3xK;prjwe@xsL?Ym+7JxMRT^tw6W^bLNo9-'
    'P0WUGI3$B;z0DZ`Gd-=%WVrL&htz-$v}Dk?UH0-yYMc>Nl%fh<L}=&l}%Z{glR`nQ@QufBO9g;_VOUo{z-'
    'qJ>YJTdWmu3sZ8u)D*QPMe9!f|DckST&WqM_^3i)yJ%jF7=;zN%kCgI#q+bj#>c0f`T8$p4f!B_L-'
    '{br)nl};;pMwuB(7wyy?<%_EI(B>$zP#;qbn37BT=x)N^w`%a%I`e$eSEAQN;rt-'
    '6|D|RIF0I`#7EKmkovm;d^QkoH{#bCdH+W8fQ`g=jpTRQSU2AWKScXJ$sa`P1*{HJ{N2L!E$G)~{7n<}Gfkc^7XIIRy|3wCJ6}z9HtIS?xQfm%'
    '()-Nyx=dRiARMnEUdX54*892u@pm-eX!8N$<ud$tgcmz!-s-'
    '!pjzRrn=R6;0JZtfXXBd}r;5n*~vUvd8A4>Lr3%<I84!_6u55UbsUnipHKLzK{8NV0c;uZIQjXtSEpVq@?Z@vCjJec%(XTyuGYvB2f*ij??xe?'
    'xK#Qqvnll#Vrf7*QgqUCFCor&&ibquZ4wY2y?49aIV<9C|DQ<L+G#^XJ8FwM*}bo%~@icdz!>!o8K*|cwl&sXcc7NXaedR>F<AEo|Wk51m?=g@'
    '0>i?RO_&+qCvk$y3}=>OIHy@u<L;^&TIm$l&N4DC4Q`?&~*m*I=6@W^%F$3?%p!)H`?DV-GM>11zD(R0szpB9@hvN+n-'
    'uL|e&Uf*x?MB>5Jx8lX(Xp4(9{*BmA#4EyGBmLZlK5g^;!i)zDH^w)nbEKD|^=snm7S_o&GhY<tYivGK_F{DtwqHyyIJ5Nwk?xi5m`;0VGwutp'
    '&!yPYN_b}tx??@Ox(U15N?cM5|CBIJ(f%%m7dvlW{ZP%g*T6?d;inURK9O*AhJHN9eDp=eIa)_=^G3G+w(fU_cHSdz6XkW~w;p5vPkkRk@!Jc}'
    'yU6}tqhsp8Z4?)&JxO#&l79U*cv1Tr(RGn-'
    'k#1^)&l~ZJZN$fI#KCRUsk9L<M}A6t@om<#8PAvww)#!+mc>UOz}I_UH*5P@**R&_!Jo<hWTD%pV^6br&jr}+5}y~a^U?IVp7=I8cTxVK7~GZc'
    '_b9(ByNvK+>!gMA8b5!=_Fs@5sAas*VE5;UYc9f5m+>!GeLolZ>1f_a_I!`~JfK~V81Ki#>rZ`Mk<CY|y|3WgXnmsEQP1<<!8=j@Uv`i}_kRbx'
    'SUhBYNdBZTHM!4^t*6)cw-N8OG0)hBK5e7^rPbF_+d4PP+o=7~`ZkN3)ZPd$rk`!UZ~5Or>Z-=c+hlp&o$Mo*cF#xWErCB)(9dhI-'
    '{@Rd;c6@PSIqrNe12Nbi}EjD#f$ClA{^TJ@+XMPYJEL`;-'
    'Yitt&8x&W!iVu&kYgoZo!Lph+FUZKDp}WXkQM+Q%~W?=jfD|*#9eE|1AAj=j)wypLgj0B>E}ob(I!Rn|?98SbpxScoCm8Vz2F9$0Gc;Q{U1?eP'
    '$bRO&fIxZOj|kzJ;ym*%owjOLB5ulish{*DWdk*90Fm`8gA|U$pFFEIGOU-'
    'p;3yJ?DD;l*WGvdDj*6?;84VJ^DD>M@qV@7=K*i>y8xvM0hd%@>RT89j5%}3F56<zK`}rwYnGEKUX|)6&&B-'
    '`e?nYtsAj@{cT;e%^QiYpTcv|IyBkcE8?~{#9?*lm1rH2)%#nWi{3Mer~fd#sGlvL8{x(Fa}htayPq)sWc#!0K5fa#_15wut)5pA4x@Pmo39o>'
    'NAs5&hbI5O?PF#2;kM6|uFItVrlDJMdEfcI52pBf1^8IQd#}f?H!^NpvHN23z25;Z#xJsyYV7vg;6=Pu3oo4U^UtI+F8cWph8M*%H@N;5IJtuk'
    'xd+cYK-WB?ebN3<HgBYHj_O^+TM=F~ZuQttG#_pA0P+{#1z!FyP)h*<Edwn8000O8001EXJe&9E5di=I;B5c^3IG5A0000000000fB^si003!X'
    'Z*^{DE^csnP)h*<Edwn8000O8001EXL*yrsHUa<uK-'
    '&NS2LJ#70000000000fB{Vb004Ava4v3ec~DCM0xbhA000080000X0N5f#qDBG$06^OS015yA00000000000Du9!0{{SGZ*+8TZ7yzbc~DCM0x'
    'bhA000080000X0N+qA8N2`h06^OS00;m800000000000Du8L1^@tabaHeqZg6=}O928c11$gm00;m803iVM_wyF&0000$+W-'
    'It00000000000001h0W=2y0BCD2Zg6=}O928c11$gm00;m803iU{oi<bJ0000$+W-'
    'Iu00000000000001h0ageA0CsC(E^csnP)h*<Edwn8000O8001EX#X&}hoCN>?fD!-'
    'z5C8xG0000000000fB||5004JoY;0e1Z*_8GWpgfWaCuNm0Rk-pEdT%j2mk;8ApkbYAVF{l000mi000R90000000000004jiSPuXIa%pyDaxQL'
    'gc~DCM0xbhA000080000X06~(VaOD610N4ir01N;C00000000000Du7l7ytleVRLj}V`yY9Zg6=}O928c11$gm00;m803iTFCCLfEMgRan+W-'
    'Iz00000000000001h0VWv$0BB`lWM6V+W-e}Uc~DCQ1^@s6015yK04)Ll03=`l0000'
)


# =============================================================================
# 1. REFERENCE DATA (embedded archive above; immutable on retrieval)
# =============================================================================
@lru_cache(maxsize=1)
def reference():
    payload = base64.b85decode(REFERENCE_B85)
    with np.load(io.BytesIO(payload), allow_pickle=False) as archive:
        a = {name: np.array(archive[name]) for name in archive.files}
    assert a['ibound'].shape == (100, 70)
    assert a['well_sources'].shape == (144, 4)
    assert a['river'].shape == (147, 6)
    assert a['east_chd'].shape == (47, 5)
    return a


# =============================================================================
# 2. MODEL, SOLVER AND PARTICLE INPUT DATA
# =============================================================================
@dataclass(frozen=True)
class Well:
    """User-facing one-based MODFLOW row/column."""
    row: int
    col: int
    enabled: bool = True


# Existing map coordinates map to these original row/column centers.
WELL_CELLS = ((47, 26), (51, 25), (56, 24))


@dataclass(frozen=True)
class Options:
    pump_on: bool = False
    pump_per_well_m3_day: float = 3000.0
    wells: tuple[Well, ...] = tuple(Well(r, c) for r, c in WELL_CELLS)
    kh_m_s: float = BASE_K
    keep_lake: bool = True
    recharge_mm_year: float = BASE_RECHARGE
    bedrock_multiplier: float = 1.0
    chd_head_m: float = DEFAULT_EAST_CHD_HEAD
    river_cper_m_m_s: float = BASE_C_PER_M


@dataclass(frozen=True)
class SolverSettings:
    """NWT tolerances expressed in human-friendly units for the UI.

    MODFLOW model time is seconds, so convert the specified m³/day
    FLUXTOL to m³/s exactly once when constructing the solver package.
    HCLOSE/RCLOSE are legacy labels; NWT parameters are HEADTOL/FLUXTOL.
    """
    headtol_m: float = 1e-3
    fluxtol_m3_day: float = 500.0
    maxiterout: int = 500
    complexity: str = 'COMPLEX'
    linear_method: str = 'GMRES'


def stable_signature(opts: Options, solver: SolverSettings, executable: str) -> str:
    """Stable across Streamlit re-runs and dataclass class redefinitions.

    Comparing saved dataclass instances directly is incorrect in Streamlit:
    the script reload creates a *new class* with different type identity.
    """
    return json.dumps({'model': asdict(opts), 'solver': asdict(solver),
                       'executable': str(executable).strip()},
                      sort_keys=True, separators=(',', ':'), allow_nan=False)


def particle_signature(settings, executable: str) -> str:
    return json.dumps({'particle': asdict(settings),
                       'executable': str(executable).strip()},
                      sort_keys=True, separators=(',', ':'), allow_nan=False)


@dataclass(frozen=True)
class ParticleOptions:
    """MODPATH configuration; deliberately independent of flow inputs."""
    sources: tuple[str, ...] = ('River',)
    porosity: float = 0.25
    # Exact number of particles per source cell (not subdivisions per side).
    well_particles_per_cell: int = 10
    river_particles_per_cell: int = 1
    max_river_cells: int = 35


def log_slider(st, label, *, minimum, maximum, default, key, help=None):
    """Physical-unit values with logarithmically spaced slider positions.

    The exact baseline is inserted to avoid modifying model parameters on load.
    """
    values = np.logspace(np.log10(minimum), np.log10(maximum), 101)
    values = tuple(sorted(set(float(v) for v in values) | {float(default)}))
    return float(st.select_slider(label, options=values, value=float(default),
                                  format_func=lambda value: f'{value:.2e}',
                                  help=help, key=key))


def cell_of(east_km, south_km):
    """Map east/south coordinate -> rotated MODFLOW zero-based (row,col)."""
    east, south = float(east_km) * 1000.0, float(south_km) * 1000.0
    if not (0 <= east < WIDTH and 0 < south <= HEIGHT):
        raise ValueError('Well outside model domain: 0 <= east < 10 km, 0 < south <= 7 km.')
    row = int(np.floor(east / DX))
    col = int(np.floor((HEIGHT - south) / DX))
    return row, min(69, max(0, col))


def xy_of(row, col):
    """Centre coordinates in figure reference system (metres)."""
    return (float(row) + .5) * DX, -HEIGHT + (float(col) + .5) * DX


def split_boundaries():
    """Extract disjoint boundary groups using archived CHD locations.

    Original: 144 WEL inflow records; 47 eastern cells overlap CHD locations,
    97 other records form the western/northwestern bedrock-inflow boundary.
    Eight of the latter are in inactive cells and are omitted from new SPD.
    """
    a = reference()
    chd = a['east_chd']
    well_src = a['well_sources']
    east_cells = set((int(q[1]), int(q[2])) for q in chd)
    eastern = np.array([q for q in well_src if (int(q[1]), int(q[2])) in east_cells])
    bedrock_all = np.array([q for q in well_src if (int(q[1]), int(q[2])) not in east_cells])
    bedrock = np.array([q for q in bedrock_all if a['ibound'][int(q[1]), int(q[2])] > 0])
    assert (len(eastern), len(bedrock_all), len(bedrock)) == (47, 97, 89)
    assert all((int(q[1]), int(q[2])) in east_cells for q in eastern)
    return eastern, bedrock_all, bedrock


def pumping_cells(opts: Options):
    if not opts.pump_on or opts.pump_per_well_m3_day <= 0:
        return []
    return [(int(w.row)-1, int(w.col)-1) for w in opts.wells if w.enabled]

def validate_options(opts: Options):
    a = reference()
    if opts.kh_m_s <= 0 or opts.kh_m_s > 1:
        raise ValueError('Hydraulic conductivity must be positive and <= 1 m/s.')
    if not (0 <= opts.recharge_mm_year <= 3000):
        raise ValueError('Recharge must be between 0 and 3000 mm/year.')
    if not (0 <= opts.bedrock_multiplier <= 5):
        raise ValueError('Bedrock inflow multiplier must be between 0 and 5.')
    if not (360 <= opts.chd_head_m <= 385):
        raise ValueError('Eastern CHD head is outside the configured range.')
    if not (0 < opts.river_cper_m_m_s <= 0.1):
        raise ValueError('River conductance per length must be > 0 and <= 0.1 m/s.')
    _, _, bedrock = split_boundaries()
    forbidden = set((int(q[1]), int(q[2])) for q in a['east_chd'])
    forbidden.update((int(q[1]), int(q[2])) for q in a['river'])
    forbidden.update((int(q[1]), int(q[2])) for q in bedrock)
    selected = pumping_cells(opts)
    for w in opts.wells:
        if not (1 <= w.row <= 100 and 1 <= w.col <= 70):
            raise ValueError(f'Well position row {w.row}, column {w.col} is outside the grid.')
    if not (0 <= opts.pump_per_well_m3_day <= 30000):
        raise ValueError('Pumping must be between 0 and 30,000 m³/day per well.')
    for i, j in selected:
        if a['ibound'][i, j] == 0:
            raise ValueError(f'Active well at row {i+1}, column {j+1} is in an inactive cell.')
        if a['hk'][i, j] > 1:
            raise ValueError(f'Active well at row {i+1}, column {j+1} is inside the high-K lake.')
        if (i, j) in forbidden:
            raise ValueError(f'Active well at row {i+1}, column {j+1} overlaps an inflow, CHD or river cell.')
    if len(selected) != len(set(selected)):
        raise ValueError('Two pumping wells occupy the same model cell.')
    return True


# =============================================================================
# 3. FLOW MODEL: boundary stress data, conductivity, input creation
# =============================================================================
def make_stress_data(opts: Options):
    """Generate one-period WEL (bedrock+pumps), RIV and CHD inputs.

    Arrays are copies: user control changes cannot corrupt embedded data.
    WEL and RIV fluxes use m3/s and river conductance m2/s.
    """
    validate_options(opts)
    a = reference()
    _, _, bedrock = split_boundaries()
    bedrock = bedrock.copy()
    bedrock[:, 3] *= opts.bedrock_multiplier
    pumps = np.array([[0, i, j, -opts.pump_per_well_m3_day / SEC_DAY]
                      for i, j in pumping_cells(opts)], dtype=float).reshape(-1, 4)
    wells = np.vstack([bedrock, pumps])
    river = a['river'].copy()
    river[:, 4] *= opts.river_cper_m_m_s / BASE_C_PER_M
    chd = a['east_chd'].copy()
    chd[:, 3:5] = opts.chd_head_m
    return wells, river, chd


def conductivity_arrays(opts: Options):
    a = reference()
    hk = np.full((100, 70), opts.kh_m_s)
    vk = hk * .1  # preserved original Kv/Kh ratio
    if opts.keep_lake:
        is_lake = (a['ibound'] > 0) & (a['hk'] > 1.0)
        hk[is_lake] = a['hk'][is_lake]
        vk[is_lake] = a['vka'][is_lake]
    return hk, vk


def make_flow_model(opts: Options, workspace: Path, executable: str = 'mfnwt',
                    initial_heads=None, solver: SolverSettings | None = None):
    import flopy
    solver = solver if solver is not None else SolverSettings()
    if not (0 < solver.headtol_m <= 1.0 and 0 < solver.fluxtol_m3_day <= 1e7
            and 10 <= solver.maxiterout <= 10000
            and solver.complexity in ('SIMPLE', 'MODERATE', 'COMPLEX')
            and solver.linear_method in ('GMRES', 'XMD')):
        raise ValueError('Invalid MODFLOW-NWT solver settings.')
    a = reference()
    workspace.mkdir(parents=True, exist_ok=True)
    wells, river, chd = make_stress_data(opts)
    hk, vk = conductivity_arrays(opts)
    mf = flopy.modflow.Modflow(modelname='fieldcase', model_ws=str(workspace),
                              version='mfnwt', exe_name=executable)
    flopy.modflow.ModflowDis(
        mf, nlay=1, nrow=100, ncol=70, nper=1,
        delr=100.0, delc=100.0, top=a['top'], botm=a['bottom'][np.newaxis],
        perlen=[SEC_YEAR], nstp=[1], tsmult=[1], steady=[True],
        itmuni=1, lenuni=2)
    # Use the original unpumped solution only as a numerical starting guess;
    # active CHD cells are initialized to their specified head.
    initial = np.where((a['ibound'] > 0) & np.isfinite(a['head_ref']) &
                       (a['head_ref'] > a['bottom'] + .001) &
                       (np.abs(a['head_ref']) < 1e10), a['head_ref'], 373.0)
    initial = initial.copy()
    if initial_heads is not None:
        candidate = np.asarray(initial_heads, dtype=float)
        if candidate.shape != initial.shape:
            raise ValueError('Continuation initial heads have an unexpected shape.')
        usable = ((a['ibound']>0) & np.isfinite(candidate) &
                  (np.abs(candidate)<1e10) & (candidate>a['bottom']+1e-3))
        initial[usable] = candidate[usable]
    for row in chd:
        initial[int(row[1]), int(row[2])] = opts.chd_head_m
    flopy.modflow.ModflowBas(mf, ibound=a['ibound'][np.newaxis],
                             strt=initial[np.newaxis], hnoflo=-2e20)
    flopy.modflow.ModflowUpw(
        mf, laytyp=[1], layavg=[0], chani=[-1], layvka=[0], laywet=[0],
        hk=hk[np.newaxis], hani=np.ones((1, 100, 70)),
        vka=vk[np.newaxis], ss=1e-5, sy=0.2, ipakcb=53, hdry=-1e30)
    # Eastern boundary is exclusively CHD: NO positive WEL entries here.
    flopy.modflow.ModflowChd(mf, stress_period_data={0: chd.tolist()})
    flopy.modflow.ModflowWel(mf, stress_period_data={0: wells.tolist()}, ipakcb=53)
    flopy.modflow.ModflowRiv(mf, stress_period_data={0: river.tolist()}, ipakcb=53)
    flopy.modflow.ModflowRch(mf, nrchop=1,
                             rech=opts.recharge_mm_year / 1000.0 / SEC_YEAR, ipakcb=53)
    flopy.modflow.ModflowOc(mf, stress_period_data={(0, 0):
        ['save head', 'save budget', 'print budget']}, compact=True)
    # MODFLOW-NWT uses HEADTOL [m] and FLUXTOL [m³/s], not the PCG
    # HCLOSE/RCLOSE keywords. The UI deliberately presents FLUXTOL in m³/day.
    # 500 m³/day = 0.005787037037 m³/s. This is a loose diagnostic DEFAULT,
    # not an assurance of mass-balance accuracy. Always check the listing.
    # `options` presets provide their own linear solver parameters; changing
    # MAXITINNER here without SPECIFIED would not alter the preset settings.
    flopy.modflow.ModflowNwt(
        mf, headtol=solver.headtol_m,
        fluxtol=solver.fluxtol_m3_day / SEC_DAY,
        maxiterout=solver.maxiterout,
        linmeth=1 if solver.linear_method == 'GMRES' else 2,
        iprnwt=2, options=solver.complexity)
    # Original grid is rotated 90 degrees to align with map; all plotting
    # converts grid model coordinates to local east/north drawing coordinates.
    mf.modelgrid.set_coord_info(xoff=10000.0, yoff=-7000.0, angrot=90.0)
    mf.write_input()
    return mf


def _budget_arr(cbc, text):
    """Read the complete spatial CBC term, preserving 2-D or 3-D records.

    MODFLOW CBC records differ by storage method (IMETH). In particular,
    recharge may be returned directly as a 2-D (nrow,ncol) array, while
    node-based terms may be (1,nrow,ncol). Unconditionally indexing [0]
    silently retained *only the first recharge row* in Version 6.
    """
    found = [item.strip().upper() for item in cbc.get_unique_record_names(decode=True)]
    if text.upper() not in found:
        raise RuntimeError(f'Missing binary-budget term {text!r}; found: {found}')
    records = cbc.get_data(kstpkper=(0, 0), text=text, full3D=True)
    if len(records) != 1:
        raise RuntimeError(f'Expected one CBC record for {text}: got {len(records)}')
    values = np.asarray(np.ma.filled(records[0], 0.0), dtype=float)
    expected = reference()['ibound'].shape
    if values.ndim == 3 and values.shape[0] == 1:
        values = values[0]
    if values.shape != expected:
        raise RuntimeError(f'CBC {text!r} must cover the entire {expected} grid; '
                           f'got {values.shape}. Refusing partial budget data.')
    if not np.all(np.isfinite(values)):
        raise RuntimeError(f'Nonfinite spatial CBC values in {text!r}.')
    return values


def signed_rates(arr):
    """Positive inflow and positive outflow, in MODEL units m³/s."""
    values = np.asarray(arr, dtype=float)
    return (float(np.maximum(values, 0).sum(dtype=np.float64)),
            float(-np.minimum(values, 0).sum(dtype=np.float64)))


def listing_budget(workspace):
    """Read the *last incremental rate* (NOT cumulative volumes) from LIST.

    MfListBudget reports rates in model m³/s, even though the period length is
    one year; convert only at presentation time. All terms must be present.
    """
    import flopy
    path = workspace / 'fieldcase.list'
    if not path.exists():
        alt = workspace / 'fieldcase.lst'
        if alt.exists():
            path = alt
    if not path.exists():
        raise FileNotFoundError(f'No MODFLOW listing file in {workspace}')
    incremental, _ = flopy.utils.MfListBudget(str(path)).get_dataframes()
    if incremental.empty:
        raise ValueError('No incremental volumetric-budget records found in listing.')
    row = incremental.iloc[-1]
    # Strip punctuation/spacing and normalize common spelling conventions.
    import re
    data = {re.sub(r'[^A-Z0-9]+', '_', str(k).upper()).strip('_'): float(v)
            for k, v in row.items()}
    def require(name):
        if name not in data or not np.isfinite(data[name]):
            raise ValueError(f'Listing lacks {name}. Available terms: {sorted(data)}')
        return data[name]
    labels = {'CHD':'CONSTANT_HEAD', 'RIV':'RIVER_LEAKAGE',
              'RCH':'RECHARGE', 'WEL':'WELLS'}
    packages = {key: (require(f'{token}_IN'), require(f'{token}_OUT'))
                for key,token in labels.items()}
    return {'packages': packages, 'total_in': require('TOTAL_IN'),
            'total_out': require('TOTAL_OUT'),
            'percent_discrepancy': require('PERCENT_DISCREPANCY'),
            'path': str(path)}


def assemble_budget(raw, opts, listing):
    """Build the *displayed* component budget from MODFLOW LIST rates.

    CBC provides spatial data and WEL cell diagnostics, NOT authoritative
    gross IN/OUT totals. In CHD cells, flows through individual faces can
    have opposite signs. The net cell-wise CBC flow cannot recover those
    separate gross inflow/outflow contributions shown by MODFLOW LIST.

    The WEL input in this model is disjoint by sign: positive entries ONLY
    represent bedrock inflow; negative entries ONLY represent pumping. Thus
    LIST's WEL IN and OUT identify these components without an uncertain
    reconstruction from net cell exchanges.
    """
    _, _, bedrock = split_boundaries()
    wel = raw['WEL']
    rock = np.zeros_like(wel)
    pump = np.zeros_like(wel)
    for rec in bedrock:
        i, j = int(rec[1]), int(rec[2])
        rock[i, j] += wel[i, j]
    for i, j in pumping_cells(opts):
        pump[i, j] += wel[i, j]
    if not np.allclose(rock + pump, wel, rtol=1e-5, atol=1e-9):
        raise RuntimeError('WEL CBC cannot be reconciled to bedrock and pumping records.')
    if np.any(rock < -1e-12) or np.any(pump > 1e-12):
        raise RuntimeError('WEL source signs differ from the expected bedrock/pumping setup.')

    packages = listing['packages']
    # All five rows are derived from LIST. This fixes the earlier presentation
    # error: 2-D RCH had been reduced to the first row, and CHD gross IN/OUT
    # had been replaced with incomplete net-cell CBC aggregations.
    groups = (
        ('Eastern CHD', *packages['CHD']),
        ('Bedrock inflow (WEL)', packages['WEL'][0], 0.0),
        ('Areal recharge (RCH)', *packages['RCH']),
        ('River exchange (RIV)', *packages['RIV']),
        ('Pumping (WEL)', 0.0, packages['WEL'][1]),
    )
    rows = [{'Component': label, 'In (m³/day)': qin * SEC_DAY,
             'Out (m³/day)': qout * SEC_DAY,
             'Net (m³/day)': (qin - qout) * SEC_DAY}
            for label, qin, qout in groups]

    checks = []
    for key in ('CHD', 'RIV', 'RCH', 'WEL'):
        cbc_in, cbc_out = signed_rates(raw[key])
        lst_in, lst_out = packages[key]
        gross_difference = max(abs(lst_in-cbc_in), abs(lst_out-cbc_out))*SEC_DAY
        net_difference = abs((lst_in-lst_out)-(cbc_in-cbc_out))*SEC_DAY
        # For CHD, compare NET cell exchanges with LIST: gross signed face
        # contributions can legitimately cancel before entering the CBC grid.
        critical_difference = net_difference if key == 'CHD' else gross_difference
        checks.append({'Package': key, 'LIST IN (m³/s)': lst_in,
                       'CBC IN (m³/s)': cbc_in, 'LIST OUT (m³/s)': lst_out,
                       'CBC OUT (m³/s)': cbc_out,
                       'Gross difference (m³/day)': gross_difference,
                       'Net difference (m³/day)': net_difference,
                       'Max difference (m³/day)': critical_difference,
                       'Comparison': 'NET (gross face flows can cancel)' if key == 'CHD'
                                     else 'IN/OUT'})
    total_cbc_in = sum(signed_rates(raw[key])[0] for key in raw)
    total_cbc_out = sum(signed_rates(raw[key])[1] for key in raw)
    total_in = listing['total_in'] * SEC_DAY
    total_out = listing['total_out'] * SEC_DAY
    calc_percent = (200*(total_in-total_out)/(total_in+total_out)
                    if total_in+total_out else 0.0)
    return {'rows': rows, 'checks': checks, 'listing': listing,
            'listing_total_in_m3day': total_in,
            'listing_total_out_m3day': total_out,
            'cbc_total_in_m3day': total_cbc_in*SEC_DAY,
            'cbc_total_out_m3day': total_cbc_out*SEC_DAY,
            'computed_discrepancy': calc_percent}


# =============================================================================
# 4. WATER BUDGET: LIST is authoritative; CBC subdivides WEL inflows/outflows
# =============================================================================
class BudgetDiscrepancyError(RuntimeError):
    """A converged flow run has an unacceptable LIST mass-balance error.

    Preserve the calculated budget for display even though the model results
    must NOT be exposed as valid postprocessing output.
    """

    def __init__(self, budget: dict):
        self.budget = budget
        percent = float(budget['listing']['percent_discrepancy'])
        super().__init__(
            f'Listing-file water-budget discrepancy is {percent:+.3f}%, '
            f'exceeding the allowed ±{MAX_BUDGET_DISCREPANCY_PERCENT:g}%. '
            'Simulation results were rejected.'
        )


def listing_budget_text(workspace: Path) -> str:
    """Return the final MODFLOW volumetric-budget block *verbatim* from LIST.

    Keep original units/precision and the adjacent cumulative-volume columns;
    the full LIST remains in the rejected run directory for troubleshooting.
    """
    path = Path(workspace) / 'fieldcase.list'
    if not path.is_file():
        path = Path(workspace) / 'fieldcase.lst'
    if not path.is_file():
        return 'No MODFLOW listing file is available.'
    text = path.read_text(encoding='utf-8', errors='replace')
    marker = 'VOLUMETRIC BUDGET FOR ENTIRE MODEL'
    start = text.rfind(marker)
    if start < 0:
        return 'No volumetric budget block was found in the listing file.'
    # Start at the printed header rather than at the file's beginning.
    end_marker = 'PERCENT DISCREPANCY'
    end = text.find(end_marker, start)
    if end < 0:
        return text[start:start + 5000]
    end = text.find('\n', end)
    return text[start:end if end >= 0 else len(text)].rstrip()


def read_budget(opts: Options, workspace: Path):
    import flopy
    cbc = flopy.utils.CellBudgetFile(str(workspace / 'fieldcase.cbc'), precision='auto')
    try:
        raw = {'CHD': _budget_arr(cbc, 'CONSTANT HEAD'),
               'RIV': _budget_arr(cbc, 'RIVER LEAKAGE'),
               'RCH': _budget_arr(cbc, 'RECHARGE'),
               'WEL': _budget_arr(cbc, 'WELLS')}
    finally:
        cbc.close()
    lst = listing_budget(workspace)
    return assemble_budget(raw, opts, lst), raw

def _read_heads(workspace):
    import flopy
    hds = flopy.utils.HeadFile(str(workspace / 'fieldcase.hds'))
    try:
        return np.asarray(hds.get_data(kstpkper=(0, 0))[0])
    finally:
        hds.close()


def run_flow(opts: Options, workspace: Path, exe: str,
             solver: SolverSettings | None = None):
    """Try direct NWT solution; if needed, ramp pumping with head continuation.

    Only the exact requested final pumping scenario is returned. Intermediate
    continuation stages are separate workspaces and never used for accounting.
    """
    solver = solver if solver is not None else SolverSettings()
    mf = make_flow_model(opts, workspace, exe, solver=solver)
    success, log = mf.run_model(silent=True, report=True)
    full_log = list(log)
    if not success and pumping_cells(opts):
        previous = None
        # Small initial pumping increment encourages stable Newton convergence.
        # Five intermediate solutions are computed only when the direct run fails.
        for idx,fraction in enumerate((.10,.25,.45,.70,1.0)):
            step_opts = replace(opts,
                pump_per_well_m3_day=opts.pump_per_well_m3_day*fraction)
            step_ws = workspace if fraction == 1.0 else workspace / f'_ramp_{idx+1}'
            mf_step = make_flow_model(step_opts,step_ws,exe,initial_heads=previous,
                                      solver=solver)
            stage_success,stage_log = mf_step.run_model(silent=True,report=True)
            full_log.append(f'Continuation stage {idx+1}: {fraction:.0%} pumping; '
                            f'success={stage_success}')
            full_log.extend(stage_log[-10:])
            if not stage_success or not (step_ws/'fieldcase.hds').is_file():
                success = False
                break
            previous = _read_heads(step_ws)
            if fraction == 1.0:
                mf,success = mf_step,True
    if not success:
        raise RuntimeError('MODFLOW-NWT did not converge.\n'+ '\n'.join(full_log[-45:]) +
                           '\nNonconvergence may arise from linear-solver stagnation, '
                           'strong conductivity contrasts or dewatering. '
                           'Inspect the listing-file flux residual and budget '
                           'before changing tolerances.')
    if not (workspace / 'fieldcase.hds').is_file() or not (workspace/'fieldcase.cbc').is_file():
        raise RuntimeError('Model terminated but HDS/CBC files were not created.')
    heads = _read_heads(workspace)
    budget,raw = read_budget(opts,workspace)
    if not np.any(np.isfinite(heads) & (np.abs(heads)<1e10)):
        raise RuntimeError('No valid simulated hydraulic heads.')
    if abs(budget['listing']['percent_discrepancy']) > MAX_BUDGET_DISCREPANCY_PERCENT:
        raise BudgetDiscrepancyError(budget)
    return mf,heads,budget,raw,full_log


# =============================================================================
# 5. MODPATH: release locations, independent reruns and pathline coordinates
# =============================================================================
def select_river_release_cells(raw_riv, max_cells: int):
    a = reference()
    # RIV flow to aquifer is positive. Backward tracking is meaningful from
    # gaining river cells where groundwater discharges (RIV budget < 0).
    candidates = sorted({int(r[1]) * 70 + int(r[2]) for r in a['river']
                         if raw_riv[int(r[1]), int(r[2])] < -1e-12
                         and a['ibound'][int(r[1]), int(r[2])] > 0})
    if len(candidates) > max_cells:
        indexes = np.linspace(0, len(candidates) - 1, max_cells, dtype=int)
        candidates = [candidates[int(i)] for i in indexes]
    return candidates


def particle_ring_offsets(count: int, radius: float = 0.25):
    """Return exactly ``count`` well-cell release points (local x/y in [0,1]).

    A single particle starts at the cell center; for >=2, points are evenly
    spaced on a circle entirely *inside* the model cell.  The same compact
    distribution is used for river cells when users request >1 particle.
    """
    if not 1 <= int(count) <= 20 or int(count) != count:
        raise ValueError('Particle count must be an integer between 1 and 20.')
    if not 0 < radius < 0.5:
        raise ValueError('Ring radius must lie strictly inside the cell.')
    if count == 1:
        return [(0.5, 0.5)]
    return [(0.5 + radius * math.cos(2 * math.pi * k / count),
             0.5 + radius * math.sin(2 * math.pi * k / count))
            for k in range(count)]


def particle_release_groups(settings: ParticleOptions, opts: Options, raw: dict):
    """Build explicit release points for each source, without using FloPy.

    Returns (source, partlocs, localx, localy) for each *nonempty* source.
    partlocs use zero-based (layer, row, column) for the structured 1-layer
    MODFLOW-NWT grid; local coordinates are relative to each cell.
    """
    if not set(settings.sources).issubset({'River', 'Wells'}):
        raise ValueError('Unknown particle release source.')
    if not (0 < settings.porosity < 1
            and 1 <= settings.well_particles_per_cell <= 20
            and 1 <= settings.river_particles_per_cell <= 5
            and 1 <= settings.max_river_cells <= 147):
        raise ValueError('Invalid particle tracking settings.')

    groups = []
    if 'Wells' in settings.sources:
        well_cells = pumping_cells(opts)
        if well_cells:
            offsets = particle_ring_offsets(settings.well_particles_per_cell)
            cells = [(0, i, j) for i, j in well_cells]
            locs = [cell for cell in cells for _ in offsets]
            xs = [x for _ in cells for x, y in offsets]
            ys = [y for _ in cells for x, y in offsets]
            groups.append(('Wells', locs, xs, ys))
    if 'River' in settings.sources:
        nodes = select_river_release_cells(raw['RIV'], settings.max_river_cells)
        if nodes:
            offsets = particle_ring_offsets(settings.river_particles_per_cell)
            cells = [(0, *divmod(int(node), 70)) for node in nodes]
            locs = [cell for cell in cells for _ in offsets]
            xs = [x for _ in cells for x, y in offsets]
            ys = [y for _ in cells for x, y in offsets]
            groups.append(('River', locs, xs, ys))
    return groups


def run_modpath(settings: ParticleOptions, opts: Options, mf, raw: dict,
                workspace: Path, exe: str):
    """Rerun only MODPATH with independent well and river particle counts."""
    import flopy
    groups_data = particle_release_groups(settings, opts, raw)
    if not groups_data:
        return [], 'No eligible release cells for the selected sources.'
    mp = flopy.modpath.Modpath7(modelname='fieldcase_mp', flowmodel=mf,
                                model_ws=str(workspace), exe_name=exe)
    flopy.modpath.Modpath7Bas(mp, porosity=settings.porosity,
                              defaultiface={'RECHARGE': 6, 'RIVER LEAKAGE': 6})
    groups = []
    for source, locations, xs, ys in groups_data:
        releases = flopy.modpath.ParticleData(
            partlocs=locations, structured=True, localx=xs, localy=ys,
            localz=0.5, drape=0)
        groups.append(flopy.modpath.ParticleGroup(
            particlegroupname=source.lower() + '_backward', particledata=releases))
    flopy.modpath.Modpath7Sim(
        mp, simulationtype='combined', trackingdirection='backward',
        weaksinkoption='pass_through', weaksourceoption='pass_through',
        referencetime=0.0, stoptimeoption='extend', particlegroups=groups)
    mp.write_input()
    success, log = mp.run_model(silent=True, report=True)
    if not success:
        return [], 'MODPATH failed: ' + '\n'.join(log[-25:])
    pth = workspace / 'fieldcase_mp.mppth'
    if not pth.is_file():
        return [], 'MODPATH finished but produced no pathline file.'
    paths = flopy.utils.PathlineFile(str(pth)).get_alldata()
    summary = ', '.join(
        f'{source}: {len(locations)} particles in '
        f'{len(set(locations))} cells'
        for source, locations, _, _ in groups_data)
    return paths, f'{summary}; {len(paths)} backward pathlines.'


def path_xy(record):
    """Convert MODPATH local model coordinates to map coordinates.

    Some readers/output conventions expose already transformed coordinates;
    in that case choose whichever convention places most points in-domain.
    """
    x = np.asarray(record['x'], dtype=float)
    y = np.asarray(record['y'], dtype=float)
    rotated = (10000.0 - y, -7000.0 + x)
    direct = (x, y)

    def count_in_domain(pair):
        xx, yy = pair
        return np.count_nonzero(np.isfinite(xx) & np.isfinite(yy) &
                                (xx >= 0) & (xx <= WIDTH) &
                                (yy >= -HEIGHT) & (yy <= 0))

    return direct if count_in_domain(direct) > count_in_domain(rotated) else rotated


# =============================================================================
# 6. MAP PLOTTING: background, active grid, boundary symbols and head contours
# =============================================================================
def locate_image():
    candidates = [ROOT / 'Hintergrund.png', ROOT / 'FIGS' / 'Hintergrund.png',
                  ROOT / 'MODFLOW_NWT_Streamlit_Education_Prototype' /
                  'modflow_education' / 'data' / 'Hintergrund.png']
    return next((file for file in candidates if file.is_file()), None)


def _active_cell_grid_segments(ibound: np.ndarray):
    """Unique grid-edge segments belonging to at least one active cell.

    Grid rows correspond to east and grid columns correspond to north in the
    rotated local map. Segments on the active/inactive boundary are retained;
    inactive-only cell edges are excluded. No hard-coded plot pixel sizes.
    """
    active = np.asarray(ibound) > 0
    cells = np.argwhere(active)
    edges = set()
    for row, col in cells:
        r, c = int(row), int(col)
        edges.update((('v', r, c), ('v', r+1, c),
                      ('h', r, c), ('h', r, c+1)))
    segments = []
    for direction, r, c in sorted(edges):
        x, y = r*DX, -HEIGHT + c*DX
        if direction == 'v':
            segments.append(((x,y),(x,y+DX)))
        else:
            segments.append(((x,y),(x+DX,y)))
    return segments


def _draw_active_grid(ax, ibound: np.ndarray):
    """Draw only active-model cell boundaries, not the enclosing full grid."""
    segments = _active_cell_grid_segments(ibound)
    if segments:
        ax.add_collection(LineCollection(
            segments, colors='#555555', linewidths=0.21,
            alpha=0.45, zorder=2))


def draw_map(opts: Options, heads=None, paths=None, grid=False,
             show_bounds=True, show_background=True, show_head_contours=True,
             contour_count=14, contour_labels=True, head_fill=False,
             fill_alpha=0.35, title=None):
    """Map plot in fixed world coordinates, with optional true cellwise fill."""
    a = reference()
    fig, ax = plt.subplots(figsize=(10.2, 7.6), layout='constrained')
    image = locate_image()
    if image and show_background:
        ax.imshow(plt.imread(str(image)), extent=(0, WIDTH, -HEIGHT, 0),
                  origin='upper', zorder=0, alpha=.9)
    xx = (np.arange(a['ibound'].shape[0]) + .5) * DX
    yy = -HEIGHT + (np.arange(a['ibound'].shape[1]) + .5) * DX
    if heads is not None:
        h = np.asarray(heads)
        valid = ((a['ibound'] > 0) & np.isfinite(h) &
                 (np.abs(h) < 1e10) & (h > a['bottom'] + 1e-4))
        z = np.ma.masked_where(~valid.T, h.T)
        if head_fill and z.count():
            # Explicit cell edges, NOT interpolated/smoothed contours.
            edges_x = np.arange(a['ibound'].shape[0] + 1) * DX
            edges_y = -HEIGHT + np.arange(a['ibound'].shape[1] + 1) * DX
            mesh = ax.pcolormesh(edges_x, edges_y, z, shading='flat',
                                 cmap='viridis', alpha=fill_alpha, zorder=1)
            fig.colorbar(mesh, ax=ax, shrink=.70, pad=.02, label='Hydraulic head (m)')
        if show_head_contours and z.count() >= 10 and float(z.max()-z.min()) > 1e-5:
            levels = np.linspace(float(z.min()), float(z.max()), int(contour_count))
            lines = ax.contour(xx, yy, z, levels=levels,
                               colors='#192a4a', linewidths=.85, zorder=3)
            if contour_labels:
                ax.clabel(lines, fmt='%.1f', fontsize=7, inline=True)
    if grid:
        _draw_active_grid(ax, a['ibound'])
    handles=[]
    if show_bounds:
        _, _, bedrock = split_boundaries()
        # Markers are scaled close to the model-cell footprint (DX), rather
        # than the tiny points used previously. RIV is displayed as rectangles
        # in data coordinates, remaining almost cell-sized if figure size changes.
        marker_styles = (
            (bedrock, '#8e44ad', 'Bedrock inflow (WEL)', 's', 52),
            (a['east_chd'], '#d35400', 'Eastern CHD', '^', 72),
        )
        for records, color, label, marker, size in marker_styles:
            xy = np.array([xy_of(q[1], q[2]) for q in records])
            ax.scatter(xy[:, 0], xy[:, 1], s=size, c=color, marker=marker,
                       linewidths=0, zorder=5, alpha=.92)
            handles.append(Line2D([], [], marker=marker, markersize=8,
                                  linestyle='None', color=color, label=label))
        river_blue = '#10253c'  # very dark navy; white cell outlines contrast with map
        river_half_width = 0.44 * DX
        river_cells = [Rectangle(
            (x - river_half_width, y - river_half_width),
            2*river_half_width, 2*river_half_width)
            for x, y in (xy_of(q[1], q[2]) for q in a['river'])]
        from matplotlib.collections import PatchCollection
        ax.add_collection(PatchCollection(
            river_cells, facecolor=river_blue, edgecolor='white',
            linewidths=0.40, alpha=.98, zorder=5))
        handles.append(Patch(facecolor=river_blue, edgecolor='white', label='River (RIV)'))
    for n,w in enumerate(opts.wells,1):
        active = opts.pump_on and w.enabled and opts.pump_per_well_m3_day>0
        x,y=xy_of(w.row-1,w.col-1)
        ax.scatter([x],[y],s=85,c='#d22630' if active else '#666666',
                   linewidths=1.2,edgecolors='white',zorder=10)
        ax.annotate(f'W{n}',(x,y),xytext=(6,6),textcoords='offset points',
                    fontsize=9,fontweight='bold',color='#1b1b1b',zorder=11,
                    bbox={'fc':'white','ec':'none','alpha':.7,'pad':.3})
    if show_bounds:
        handles.append(Line2D([],[],marker='o',markersize=8,linestyle='None',
                              color='#d22630' if opts.pump_on else '#666666',
                              label='Pumping wells' if opts.pump_on else 'Well locations (off)'))
    if paths:
        for path in paths:
            if len(path)<2:continue
            x,y=path_xy(path)
            good=np.isfinite(x)&np.isfinite(y)&(x>=0)&(x<=WIDTH)&(y>=-HEIGHT)&(y<=0)
            if np.count_nonzero(good)>=2:
                ax.plot(x[good],y[good],color='#e10f89',alpha=.58,linewidth=.85,zorder=6)
        handles.append(Line2D([],[],color='#e10f89',linewidth=1.4,label='Backward pathlines'))
    if handles:
        # Legend is intentionally BELOW the map, never over important geography.
        ax.legend(handles=handles,loc='upper center',bbox_to_anchor=(.5,-.105),
                  fontsize=10,frameon=False,ncol=3)
    ax.set(xlim=(0,WIDTH),ylim=(-HEIGHT,0),
           xlabel='East in local map system (m)',ylabel='North in local map system (m)',
           title=title or 'Hydraulic heads and boundary conditions')
    ax.set_aspect('equal')
    return fig


def _run_modpath_for_result(st, result: dict, exe_mp: str) -> None:
    """Run MODPATH on an existing flow solution; never rerun MODFLOW.

    Called after a fresh flow run and by the independent MODPATH-only button.
    Reuses the postprocessing particle counts retained in session preferences.
    """
    restore_postprocessing_preferences(st)
    opts = result['opts']
    settings = configured_particle_options(st, opts)
    st.session_state.pop('fc_mp_paths', None)
    st.session_state.pop('fc_mp_signature', None)
    st.session_state.pop('fc_mp_message', None)
    if not settings.sources:
        st.info('Select at least one applicable particle release source in '
                '**5 · MODPATH particle tracking**.')
        return
    try:
        with st.spinner('Computing backward MODPATH trajectories...'):
            tracks, message = run_modpath(
                settings, opts, result['flowmodel'], result['raw'],
                Path(result['workspace']), resolve_executable(exe_mp))
        if message.startswith('MODPATH failed'):
            st.session_state['fc_mp_message'] = message
            st.warning(message)
        else:
            st.session_state['fc_mp_paths'] = tracks
            st.session_state['fc_mp_signature'] = particle_signature(settings, exe_mp)
            st.session_state['fc_mp_message'] = message
            st.success('MODPATH: ' + message)
    except Exception as exc:
        st.session_state['fc_mp_message'] = str(exc)
        st.warning(f'MODPATH did not finish: {exc}. MODFLOW results remain available.')


def zip_run(folder: Path):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as archive:
        for entry in folder.iterdir():
            if entry.is_file() and entry.stat().st_size < 80_000_000:
                archive.write(entry, entry.name)
    return buf.getvalue()


def self_test():
    a = reference()
    east, bedrock_all, west = split_boundaries()
    assert (len(east),len(bedrock_all),len(west))==(47,97,89)
    assert [cell_of(x,y) for x,y in WELL_CENTRES] == [(46,25),(50,24),(55,23)]
    assert WELL_CELLS==((47,26),(51,25),(56,24))
    no_pumps=Options(); validate_options(no_pumps)
    wel,riv,chd=make_stress_data(no_pumps)
    assert len(wel)==89 and np.all(wel[:,3]>0)
    assert len(riv)==147 and len(chd)==47
    assert np.isclose(wel[:,3].sum()*SEC_DAY,1467.2212302945745)
    with_pumps=Options(pump_on=True)
    wells_p,_,_=make_stress_data(with_pumps)
    assert len(wells_p)==92 and np.isclose(np.minimum(0,wells_p[:,3]).sum()*SEC_DAY,-9000)
    assert pumping_cells(with_pumps)==[(46,25),(50,24),(55,23)]
    assert np.allclose(conductivity_arrays(no_pumps)[0][a['hk']>1],100)
    assert len(select_river_release_cells(np.where(a['ibound']>0,-.01,0),20))==20
    from dataclasses import replace
    try:
        validate_options(replace(with_pumps,wells=(Well(1,1),)))
    except ValueError:
        pass
    # WEL binary splitting and listing numeric reconciliation on synthetic data.
    raw={k:np.zeros_like(a['ibound'],dtype=float) for k in ['WEL','RIV','CHD','RCH']}
    for q in west:raw['WEL'][int(q[1]),int(q[2])] = q[3]
    raw['RCH'][12,12]=.012;raw['RIV'][12,13]=-.005;raw['CHD'][12,14]=.001
    pkg={k:signed_rates(v) for k,v in raw.items()}
    totin=sum(t[0] for t in pkg.values());totout=sum(t[1] for t in pkg.values())
    lst={'packages':pkg,'total_in':totin,'total_out':totout,
         'percent_discrepancy':200*(totin-totout)/(totin+totout),'path':'synthetic'}
    budget=assemble_budget(raw,no_pumps,lst)
    assert abs(budget['listing_total_in_m3day']-totin*SEC_DAY)<1e-4
    assert max(v['Max difference (m³/day)'] for v in budget['checks'])<1e-7
    fig=draw_map(no_pumps,heads=a['head_ref'],head_fill=True,grid=True,show_bounds=True)
    plt.close(fig)
    one=stable_signature(no_pumps,SolverSettings(),'MODFLOW-NWT_64.exe')
    again=stable_signature(Options(),SolverSettings(),'MODFLOW-NWT_64.exe')
    assert one==again
    assert one!=stable_signature(no_pumps,replace(SolverSettings(),
                          fluxtol_m3_day=100),'MODFLOW-NWT_64.exe')
    p=ParticleOptions()
    assert (p.well_particles_per_cell,p.river_particles_per_cell,p.max_river_cells)==(10,1,35)
    for n in range(1,21):
        points=particle_ring_offsets(n)
        assert len(points)==n and all(.0<x<1 and .0<y<1 for x,y in points)
        if n>=2:
            assert all(abs(math.hypot(x-.5,y-.5)-.25)<1e-12
                       for x,y in points)
    for n in range(1,6):
        river_settings=replace(p,sources=('River',),river_particles_per_cell=n,
                               max_river_cells=5)
        fake_riv=np.full_like(a['ibound'], -.01, dtype=float)
        groups=particle_release_groups(river_settings,no_pumps,{'RIV':fake_riv})
        assert len(groups)==1 and len(groups[0][1])==5*n
    both=replace(p,sources=('Wells','River'),well_particles_per_cell=20,
                 river_particles_per_cell=1,max_river_cells=5)
    fake_riv=np.full_like(a['ibound'], -.01, dtype=float)
    groups=particle_release_groups(both,with_pumps,{'RIV':fake_riv})
    assert len(groups)==2
    assert len(groups[0][1])==3*20 and len(groups[1][1])==5
    assert particle_signature(p,'mp7') != particle_signature(
        replace(p,well_particles_per_cell=12),'mp7')
    assert particle_signature(p,'mp7') != particle_signature(
        replace(p,river_particles_per_cell=5),'mp7')
    assert particle_signature(p,'mp7')==particle_signature(
        ParticleOptions(),'mp7')
    assert particle_signature(p,'mp7')!=particle_signature(
        replace(p,porosity=.3),'mp7')
    assert abs(SolverSettings().fluxtol_m3_day/SEC_DAY-500/86400)<1e-15
    print('PASS: geometry, SPD, pump defaults, budget bookkeeping, cell fill, plotting, '
          'stable model/particle signatures and unit conversion.')


def _usable_binary(path: Path) -> Path:
    """Validate a candidate executable, handling Git's missing +x bit.

    A Windows PE (.exe) cannot run on Linux even if renamed to mfnwt.
    Distinguish that case explicitly to avoid confusing solver errors.
    """
    path = path.resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    if os.name != 'nt':
        with path.open('rb') as binary:
            prefix = binary.read(4)
        if prefix[:2] == b'MZ':
            raise RuntimeError(
                f'{path.name} is a Windows executable. Streamlit Community '
                'Cloud runs Linux. Use the Linux mfnwt/mp7 programs in bin/.')
        try:
            path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        except OSError:
            # A read-only deployment can still run a binary with +x set.
            if not os.access(path, os.X_OK):
                raise PermissionError(f'Executable is not runnable: {path}')
    return path


def _official_usgs_executable(name: str) -> Path:
    """Last-resort provision of official Linux programs, once per server.

    Only the two exact, supported executables may be downloaded; this is
    never applied to arbitrary user-supplied executable names. get_modflow
    uses official MODFLOW-ORG releases and the correct Linux distribution.
    Program files stay in a writable *temporary* cache outside the repo.
    """
    if os.name == 'nt' or name not in {'mfnwt', 'mp7'}:
        raise FileNotFoundError(name)
    location = EXECUTABLE_CACHE / name
    if location.is_file():
        return _usable_binary(location)
    EXECUTABLE_CACHE.mkdir(parents=True, exist_ok=True)
    try:
        import flopy
        # Pin the established USGS release: new upstream releases must
        # not silently change a scientifically verified model workflow.
        flopy.utils.get_modflow(
            EXECUTABLE_CACHE, repo='executables', release_id='29.0',
            subset=['mfnwt', 'mp7'], quiet=True)
    except Exception as exc:
        raise FileNotFoundError(
            f'Linux executable {name!r} not available. Place the official '
            f'Linux mfnwt and mp7 binaries in the repository bin/ folder '
            f'or allow the USGS download. Detail: {exc}') from exc
    if not location.is_file():
        raise FileNotFoundError(
            f'USGS installation finished but {name!r} was not found in '
            f'{EXECUTABLE_CACHE}. Check your GitHub rate limit or copy '
            'the Linux executable into bin/.')
    return _usable_binary(location)


def resolve_executable(program: str):
    """Locate an installed solver for Linux Cloud or local development.

    Priority: explicit existing path; configured environment override;
    repository bin/; PATH; official USGS download (Linux defaults only).
    Models are always executed in per-session temporary workspaces.
    """
    name = str(program).strip()
    if not name:
        raise ValueError('Executable name cannot be empty.')
    direct = Path(name).expanduser()
    if direct.is_file():
        return str(_usable_binary(direct))

    is_mfnwt = name.lower() in {'mfnwt', 'mfnwtdbl', 'modflow-nwt_64.exe'}
    is_mp7 = name.lower() in {'mp7', 'mp7.exe'}
    overrides = []
    if is_mfnwt and os.getenv('MFNWT_EXECUTABLE'):
        overrides.append(Path(os.environ['MFNWT_EXECUTABLE']).expanduser())
    if is_mp7 and os.getenv('MP7_EXECUTABLE'):
        overrides.append(Path(os.environ['MP7_EXECUTABLE']).expanduser())
    variants = [name]
    if is_mfnwt:
        variants += ['mfnwt', 'mfnwtdbl', 'MODFLOW-NWT_64.exe']
    if is_mp7:
        variants += ['mp7', 'mp7.exe']
    folders = [ROOT / 'bin', ROOT.parent / 'bin', Path.cwd() / 'bin']
    checked = set()
    for candidate in overrides + [folder / variant for folder in folders for variant in variants]:
        candidate = candidate.resolve()
        if candidate in checked:
            continue
        checked.add(candidate)
        if candidate.is_file():
            return str(_usable_binary(candidate))
    for variant in variants:
        on_path = shutil.which(variant)
        if on_path:
            return str(_usable_binary(Path(on_path)))

    if os.name != 'nt':
        if name.lower().endswith('.exe'):
            raise FileNotFoundError(
                f'The executable name {name!r} is Windows-specific. '
                'Select the Linux program mfnwt or mp7 for Streamlit Cloud.')
        if name in ('mfnwt', 'mp7'):
            return str(_official_usgs_executable(name))
    # Preserve the local-app behavior for custom executable names.
    return name


def _budget_figure(budget):
    """Signed component and total flow rates, with explicit IN/OUT conventions."""
    rows = budget['rows']
    labels = [r['Component'] for r in rows] + ['TOTAL (LIST)']
    qin = [r['In (m³/day)'] for r in rows] + [budget['listing_total_in_m3day']]
    qout = [r['Out (m³/day)'] for r in rows] + [budget['listing_total_out_m3day']]
    yy = np.arange(len(labels))
    fig,ax = plt.subplots(figsize=(8.8,4.5),layout='constrained')
    ax.barh(yy-.19,qin,height=.38,color='#2577a7',label='IN (+)')
    ax.barh(yy+.19,-np.array(qout),height=.38,color='#d7853a',label='OUT (−)')
    ax.invert_yaxis()
    ax.set_yticks(yy,labels)
    ax.axvline(0,color='black',lw=.7)
    ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
    ax.set_xlabel('Volumetric flow rate (m³/day)')
    ax.legend(loc='lower right',ncol=2,fontsize=8)
    return fig


# =============================================================================
# 7. POSTPROCESSING STATE: widget preferences remain persistent across runs
# =============================================================================
_POSTPROCESSING_DEFAULTS = {
    'fc_bg': True,
    'fc_bc': False,
    'fc_grid': False,
    'fc_cont': True,
    'fc_labels': True,
    'fc_fill': False,
    'fc_particle_view': True,  # display preference; MODPATH activation is an input control
    'fc_levels': 14,
    'fc_opacity': 0.35,
    'fc_mp_well_count': 10,
    'fc_mp_river_count': 1,
    'fc_mp_cap': 35,
    'fc_log': False,
}


def _store_particle_control(st, preference_key: str, widget_key: str) -> None:
    """Synchronize a particle slider *before* Streamlit reruns the app.

    The particle-count sliders sit below the main MODFLOW/MODPATH buttons.
    A Streamlit `on_change` callback is essential: without it, clicking a
    button above those sliders may use the previous particle count.  Keep a
    separate persistent value so hiding Results does not reset the slider.
    """
    value = int(st.session_state[widget_key])
    st.session_state[preference_key] = value
    st.session_state.setdefault('fc_postprocessing_preferences', {})[preference_key] = value


def particle_count_slider(st, label: str, minimum: int, maximum: int,
                          *, preference_key: str, disabled: bool, help: str) -> int:
    """Render an MP-only slider with explicit, persistent initial value.

    Streamlit removes keyed widget values if Results are not displayed.  Use
    a separate widget key and durable preference instead of relying on the
    slider's implicit default (which is the minimum, i.e. one particle/cell).
    """
    preferences = st.session_state.setdefault('fc_postprocessing_preferences', {})
    default = _POSTPROCESSING_DEFAULTS[preference_key]
    initial = int(preferences.get(preference_key,
                                  st.session_state.get(preference_key, default)))
    initial = max(minimum, min(maximum, initial))
    widget_key = preference_key + '_ui'
    value = st.slider(label, minimum, maximum, value=initial,
                      key=widget_key, disabled=disabled, help=help,
                      on_change=_store_particle_control,
                      args=(st, preference_key, widget_key))
    # Also mirror the returned value on normal renders (including first mount).
    _store_particle_control(st, preference_key, widget_key)
    return int(value)


def configured_particle_options(st, opts: Options) -> ParticleOptions:
    """Compose settings from stable pre-run inputs and post-run particle counts.

    The number of release cells/particles is DISPLAY/POSTPROCESSING state;
    changing those counts never invalidates or reruns the flow solution.
    """
    sources = []
    if st.session_state.get('fc_mp_sources_well', False) and pumping_cells(opts):
        sources.append('Wells')
    if st.session_state.get('fc_mp_sources_riv', True):
        sources.append('River')
    return ParticleOptions(
        sources=tuple(sources),
        porosity=float(st.session_state.get('fc_mp_porosity', 0.25)),
        well_particles_per_cell=int(st.session_state.get('fc_mp_well_count', 10)),
        river_particles_per_cell=int(st.session_state.get('fc_mp_river_count', 1)),
        max_river_cells=int(st.session_state.get('fc_mp_cap', 35)),
    )


def restore_postprocessing_preferences(st):
    """Hydrate widgets from independent preferences after a new MODFLOW run.

    Unrendered Streamlit widgets lose their own keyed state on subsequent
    reruns. A plain persistent dict is not associated with any widget and
    therefore survives even while the Results section is absent.
    """
    stored = st.session_state.setdefault('fc_postprocessing_preferences', {})
    for key, fallback in _POSTPROCESSING_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = stored.get(key, fallback)


def save_postprocessing_preferences(st):
    """Copy widget inputs to durable session data before Streamlit cleanup."""
    stored = st.session_state.setdefault('fc_postprocessing_preferences', {})
    stored.update({key: st.session_state[key]
                   for key in _POSTPROCESSING_DEFAULTS
                   if key in st.session_state})


# =============================================================================
# 8. RESULTS: map, MODPATH controls, budget and downloads
# =============================================================================
def _render_results(st, result, exe_mp):
    opts = result['opts']
    heads = result['heads']
    budget = result['budget']
    restore_postprocessing_preferences(st)
    st.subheader('Results')
    with st.container(key='fc-panel-postprocess'):
        with st.expander('Postprocessing options (Click to open/close)', expanded=False):
            a,b=st.columns(2)
            with a:
                show_background=st.checkbox('Background map',key='fc_bg')
                show_bounds=st.checkbox('Boundary conditions',key='fc_bc')
                show_grid=st.checkbox('Model grid',key='fc_grid')
                show_contours=st.checkbox('Hydraulic-head contours',key='fc_cont')
            with b:
                show_labels=st.checkbox('Contour labels',key='fc_labels',
                                         disabled=not show_contours)
                show_fill=st.checkbox('Cellwise head color fill',key='fc_fill')
                show_particles=st.checkbox('Show particle trajectories',key='fc_particle_view',
                    disabled=not st.session_state.get('fc_mp_active', False))
            c,d=st.columns(2)
            with c:
                count=st.slider('Number of contour levels',6,30,key='fc_levels',
                                disabled=not show_contours)
            with d:
                alpha=st.slider('Head-fill opacity',.1,.9,step=.05,key='fc_opacity',
                                disabled=not show_fill)
            if st.session_state.get('fc_mp_active', False):
                st.markdown('**Backward MODPATH 7 particle releases**')
                st.caption('Choose release locations and porosity in **5 · MODPATH '
                           'settings** above. The counts below affect MODPATH only, '
                           'not the MODFLOW solution.')
                source_settings = configured_particle_options(st, opts)
                ca, cb = st.columns(2)
                with ca:
                    well_count = particle_count_slider(
                        st, 'Particles per active pumping-well cell', 1, 20,
                        preference_key='fc_mp_well_count',
                        disabled='Wells' not in source_settings.sources,
                        help='Default: 10 particles around a ring in each active well cell.')
                with cb:
                    river_count = particle_count_slider(
                        st, 'Particles per gaining RIV cell', 1, 5,
                        preference_key='fc_mp_river_count',
                        disabled='River' not in source_settings.sources,
                        help='Default: one particle per selected gaining river cell.')
                max_river_cells = particle_count_slider(
                    st, 'Number of gaining RIV release cells', 1, 147,
                    preference_key='fc_mp_cap',
                    disabled='River' not in source_settings.sources,
                    help='Initial default: 35 release cells along gaining reaches; '
                         'with one particle per cell, this starts 35 river particles. '
                         'Your modified count is preserved between model runs.')
                settings = replace(source_settings,
                                   well_particles_per_cell=well_count,
                                   river_particles_per_cell=river_count,
                                   max_river_cells=max_river_cells)
                sig = particle_signature(settings, exe_mp)
                if st.session_state.get('fc_mp_signature') != sig:
                    # Preserve an automatic-run failure message (no old paths),
                    # so the student can inspect it and retry MODPATH alone.
                    if 'fc_mp_paths' in st.session_state:
                        st.session_state.pop('fc_mp_message', None)
                    st.session_state.pop('fc_mp_paths', None)
                if not settings.sources:
                    st.info('Activate one or both release sources in MODPATH settings.')
                elif (st.session_state.get('fc_mp_signature') != sig or
                      'fc_mp_paths' not in st.session_state):
                    # This contextual action returns when a student edits particle
                    # counts or porosity. The flow field, workspace and water budget
                    # are reused; no MODFLOW call is made.
                    st.caption('Particle settings have changed or tracking has not '
                               'yet run. The flow solution remains available.')
                    with st.container(key='fc-action-mp-postprocess'):
                        if st.button('↻ Re-run MODPATH', key='fc_rerun_mp_post',
                                     type='secondary'):
                            _run_modpath_for_result(st, result, exe_mp)
                if st.session_state.get('fc_mp_message'):
                    st.caption(st.session_state['fc_mp_message'])
            elif st.session_state.get('fc_mp_paths') is not None:
                # Switching tracking off must hide old paths, but never clear heads.
                st.session_state.pop('fc_mp_paths', None)
                st.session_state.pop('fc_mp_signature', None)
                st.session_state.pop('fc_mp_message', None)
    paths=(st.session_state.get('fc_mp_paths',[]) if (show_particles and
        st.session_state.get('fc_mp_active', False)) else [])
    st.markdown('**Simulated steady-state hydraulic heads**')
    fig=draw_map(opts,heads=heads,paths=paths,grid=show_grid,
                 show_bounds=show_bounds,show_background=show_background,
                 show_head_contours=show_contours,contour_count=count,
                 contour_labels=show_labels,head_fill=show_fill,fill_alpha=alpha,
                 title='Hydraulic heads (m)')
    st.pyplot(fig,use_container_width=True)
    plt.close(fig)
    a=reference()
    good=((a['ibound']>0)&np.isfinite(heads)&(np.abs(heads)<1e10)&
          (heads>a['bottom']+1e-4))
    if np.any(good):
        min_head,max_head=float(heads[good].min()),float(heads[good].max())
        river_out=budget['listing']['packages']['RIV'][1]*SEC_DAY
        st.caption(f'Minimum head: **{min_head:.2f} m**  ·  '
                   f'Maximum head: **{max_head:.2f} m**  ·  '
                   f'Outflow to the river: **{river_out:,.1f} m³/day**')
    dry=np.count_nonzero((a['ibound']>0)&~good)
    if dry:
        st.warning(f'{dry} active cells have dry, inactive, or invalid head values. '
                   'High pumping may drain parts of the aquifer.')
    # Budget is BELOW the hydraulic-head plot and in its OWN expander.
    with st.container(key='fc-panel-budget'):
        with st.expander('Water budget (MODFLOW listing file) (Click to open/close)',expanded=False):
            lst=budget['listing']
            st.caption('Rates are taken from the last **incremental** listing-file '
                       'budget (m³/s), converted to m³/day. '
                       'They are not cumulative volumes.')
            ca,cb,cc=st.columns(3)
            ca.metric('Total IN',f"{budget['listing_total_in_m3day']:,.1f} m³/day")
            cb.metric('Total OUT',f"{budget['listing_total_out_m3day']:,.1f} m³/day")
            cc.metric('Discrepancy',f"{lst['percent_discrepancy']:+.3f} %")
            fig_b=_budget_figure(budget)
            st.pyplot(fig_b,use_container_width=True)
            plt.close(fig_b)
            # Avoid DataFrame.style, which depends on optional `jinja2`.
            # Numerical values are *only displayed* at two decimals;
            # all budget computations use unrounded listing/CBC rates.
            table=pd.DataFrame(budget['rows'])
            for col in ('In (m³/day)', 'Out (m³/day)', 'Net (m³/day)'):
                if col in table.columns:
                    table[col]=table[col].round(2)
            st.dataframe(table,hide_index=True,use_container_width=True)
            if abs(lst['percent_discrepancy']) > 1.0:
                st.warning('Listing-file budget discrepancy exceeds 1%. '
                           f'Only discrepancies above ±{MAX_BUDGET_DISCREPANCY_PERCENT:g}% '
                           'cause rejection; inspect results critically.')
            st.caption('All displayed component IN/OUT rates come from the '
                       'incremental MODFLOW listing budget. Positive WEL inflow '
                       'represents bedrock inflow; negative WEL flow represents '
                       'extraction. The CBC is used for spatial release selection '
                       'and independent reconciliation checks.')
            # The listing-file total is the authoritative reference, not sum of rounded values.
            checks=pd.DataFrame(budget['checks'])
            tol=max(.005*max(budget['listing_total_in_m3day'],
                             budget['listing_total_out_m3day']),1.0)
            if any(checks['Max difference (m³/day)']>tol):
                st.error('LIST and CBC reconciliation fails the 0.5% test '
                         '(for CHD: net exchange; otherwise: gross IN/OUT). '
                         'Inspect the diagnostics. Displayed values still use LIST.')
    with st.container(key='fc-panel-details'):
        with st.expander('Model details and files (Click to open/close)',expanded=False):
            st.caption('One unconfined layer, 100 rows × 70 columns, one steady-state '
                       'stress period; 47 eastern CHD cells, 89 active bedrock '
                       'inflow cells, 147 RIV cells, areal RCH and optional wells.')
            st.caption('The eastern CHD replaces the original WEL inflow and changes '
                       'the conceptual model. Its 375.6 m initial head is provisional.')
            rows=[{'Well':f'W{i}','Cell number x-direction':w.row,
                   'Cell number y-direction':w.col,
                   'Pumping active':bool(opts.pump_on and w.enabled and
                                         opts.pump_per_well_m3_day>0)}
                  for i,w in enumerate(opts.wells,1)]
            st.dataframe(pd.DataFrame(rows),hide_index=True,use_container_width=True)
            st.caption('Run directory:')
            st.code(result['workspace'])
            if st.checkbox('Show solver log',key='fc_log'):
                st.code('\n'.join(result['flow_log'][-90:]))
            st.download_button('Download model inputs and outputs (ZIP)',
                               data=zip_run(Path(result['workspace'])),
                               file_name='fieldcase_last_run.zip',mime='application/zip',
                               key='fc_download')
    save_postprocessing_preferences(st)


def _render_rejected_budget(st, rejected: dict):
    """Show budget diagnostics for runs rejected by the 5% LIST criterion."""
    budget = rejected['budget']
    listing = budget['listing']
    workspace = Path(rejected['workspace'])
    with st.container(key='fc-panel-failure'):
        with st.expander('Failed-run water budget (MODFLOW listing file) (Click to open/close)',
                         expanded=True):
            if rejected.get('reason') == 'solver':
                st.error('The MODFLOW solver did not converge. ' 
                         'Listing-file budget values are diagnostic only; '
                         'these heads and pathlines must not be interpreted.')
            else:
                st.error(f"Mass-balance discrepancy: "
                         f"{listing['percent_discrepancy']:+.3f}% "
                         f"(limit ±{MAX_BUDGET_DISCREPANCY_PERCENT:g}%). "
                         'These heads and pathlines are not considered valid results.')
            st.caption('Listing-file incremental rates. The original printed '
                       'budget appears below for cross-checking.')
            rows = []
            for key, (qin, qout) in listing['packages'].items():
                rows.append({'Package': key, 'IN (m³/s)': qin,
                             'OUT (m³/s)': qout, 'IN (m³/day)': qin*SEC_DAY,
                             'OUT (m³/day)': qout*SEC_DAY})
            rows.append({'Package': 'TOTAL', 'IN (m³/s)': listing['total_in'],
                         'OUT (m³/s)': listing['total_out'],
                         'IN (m³/day)': budget['listing_total_in_m3day'],
                         'OUT (m³/day)': budget['listing_total_out_m3day']})
            st.dataframe(pd.DataFrame(rows), hide_index=True,
                         use_container_width=True)
            st.code(listing_budget_text(workspace), language='text')
            st.caption(f'Original listing: {listing["path"]}')


# =============================================================================
# 9. EXPANDER APPEARANCE: map-inspired colors; presentation only
# =============================================================================
def inject_expander_styles(st):
    """Apply soft expander panels and scoped orange MODPATH-only buttons.

    Each expander is wrapped in a keyed ``st.container``. Streamlit attaches a
    stable ``st-key-...`` CSS class to that container, so themes do not depend
    on the position of widgets within the page or the text of labels.

    The color palette refers to the map's pale yellow aquifer, green areas,
    dark-blue rivers, gray built areas and muted boundary markers. These CSS
    rules do not change the model, data, session keys or any computation.
    """
    css = [
        # Base appearance used by all model-input and result expanders.
        '[class*="st-key-fc-panel-"] [data-testid="stExpander"] > details { '
        'border-radius: 0.70rem !important; '
        'border-width: 1px !important; overflow: hidden; }',
        '[class*="st-key-fc-panel-"] [data-testid="stExpander"] > details > summary { '
        'padding-top: .85rem; padding-bottom: .85rem; '
        'transition: background-color 120ms ease; }',
        '[class*="st-key-fc-panel-"] [data-testid="stExpander"] > details > summary p { '
        'font-weight: 650 !important; }',
        '[class*="st-key-fc-panel-"] [data-testid="stExpander"] > details > summary:hover { '
        'filter: brightness(.97); }',
    ]
    # (panel key, translucent panel color, border, heading, dark-panel color,
    #  high-contrast heading for users in dark mode)
    palette = [
        ('aquifer', 'rgba(248, 226, 107, 0.20)', '#c3a846', '#6c5a16', 'rgba(255, 244, 175, 0.19)', '#e6ca62'),
        ('boundaries', 'rgba(83, 163, 108, 0.15)', '#76ae79', '#245c3e', 'rgba(126, 178, 137, 0.18)', '#81b489'),
        ('wells', 'rgba(161, 161, 169, 0.19)', '#a6a7af', '#48505a', 'rgba(164, 164, 177, 0.19)', '#b7b5bf'),
        ('solver', 'rgba(178, 143, 192, 0.16)', '#b795bf', '#654677', 'rgba(166, 140, 177, 0.19)', '#bf9acb'),
        ('modpath', 'rgba(72, 153, 187, 0.14)', '#529cbc', '#135b7a', 'rgba(78, 140, 173, 0.20)', '#68b4d1'),
        ('preview', 'rgba(180, 195, 81, 0.18)', '#9baf48', '#566623', 'rgba(168, 179, 91, 0.20)', '#bbca75'),
        ('postprocess', 'rgba(93, 169, 206, 0.14)', '#6eafcb', '#175c7b', 'rgba(89, 149, 189, 0.18)', '#77bddb'),
        ('budget', 'rgba(80, 156, 142, 0.14)', '#69a89c', '#236e65', 'rgba(93, 156, 149, 0.18)', '#77b7a9'),
        ('details', 'rgba(151, 160, 167, 0.15)', '#a3abb0', '#4f606a', 'rgba(157, 171, 180, 0.18)', '#bac5cd'),
        ('failure', 'rgba(210, 126, 116, 0.13)', '#d1a09a', '#9d4d42', 'rgba(173, 100, 98, 0.19)', '#dea29b'),
    ]
    dark_css = []
    for key, color, border, heading, dark_color, dark_heading in palette:
        scope = f'.st-key-fc-panel-{key} [data-testid="stExpander"]'
        css.append(f'{scope} > details {{ background-color: {color} !important; '
                   f'border-color: {border} !important; }}')
        css.append(f'{scope} > details > summary p {{ color: {heading} !important; }}')
        dark_css.append(f'{scope} > details {{ background-color: {dark_color} !important; '
                        f'border-color: {dark_heading} !important; }}')
        dark_css.append(f'{scope} > details > summary p {{ color: {dark_heading} !important; }}')
    css.append('@media (prefers-color-scheme: dark) {' + '\n'.join(dark_css) + '}')
    # Only the two MODPATH-only actions receive orange styling; using the
    # keyed container class avoids changing any other Streamlit buttons.
    for action_key in ('fc-action-mp-main', 'fc-action-mp-postprocess'):
        scope = f'.st-key-{action_key} button'
        css.append(f'{scope} {{ background-color: #de8d2c !important; '
                   'border-color: #bd7117 !important; color: #2b200e !important; '
                   'font-weight: 600 !important; }}')
        css.append(f'{scope}:hover {{ background-color: #f0a648 !important; '
                   'border-color: #ad6815 !important; color: #2b200e !important; }}')
        css.append(f'{scope}:disabled {{ opacity: .45 !important; }}')
    st.markdown('<style>\n' + '\n'.join(css) + '\n</style>', unsafe_allow_html=True)


# =============================================================================
# 10. STREAMLIT UI: input expanders, preview, model run and failure handling
# =============================================================================
def main():
#    try:
#        import streamlit as st
#    except ImportError as exc:
#        raise SystemExit('Streamlit missing; install streamlit and flopy.') from exc
    st.set_page_config(page_title='Groundwater · Flow and catchments',
                       page_icon='💧',layout='centered')
    inject_expander_styles(st)
    st.title('💧 Groundwater flow, rivers and pumping wells')
    st.markdown('Explore a **one-layer, steady-state MODFLOW-NWT model**. '
                'You can modify the aquifer properties, river interaction, '
                'and the location and pumping rates of three wells. '
                'The initial scenario has no active pumping.')
    if locate_image() is None:
        st.warning('Map missing: place `Hintergrund.png` in the `FIGS` '
                   'directory or next to this script.')
    with st.container(key='fc-panel-aquifer'):
        with st.expander('1 · Aquifer properties and groundwater recharge (Click to open/close)'):
            kh=log_slider(st,'Hydraulic conductivity K (m/s)',minimum=1e-7,
                          maximum=1e-2,default=BASE_K,key='fc_k',
                          help='Logarithmic scale; values are absolute m/s, not multipliers.')
            st.caption(f'Hydraulic conductivity: {kh:.3e} m/s')
            keep_lake=st.checkbox('Preserve the original lake conductivity',True,
                                  key='fc_lake',help='Retains the original K field '
                                  'in the 43 lake cells; the general K is applied elsewhere.')
            recharge=st.number_input('Areal recharge (mm/year)',min_value=0.,
                                       max_value=3000.,value=float(round(BASE_RECHARGE,2)),
                                       step=10.,format='%.2f',key='fc_recharge')
    with st.container(key='fc-panel-boundaries'):
        with st.expander('2 · Boundary conditions (Click to open/close)'):
            chd_head=st.number_input('Specified head at eastern CHD (m)',
                           min_value=360.,max_value=385.,value=DEFAULT_EAST_CHD_HEAD,
                           step=.1,format='%.2f',key='fc_chd')
            st.caption('The eastern CHD is independent of bedrock recharge. '
                       'The CHD head is provisional, not calibrated.')
            bedrock_mult=st.slider('Bedrock inflow relative to reference',
                                  0.,3.,1.,.1,key='fc_bedrock')
            river_c=log_slider(st,'River conductance per metre (m/s)',
                        minimum=1e-7,maximum=1e-2,default=BASE_C_PER_M,key='fc_riv',
                        help='Effective conductance per metre river length; '
                             'original segment lengths were inferred.')
            st.caption(f'River conductance per metre: {river_c:.3e} m/s')
    with st.container(key='fc-panel-wells'):
        with st.expander('3 · Pumping wells (Click to open/close)',expanded=False):
            pump_on=st.toggle('Activate pumping wells',False,key='fc_pump')
            pump_rate=st.number_input('Pumping rate per active well (m³/day)',
                                      min_value=0.,max_value=30000.,value=3000.,
                                      step=250.,key='fc_rate',disabled=not pump_on)
            wells=[]
            for idx,(r0,c0) in enumerate(WELL_CELLS,1):
                st.markdown(f'**Well {idx}**')
                c1,c2,c3=st.columns([.7,1,1])
                with c1:
                    enabled=st.checkbox('Use',value=True,key=f'fc_w{idx}_on',
                                        disabled=not pump_on)
                with c2:
                    row=st.number_input('Cell number x-direction',min_value=1,max_value=100,value=r0,
                                        step=1,key=f'fc_w{idx}_row')
                with c3:
                    col=st.number_input('Cell number y-direction',min_value=1,max_value=70,value=c0,
                                        step=1,key=f'fc_w{idx}_col')
                wells.append(Well(int(row),int(col),enabled))
            if pump_on and pump_rate>10000:
                st.info('Large extraction rates can dewater well cells. A failed '
                        'direct solution triggers staged pumping continuation; '
                        'if this also fails, reduce pumping or relocate wells.')
    with st.container(key='fc-panel-solver'):
        with st.expander('4 · Solver settings (Click to open/close)'):
            st.caption('NWT uses HEADTOL and FLUXTOL (corresponding to the familiar '
                       'HCLOSE / RCLOSE controls). Model units are metres and seconds.')
            a,b=st.columns(2)
            with a:
                headtol=st.number_input('HCLOSE / HEADTOL (m)',min_value=1e-8,
                    max_value=1.0,value=1e-3,format='%.6g',key='fc_headtol',
                    help='Maximum head change between nonlinear iterations, in metres.')
                niter=st.number_input('NIT / maximum outer iterations',min_value=10,
                    max_value=10000,value=500,step=50,key='fc_nit')
            with b:
                fluxday=st.number_input('RCLOSE / FLUXTOL (m³/day)',
                    min_value=0.001,max_value=1e7,value=500.0,
                    step=50.0,format='%.3f',key='fc_fluxtol_day',
                    help='NWT RMS nonlinear flux-change criterion. Converted '
                         'internally to m³/s; this is NOT the linear GMRES residual.')
                complexity=st.selectbox('NWT nonlinear preset',
                    options=['SIMPLE','MODERATE','COMPLEX'],index=2,key='fc_complexity')
            linear_method=st.selectbox('Linear solver',options=['GMRES','XMD'],
                index=0,key='fc_linear_method',
                help='XMD is an alternative linear solver to test when GMRES '
                     'stagnates. Changing this requires a new MODFLOW run.')
            st.caption(f'FLUXTOL passed to NWT: {fluxday/SEC_DAY:.6g} m³/s; '
                       'the default 500 m³/day is a diagnostic preset and does '
                       'not guarantee a satisfactory mass balance.')
            # The executable is an internal deployment setting, not a user control.
            exe_mf = 'MODFLOW-NWT_64.exe' if os.name == 'nt' else 'mfnwt'
            solver=SolverSettings(headtol_m=float(headtol),
                fluxtol_m3_day=float(fluxday),maxiterout=int(niter),
                complexity=str(complexity),linear_method=str(linear_method))
    with st.container(key='fc-panel-modpath'):
        with st.expander('5 · MODPATH particle tracking (Click to open/close)', expanded=False):
            st.caption('Tracking is optional and always backward. When activated, '
                       'the main Run button computes MODFLOW and MODPATH. If the '
                       'flow solution already exists, MODPATH can be run separately '
                       'beside the main Run button.')
            mp_active = st.checkbox('Activate backward particle tracking',
                                    value=False, key='fc_mp_active')
            c1,c2 = st.columns(2)
            with c1:
                use_pump_source = st.checkbox('Release from pumping wells',
                    value=bool(pump_on), key='fc_mp_sources_well',
                    disabled=not (mp_active and pump_on and pump_rate>0
                                      and any(w.enabled for w in wells)))
                use_riv_source = st.checkbox('Release from gaining RIV cells',
                    value=True, key='fc_mp_sources_riv', disabled=not mp_active)
            with c2:
                porosity = st.slider('Effective porosity', 0.05, 0.45,
                                     value=0.25, step=0.01, key='fc_mp_porosity',
                                     disabled=not mp_active)
                exe_mp = st.text_input('MODPATH 7 executable', value='mp7',
                                       key='fc_mp_exe')
            st.caption('Particle counts are adjusted after the run: 10 particles '
                       'per pumping-well cell and 35 selected gaining river cells '
                       'with one particle per cell by default.')
    opts=Options(pump_on=bool(pump_on),pump_per_well_m3_day=float(pump_rate),
                 wells=tuple(wells),kh_m_s=kh,keep_lake=bool(keep_lake),
                 recharge_mm_year=float(recharge),bedrock_multiplier=float(bedrock_mult),
                 chd_head_m=float(chd_head),river_cper_m_m_s=float(river_c))
    # Input changes immediately suppress prior results: do not imply an old
    # computed scenario belongs to modified boundary conditions.
    current_signature=stable_signature(opts,solver,exe_mf)
    prev=st.session_state.get('nwt_last')
    # Compare JSON primitive values, never dataclass objects across Streamlit
    # script reruns: new dataclass classes are redefined on every rerun.
    if prev is not None and prev.get('flow_signature')!=current_signature:
        st.session_state.pop('nwt_last',None)
        for key in ('fc_mp_signature','fc_mp_paths','fc_mp_message'):
            st.session_state.pop(key,None)
        try:shutil.rmtree(prev['workspace'],ignore_errors=True)
        except OSError:pass
    failed_budget = st.session_state.get('nwt_failed_budget')
    if (failed_budget is not None and
            failed_budget.get('flow_signature') != current_signature):
        # A failed run belongs to the previous inputs, just like successful
        # results. Do not display it for a newly edited pumping scenario.
        st.session_state.pop('nwt_failed_budget',None)
    with st.container(key='fc-panel-preview'):
        with st.expander('6 · Model preview: grid and boundary conditions (Click to open/close)',expanded=True):
            preview_background=st.checkbox('Show background image',value=True,
                                           key='fc_preview_background')
            fig=draw_map(opts,grid=True,show_bounds=True,
                         show_background=preview_background,
                         title='Model grid and boundaries')
            st.pyplot(fig,use_container_width=True)
            plt.close(fig)
            active_wells = len(pumping_cells(opts))
            if active_wells:
                well_summary = (f'Pumping: **ON** · {active_wells} active well(s) · '
                                f'{opts.pump_per_well_m3_day:,.0f} m³/day per well')
            else:
                well_summary = 'Pumping: **OFF** (no active abstraction)'
            st.markdown('**Model characteristics**')
            st.caption('One unconfined layer · 100 rows × 70 columns · '
                       'one **steady-state** stress period · '
                       f'{DX:g} m nominal cell spacing')
            st.markdown(well_summary)
            st.caption(f'K = {opts.kh_m_s:.2e} m/s · '
                       f'recharge = {opts.recharge_mm_year:.1f} mm/year · '
                       f'eastern CHD = {opts.chd_head_m:.2f} m · '
                       f'bedrock inflow multiplier = {opts.bedrock_multiplier:g}')
            st.caption('Boundaries: 47 eastern CHD cells, 89 active bedrock WEL '
                       'inflows and 147 RIV cells.')
            try:
                validate_options(opts)
            except ValueError as exc:
                st.warning(f'Model setup needs attention: {exc}')
    # Actions: once the flow solution exists, MODPATH can run independently.
    # Editing flow parameters clears nwt_last above and therefore restores the
    # combined MODFLOW + MODPATH first-run action automatically.
    flow_available = st.session_state.get('nwt_last') is not None
    if mp_active and flow_available:
        flow_col, mp_col = st.columns(2)
        with flow_col:
            run_flow_pressed = st.button('▶ Run MODFLOW and MODPATH',
                type='secondary', use_container_width=True, key='fc_run_flow')
        with mp_col:
            with st.container(key='fc-action-mp-main'):
                run_mp_pressed = st.button('▶ Run MODPATH only',
                    type='secondary', use_container_width=True, key='fc_run_mp_only',
                    disabled=not configured_particle_options(st, opts).sources)
    else:
        flow_label = ('▶ Run MODFLOW and MODPATH' if mp_active
                      else '▶ Run MODFLOW-NWT model')
        # First flow run is prominent (red); subsequent recomputations are
        # secondary and visually neutral, irrespective of MODPATH activation.
        run_flow_pressed = st.button(flow_label,
            type='secondary' if flow_available else 'primary',
            use_container_width=True, key='fc_run_flow')
        run_mp_pressed = False

    if run_flow_pressed:
        st.session_state.pop('nwt_failed_budget',None)
        previous=st.session_state.pop('nwt_last',None)
        if previous:
            shutil.rmtree(previous['workspace'],ignore_errors=True)
        for key in ('fc_mp_signature','fc_mp_paths','fc_mp_message'):
            st.session_state.pop(key,None)
        try:
            validate_options(opts)
            workspace=Path(tempfile.mkdtemp(prefix='fieldcase_'))
            with st.spinner('Computing one-period steady-state MODFLOW-NWT...'):
                flowmodel,heads,budget,raw,log=run_flow(
                    opts,workspace,resolve_executable(exe_mf),solver=solver)
            st.session_state['nwt_last']={
                'opts':opts,'exe_mf':exe_mf,'solver':solver,
                'flow_signature':current_signature,
                'workspace':str(workspace),'heads':heads,
                'budget':budget,'raw':raw,'flowmodel':flowmodel,'flow_log':log}
            # When requested, compute MODPATH from the newly solved flow field;
            # particle counts use the persistent postprocessing preferences.
            if mp_active:
                _run_modpath_for_result(st, st.session_state['nwt_last'], exe_mp)
            st.success('MODFLOW-NWT finished. Postprocessing is available below.')
        except BudgetDiscrepancyError as exc:
            st.error(f'MODFLOW-NWT run rejected: {exc}')
            st.session_state['nwt_failed_budget'] = {
                'workspace': str(workspace), 'budget': exc.budget,
                'flow_signature': current_signature, 'reason': 'balance'}
            st.caption(f'Failed-run files preserved in: {workspace}')
        except Exception as exc:
            st.error(f'MODFLOW-NWT failed: {type(exc).__name__}: {exc}')
            if 'workspace' in locals():
                st.caption(f'Failed-run files preserved in: {workspace}')
                # NWT often writes the LIST budget even after a failed solver
                # run. Present those *diagnostic* values instead of hiding
                # them, but NEVER enable head/pathline postprocessing.
                try:
                    lst = listing_budget(workspace)
                    partial_budget = {
                        'listing': lst,
                        'listing_total_in_m3day': lst['total_in']*SEC_DAY,
                        'listing_total_out_m3day': lst['total_out']*SEC_DAY,
                    }
                    st.session_state['nwt_failed_budget'] = {
                        'workspace': str(workspace), 'budget': partial_budget,
                        'flow_signature': current_signature, 'reason': 'solver'}
                except (OSError, ValueError, ImportError):
                    # Some failures have no complete volumetric LIST block.
                    pass
    # Only MODPATH is rerun: keep heads, budgets, solver and workspace intact.
    if run_mp_pressed:
        existing = st.session_state.get('nwt_last')
        if existing is not None:
            _run_modpath_for_result(st, existing, exe_mp)

    result=st.session_state.get('nwt_last')
    rejected=st.session_state.get('nwt_failed_budget')
    if rejected is not None:
        _render_rejected_budget(st, rejected)
    if result is None and rejected is None:
        st.caption('The head plot, particle trajectories and water budget will '
                   'appear here after a successful model run.')
    if result is not None:
        _render_results(st,result,exe_mp)


if __name__ == '__main__':
    import sys
    if '--self-test' in sys.argv:
        self_test()
    else:
        main()

'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')