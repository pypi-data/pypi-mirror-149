pro parcheck,x,y,par,flag

;  This program checks that the gaussian parameters
;  are okay.
;
;  INPUT
;   x      Array of x values
;   y      Array of y values
;   par    Array of gaussian parameters
;
;  OUTPUT
;   flag   Flag to see if some of the gaussian parameters
;          are bad.  flag = 1   Bad
;                    flag = 0   Okay
;
; Created by David Nidever April 2005

npts = n_elements(x)
ny = n_elements(y)
npar =  n_elements(par)
ngauss = npar/3

; Bad Input Values
if (n_params() eq 0) or (npts eq 0) or (ny eq 0) or (npts ne ny) or $
     (npar eq 0) then begin
  print,'Syntax - parcheck,x,y,par,flag'
  flag = 1
  return
endif

flag = 0

; Calculate dX
dx = median(slope(x[0:(10<(npts-1))]))

; checking for bad stuff
if npts lt 3 then flag = 1
if npts lt npar then flag = 1
if npar lt 3 then flag = 1

xmin = min(x)
xmax = max(x)
ymin = min(y)
ymax = max(y)

; checking the parameters
for i=0,ngauss-1 do begin

  ; checking height
  if par(3*i) le 0.01 then flag=1
  if par(3*i) gt max(y)*1.1 then flag=1

  ; checking center
  if par(3*i+1) lt min(x) or par(3*i+1) gt max(x) then flag=1

  ; checking width
  ;if par(3*i+2) le 1. then flag=1
  if par(3*i+2) le 0.5*dx then flag=1
  if par(3*i+2) gt (max(x)-min(x))*0.5 then flag=1
endfor

; Checking for Infinite or NAN
dum = where(finite(par) eq 0,nfinite)
if nfinite gt 0 then flag=1

;stop

end
