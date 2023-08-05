pro gremove,par,x,y

; This program removes gaussians that have bad parameters.
;
;  INPUT
;   par    Array of gaussian parameters
;   x      Array of x values
;   y      Array of y values
;
;  OUTPUT
;   par    Array of gaussian parameters with bad gaussians removed
;
; Created by David Nidever April 2005

nx = n_elements(x)
ny = n_elements(y)
npar = n_elements(par)
ngauss = npar/3

; Bad Input Values
if (n_params() eq 0) or (nx eq 0) or (ny eq 0) then begin
  print,'Syntax - gremove,par,x,y'
  return
endif

orig_par = par
flag = 0

for i=0,ngauss-1 do begin
  ipar = par(3*i:3*i+2)

  ; checking for infinite or NAN
  dum = where(finite(ipar) eq 0,nfinite)
  if nfinite gt 0 then flag=1

  ; getting the area
  area = garea(ipar)

  ; Using PARCHECK.PRO
  parcheck,x,y,ipar,flag

  ;; checking the height
  ;if ipar(0) le 0.01 then flag=1
  ;if ipar(0) gt max(y)*1.1 then flag=1
  ;; should allow wider and small gaussians
  ;; but remove narrow and small gaussians.
  ;; what's the cutoff.  the area?
  ;
  ;; checking the center
  ;if ipar(1) lt min(x) or par(3*i+1) gt max(x) then flag=1
  ;
  ;; checking the widths
  ;if ipar(2) le 1. then flag=1
  ;if ipar(2) gt (max(x)-min(x))*0.5 then flag=1

  ;if everything's fine add them to the final parameters
  if flag eq 0 and keyword_set(fpar) then fpar = [fpar,ipar]
  if flag eq 0 and not keyword_set(fpar) then fpar = ipar

  ; resetting the flag
  flag = 0

  ;stop

endfor

if keyword_set(fpar) then par = fpar else par=-1

;stop

end
