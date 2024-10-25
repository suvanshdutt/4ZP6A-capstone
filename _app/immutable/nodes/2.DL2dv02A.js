import{s as N,d as J,u as K,g as Q,e as W,r as X,c as Z,h as B,n as ee}from"../chunks/scheduler.3-7Zdzny.js";import{S as V,i as x,e as b,c as k,a as A,d as v,w as _,l as j,z as M,g as I,A as w,p as q,q as E,s as z,m as O,k as D,f as P,n as T,h as g,o as H,r as L,t as F,b as G}from"../chunks/index.Bqv7vdHX.js";import{b as R}from"../chunks/paths.CDgUijaE.js";/* empty css                                                     */import{t as te}from"../chunks/theme.CM6NFz8V.js";/* empty css                                                     */function se(s){let e,t,n,m;const u=s[4].default,o=J(u,s,s[3],null);return{c(){e=b("button"),o&&o.c(),this.h()},l(a){e=k(a,"BUTTON",{style:!0,class:!0});var l=A(e);o&&o.l(l),l.forEach(v),this.h()},h(){_(e,"--primary_color",s[2].primary_color),_(e,"--text_color",s[2].text_color),_(e,"--secondary_color",s[2].secondary_color),_(e,"--font_size",s[1]+"px"),_(e,"--grey",s[2].grey_text),j(e,"class","svelte-q9w981"),M(e,"inverse",s[0])},m(a,l){I(a,e,l),o&&o.m(e,null),t=!0,n||(m=[w(e,"click",s[5]),w(e,"mouseover",s[8]),w(e,"mouseout",s[9]),w(e,"blur",s[6]),w(e,"focus",s[7])],n=!0)},p(a,[l]){o&&o.p&&(!t||l&8)&&K(o,u,a,a[3],t?W(u,a[3],l,null):Q(a[3]),null),(!t||l&4)&&_(e,"--primary_color",a[2].primary_color),(!t||l&4)&&_(e,"--text_color",a[2].text_color),(!t||l&4)&&_(e,"--secondary_color",a[2].secondary_color),(!t||l&2)&&_(e,"--font_size",a[1]+"px"),(!t||l&4)&&_(e,"--grey",a[2].grey_text),(!t||l&1)&&M(e,"inverse",a[0])},i(a){t||(q(o,a),t=!0)},o(a){E(o,a),t=!1},d(a){a&&v(e),o&&o.d(a),n=!1,X(m)}}}function ne(s,e,t){let n;Z(s,te,r=>t(2,n=r));let{$$slots:m={},$$scope:u}=e,{inverse:o=!1}=e,{fontSize:a=20}=e;function l(r){B.call(this,s,r)}function h(r){B.call(this,s,r)}function y(r){B.call(this,s,r)}const S=()=>t(0,o=!o),f=()=>t(0,o=!o);return s.$$set=r=>{"inverse"in r&&t(0,o=r.inverse),"fontSize"in r&&t(1,a=r.fontSize),"$$scope"in r&&t(3,u=r.$$scope)},[o,a,n,u,m,l,h,y,S,f]}class Y extends V{constructor(e){super(),x(this,e,ne,se,N,{inverse:0,fontSize:1})}}function oe(s){let e;return{c(){e=F("Login")},l(t){e=G(t,"Login")},m(t,n){I(t,e,n)},d(t){t&&v(e)}}}function ae(s){let e;return{c(){e=F("Sign Up")},l(t){e=G(t,"Sign Up")},m(t,n){I(t,e,n)},d(t){t&&v(e)}}}function re(s){let e,t,n,m="About",u,o,a=`Our Project is based on AI chest read, Our website gives the patient a radiographed report of the chest xray\r
            provided. The report checks on the potential diseases.`,l,h,y="Project By : Suvansh Dutt, Ujjwal Raj, Yuvraj Singh Sandhu and Suhaas Parcha",S,f,r,U,d,C;return r=new Y({props:{$$slots:{default:[oe]},$$scope:{ctx:s}}}),r.$on("click",s[0]),d=new Y({props:{inverse:!0,$$slots:{default:[ae]},$$scope:{ctx:s}}}),d.$on("click",s[1]),{c(){e=b("main"),t=b("div"),n=b("h1"),n.textContent=m,u=z(),o=b("p"),o.textContent=a,l=z(),h=b("p"),h.textContent=y,S=z(),f=b("div"),O(r.$$.fragment),U=z(),O(d.$$.fragment),this.h()},l(i){e=k(i,"MAIN",{class:!0});var p=A(e);t=k(p,"DIV",{class:!0});var c=A(t);n=k(c,"H1",{class:!0,"data-svelte-h":!0}),D(n)!=="svelte-soqi9t"&&(n.textContent=m),u=P(c),o=k(c,"P",{class:!0,"data-svelte-h":!0}),D(o)!=="svelte-1jlgthr"&&(o.textContent=a),l=P(c),h=k(c,"P",{class:!0,"data-svelte-h":!0}),D(h)!=="svelte-1yz5vlz"&&(h.textContent=y),S=P(c),f=k(c,"DIV",{class:!0});var $=A(f);T(r.$$.fragment,$),U=P($),T(d.$$.fragment,$),$.forEach(v),c.forEach(v),p.forEach(v),this.h()},h(){j(n,"class","svelte-tjk91t"),j(o,"class","svelte-tjk91t"),j(h,"class","svelte-tjk91t"),j(f,"class","buttons svelte-tjk91t"),j(t,"class","About svelte-tjk91t"),j(e,"class","svelte-tjk91t")},m(i,p){I(i,e,p),g(e,t),g(t,n),g(t,u),g(t,o),g(t,l),g(t,h),g(t,S),g(t,f),H(r,f,null),g(f,U),H(d,f,null),C=!0},p(i,[p]){const c={};p&4&&(c.$$scope={dirty:p,ctx:i}),r.$set(c);const $={};p&4&&($.$$scope={dirty:p,ctx:i}),d.$set($)},i(i){C||(q(r.$$.fragment,i),q(d.$$.fragment,i),C=!0)},o(i){E(r.$$.fragment,i),E(d.$$.fragment,i),C=!1},d(i){i&&v(e),L(r),L(d)}}}function le(s){return[()=>window.location.href=`${R}/login`,()=>window.location.href=`${R}/signup`]}class ie extends V{constructor(e){super(),x(this,e,le,re,N,{})}}function ce(s){let e,t;return e=new ie({}),{c(){O(e.$$.fragment)},l(n){T(e.$$.fragment,n)},m(n,m){H(e,n,m),t=!0},p:ee,i(n){t||(q(e.$$.fragment,n),t=!0)},o(n){E(e.$$.fragment,n),t=!1},d(n){L(e,n)}}}class pe extends V{constructor(e){super(),x(this,e,null,ce,N,{})}}export{pe as component};