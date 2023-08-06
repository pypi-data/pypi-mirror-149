pro gest,v,spec,ind,par,gind=gind,nsig=nsig,stp=stp

; This program estimates the gaussian parameters
; peaking at v0.
; par = [ht,cen,wid]
;
;  INPUT
;   v     Array of velocities
;   spec  Array of spectrum
;   ind   Index of the maximum to fit
;   nsig  Number of sigmas for gind (nsig=3 by default)
;
;  OUTPUT
;   par   Gaussian parameters of best fit to maximum
;   gind  The indices of the gaussian out to 3 sigma
;
; If there is some kind of problem this program returns:
;  par = [999999., 999999., 999999.]
;  gind = -1.
;
; Created by David Nidever April 2005

gind = -1
par = [0,0,0]+999999.   ; assume bad unless proven okay

npar = n_elements(par)
npts = n_elements(v)
nspec = n_elements(spec)

; Bad Input Values
if (n_params() eq 0) or (npar eq 0) or (npts eq 0) or (npts ne nspec) or $
     (n_elements(ind) eq 0) then begin
  print,'Syntax - gest,v,spec,ind,par,gind=gind'
  return
endif

if (ind lt 0) or (ind gt npts-1) then begin
  print,'Index out of range'
  return
endif

cen = v(ind)

;smspec5 = smooth(spec,5)
;smspec12 = smooth(spec,12)
;smspec25 = smooth(spec,25)

; Using derivatives to get the parameters
dv = v(1)-v(0)
dsdv = slope(spec,/acc)/dv
vv0 = v-cen
r10 = dsdv/spec

; Finding maxima closest to IND
maxmin,r10,mina,maxa
maxind = first_el(where(maxa lt ind),/last)
if (maxind(0) eq -1) then goto,BOMB
lo = maxa(maxind)
minind = first_el(where(mina gt ind))
if (minind(0) eq -1) then goto,BOMB
hi = mina(minind)

;;indsub = indgen(121)+ind-60.
;;f = fit(r10(indsub),1,vv0(indsub),coef,sigma)
;f = fit(r10(lo:hi),1,vv0(lo:hi),coef,sigma)
;sig0 = sqrt(-1./coef(1))

; Finding the slope for r = (d(spec)/dv)/spec
; dsdv/spec = -vv0/sig^2.
m = (r10(ind+1)-r10(ind))/dv
if (-1./m lt 0.) then goto,BOmB
sig0 = sqrt(-1./m)
par = [spec(ind),cen,sig0]

; Finding the indices for this gaussian
;  3 sigma on each side
if not keyword_set(nsig) then nsig=3.0
iwid = sig0/dv  
lo = floor( 0 > ind-nsig*iwid )
hi = ceil( ind+nsig*iwid < npts-1 )
ngind = hi-lo+1

; Need at least 6 points, 3 at each side
if (ngind lt 6) then begin
  lo = floor( 0 > ind-3 )
  hi = ceil( ind+3 < npts-1 )
  ngind = hi-lo+1
endif

; Need at least 6 points, 5 at each side
if (ngind lt 6) then begin
  lo = floor( 0 > ind-5 )
  hi = ceil( ind+5 < npts-1 )
  ngind = hi-lo+1
endif

gind = findgen(ngind)+lo

BOMB:

if keyword_set(stp) then stop

end
